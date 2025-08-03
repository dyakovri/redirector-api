"""log redirect

Revision ID: b8d6bdfce7e8
Revises: b1fa3f4c93a2
Create Date: 2023-06-17 20:14:37.070739

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b8d6bdfce7e8'
down_revision = 'b1fa3f4c93a2'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("redirects", "link")
    op.create_table('redirect_fact',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('link_id', sa.Integer(), nullable=True),
        sa.Column('method', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=False),
        sa.Column('browser_family', sa.String(), nullable=False),
        sa.Column('browser_version', sa.String(), nullable=False),
        sa.Column('os_family', sa.String(), nullable=False),
        sa.Column('os_version', sa.String(), nullable=False),
        sa.Column('device_family', sa.String(), nullable=False),
        sa.Column('device_brand', sa.String(), nullable=False),
        sa.Column('device_model', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['link_id'], ['link.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.rename_table("link", "redirects")
    op.drop_table('redirect_fact')
