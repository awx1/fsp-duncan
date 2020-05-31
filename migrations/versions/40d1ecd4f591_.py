"""empty message

Revision ID: 40d1ecd4f591
Revises: 314303270c73
Create Date: 2020-05-24 19:10:18.074826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40d1ecd4f591'
down_revision = '314303270c73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='done')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'done', ['name'], unique=True)
    # ### end Alembic commands ###
