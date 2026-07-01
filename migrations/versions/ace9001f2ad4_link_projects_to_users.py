"""link projects to users

Revision ID: ace9001f2ad4
Revises: 6299f895f7a7
Create Date: 2026-07-01 17:21:27.146938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ace9001f2ad4'
down_revision: Union[str, Sequence[str], None] = '6299f895f7a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ----------------------------------
    # Add user_id column
    # ----------------------------------
    op.add_column(
        "projects",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ----------------------------------
    # Create index
    # ----------------------------------
    op.create_index(
        "ix_projects_user_id",
        "projects",
        ["user_id"],
    )

    # ----------------------------------
    # Foreign key
    # ----------------------------------
    op.create_foreign_key(
        "fk_projects_user_id",
        "projects",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_projects_user_id",
        "projects",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_projects_user_id",
        table_name="projects",
    )

    op.drop_column(
        "projects",
        "user_id",
    )