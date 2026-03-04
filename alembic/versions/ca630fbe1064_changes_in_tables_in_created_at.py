"""changes in tables in created_at

Revision ID: ca630fbe1064
Revises: f1fe95ac9ac7
Create Date: 2026-03-04 19:22:45.269624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca630fbe1064'
down_revision: Union[str, Sequence[str], None] = 'f1fe95ac9ac7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('orders', 'created_at',
                   type_=sa.DateTime(),
                   nullable=True)

    op.alter_column('products', 'created_at',
                   type_=sa.DateTime(),
                   nullable=True)

    op.alter_column('users', 'created_at',
                   type_=sa.DateTime(),
                   nullable=True)


def downgrade() -> None:
    op.alter_column('orders', 'created_at',
                   type_=sa.DateTime(),
                   nullable=False)

    op.alter_column('products', 'created_at',
                   type_=sa.DateTime(),
                   nullable=False)

    op.alter_column('users', 'created_at',
                   type_=sa.DateTime(),
                   nullable=False)
