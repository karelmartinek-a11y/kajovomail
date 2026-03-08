"""add user ai settings columns"""
from alembic import op
import sqlalchemy as sa


revision = "0002_user_ai_settings"
down_revision = "0001_initial"
branch_labels = None
depend_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS openai_api_key TEXT")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS ai_response_style VARCHAR(32) DEFAULT 'balanced'")
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS openai_model VARCHAR(64)")


def downgrade() -> None:
    op.drop_column("users", "openai_model")
    op.drop_column("users", "ai_response_style")
    op.drop_column("users", "openai_api_key")
