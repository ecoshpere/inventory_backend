"""add department to services

Revision ID: 007
Revises: 006
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    # Add department_id column to services table
    op.add_column('services', sa.Column('department_id', sa.String(), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key('fk_services_department_id', 'services', 'departments', ['department_id'], ['id'])
    
    # Make department_id required after adding the column
    op.alter_column('services', 'department_id', nullable=False)


def downgrade():
    # Remove foreign key constraint
    op.drop_constraint('fk_services_department_id', 'services', type_='foreignkey')
    
    # Remove department_id column
    op.drop_column('services', 'department_id')
