"""added relationship for users 

Revision ID: 524ff5a72de1
Revises: cdda0c53641d
Create Date: 2024-09-18 15:01:46.988889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524ff5a72de1'
down_revision = 'cdda0c53641d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['module_id'])

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('user_accesses', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_accesses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('accesses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###