import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, create_engine, event, inspect, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from .vector_type import Vector


def now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    tree: Mapped[dict] = mapped_column(JSON)
    tree_version: Mapped[int] = mapped_column(Integer, default=1)


class TreeRevision(Base):
    __tablename__ = "tree_revisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    version: Mapped[int] = mapped_column(Integer)
    tree: Mapped[dict] = mapped_column(JSON)
    reason: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class SyllabusImport(Base):
    __tablename__ = "syllabus_imports"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int | None] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    submitted_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    filename: Mapped[str] = mapped_column(String(250))
    file_hash: Mapped[str] = mapped_column(String(64), index=True)
    extracted_text: Mapped[str] = mapped_column(Text)
    warnings: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(30), default="queued", index=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Paper(Base):
    __tablename__ = "papers"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(250))
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="draft")
    archived: Mapped[bool] = mapped_column(Boolean, default=False)
    generated: Mapped[bool] = mapped_column(Boolean, default=False)
    generation: Mapped[dict] = mapped_column(JSON, default=dict)
    filename: Mapped[str | None] = mapped_column(String(250), nullable=True)
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    questions: Mapped[list["Question"]] = relationship(back_populates="paper", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id"))
    number: Mapped[str] = mapped_column(String(50))
    text: Mapped[str] = mapped_column(Text)
    marks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    structure: Mapped[dict] = mapped_column(JSON, default=dict)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    topic_ids: Mapped[list] = mapped_column(JSON, default=list)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    paper: Mapped[Paper] = relationship(back_populates="questions")
    analyses: Mapped[list["QuestionAnalysis"]] = relationship(back_populates="question", cascade="all, delete-orphan")
    embeddings: Mapped[list["QuestionEmbedding"]] = relationship(cascade="all, delete-orphan")


class QuestionEmbedding(Base):
    __tablename__ = "question_embeddings"
    __table_args__ = (UniqueConstraint("question_id", "model_digest", "part_id", name="uq_question_embedding_part"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    question_revision: Mapped[int] = mapped_column(Integer)
    model: Mapped[str] = mapped_column(String(200), index=True)
    model_digest: Mapped[str] = mapped_column(String(128), index=True)
    part_id: Mapped[str] = mapped_column(String(80))
    source_hash: Mapped[str] = mapped_column(String(64))
    dimensions: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list] = mapped_column(Vector())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class QuestionAnalysis(Base):
    __tablename__ = "question_analyses"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    question_revision: Mapped[int] = mapped_column(Integer)
    analyzer_model: Mapped[str] = mapped_column(String(120))
    prompt_version: Mapped[str] = mapped_column(String(80))
    cache_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    analysis: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    question: Mapped[Question] = relationship(back_populates="analyses")


class Comparison(Base):
    __tablename__ = "comparisons"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(250))
    generated_paper_id: Mapped[int | None] = mapped_column(ForeignKey("papers.id"), nullable=True)
    rerun_of_id: Mapped[int | None] = mapped_column(ForeignKey("comparisons.id", ondelete="SET NULL"), nullable=True)
    target_ids: Mapped[list] = mapped_column(JSON)
    reference_ids: Mapped[list] = mapped_column(JSON)
    template_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(30), default="queued")
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    activities: Mapped[list["ComparisonActivity"]] = relationship(back_populates="comparison", cascade="all, delete-orphan")


class ComparisonActivity(Base):
    __tablename__ = "comparison_activities"
    id: Mapped[int] = mapped_column(primary_key=True)
    comparison_id: Mapped[int] = mapped_column(ForeignKey("comparisons.id"), index=True)
    target_id: Mapped[int] = mapped_column(Integer)
    reference_id: Mapped[int] = mapped_column(Integer)
    agent: Mapped[str] = mapped_column(String(30))
    event: Mapped[str] = mapped_column(String(40))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    comparison: Mapped[Comparison] = relationship(back_populates="activities")


class PairResult(Base):
    __tablename__ = "pair_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    comparison_id: Mapped[int] = mapped_column(ForeignKey("comparisons.id"))
    target_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    reference_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    label: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    source: Mapped[str] = mapped_column(Text)
    model: Mapped[str | None] = mapped_column(Text, nullable=True)
    cache_key: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Template(Base):
    __tablename__ = "templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int | None] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    kind: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(200))
    definition: Mapped[dict] = mapped_column(JSON)
    version: Mapped[int] = mapped_column(Integer, default=1)


