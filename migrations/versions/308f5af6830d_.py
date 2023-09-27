"""empty message

Revision ID: 308f5af6830d
Revises: faca4510a4d1
Create Date: 2023-09-21 18:03:08.641002

"""
from alembic import op
import sqlalchemy as sa
import os

environment = (
    "production" if os.environ.get("FLASK_DEBUG") == "False" else "environment"
)
SCHEMA = os.environ.get("FLASK_SCHEMA")


# revision identifiers, used by Alembic.
revision = "308f5af6830d"
down_revision = "faca4510a4d1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_conversations")),
    )
    if environment == "production":
        op.execute(f"ALTER TABLE conversations SET SCHEMA {SCHEMA};")
    op.create_table(
        "direct_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=2000), nullable=True),
        sa.Column("conversation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name=op.f("fk_direct_message_conversation_id_conversations"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_direct_message")),
    )
    if environment == "production":
        op.execute(f"ALTER TABLE direct_message SET SCHEMA {SCHEMA};")
    op.create_table(
        "user_conversations",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name=op.f("fk_user_conversations_conversation_id_conversations"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_user_conversations_user_id_users")
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "conversation_id", name=op.f("pk_user_conversations")
        ),
    )
    if environment == "production":
        op.execute(f"ALTER TABLE user_conversations SET SCHEMA {SCHEMA};")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_conversations")
    op.drop_table("direct_message")
    op.drop_table("conversations")
    # ### end Alembic commands ###
