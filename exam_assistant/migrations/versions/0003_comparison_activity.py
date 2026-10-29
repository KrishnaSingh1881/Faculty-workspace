"""Persist helper, judge and tool activity for live comparison review."""

import sqlalchemy as sa
from alembic import op

revision = "0003_comparison_activity"
down_revision = "0002_legacy_columns"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "comparison_activities" not in inspector.get_table_names():
        op.create_table(
            "comparison_activities",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("comparison_id", sa.Integer(), sa.ForeignKey("comparisons.id"), nullable=False),
            sa.Column("target_id", sa.Integer(), nullable=False),
            sa.Column("reference_id", sa.Integer(), nullable=False),
            sa.Column("agent", sa.String(30), nullable=False),
            sa.Column("event", sa.String(40), nullable=False),
            sa.Column("payload", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        )
    inspector = sa.inspect(op.get_bind())
    indexes = {index["name"] for index in inspector.get_indexes("comparison_activities")}
    if "ix_comparison_activities_comparison_id" not in indexes:
        op.create_index("ix_comparison_activities_comparison_id", "comparison_activities", ["comparison_id"])


def downgrade():
    op.drop_table("comparison_activities")
