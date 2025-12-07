"""seed roles

Revision ID: 51f7530fa4ec
Revises: 6e274d206567
Create Date: 2025-12-07 22:19:34.318922
"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '51f7530fa4ec'
down_revision: Union[str, Sequence[str], None] = '6e274d206567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: insert predefined roles."""
    op.execute("""
        INSERT INTO roles (title, description) VALUES
        ('SUPERUSER', 'Administrator role. Full access'),
        ('USER', 'Regular user role'),
        ('STAFF', 'Moderator role');
    """)


def downgrade() -> None:
    """Downgrade schema: remove seeded roles."""
    op.execute("""
        DELETE FROM roles WHERE title IN ('SUPERUSER', 'USER', 'STAFF');
    """)
