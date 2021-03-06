"""Init

Revision ID: b1fa3f4c93a2
Revises: 
Create Date: 2021-11-08 15:52:23.358525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1fa3f4c93a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('redirects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_from', sa.String(), nullable=False),
    sa.Column('url_to', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url_from')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('redirects')
    # ### end Alembic commands ###
