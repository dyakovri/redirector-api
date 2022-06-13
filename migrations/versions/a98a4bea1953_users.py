"""Users

Revision ID: a98a4bea1953
Revises: b1fa3f4c93a2
Create Date: 2022-06-14 01:18:30.520742

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a98a4bea1953"
down_revision = "b1fa3f4c93a2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "redirector_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.execute(
        "INSERT INTO redirector_user(id, username,created_at, updated_at) VALUES "
        "(0, '### Unauthorized ###', now(), now());"
    )

    op.rename_table("redirects", "redirect")
    op.add_column("redirect", sa.Column("user_id", sa.Integer))
    op.execute("UPDATE redirect SET user_id=0;")
    op.create_foreign_key(
        "redirect_user_id_fkey", "redirect", "redirector_user", ["user_id"], ["id"]
    )
    op.alter_column("redirect", "user_id", nullable=False)


def downgrade():
    op.drop_constraint("redirect_user_id_fkey", "redirect", "foreignkey")
    op.drop_column("redirect", "user_id")
    op.rename_table("redirect", "redirects")
    op.drop_table("redirector_user")
