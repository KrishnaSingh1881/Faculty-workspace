"""Versioned per-question requirement extraction reused across pair comparisons."""

import hashlib
import json

from .model_runtime import HELPER_MODEL, JUDGE_MODEL, ModelUnavailable, chat_json_in_session, comparison_context_tokens, model_session, unload_model
from .comparison_tools import requirement_is_grounded


ANALYSIS_PROMPT_VERSION = "question-requirements-v4"

ANALYSIS_SYSTEM = """Extract assessed requirements from one exam question. Do not compare it to another
question and do not assign a redundancy label. Preserve each independently assessed ask, action,
object, scope, expected depth/output, conditions, negation and qualifiers. Represent subparts and
OR/choose-any alternatives in `parts`, and list requirement IDs within each part. Every requirement
must include a short exact quote copied from the question. Do not add syllabus facts or infer asks
that are not present. Return JSON with `requirements` (objects: id, quote, concept, action, object,
scope, depth, output, conditions, negation, part_id), `parts` (objects: part_id, kind, requirement_ids),
`choice_rule` (string or null), and `concerns` (array). Use IDs r1, r2, ... in reading order. If
extraction is uncertain, explain it in concerns rather than inventing a requirement. For a simple
question use one part with part_id p1, kind main, and its requirement IDs. Every part must contain
all three keys part_id, kind, requirement_ids; every requirement must reference exactly one part.
Concerns are extraction blockers: unreadable text, conflicting instructions or an ask you cannot
represent faithfully. An open-ended ask such as 'explain the main functions' is a valid requirement;
do not flag its unspecified number of examples or level of detail as a missing requirement. A
detected_structure may contain parsed subparts and OR alternatives; treat it only as a parsing hint,
verify every item against the original question, and report ambiguity in concerns."""


def analysis_cache_key(question) -> str:
    payload = {
        "question_id": question.id,
        "revision": question.revision,
        "text": hashlib.sha256(question.text.encode()).hexdigest(),
        "model": JUDGE_MODEL,
        "prompt": ANALYSIS_PROMPT_VERSION,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def validate_analysis(profile: dict, question) -> dict:
    requirements = profile.get("requirements")
    parts = profile.get("parts")
    concerns = profile.get("concerns")
    if not isinstance(requirements, list) or not requirements or not isinstance(parts, list) or not isinstance(concerns, list):
        raise ValueError("Question analysis is missing requirements, parts, or concerns")
    seen = set()
    for requirement in requirements:
        if not isinstance(requirement, dict) or not isinstance(requirement.get("id"), str):
            raise ValueError("Question analysis contains a requirement without an ID")
        rid = requirement["id"]
        if rid in seen or not rid.startswith("r"):
            raise ValueError("Question requirement IDs must be unique and ordered IDs")
        if not requirement_is_grounded(requirement, question.text, "source"):
            raise ValueError(f"Requirement {rid} is not grounded in the original question")
        seen.add(rid)
    part_ids = set()
    for part in parts:
        if not isinstance(part, dict) or not isinstance(part.get("part_id"), str) or not isinstance(part.get("kind"), str) or not isinstance(part.get("requirement_ids"), list):
            raise ValueError("Question analysis contains an invalid part structure")
        if part["part_id"] in part_ids or any(not isinstance(item, str) or item not in seen for item in part["requirement_ids"]):
            raise ValueError("Question part references duplicate or unknown requirements")
        if len(part["requirement_ids"]) != len(set(part["requirement_ids"])):
            raise ValueError("Question part contains duplicate requirement IDs")
        part_ids.add(part["part_id"])
    if any(item.get("part_id") not in part_ids for item in requirements):
        raise ValueError("Question requirement references an unknown part")
    if profile.get("choice_rule") is not None and not isinstance(profile.get("choice_rule"), str):
        raise ValueError("Question choice_rule must be text or null")
    if any(sum(requirement["id"] in part["requirement_ids"] for part in parts) != 1 for requirement in requirements):
        raise ValueError("Each requirement must belong to exactly one question part")
    parts_by_id = {part["part_id"]: set(part["requirement_ids"]) for part in parts}
    if any(requirement["id"] not in parts_by_id[requirement["part_id"]] for requirement in requirements):
        raise ValueError("Question requirement and part assignment disagree")
    return profile


async def analyze_questions(questions: list) -> list[dict]:
    """Extract a pair's profiles in one model session to avoid reloads per question."""
    if not questions:
        return []
    output = []
    async with model_session():
        if HELPER_MODEL != JUDGE_MODEL:
            await unload_model(HELPER_MODEL)
        try:
            for question in questions:
                messages = [
                    {"role": "system", "content": ANALYSIS_SYSTEM},
                    {"role": "user", "content": json.dumps({"question": question.text, "question_number": getattr(question, "number", None), "marks": question.marks, "detected_structure": getattr(question, "structure", None)}, ensure_ascii=False)},
                ]
                last_error = "invalid JSON"
                for attempt in range(2):
                    response = await chat_json_in_session(JUDGE_MODEL, messages, keep_alive="5m", think=False, num_ctx=comparison_context_tokens())
                    content = response["message"].get("content", "")
                    try:
                        result = json.loads(content)
                        if not isinstance(result, dict):
                            raise ValueError("response must be a JSON object")
                        if isinstance(result.get("requirements"), list):
                            result["requirements"] = [{**item, "evidence_id": "source"} if isinstance(item, dict) else item for item in result["requirements"]]
                        output.append(validate_analysis(result, question))
                        break
                    except (TypeError, ValueError) as exc:
                        last_error = str(exc)
                        if attempt:
                            raise ModelUnavailable(
                                f"Question {getattr(question, 'number', '?')} requirement extraction failed validation after one schema-repair retry: {last_error}"
                            ) from exc
                        messages.append({"role": "assistant", "content": content if isinstance(content, str) else ""})
                        messages.append({
                            "role": "user",
                            "content": "Repair the JSON response to satisfy the required schema and the validation error below. Preserve grounded content; do not add requirements. Return only the corrected JSON object.\nValidation error: " + last_error,
                        })
        finally:
            await unload_model(JUDGE_MODEL)
    return output


async def analyze_question(question) -> dict:
    return (await analyze_questions([question]))[0]


def bind_profile(profile: dict, evidence_id: str) -> dict:
    """Attach pair-local source IDs without mutating the reusable cached profile."""
    id_map = {item["id"]: f"{evidence_id}_{item['id']}" for item in profile["requirements"]}
    return {
        **profile,
        "requirements": [{**item, "id": id_map[item["id"]], "evidence_id": evidence_id} for item in profile["requirements"]],
        "parts": [
            {**part, "requirement_ids": [id_map[item] for item in part["requirement_ids"]]}
            for part in profile["parts"]
        ],
    }
