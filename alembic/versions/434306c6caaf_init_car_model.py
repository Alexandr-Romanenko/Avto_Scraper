"""init Car model

Revision ID: 434306c6caaf
Revises: 
Create Date: 2025-12-16 14:16:11.946453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '434306c6caaf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import TIMESTAMP

def upgrade() -> None:
    """Upgrade schema: create car table with proper unique indexes."""
    op.create_table(
        'car',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('url', sa.String, nullable=False, unique=True),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('price_usd', sa.Float, nullable=True),
        sa.Column('odometer', sa.Integer, nullable=True),
        sa.Column('username', sa.String, nullable=True),
        sa.Column('phone_number', sa.String, nullable=True),
        sa.Column('image_url', sa.String, nullable=True),
        sa.Column('images_count', sa.Integer, nullable=True),
        sa.Column('car_number', sa.String, nullable=True),
        sa.Column('car_vin', sa.String, nullable=True),
        sa.Column('datetime_found', TIMESTAMP(timezone=True), nullable=False)
    )

    op.create_index(
        'uq_car_vin_number',
        'car',
        ['car_vin', 'car_number'],
        unique=True
    )


def downgrade() -> None:
    """Drop car table and indexes."""
    op.drop_index('uq_car_vin_number', table_name='car')
    op.drop_table('car')