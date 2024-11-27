from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7f8630940e45'
down_revision: Union[str, None] = '7b2fb6b0dc54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the schedule_id column to the recycle table
    op.add_column('recycle', sa.Column('schedule_id', sa.UUID(), nullable=True))

    # Add a foreign key constraint to the schedule_id column
    op.create_foreign_key(
        'fk_recycle_schedule',  # Name of the foreign key constraint
        'recycle',              # Source table
        'schedules',            # Target table
        ['schedule_id'],        # Source column(s)
        ['id']                  # Target column(s)
    )


def downgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint('fk_recycle_schedule', 'recycle', type_='foreignkey')

    # Drop the schedule_id column from the recycle table
    op.drop_column('recycle', 'schedule_id')
