"""add rest of post columns

Revision ID: 79f3b421011b
Revises: a230a2685beb
Create Date: 2022-04-18 16:18:31.434140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79f3b421011b'
down_revision = 'a230a2685beb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              nullable=False, server_default=sa.text('now()') ))

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
