"""rename user_id to owner_id

Revision ID: 6bde33a12ada
Revises: ace9001f2ad4
Create Date: 2026-07-01 19:41:56.598235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bde33a12ada'
down_revision: Union[str, Sequence[str], None] = 'ace9001f2ad4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "projects",
        "user_id",
        new_column_name="owner_id",
    )

def downgrade():
    op.alter_column(
        "projects",
        "owner_id",
        new_column_name="user_id",
    )