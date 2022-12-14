"""Create stat_received_objects table

Revision ID: bfc9ce28865a
Revises: 
Create Date: 2022-12-15 00:44:37.095166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfc9ce28865a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stat_received_objects',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stat_received_objects_created_at'), 'stat_received_objects', ['created_at'], unique=False)
    op.create_index(op.f('ix_stat_received_objects_id'), 'stat_received_objects', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stat_received_objects_id'), table_name='stat_received_objects')
    op.drop_index(op.f('ix_stat_received_objects_created_at'), table_name='stat_received_objects')
    op.drop_table('stat_received_objects')
    # ### end Alembic commands ###