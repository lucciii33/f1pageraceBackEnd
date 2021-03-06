"""empty message

Revision ID: f5db7181b83e
Revises: 9654489b5720
Create Date: 2022-05-11 18:47:19.060504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5db7181b83e'
down_revision = '9654489b5720'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('favorite', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite', sa.Column('name', mysql.VARCHAR(length=150), nullable=False))
    # ### end Alembic commands ###
