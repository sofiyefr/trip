"""update route points schema

Revision ID: update_route_points
Revises: 
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_route_points'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Remove columns from trips table
    with op.batch_alter_table('trips') as batch_op:
        batch_op.drop_column('transportation_type')
        batch_op.drop_column('departure_city')
        batch_op.drop_column('destination_city')
    
    # Add transportation_type to route_points table
    with op.batch_alter_table('route_points') as batch_op:
        batch_op.add_column(sa.Column('transportation_type', sa.String(50)))

def downgrade():
    # Add columns back to trips table
    with op.batch_alter_table('trips') as batch_op:
        batch_op.add_column(sa.Column('transportation_type', sa.String(50)))
        batch_op.add_column(sa.Column('departure_city', sa.String(100)))
        batch_op.add_column(sa.Column('destination_city', sa.String(100)))
    
    # Remove transportation_type from route_points table
    with op.batch_alter_table('route_points') as batch_op:
        batch_op.drop_column('transportation_type') 