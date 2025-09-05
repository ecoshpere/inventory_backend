"""create services table

Revision ID: 006
Revises: 005
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '006'
down_revision = 'add_staff_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create services table
    op.create_table('services',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('category_id', sa.String(), nullable=False),
        sa.Column('image_thumbnail', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('barcode', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_services_name'), 'services', ['name'], unique=False)
    op.create_index(op.f('ix_services_barcode'), 'services', ['barcode'], unique=True)
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_index(op.f('ix_services_barcode'), table_name='services')
    op.drop_index(op.f('ix_services_name'), table_name='services')
    
    # Drop services table
    op.drop_table('services')
