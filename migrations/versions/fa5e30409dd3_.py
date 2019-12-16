"""empty message

Revision ID: fa5e30409dd3
Revises: f1e107f5388e
Create Date: 2019-12-16 21:35:10.765894

"""

# revision identifiers, used by Alembic.
revision = 'fa5e30409dd3'
down_revision = 'f1e107f5388e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrows', sa.Column('end_date', sa.Date(), nullable=True))
    op.add_column('borrows', sa.Column('start_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('borrows', 'start_date')
    op.drop_column('borrows', 'end_date')
    # ### end Alembic commands ###