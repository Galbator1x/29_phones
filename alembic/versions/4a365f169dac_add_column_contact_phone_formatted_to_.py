"""Add column contact_phone_formatted to orders

Revision ID: 4a365f169dac
Revises:
Create Date: 2017-03-01 10:31:05.149882

"""
from alembic import op
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = '4a365f169dac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders',
                  Column('contact_phone_formatted', String(100)))


def downgrade():
    pass
