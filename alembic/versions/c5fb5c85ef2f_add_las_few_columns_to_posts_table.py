"""add las few columns to posts table

Revision ID: c5fb5c85ef2f
Revises: c882efaa6f66
Create Date: 2021-11-06 17:13:25.843758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5fb5c85ef2f'
down_revision = 'c882efaa6f66'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(), nullable=False, server_default= "TRUE")
    )
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))

def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
