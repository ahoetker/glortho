"""unique email and username

Revision ID: cd218780f3f9
Revises: 382b84a3c7af
Create Date: 2021-06-22 16:04:55.465593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column, func


# revision identifiers, used by Alembic
revision = "cd218780f3f9"
down_revision = "382b84a3c7af"
branch_labels = None
depends_on = None


def create_length_constraint():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_check_constraint(
            "ck_username_min_len",
            func.char_length(column("username")) >= 3,
        )
        batch_op.create_check_constraint(
            "ck_username_max_len",
            func.char_length(column("username")) <= 30,
        )


def create_unique_constraints():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_user_name", ["username"])
        batch_op.create_unique_constraint("uq_email", ["email"])


def drop_length_constraint():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("ck_username_min_len")
        batch_op.drop_constraint("ck_username_max_len")


def drop_unique_constraints():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("uq_user_name")
        batch_op.drop_constraint("uq_email")


def upgrade() -> None:
    create_length_constraint()
    create_unique_constraints()


def downgrade() -> None:
    drop_length_constraint()
    drop_unique_constraints()
