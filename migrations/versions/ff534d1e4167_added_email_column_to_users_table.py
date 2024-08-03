from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'ff534d1e4167'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the email column as nullable
    op.add_column('users', sa.Column('email', sa.String(length=150), nullable=True))

    # Step 2: Update existing rows with a default value
    op.execute(text("UPDATE users SET email = 'user_' || user_id || '@example.com' WHERE email IS NULL"))

    # Step 3: Alter the column to be NOT NULL
    op.alter_column('users', 'email', nullable=False)

    # Step 4: Add the unique constraint
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

def downgrade():
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_column('users', 'email')