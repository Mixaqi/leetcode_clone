"""add composite pk to users_roles, hashed_password renamed to password in userBase

Revision ID: 3648d6b449e3
Revises: 052432239c1c
Create Date: 2025-12-19 14:14:14.856535

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3648d6b449e3"
down_revision: Union[str, Sequence[str], None] = "052432239c1c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f("logins_user_id_fkey"), "logins", type_="foreignkey")
    op.create_foreign_key(None, "logins", "users", ["user_id"], ["id"])
    op.add_column("users", sa.Column("password", sa.String(), nullable=False))
    op.drop_column("users", "hashed_password")
    op.drop_column("users_roles", "id")



def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users_roles", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("users", "password")
    op.drop_constraint(None, "logins", type_="foreignkey")
    op.create_foreign_key(
        op.f("logins_user_id_fkey"),
        "logins",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
