"""User

Revision ID: 3e5b8cfd7d4a
Revises: 907eebbb213f
Create Date: 2025-08-03 09:08:37.634918

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3e5b8cfd7d4a"
down_revision = "907eebbb213f"
branch_labels = None
depends_on = None


def upgrade():
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.bulk_insert(user_table, [{"id": 0, "username": "undefined", "email": None, "full_name": None}])

    op.add_column("link", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.execute("UPDATE link SET owner_id = 0")
    op.alter_column("link", "owner_id", nullable=False)

    op.create_foreign_key("fk__link_owner_id__user_id", "link", "user", ["owner_id"], ["id"])


def downgrade():
    op.drop_constraint("fk__link_owner_id__user_id", "link", type_="foreignkey")
    op.drop_column("link", "owner_id")
    op.drop_table("user")
