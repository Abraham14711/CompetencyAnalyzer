"""added answers field to question model

Revision ID: e99ac8a9acab
Revises: bd149012d885
Create Date: 2024-07-16 21:16:14.984128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e99ac8a9acab'
down_revision: Union[str, None] = 'bd149012d885'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'questions',
        sa.Column(
            'answers',
            sa.String(255),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('questions', 'answers')
