"""add some columns to user model

Revision ID: 0e9f780c0b4a
Revises: e99ac8a9acab
Create Date: 2024-07-18 18:42:12.949480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0e9f780c0b4a'
down_revision: Union[str, None] = 'e99ac8a9acab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "name")
    op.add_column("users", sa.Column(
        "first_name", sa.String(255), nullable=True))
    op.add_column("users", sa.Column(
        "last_name", sa.String(255), nullable=True))
    op.add_column("users", sa.Column(
        "username", sa.String(255), nullable=False))
    op.add_column("users", sa.Column(
        "photo_url", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "first_name")
    op.drop_column("users", "last_name")
    op.drop_column("users", "username")
    op.drop_column("users", "photo_url")
    op.add_column("users", sa.Column(
        "name", sa.String(255), nullable=True)
                  )