class Material(Base):
    __tablename__ = "materials"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    filename: Mapped[str] = mapped_column(String(250))
    file_hash: Mapped[str] = mapped_column(String(64))
    extracted_text: Mapped[str] = mapped_column(Text)
    warnings: Mapped[list] = mapped_column(JSON, default=list)
    proposals: Mapped[dict] = mapped_column(JSON, default=dict)
    enrichment: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(100))
    details: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True)
    display_name: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(20))
    password_hash: Mapped[str] = mapped_column(String(200))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    subject_ids: Mapped[list] = mapped_column(JSON, default=list)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))
    text: Mapped[str] = mapped_column(Text)
    card: Mapped[str | None] = mapped_column(String(40), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class BackgroundJob(Base):
    __tablename__ = "background_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(60), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=2)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


ROOT = Path(__file__).resolve().parents[1]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://faculty@127.0.0.1:5432/faculty")
if DATABASE_URL.startswith("sqlite"):
    (ROOT / "data").mkdir(exist_ok=True)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
Session = sessionmaker(engine, expire_on_commit=False)


@event.listens_for(Session.class_, "before_flush")
def queue_changed_question_embeddings(db, flush_context, instances):
    """Every authoring path schedules the same incremental embedding worker."""
    if not os.getenv("EMBEDDING_MODEL_NAME", "qwen3-embedding:4b"):
        return
    paper_ids = {item.paper_id for item in db.new if isinstance(item, Question) and item.paper_id}
    paper_ids.update(item.paper_id for item in db.dirty if isinstance(item, Question) and (
        inspect(item).attrs.text.history.has_changes() or inspect(item).attrs.revision.history.has_changes()
    ))
    for item in list(db.new):
        if isinstance(item, QuestionAnalysis):
            question = db.get(Question, item.question_id)
            if question:
                paper_ids.add(question.paper_id)
    for pid in paper_ids:
        if any(isinstance(job, BackgroundJob) and job.kind == "index_paper" and job.payload.get("paper_id") == pid for job in db.new):
            continue
        queued = db.scalar(select(BackgroundJob.id).where(BackgroundJob.kind == "index_paper", BackgroundJob.status == "queued", BackgroundJob.payload["paper_id"].as_integer() == pid))
        if queued is None:
            db.add(BackgroundJob(kind="index_paper", payload={"paper_id": pid}))


def initialize() -> None:
    from alembic import command
    from alembic.config import Config

    migration = Config()
    migration.set_main_option("script_location", str(Path(__file__).resolve().parent / "migrations"))
    migration.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))
    command.upgrade(migration, "head")
    from json import loads

    with Session.begin() as db:
        for short in ("os", "iot"):
            tree = loads((ROOT / "project-handoff" / "trees" / f"{short}-enriched-tree.json").read_text())
            existing = db.query(Subject).filter_by(code=tree["course"]["code"]).first()
            if not existing:
                db.add(Subject(code=tree["course"]["code"], name=tree["course"]["title"], tree=tree))
        db.flush()
        for subject in db.query(Subject).all():
            if not db.query(TreeRevision).filter_by(subject_id=subject.id).first():
                db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=subject.tree, reason="active tree snapshot"))
        if not db.query(AuditEvent).filter_by(action="default_templates_seeded").first():
            default_scopes = [
                ("Check this paper", {"target_rule": "selected_paper", "reference_rule": "all_reference", "include_within_target": True}),
                ("Compare against the last five reference papers", {"target_rule": "selected_paper", "reference_rule": "last_n_reference", "last_n": 5, "include_within_target": False}),
                ("Check within one paper", {"target_rule": "within_paper", "reference_rule": "same_paper", "include_within_target": True}),
                ("Selected questions against references", {"target_rule": "selected_questions", "reference_rule": "all_reference", "include_within_target": False}),
                ("Audit the question bank", {"target_rule": "whole_bank", "reference_rule": "all_bank", "include_within_target": True}),
            ]
            for name, definition in default_scopes:
                db.add(Template(subject_id=None, kind="comparison", name=name, definition=definition))
            default_result = {"title": "Comparison results", "columns": ["base_paper", "base_question_number", "reference_paper", "reference_question_number", "label", "reason", "evidence_ids", "stale"]}
            db.add(Template(subject_id=None, kind="result", name="Default comparison report", definition=default_result))
            db.add(AuditEvent(action="default_templates_seeded", details={"templates": 6, "version": 1}))
        if os.getenv("AUTH_MODE", "local") == "shared" and not db.query(User).first():
            email, password = os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD")
            if not email or not password:
                raise RuntimeError("Shared mode requires ADMIN_EMAIL and ADMIN_PASSWORD on first start")
            from .security import hash_password

            db.add(User(email=email.lower().strip(), display_name="Administrator", role="admin", password_hash=hash_password(password), subject_ids=[]))
