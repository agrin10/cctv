"""adding initial changes for user accesses and permissions

Revision ID: 0f955a0150bd
Revises: 8a78208acf04
Create Date: 2024-09-10 15:51:27.083830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f955a0150bd'
down_revision = '8a78208acf04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=225), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('accesses',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('module_id', sa.String(), nullable=True),
    sa.Column('permisions_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['cameras.camera_id'], ),
    sa.ForeignKeyConstraint(['permisions_id'], ['permissions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user_access',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('camera_id', sa.String(), nullable=True),
    sa.Column('permission_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['camera_id'], ['cameras.camera_id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_access')
    op.drop_table('accesses')
    op.drop_table('permissions')
    # ### end Alembic commands ###