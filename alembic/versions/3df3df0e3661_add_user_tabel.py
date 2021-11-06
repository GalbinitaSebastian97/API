"""add user tabel

Revision ID: 3df3df0e3661
Revises: 87adf6876150
Create Date: 2021-11-06 16:46:50.335622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df3df0e3661'
down_revision = '87adf6876150'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    
def downgrade():
    op.drop_table('users')
    pass
