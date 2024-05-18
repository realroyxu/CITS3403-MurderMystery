"""Initial migration

Revision ID: 692e45dc95ec
Revises: None
Create Date: 2024-05-18 12:44:06.645793

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '692e45dc95ec'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create initial tables, no need to add `characters` or `generated_story` columns here.
    op.create_table('post',
        sa.Column('postid', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('userid', sa.Integer, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('posttime', sa.String, nullable=False),
        sa.Column('posttype', sa.String, nullable=False),
        sa.Column('puzzleid', sa.Integer, nullable=True),
        sa.ForeignKeyConstraint(['userid'], ['user.userid'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['puzzleid'], ['puzzle.puzzleid'], ondelete='CASCADE')
    )

def downgrade():
    # Drop the `post` table if you need to revert the migration
    op.drop_table('post')
