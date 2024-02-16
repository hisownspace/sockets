from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_production

class DirectMessage(db.Model):
    __tablename__ = "direct_messages"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    conversation_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_production("conversations.id"))
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_production("users.id"))
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship("User", back_populates="direct_messages")
    conversation = db.relationship("Conversation", back_populates="direct_messages")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.strftime("%A, %B %-d at %-I:%M %p"),
            "updated_at": str(self.updated_at),
            "user": self.user.to_dict(from_dm=True),
            "conversation_id": self.conversation.id,
            "members": [member.username for member in self.conversation.members],
        }

