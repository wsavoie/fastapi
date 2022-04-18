"""create post table

Revision ID: 5306497ff972
Revises: 
Create Date: 2022-04-18 15:52:36.226892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5306497ff972'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                    sa.Column('title', sa.String(), nullable = False),
            )


def downgrade():
    op.drop_table('posts')
    pass
