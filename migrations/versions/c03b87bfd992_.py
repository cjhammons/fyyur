"""empty message

Revision ID: c03b87bfd992
Revises: b428e2efa493
Create Date: 2020-06-10 16:01:18.313030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c03b87bfd992'
down_revision = 'b428e2efa493'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'past_shows_count',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('artists', 'upcoming_shows_count',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('venues', 'past_shows_count',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('venues', 'upcoming_shows_count',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'upcoming_shows_count',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('venues', 'past_shows_count',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('artists', 'upcoming_shows_count',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('artists', 'past_shows_count',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
