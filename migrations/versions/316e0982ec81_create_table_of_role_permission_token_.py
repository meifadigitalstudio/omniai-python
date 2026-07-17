"""create table of role, permission, token, and audit

Revision ID: 316e0982ec81
Revises: c85a3fb5d4f5
Create Date: 2026-07-17 11:30:44.770731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '316e0982ec81'
down_revision: Union[str, Sequence[str], None] = 'c85a3fb5d4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
