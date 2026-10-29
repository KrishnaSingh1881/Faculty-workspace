"""Upgrade columns added before versioned migrations were introduced."""

import sqlalchemy as sa
from alembic import op

revision = "0002_legacy_columns"
down_revision = "0001_legacy_baseline"
branch_labels = None
depends_on = None


def _add_if_missing(table: str, column: sa.Column) -> None:
    inspector = sa.inspect(op.get_bind())
    if table in inspector.get_table_names() and column.name not in {item["name"] for item in inspector.get_columns(table)}:
        with op.batch_alter_table(table) as batch:
            batch.add_column(column)


def upgrade():
    _add_if_missing("materials", sa.Column("enrichment", sa.JSON(), nullable=False, server_default=sa.text("'{}'")))
    _add_if_missing("papers", sa.Column("generated", sa.Boolean(), nullable=False, server_default=sa.false()))
    _add_if_missing("papers", sa.Column("generation", sa.JSON(), nullable=False, server_default=sa.text("'{}'")))
    _add_if_missing("papers", sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.false()))
    _add_if_missing("comparisons", sa.Column("generated_paper_id", sa.Integer(), sa.ForeignKey("papers.id"), nullable=True))


def downgrade():
    pass
