"""upgrade tables'

Revision ID: 662a3ee1fceb
Revises: 7e1e7e5f650f
Create Date: 2024-07-21 18:56:00.690918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '662a3ee1fceb'
down_revision: Union[str, None] = '7e1e7e5f650f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###