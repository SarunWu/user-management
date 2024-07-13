"""create models

Revision ID: 10583fb080cb
Revises: 
Create Date: 2024-07-13 05:26:36.308143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10583fb080cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('migrate_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source_file_name', sa.String(), nullable=False),
    sa.Column('target_table', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('tel_no', sa.String(length=10), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('district', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('province', sa.String(length=25), nullable=False),
    sa.Column('zip_code', sa.String(length=5), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('access_group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['access_group_id'], ['user_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###