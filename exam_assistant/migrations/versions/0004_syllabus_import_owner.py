"""Track the account that submitted a syllabus import before activation."""

import sqlalchemy as sa
from alembic import op

revision = "0004_syllabus_import_owner"
down_revision = "0003_comparison_activity"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "syllabus_imports" in inspector.get_table_names() and "submitted_by" not in {column["name"] for column in inspector.get_columns("syllabus_imports")}:
        with op.batch_alter_table("syllabus_imports") as batch:
            batch.add_column(sa.Column("submitted_by", sa.Integer(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if "syllabus_imports" in inspector.get_table_names() and "submitted_by" in {column["name"] for column in inspector.get_columns("syllabus_imports")}:
        with op.batch_alter_table("syllabus_imports") as batch:
            batch.drop_column("submitted_by")
