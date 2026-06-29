"""link api keys to plans

Revision ID: 9f5cae4b4982
Revises: fa1b4e0f56c5
Create Date: 2026-06-29 20:04:56.914503

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9f5cae4b4982"
down_revision: Union[str, Sequence[str], None] = "fa1b4e0f56c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------
    # Add plan_id safely (backfill old rows)
    # ---------------------------------------
    op.add_column(
        "api_keys",
        sa.Column(
            "plan_id",
            sa.Integer(),
            nullable=False,
            server_default="1",  # ensures existing rows get default plan
        ),
    )

    # ---------------------------------------
    # Foreign key constraint
    # ---------------------------------------
    op.create_foreign_key(
        "fk_api_keys_plan",
        "api_keys",
        "plans",
        ["plan_id"],
        ["id"],
    )

    # ---------------------------------------
    # Adjust plans.name size (autogen change)
    # ---------------------------------------
    op.alter_column(
        "plans",
        "name",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=False,
    )


def downgrade() -> None:
    # ---------------------------------------
    # Remove FK first
    # ---------------------------------------
    op.drop_constraint(
        "fk_api_keys_plan",
        "api_keys",
        type_="foreignkey",
    )

    # ---------------------------------------
    # Remove column
    # ---------------------------------------
    op.drop_column("api_keys", "plan_id")

    # ---------------------------------------
    # Revert plans.name change
    # ---------------------------------------
    op.alter_column(
        "plans",
        "name",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
    )