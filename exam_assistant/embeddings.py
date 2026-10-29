"""Incremental local Qwen indexing and exact pgvector candidate retrieval."""

import hashlib
import math
import re

import httpx
from sqlalchemy import Float, delete, select

from .db import BackgroundJob, Paper, Question, QuestionAnalysis, QuestionEmbedding, Session
from .jobs import ensure_not_cancelled, set_progress
from .model_runtime import EMBEDDING_MODEL, HELPER_MODEL, JUDGE_MODEL, MODEL_URL, ModelUnavailable, _validate_local_endpoint, inspect_local_models, model_session, unload_model
from .vector_type import checked_vector


async def embedding_identity() -> dict:
    inventory = await inspect_local_models()
    identity = inventory.get("embedding")
    if not identity or not identity.get("digest"):
        raise ModelUnavailable(f"Install the configured local embedding model {EMBEDDING_MODEL or '(not configured)'}")
    return identity


async def schedule_missing_index_jobs() -> int:
    """Backfill existing questions and detect a changed model digest at startup."""
    if not EMBEDDING_MODEL:
        return 0
    try:
        digest = (await embedding_identity())["digest"]
    except ModelUnavailable:
        return 0
    queued = 0
    with Session.begin() as db:
        valid = {(row.question_id, row.question_revision) for row in db.scalars(select(QuestionEmbedding).where(
            QuestionEmbedding.model_digest == digest, QuestionEmbedding.part_id == "whole"
        ))}
        pending = {job.payload.get("paper_id") for job in db.scalars(select(BackgroundJob).where(
            BackgroundJob.kind == "index_paper", BackgroundJob.status.in_(("queued", "running", "cancel_requested"))
        ))}
        for paper in db.scalars(select(Paper)):
            if paper.id not in pending and any((question.id, question.revision) not in valid for question in paper.questions):
                db.add(BackgroundJob(kind="index_paper", payload={"paper_id": paper.id}, total=len(paper.questions)))
                queued += 1
    return queued


async def embed_texts(texts: list[str]) -> list[list[float]]:
    if not EMBEDDING_MODEL:
        raise ModelUnavailable("Configure EMBEDDING_MODEL_NAME before semantic indexing/search")
    _validate_local_endpoint()
    if not texts or any(not isinstance(value, str) or not value.strip() for value in texts):
        raise ValueError("Embedding inputs must contain text")
    vectors = []
    async with model_session():
        for model in dict.fromkeys([JUDGE_MODEL, HELPER_MODEL]):
            if model and model != EMBEDDING_MODEL:
                await unload_model(model)
        try:
            async with httpx.AsyncClient(timeout=240, trust_env=False) as client:
                for offset in range(0, len(texts), 8):
                    batch = texts[offset:offset + 8]
                    response = await client.post(f"{MODEL_URL}/api/embed", json={"model": EMBEDDING_MODEL, "input": batch, "truncate": False, "keep_alive": "5m"})
                    response.raise_for_status()
                    result = response.json().get("embeddings")
                    if not isinstance(result, list) or len(result) != len(batch):
                        raise ModelUnavailable("Embedding runtime returned the wrong number of vectors")
                    vectors.extend(checked_vector(vector) for vector in result)
            if len({len(vector) for vector in vectors}) != 1:
                raise ModelUnavailable("Embedding runtime returned inconsistent dimensions")
            return vectors
        except (httpx.HTTPError, ValueError) as exc:
            raise ModelUnavailable(f"Local embedding failed: {exc}") from exc
        finally:
            await unload_model(EMBEDDING_MODEL)


def fragments(question, profile=None) -> dict[str, str]:
    result = {"whole": question.text}
    if profile and len(profile.get("parts", [])) > 1:
        requirements = {item["id"]: item for item in profile["requirements"]}
        for part in profile["parts"]:
            quotes = [requirements[rid]["quote"] for rid in part["requirement_ids"]]
            if quotes and all(quote in question.text for quote in quotes):
                result[part["part_id"]] = "\n".join(quotes)
    else:
        # Keep literal subpart spans until cached requirement analysis is available.
        parts = list(re.finditer(r"(?m)^\s*(?:\([a-z]\)|[a-z]\))\s+", question.text))
        for index, match in enumerate(parts):
            result[f"part_{index + 1}"] = question.text[match.start():parts[index + 1].start() if index + 1 < len(parts) else len(question.text)].strip()
    return result


