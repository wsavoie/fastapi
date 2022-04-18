"""add content column

Revision ID: 05ad19193622
Revises: 5306497ff972
Create Date: 2022-04-18 15:59:39.007471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ad19193622'
down_revision = '5306497ff972'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
