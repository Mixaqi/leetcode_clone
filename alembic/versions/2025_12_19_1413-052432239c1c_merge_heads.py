"""merge heads

Revision ID: 052432239c1c
Revises: c5c1150d166b, 6455dead39f8
Create Date: 2025-12-19 14:13:03.444136

"""

from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "052432239c1c"
down_revision: str | Sequence[str] | None = ("c5c1150d166b", "6455dead39f8")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
