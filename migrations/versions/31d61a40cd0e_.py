"""empty message

Revision ID: 31d61a40cd0e
Revises: 4aad4a6fba09
Create Date: 2024-09-16 11:45:08.583649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31d61a40cd0e'
down_revision = '4aad4a6fba09'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('module_id', sa.String(length=225), nullable=False))
        batch_op.alter_column('permissions_id', existing_type=sa.VARCHAR(length=225), nullable=False)
        batch_op.create_unique_constraint('uq_accesses_id', ['id'])
        batch_op.create_foreign_key('fk_accesses_module_id', 'modules', ['module_id'], ['module_id'])

    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_modules_name', ['module_name'])

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_permissions_id', ['id'])

    with op.batch_alter_table('user_accesses', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_user_accesses_id', ['id'])


def downgrade():
    with op.batch_alter_table('user_accesses', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_accesses_id', type_='unique')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.drop_constraint('uq_permissions_id', type_='unique')

    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.drop_constraint('uq_modules_name', type_='unique')

    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.drop_constraint('fk_accesses_module_id', type_='foreignkey')
        batch_op.drop_constraint('uq_accesses_id', type_='unique')
        batch_op.alter_column('permissions_id', existing_type=sa.VARCHAR(length=225), nullable=True)
        batch_op.drop_column('module_id')


    # ### end Alembic commands ###
