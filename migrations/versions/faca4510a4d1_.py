"""empty message

Revision ID: faca4510a4d1
Revises: 4471194c0873
Create Date: 2023-09-19 22:21:56.557015

"""
from alembic import op
import sqlalchemy as sa
import os

environment = (
    "production" if os.environ.get("FLASK_DEBUG") == "False" else "environment"
)
SCHEMA = os.environ.get("FLASK_SCHEMA")


# revision identifiers, used by Alembic.
revision = "faca4510a4d1"
down_revision = "4471194c0873"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "users", schema=SCHEMA if environment == "production" else None
    ) as batch_op:
        batch_op.add_column(sa.Column("theme", sa.String(length=31), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "users", schema=SCHEMA if environment == "production" else None
    ) as batch_op:
        batch_op.drop_column("theme")

    # ### end Alembic commands ###
