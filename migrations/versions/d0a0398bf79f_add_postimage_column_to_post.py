"""Add postimage column to Post

Revision ID: d0a0398bf79f
Revises: baa06cb5a46e
Create Date: 2024-05-18 15:26:32.503553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0a0398bf79f'
down_revision: Union[str, None] = 'baa06cb5a46e'
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
