"""table followers

Revision ID: 459e9d73bb8b
Revises: a6afafb0815f
Create Date: 2022-03-25 22:52:50.646419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459e9d73bb8b'
down_revision = 'a6afafb0815f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###