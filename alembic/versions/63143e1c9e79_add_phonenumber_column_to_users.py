"""add phonenumber column to users

Revision ID: 63143e1c9e79
Revises: f7ce22ff59f9
Create Date: 2022-04-18 16:29:51.605182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63143e1c9e79'
down_revision = 'f7ce22ff59f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
