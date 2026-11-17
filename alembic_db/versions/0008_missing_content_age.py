"""Track when content becomes missing for age-based catalog cleanup."""

from alembic import op
import sqlalchemy as sa


revision = "0008_missing_content_age"
down_revision = "0007_record_content_split"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("asset_contents", sa.Column("missing_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE asset_contents SET missing_at = CURRENT_TIMESTAMP WHERE is_missing = 1")
    op.create_index("ix_asset_contents_missing_at", "asset_contents", ["is_missing", "missing_at"])


def downgrade() -> None:
    op.drop_index("ix_asset_contents_missing_at", table_name="asset_contents")
    op.drop_column("asset_contents", "missing_at")
