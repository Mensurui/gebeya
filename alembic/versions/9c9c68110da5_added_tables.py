"""Added Tables

Revision ID: 9c9c68110da5
Revises: 52b38d103bae
Create Date: 2024-07-16 13:41:06.599518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c9c68110da5'
down_revision: Union[str, None] = '52b38d103bae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('item_selling_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'selling_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('selling_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('item_selling_id_fkey', 'item', 'selling', ['selling_id'], ['id'])
    # ### end Alembic commands ###
