"""add content column to posts table

Revision ID: 87adf6876150
Revises: 71c01a17b8a9
Create Date: 2021-11-06 16:40:53.016287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87adf6876150'
down_revision = '71c01a17b8a9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    


def downgrade():
    op.drop_column('posts','content')
    pass
