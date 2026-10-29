"""Versioned question/part embeddings and full-length model provenance."""

from alembic import op
import sqlalchemy as sa

revision = "0007_question_embeddings"
down_revision = "0006_comparison_template_snapshot"
branch_labels = None
depends_on = None


def upgrade():
    from exam_assistant.db import QuestionEmbedding
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    QuestionEmbedding.__table__.create(bind, checkfirst=True)
    if bind.dialect.name == "postgresql":
        op.alter_column("pair_results", "source", type_=sa.Text())
        op.alter_column("pair_results", "model", type_=sa.Text())
        op.create_check_constraint("embedding_dimensions_match", "question_embeddings", "dimensions BETWEEN 1 AND 16000 AND vector_dims(embedding) = dimensions")


def downgrade():
    op.drop_table("question_embeddings")
