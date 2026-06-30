from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "1c119759d966"
down_revision = "9f5cae4b4982"
branch_labels = None
depends_on = None


def upgrade():

    # ---------------------------------------
    # Projects
    # ---------------------------------------

    op.create_table(
        "projects",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "slug",
            sa.String(),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "description",
            sa.String(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # ---------------------------------------
    # Default Project
    # ---------------------------------------

    op.execute("""
        INSERT INTO projects
        (id, name, slug, description)
        VALUES
        (
            1,
            'Default Project',
            'default-project',
            'Automatically created project'
        );
    """)

    # ---------------------------------------
    # Link API Keys
    # ---------------------------------------

    op.add_column(
        "api_keys",
        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.execute("""
        UPDATE api_keys
        SET project_id = 1;
    """)

    op.alter_column(
        "api_keys",
        "project_id",
        nullable=False,
    )

    op.create_foreign_key(
        "fk_api_keys_project",
        "api_keys",
        "projects",
        ["project_id"],
        ["id"],
    )


def downgrade():

    op.drop_constraint(
        "fk_api_keys_project",
        "api_keys",
        type_="foreignkey",
    )

    op.drop_column(
        "api_keys",
        "project_id",
    )

    op.drop_table(
        "projects",
    )