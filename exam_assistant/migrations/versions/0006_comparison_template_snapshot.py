"""Persist the scope and report layout used by a comparison run."""

import sqlalchemy as sa
from alembic import op

revision = "0006_comparison_template_snapshot"
down_revision = "0005_comparison_reruns"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "comparisons" in inspector.get_table_names() and "template_snapshot" not in {column["name"] for column in inspector.get_columns("comparisons")}:
        with op.batch_alter_table("comparisons") as batch:
            batch.add_column(sa.Column("template_snapshot", sa.JSON(), nullable=False, server_default=sa.text("'{}'")))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if "comparisons" in inspector.get_table_names() and "template_snapshot" in {column["name"] for column in inspector.get_columns("comparisons")}:
        with op.batch_alter_table("comparisons") as batch:
            batch.drop_column("template_snapshot")
