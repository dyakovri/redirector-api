"""log redirect fix nullable

Revision ID: 907eebbb213f
Revises: b8d6bdfce7e8
Create Date: 2023-06-17 21:20:08.155364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '907eebbb213f'
down_revision = 'b8d6bdfce7e8'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('redirect_fact', 'browser_family', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'browser_version', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'os_family', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'os_version', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'device_family', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'device_brand', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('redirect_fact', 'device_model', existing_type=sa.VARCHAR(), nullable=True)


def downgrade():
    op.alter_column('redirect_fact', 'device_model', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'device_brand', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'device_family', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'os_version', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'os_family', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'browser_version', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('redirect_fact', 'browser_family', existing_type=sa.VARCHAR(), nullable=False)
