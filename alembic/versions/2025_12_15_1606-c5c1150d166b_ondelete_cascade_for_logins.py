"""ondelete=cascade for logins

Revision ID: c5c1150d166b
Revises: 51f7530fa4ec
Create Date: 2025-12-15 16:06:32.431362

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5c1150d166b"
down_revision: Union[str, Sequence[str], None] = "51f7530fa4ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f("logins_user_id_fkey"), "logins", type_="foreignkey")
    op.create_foreign_key(
        None, "logins", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "logins", type_="foreignkey")
    op.create_foreign_key(
        op.f("logins_user_id_fkey"), "logins", "users", ["user_id"], ["id"]
    )
