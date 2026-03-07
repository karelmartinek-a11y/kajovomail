"""add user ai settings columns"""
from alembic import op
import sqlalchemy as sa


revision = "0002_user_ai_settings"
down_revision = "0001_initial"
branch_labels = None
depend_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("openai_api_key", sa.Text(), nullable=True))
    op.add_column(
        "users",
        sa.Column("ai_response_style", sa.String(length=32), nullable=False, server_default="balanced"),
    )
    op.add_column("users", sa.Column("openai_model", sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "openai_model")
    op.drop_column("users", "ai_response_style")
    op.drop_column("users", "openai_api_key")
