"""Small durable SQL queue for local OCR and model work."""

import asyncio
import logging
import os
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable

from sqlalchemy import select

from .db import BackgroundJob, Comparison, Material, Paper, ROOT, Session, SyllabusImport


JobHandler = Callable[[dict, int], Awaitable[None]]
logger = logging.getLogger(__name__)
CLAIM_LOCK_PATH = ROOT / "data" / "job-claim.lock"


class JobCancelled(Exception):
    """Raised when a handler reaches a safe cancellation boundary."""


def ensure_not_cancelled(job_id: int) -> None:
    with Session() as db:
        job = db.get(BackgroundJob, job_id)
        if job is None or job.status in ("cancel_requested", "cancelled"):
            raise JobCancelled(f"Job {job_id} was cancelled")


@contextmanager
def _claim_lock():
    """Serialize queue claims across app processes using a shared data-volume lock."""
    CLAIM_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = CLAIM_LOCK_PATH.open("a+b")
    try:
        if os.name == "nt":
            import msvcrt
            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    time.sleep(0.05)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def now():
    return datetime.now(timezone.utc)


def enqueue_job(db, kind: str, payload: dict, *, total: int = 0, max_attempts: int = 2) -> BackgroundJob:
    job = BackgroundJob(kind=kind, payload=payload, total=total, max_attempts=max_attempts)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def set_progress(job_id: int, progress: int, total: int | None = None) -> None:
    with Session.begin() as db:
        job = db.get(BackgroundJob, job_id)
        if job and job.status == "running":
            job.started_at = now()  # heartbeat for recovery in multi-process deployments
            job.progress = max(0, progress)
            if total is not None:
                job.total = max(0, total)
            if job.kind == "material_enrichment":
                material_id = (job.payload or {}).get("material_id")
                material = db.get(Material, material_id) if material_id else None
                if material:
                    material.enrichment = {**(material.enrichment or {}), "status": "running", "progress": job.progress, "total": job.total}
            elif job.kind == "syllabus_import":
                source_id = (job.payload or {}).get("source_id")
                source = db.get(SyllabusImport, source_id) if source_id else None
                if source:
                    source.status = "processing"
            elif job.kind == "question_generation":
                paper_id = (job.payload or {}).get("paper_id")
                paper = db.get(Paper, paper_id) if paper_id else None
                if paper:
                    paper.generation = {**(paper.generation or {}), "status": "running", "progress": job.progress, "total": job.total}


def recover_jobs() -> None:
    """Requeue expired worker leases without interrupting jobs owned by live processes."""
    with Session.begin() as db:
        cutoff = now() - timedelta(minutes=30)
        expired = list(db.scalars(select(BackgroundJob).where(
            BackgroundJob.status == "running",
            (BackgroundJob.started_at.is_(None)) | (BackgroundJob.started_at < cutoff),
        )))
        for job in expired:
            job.status = "queued"
            job.started_at = None
            job.error = "Recovered after the worker stopped before completion"
        comparison_jobs = list(db.scalars(select(BackgroundJob).where(
            BackgroundJob.kind == "comparison",
            BackgroundJob.status.in_(("queued", "running")),
        )))
        queued_comparison_ids = {job.payload.get("comparison_id") for job in comparison_jobs if job.status == "queued" and isinstance(job.payload, dict)}
        running_comparison_ids = {job.payload.get("comparison_id") for job in comparison_jobs if job.status == "running" and isinstance(job.payload, dict)}
        for comparison in db.scalars(select(Comparison).where(Comparison.status.in_(("queued", "running")))):
            if comparison.status == "running" and comparison.id in running_comparison_ids:
                continue
            if comparison.status == "running":
                comparison.status = "queued"
            if comparison.id not in queued_comparison_ids:
                db.add(BackgroundJob(
                    kind="comparison",
                    payload={"comparison_id": comparison.id},
                    total=comparison.total,
                    max_attempts=2,
                ))


def expire_export_artifacts(retention_days: int | None = None) -> int:
    """Remove old generated files while retaining their job and audit records."""
    days = retention_days if retention_days is not None else int(os.getenv("EXPORT_RETENTION_DAYS", "30"))
    if days < 1:
        raise ValueError("EXPORT_RETENTION_DAYS must be at least 1")
    cutoff = now() - timedelta(days=days)
    removed = 0
    with Session.begin() as db:
        jobs = db.scalars(select(BackgroundJob).where(BackgroundJob.kind == "comparison_export", BackgroundJob.status == "complete", BackgroundJob.finished_at < cutoff)).all()
        for job in jobs:
            payload = dict(job.payload or {})
            filename = payload.get("artifact")
            comparison_id = payload.get("comparison_id")
            format_name = payload.get("format")
            expected = f"comparison-{comparison_id}-job-{job.id}.{format_name}"
            if filename != expected or format_name not in {"md", "txt", "pdf", "xlsx"}:
                continue
            (ROOT / "data" / "exports" / filename).unlink(missing_ok=True)
            payload.pop("artifact")
            payload["artifact_expired"] = True
            job.payload = payload
            removed += 1
    return removed


