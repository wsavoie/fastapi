"""link user table to the post table

Revision ID: a230a2685beb
Revises: f9c343381545
Create Date: 2022-04-18 16:11:35.801551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a230a2685beb'
down_revision = 'f9c343381545'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                           local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
