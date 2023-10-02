"""empty message

Revision ID: 87330e1cefd9
Revises: 
Create Date: 2023-10-01 21:33:37.236882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87330e1cefd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('introduction', sa.String(length=500), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('exp', sa.Integer(), nullable=False),
    sa.Column('image_filename', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('tag', sa.Text(), nullable=False),
    sa.Column('create_Time', sa.DateTime(), nullable=True),
    sa.Column('NumOfLikes', sa.Integer(), nullable=False),
    sa.Column('NumOfView', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('image_filename', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_Time', sa.DateTime(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('answer_to_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('reply_info', sa.String(length=200), nullable=True),
    sa.Column('last_to_user', sa.String(length=100), nullable=True),
    sa.Column('NumOfLikes', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_question_history',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'question_id')
    )
    op.create_table('user_question_save',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'question_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_question_save')
    op.drop_table('user_question_history')
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('user')
    # ### end Alembic commands ###