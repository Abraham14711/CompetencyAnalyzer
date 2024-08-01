"""add role to users model

Revision ID: f76b0af26e31
Revises: 0e9f780c0b4a
Create Date: 2024-07-18 20:31:52.246403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f76b0af26e31'
down_revision: Union[str, None] = '0e9f780c0b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column(
        "role", sa.String(255), nullable=False,
        default="USER"))


def downgrade() -> None:
    op.drop_column("users", "role")
