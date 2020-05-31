"""empty message

Revision ID: 314303270c73
Revises: a0a3d8301838
Create Date: 2020-05-24 18:45:09.821238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '314303270c73'
down_revision = 'a0a3d8301838'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('done', sa.Column('points_given', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('done', 'points_given')
    # ### end Alembic commands ###
