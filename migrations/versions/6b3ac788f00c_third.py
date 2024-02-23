"""'Third'

Revision ID: 6b3ac788f00c
Revises: 21f16d754167
Create Date: 2024-02-22 23:44:02.178091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b3ac788f00c'
down_revision: Union[str, None] = '21f16d754167'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('image_tag_association_comment_id_fkey', 'image_tag_association', type_='foreignkey')
    op.drop_column('image_tag_association', 'comment_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image_tag_association', sa.Column('comment_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('image_tag_association_comment_id_fkey', 'image_tag_association', 'comments', ['comment_id'], ['id'])
    # ### end Alembic commands ###