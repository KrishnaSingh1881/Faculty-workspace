"""Link refreshed comparison runs to their retained source run."""

import sqlalchemy as sa
from alembic import op

revision = "0005_comparison_reruns"
down_revision = "0004_syllabus_import_owner"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "comparisons" in inspector.get_table_names() and "rerun_of_id" not in {column["name"] for column in inspector.get_columns("comparisons")}:
        with op.batch_alter_table("comparisons") as batch:
            batch.add_column(sa.Column("rerun_of_id", sa.Integer(), sa.ForeignKey("comparisons.id", ondelete="SET NULL"), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if "comparisons" in inspector.get_table_names() and "rerun_of_id" in {column["name"] for column in inspector.get_columns("comparisons")}:
        with op.batch_alter_table("comparisons") as batch:
            batch.drop_column("rerun_of_id")
