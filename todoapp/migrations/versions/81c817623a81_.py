"""empty message

Revision ID: 81c817623a81
Revises: 5871e186a7b1
Create Date: 2020-01-28 15:15:55.152155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c817623a81'
down_revision = '5871e186a7b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###
    #create the missing old values as the col values cant be null
    op.execute('update todos set completed = False whers completed IS NULL;')
    #new vals can't be null
    op.alter_column('todos', 'completed', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
