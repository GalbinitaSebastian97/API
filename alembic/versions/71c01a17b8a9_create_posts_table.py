"""create posts table

Revision ID: 71c01a17b8a9
Revises: 
Create Date: 2021-11-06 15:53:28.061615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71c01a17b8a9'
down_revision = None
branch_labels = None
depends_on = None

# handles the changes
def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column('title',sa.String(), nullable=False))
    pass

# handles rolling it back
def downgrade():
    op.drop_table('posts')
    pass
