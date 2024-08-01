"""rebase users and answers tables

Revision ID: bd149012d885
Revises: 2cae90bf653d
Create Date: 2024-07-14 13:52:12.513512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd149012d885'
down_revision: Union[str, None] = '2cae90bf653d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'id')
    op.drop_column('answers', 'personal_data')
    op.add_column(
        'users',
        sa.Column(
            'telegram_id',
            sa.String(255),
            nullable=False,
            unique=True,
        )
    )
    op.create_primary_key(
        'users_pkey',
        'users',
        ['telegram_id']
    )
    op.create_unique_constraint(
        'users_telegram_id_key',
        'users',
        ['telegram_id']
    )
    print("SUCCESS")
    op.add_column(
        'users',
        sa.Column(
            'name',
            sa.String(255),
            nullable=False
        )
    )
    print("SUCCESS")
    op.add_column(
        'users',
        sa.Column(
            'email',
            sa.String(255),
            nullable=False
        )
    )
    print("SUCCESS")
    op.add_column(
        'answers',
        sa.Column(
            'user_id',
            sa.String(255),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('users', 'telegram_id')
    op.drop_column('users', 'name')
    op.drop_column('users', 'email')
    op.drop_column('answers', 'user_id')
    op.add_column(
        'users',
        sa.Column(
            'id',
            sa.UUID(),
            autoincrement=False,
            nullable=False
        )
    )
    op.add_column(
        'answers',
        sa.Column(
            'personal_data',
            sa.TEXT(),
            autoincrement=False,
            nullable=False
        )
    )
