"""empty message

Revision ID: 2cc88b90620e
Revises: 48ef2c8f0c45
Create Date: 2015-11-07 18:50:08.359000

"""

# revision identifiers, used by Alembic.
revision = '2cc88b90620e'
down_revision = '48ef2c8f0c45'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TPtransactions', sa.Column('type', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TPtransactions', 'type')
    ### end Alembic commands ###
