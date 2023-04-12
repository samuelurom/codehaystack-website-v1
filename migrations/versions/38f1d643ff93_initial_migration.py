"""Initial migration

Revision ID: 38f1d643ff93
Revises: 
Create Date: 2023-04-12 19:26:16.224888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38f1d643ff93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('title', sa.VARCHAR(length=250), nullable=False),
                    sa.Column('url', sa.VARCHAR(length=120), nullable=False),
                    sa.Column('description', sa.TEXT(), nullable=False),
                    sa.Column('content', sa.TEXT(), nullable=True),
                    sa.Column('featured_image_path', sa.VARCHAR(
                        length=250), nullable=True),
                    sa.Column('status', sa.VARCHAR(length=20), nullable=False),
                    sa.Column('comment_status', sa.VARCHAR(
                        length=20), nullable=False),
                    sa.Column('published', sa.DATETIME(), nullable=False),
                    sa.Column('modifiled', sa.DATETIME(), nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('url')
                    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index('ix_post_title', ['title'], unique=False)
        batch_op.create_index('ix_post_status', ['status'], unique=False)
        batch_op.create_index('ix_post_published', ['published'], unique=False)
        batch_op.create_index('ix_post_modifiled', ['modifiled'], unique=False)
        batch_op.create_index('ix_post_description', [
                              'description'], unique=False)
        batch_op.create_index('ix_post_content', ['content'], unique=False)

    op.create_table('user',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('username', sa.VARCHAR(
                        length=50), nullable=False),
                    sa.Column('full_name', sa.VARCHAR(
                        length=80), nullable=True),
                    sa.Column('email', sa.VARCHAR(length=250), nullable=False),
                    sa.Column('bio', sa.TEXT(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('ix_user_username', ['username'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_username')

    op.drop_table('user')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index('ix_post_content')
        batch_op.drop_index('ix_post_description')
        batch_op.drop_index('ix_post_modifiled')
        batch_op.drop_index('ix_post_published')
        batch_op.drop_index('ix_post_status')
        batch_op.drop_index('ix_post_title')

    op.drop_table('post')
    # ### end Alembic commands ###
