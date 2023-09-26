"""empty message

Revision ID: c764d2db8e91
Revises: 20cf6aaa39d4
Create Date: 2023-09-19 08:02:18.476000

"""
from alembic import op
import sqlalchemy as sa
import os

environment = (
    "production" if os.environ.get("FLASK_DEBUG") == "False" else "environment"
)
SCHEMA = os.environ.get("FLASK_SCHEMA")

# revision identifiers, used by Alembic.
revision = "c764d2db8e91"
down_revision = "20cf6aaa39d4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rooms")),
    )
    if environment == "production":
        op.execute(f"ALTER TABLE rooms SET SCHEMA {SCHEMA};")

    with op.batch_alter_table(
        "messages", schema=SCHEMA if environment == "production" else None
    ) as batch_op:
        batch_op.add_column(sa.Column("channel_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_messages_channel_id_rooms"), "rooms", ["channel_id"], ["id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "messages", schema=SCHEMA if environment == "production" else None
    ) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_messages_channel_id_rooms"), type_="foreignkey"
        )
        batch_op.drop_column("channel_id")

    op.drop_table("rooms")
    # ### end Alembic commands ###
