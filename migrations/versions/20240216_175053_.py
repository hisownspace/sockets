"""empty message

Revision ID: ced8cb83fde4
Revises: 
Create Date: 2024-02-16 17:50:53.448460

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = 'ced8cb83fde4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_conversations'))
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rooms'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('theme', sa.String(length=31), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_table('direct_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=True),
    sa.Column('conversation_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name=op.f('fk_direct_messages_conversation_id_conversations')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_direct_messages_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_direct_messages'))
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['rooms.id'], name=op.f('fk_messages_channel_id_rooms')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_messages_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    op.create_table('user_conversations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name=op.f('fk_user_conversations_conversation_id_conversations')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_conversations_user_id_users')),
    sa.PrimaryKeyConstraint('user_id', 'conversation_id', name=op.f('pk_user_conversations'))
    )
    if environment == "production":
        op.execute(f"ALTER TABLE users SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE direct_messages SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE messages SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE user_conversations SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE rooms SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE conversations SET SCHEMA {SCHEMA};")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_conversations')
    op.drop_table('messages')
    op.drop_table('direct_messages')
    op.drop_table('users')
    op.drop_table('rooms')
    op.drop_table('conversations')
    # ### end Alembic commands ###
