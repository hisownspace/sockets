"""empty message

Revision ID: 03be6f71bdd7
Revises: 308f5af6830d
Create Date: 2023-09-21 18:03:39.963823

"""
from alembic import op
import sqlalchemy as sa
import os

environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("FLASK_SCHEMA")


# revision identifiers, used by Alembic.
revision = "03be6f71bdd7"
down_revision = "308f5af6830d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "direct_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=2000), nullable=True),
        sa.Column("conversation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name=op.f("fk_direct_messages_conversation_id_conversations"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_direct_messages")),
    )
    if environment == "production":
        op.execute(f"ALTER TABLE direct_messages SET SCHEMA {SCHEMA};")
    op.drop_table("direct_message")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "direct_message",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("content", sa.VARCHAR(length=2000), nullable=True),
        sa.Column("conversation_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name="fk_direct_message_conversation_id_conversations",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_direct_message"),
    )
    op.drop_table("direct_messages")
    # ### end Alembic commands ###
