"""added module table 

Revision ID: 60f4e1e82e8b
Revises: 6334054fba19
Create Date: 2024-09-11 11:28:08.923499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60f4e1e82e8b'
down_revision = '6334054fba19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('modules',
    sa.Column('module_id', sa.String(length=225), nullable=False),
    sa.Column('module_name', sa.String(length=225), nullable=False),
    sa.PrimaryKeyConstraint('module_id'),
    sa.UniqueConstraint('module_id')
    )
    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permissions_id', sa.String(length=225), nullable=True))
        batch_op.drop_constraint('accesses_permisions_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('accesses_camera_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'permissions', ['permissions_id'], ['id'])
        batch_op.drop_column('camera_id')
        batch_op.drop_column('permisions_id')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.drop_column('description')

    with op.batch_alter_table('user_access', schema=None) as batch_op:
        batch_op.add_column(sa.Column('access_id', sa.String(length=225), nullable=True))
        batch_op.drop_constraint('user_access_camera_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_access_permission_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'accesses', ['access_id'], ['id'])
        batch_op.drop_column('camera_id')
        batch_op.drop_column('permission_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_access', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permission_id', sa.VARCHAR(length=225), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('camera_id', sa.VARCHAR(length=225), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_access_permission_id_fkey', 'permissions', ['permission_id'], ['id'])
        batch_op.create_foreign_key('user_access_camera_id_fkey', 'cameras', ['camera_id'], ['camera_id'])
        batch_op.drop_column('access_id')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))

    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permisions_id', sa.VARCHAR(length=225), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('camera_id', sa.VARCHAR(length=225), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('accesses_camera_id_fkey', 'cameras', ['camera_id'], ['camera_id'])
        batch_op.create_foreign_key('accesses_permisions_id_fkey', 'permissions', ['permisions_id'], ['id'])
        batch_op.drop_column('permissions_id')

    op.drop_table('modules')
    # ### end Alembic commands ###