"""Adopt existing workspaces and create the current schema for new installs."""

from alembic import op

revision = "0001_legacy_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    from exam_assistant.db import Base

    if op.get_bind().dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    Base.metadata.create_all(bind=op.get_bind())


def downgrade():
    # The baseline adopts user data and is deliberately irreversible.
    pass
