from .db import db, environment, SCHEMA

class Conversation(db.Model):
    __tablename__ = "conversations"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)

    members = db.relationship(
        "User", secondary="user_conversations", back_populates="conversations"
    )
    direct_messages = db.relationship("DirectMessage", back_populates="conversation")

    def to_dict(self):
        return {
            "id": self.id,
            "members": [member.username for member in self.members],
            "messages": [message.to_dict() for message in self.direct_messages],
        }

