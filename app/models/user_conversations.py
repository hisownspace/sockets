from .db import db, SCHEMA, environment, add_prefix_for_production


user_conversations = db.Table(
    "user_conversations",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_production("users.id")),
        primary_key=True,
    ),
    db.Column(
        "conversation_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_production("conversations.id")),
        primary_key=True,
    ),
)

if environment == "production":
    user_conversations.schema = SCHEMA
