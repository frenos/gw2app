"""empty message

Revision ID: 30f140742043
Revises: 2cc88b90620e
Create Date: 2015-11-07 18:51:59.658000

"""

# revision identifiers, used by Alembic.
revision = '30f140742043'
down_revision = '2cc88b90620e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TPtransactions_broken', sa.Column('type', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TPtransactions_broken', 'type')
    ### end Alembic commands ###
