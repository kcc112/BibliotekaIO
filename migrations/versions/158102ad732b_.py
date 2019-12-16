"""empty message

Revision ID: 158102ad732b
Revises: 540738ce30a2
Create Date: 2019-12-16 19:24:23.399101

"""

# revision identifiers, used by Alembic.
revision = '158102ad732b'
down_revision = '540738ce30a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nazwa', sa.String(length=64), nullable=False),
    sa.Column('opis', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=True)
    op.create_index(op.f('ix_books_name'), 'books', ['name'], unique=True)
    op.create_index(op.f('ix_books_quantity'), 'books', ['quantity'], unique=True)
    op.create_index(op.f('ix_books_year'), 'books', ['year'], unique=True)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nazwa', sa.String(length=64), nullable=False),
    sa.Column('data', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('borrows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrows')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('events')
    op.drop_index(op.f('ix_books_year'), table_name='books')
    op.drop_index(op.f('ix_books_quantity'), table_name='books')
    op.drop_index(op.f('ix_books_name'), table_name='books')
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_table('books')
    op.drop_table('announcements')
    # ### end Alembic commands ###