"""empty message

Revision ID: 1360cc8bab82
Revises: 
Create Date: 2020-05-31 01:52:43.443980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1360cc8bab82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('associates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start', sa.Time(), nullable=True),
    sa.Column('end', sa.Time(), nullable=True),
    sa.Column('fsp', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('numPeople', sa.Integer(), nullable=True),
    sa.Column('sent', sa.Boolean(), nullable=True),
    sa.Column('employees', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('bike',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start', sa.Time(), nullable=True),
    sa.Column('end', sa.Time(), nullable=True),
    sa.Column('fsp', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('numPeople', sa.Integer(), nullable=True),
    sa.Column('sent', sa.Boolean(), nullable=True),
    sa.Column('employees', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bike')
    op.drop_table('associates')
    # ### end Alembic commands ###