def _claim_next() -> tuple[int, str, dict, int, int] | None:
    with _claim_lock(), Session() as db:
        statement = select(BackgroundJob).where(BackgroundJob.status == "queued").order_by(BackgroundJob.created_at, BackgroundJob.id)
        if db.get_bind().dialect.name == "postgresql":
            statement = statement.with_for_update(skip_locked=True)
        job = db.scalar(statement)
        if job is None:
            return None
        job.status = "running"
        job.attempts += 1
        job.started_at = now()
        job.error = None
        db.commit()
        return job.id, job.kind, dict(job.payload), job.attempts, job.max_attempts


def _finish(job_id: int, *, status: str, error: str | None = None) -> None:
    with Session.begin() as db:
        job = db.get(BackgroundJob, job_id)
        if job is None:
            return
        job.status = status
        job.error = error[:2000] if error else None
        job.finished_at = now() if status in ("complete", "failed", "cancelled") else None
        job.started_at = None if status == "queued" else job.started_at
        if job.kind == "material_enrichment":
            material_id = (job.payload or {}).get("material_id")
            material = db.get(Material, material_id) if material_id else None
            if material:
                state = (material.enrichment or {}).get("status", "review_ready") if status == "complete" else "failed" if status == "failed" else "cancelled" if status == "cancelled" else "queued"
                material.enrichment = {**(material.enrichment or {}), "status": state, "error": error}
        elif job.kind == "syllabus_import":
            source_id = (job.payload or {}).get("source_id")
            source = db.get(SyllabusImport, source_id) if source_id else None
            if source:
                source.status = "active" if status == "complete" else "failed" if status == "failed" else "cancelled" if status == "cancelled" else "queued"
                source.error = error[:2000] if status == "failed" and error else None
        elif job.kind == "question_generation":
            paper_id = (job.payload or {}).get("paper_id")
            paper = db.get(Paper, paper_id) if paper_id else None
            if paper:
                generation_status = paper.generation.get("status")
                state = generation_status if status == "complete" and generation_status == "checking" else "complete" if status == "complete" else "failed" if status == "failed" else "cancelled" if status == "cancelled" else "queued"
                paper.generation = {**(paper.generation or {}), "status": state, "error": error[:2000] if status == "failed" and error else None}
        elif job.kind == "comparison":
            comparison_id = (job.payload or {}).get("comparison_id")
            comparison = db.get(Comparison, comparison_id) if comparison_id else None
            if comparison and comparison.generated_paper_id:
                paper = db.get(Paper, comparison.generated_paper_id)
                if paper:
                    paper.generation = {**(paper.generation or {}), "status": "checked" if status == "complete" else "check_failed" if status == "failed" else "cancelled" if status == "cancelled" else "checking", "comparison_id": comparison.id, "check_error": error[:2000] if status == "failed" and error else None}


async def run_worker(handlers: dict[str, JobHandler]) -> None:
    recover_jobs()
    try:
        expire_export_artifacts()
    except Exception:
        logger.exception("Export retention cleanup failed")
    next_cleanup = time.monotonic() + 3600
    while True:
        if time.monotonic() >= next_cleanup:
            try:
                await asyncio.to_thread(expire_export_artifacts)
            except Exception:
                logger.exception("Export retention cleanup failed")
            next_cleanup = time.monotonic() + 3600
        try:
            claimed = await asyncio.to_thread(_claim_next)
        except Exception:
            logger.exception("Background job claim failed; retrying")
            await asyncio.sleep(2)
            continue
        if claimed is None:
            await asyncio.sleep(0.5)
            continue
        job_id, kind, payload, attempt, max_attempts = claimed
        handler = handlers.get(kind)
        if handler is None:
            _finish(job_id, status="failed", error=f"No worker is registered for job type {kind}")
            continue
        try:
            await handler(payload, job_id)
        except asyncio.CancelledError:
            raise
        except JobCancelled as exc:
            _finish(job_id, status="cancelled", error=str(exc))
        except Exception as exc:
            try:
                if attempt < max_attempts:
                    _finish(job_id, status="queued", error=f"Attempt {attempt} failed: {exc}")
                    await asyncio.sleep(min(2 ** attempt, 10))
                else:
                    _finish(job_id, status="failed", error=str(exc))
            except Exception:
                logger.exception("Could not record failure for job %s", job_id)
        else:
            try:
                _finish(job_id, status="complete")
            except Exception:
                logger.exception("Could not mark job %s complete", job_id)
