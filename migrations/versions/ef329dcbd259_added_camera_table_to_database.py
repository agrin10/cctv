"""added camera table to database

Revision ID: ef329dcbd259
Revises: 1bcd15178692
Create Date: 2024-08-10 12:14:18.240170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef329dcbd259'
down_revision = '1bcd15178692'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cameras',
    sa.Column('camera_id', sa.String(length=225), nullable=False),
    sa.Column('camera_name', sa.String(length=150), nullable=False),
    sa.Column('camera_ip', sa.String(length=150), nullable=False),
    sa.Column('cameera_type', sa.String(length=150), nullable=False),
    sa.Column('camera_zone', sa.String(length=225), nullable=False),
    sa.Column('camera_password_hash', sa.String(length=150), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['camera_zone'], ['zones.name'], ),
    sa.PrimaryKeyConstraint('camera_id'),
    sa.UniqueConstraint('camera_id'),
    sa.UniqueConstraint('camera_ip')
    )
    with op.batch_alter_table('zones', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['zone_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('zones', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('cameras')
    # ### end Alembic commands ###