"""create_user_jwt_tables

Revision ID: 382b84a3c7af
Revises: 90c9385481ba
Create Date: 2021-06-21 22:11:00.474778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "382b84a3c7af"
down_revision = "90c9385481ba"
branch_labels = None
depends_on = None


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, nullable=False, index=True),
        sa.Column("email", sa.Text, nullable=True),
        sa.Column("full_name", sa.Text, nullable=True),
        sa.Column("disabled", sa.Boolean, default=False),
        sa.Column("hashed_password", sa.Text, nullable=False),
    )


def create_token_blacklist_table() -> None:
    op.create_table(
        "blacklist",
        sa.Column("token", sa.Text, nullable=False, index=True),
    )


def upgrade() -> None:
    create_users_table()
    create_token_blacklist_table()


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("blacklist")
