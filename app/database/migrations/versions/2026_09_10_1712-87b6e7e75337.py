"""add admin to userrole enum

Revision ID: 87b6e7e75337
Revises: db589d13e28d
Create Date: 2026-09-10 17:12:21.982353

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "87b6e7e75337"
down_revision: Union[str, Sequence[str], None] = "db589d13e28d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'admin'")


def downgrade() -> None:
    """Downgrade schema."""
    # Удалить значение из enum в PostgreSQL нельзя без пересоздания типа.
    pass
