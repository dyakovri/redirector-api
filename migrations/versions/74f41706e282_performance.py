"""Performance

Revision ID: 74f41706e282
Revises: 3e5b8cfd7d4a
Create Date: 2025-08-03 09:34:35.074312

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "74f41706e282"
down_revision = "3e5b8cfd7d4a"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DELETE FROM redirect_fact WHERE link_id IS NULL;")
    op.alter_column("redirect_fact", "link_id", existing_type=sa.INTEGER(), nullable=False)
    op.create_unique_constraint("unique__user__username", "user", ["username"])

    op.create_index("idx__link__owner_id", "link", ["owner_id"], unique=False, postgresql_using="hash")
    op.create_index("idx__link__url_from", "link", ["url_from"], unique=False, postgresql_using="hash")
    op.create_index("idx__redirect_fact__link_id", "redirect_fact", ["link_id", "created_at"], unique=False)
    op.create_index("idx__user__username", "user", ["username"], unique=False, postgresql_using="hash")


def downgrade():
    op.drop_index("idx__user__username", table_name="user", postgresql_using="hash")
    op.drop_index("idx__redirect_fact__link_id", table_name="redirect_fact")
    op.drop_index("idx__link__url_from", table_name="link", postgresql_using="hash")
    op.drop_index("idx__link__owner_id", table_name="link", postgresql_using="hash")

    op.drop_constraint("unique__user__username", "user", type_="unique")
    op.alter_column("redirect_fact", "link_id", existing_type=sa.INTEGER(), nullable=True)
