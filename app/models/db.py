import os
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

db = SQLAlchemy(metadata=metadata)


def add_prefix_for_production(attr):
    if environment == "production":
        return f"{SCHEMA}.{attr}"
    else:
        return attr
