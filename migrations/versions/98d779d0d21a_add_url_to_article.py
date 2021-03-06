"""add url to Article

Revision ID: 98d779d0d21a
Revises: 99d45ddd138c
Create Date: 2017-09-07 21:25:57.431704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98d779d0d21a'
down_revision = '99d45ddd138c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('url', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_article_url'), 'article', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_article_url'), table_name='article')
    op.drop_column('article', 'url')
    # ### end Alembic commands ###