async def index_paper(payload: dict, job_id: int):
    paper_id = int(payload["paper_id"])
    identity = await embedding_identity()
    with Session() as db:
        paper = db.get(Paper, paper_id)
        if not paper:
            return
        ids = [question.id for question in paper.questions]
    for index, qid in enumerate(ids):
        ensure_not_cancelled(job_id)
        with Session() as db:
            question = db.get(Question, qid)
            if not question:
                continue
            revision = question.revision
            analysis = db.scalar(select(QuestionAnalysis).where(QuestionAnalysis.question_id == qid, QuestionAnalysis.question_revision == revision).order_by(QuestionAnalysis.id.desc()))
            texts = fragments(question, analysis.analysis if analysis else None)
            hashes = {part: hashlib.sha256(text.encode()).hexdigest() for part, text in texts.items()}
            old = list(db.scalars(select(QuestionEmbedding).where(QuestionEmbedding.question_id == qid, QuestionEmbedding.model_digest == identity["digest"])))
            by_hash = {row.source_hash: row.embedding for row in old}
        missing = [part for part in texts if hashes[part] not in by_hash]
        fresh = await embed_texts([texts[part] for part in missing]) if missing else []
        by_hash.update({hashes[part]: vector for part, vector in zip(missing, fresh)})
        ensure_not_cancelled(job_id)
        with Session.begin() as db:
            current = db.get(Question, qid)
            if not current or current.revision != revision:
                continue  # The authoring hook has queued the newer revision.
            db.execute(delete(QuestionEmbedding).where(QuestionEmbedding.question_id == qid, QuestionEmbedding.model == EMBEDDING_MODEL))
            for part in texts:
                vector = by_hash[hashes[part]]
                db.add(QuestionEmbedding(question_id=qid, question_revision=revision, model=EMBEDDING_MODEL, model_digest=identity["digest"], part_id=part, source_hash=hashes[part], dimensions=len(vector), embedding=vector))
        set_progress(job_id, index + 1, len(ids))


def nearest_questions(db, subject_id: int, vector: list[float], digest: str, *, unit: int | None = None, limit: int = 50, bank_only: bool = True) -> list[dict]:
    vector = checked_vector(vector)
    query = select(QuestionEmbedding, Question).join(Question, Question.id == QuestionEmbedding.question_id).join(Paper, Paper.id == Question.paper_id).where(
        Paper.subject_id == subject_id, Paper.archived.is_(False),
        QuestionEmbedding.question_revision == Question.revision,
        QuestionEmbedding.model_digest == digest, QuestionEmbedding.dimensions == len(vector),
    )
    if bank_only:
        query = query.where(Paper.status == "bank")
    if unit is not None:
        query = query.where(Question.unit == unit)
    if db.get_bind().dialect.name == "postgresql":
        distance = QuestionEmbedding.embedding.op("<=>", return_type=Float)(vector)
        rows = ((record, question, float(score)) for record, question, score in db.execute(query.add_columns(distance).order_by(distance, Question.id)))
    else:
        # SQLite is a test/fallback path. Production retrieval executes <=> in pgvector.
        norm = math.sqrt(sum(value * value for value in vector))
        rows = sorted(((record, question, 1 - sum(a * b for a, b in zip(record.embedding, vector)) / (math.sqrt(sum(a * a for a in record.embedding)) * norm)) for record, question in db.execute(query)), key=lambda row: row[2])
    result, seen = [], set()
    for record, question, distance in rows:
        if question.id in seen:
            continue
        seen.add(question.id)
        result.append({"question": question, "similarity": round(1 - distance, 6), "matched_part": record.part_id})
        if len(result) >= min(max(limit, 1), 100):
            break
    return result


async def semantic_search(db, subject_id, query, *, unit=None, limit=50, bank_only=True):
    identity = await embedding_identity()
    vectors = await embed_texts(["Instruct: Retrieve exam questions with matching assessed requirements.\nQuery: " + query])
    return nearest_questions(db, subject_id, vectors[0], identity["digest"], unit=unit, limit=limit, bank_only=bank_only)
