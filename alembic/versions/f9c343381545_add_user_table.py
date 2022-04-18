"""add user table

Revision ID: f9c343381545
Revises: 05ad19193622
Create Date: 2022-04-18 16:04:40.802297

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9c343381545'
down_revision = '05ad19193622'
branch_labels = None
depends_on = None


def upgrade():
        op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),       
            )


def downgrade():
    op.drop_table('users')
