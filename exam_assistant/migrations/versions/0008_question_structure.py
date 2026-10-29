"""Persist parsed subparts and choice groups for each uploaded question."""

from alembic import op
import sqlalchemy as sa

revision = "0008_question_structure"
down_revision = "0007_question_embeddings"
branch_labels = None
depends_on = None


def upgrade():
    columns = {item["name"] for item in sa.inspect(op.get_bind()).get_columns("questions")}
    if "structure" not in columns:
        with op.batch_alter_table("questions") as batch:
            batch.add_column(sa.Column("structure", sa.JSON(), nullable=False, server_default=sa.text("'{}'")))


def downgrade():
    with op.batch_alter_table("questions") as batch:
        batch.drop_column("structure")
