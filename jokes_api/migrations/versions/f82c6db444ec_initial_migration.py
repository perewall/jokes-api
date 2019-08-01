"""initial migration

Revision ID: f82c6db444ec
Revises:
Create Date: 2019-08-01 15:18:27.728112
"""

from alembic import op
import sqlalchemy as sa


revision = 'f82c6db444ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('token', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('username'),
        sa.UniqueConstraint('token'))

    op.create_table(
        'jokes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('user_id', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.username'], ),
        sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('jokes')
    op.drop_table('users')
