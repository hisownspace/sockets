from datetime import datetime
from .db import db, SCHEMA, environment


class Room(db.Model):
    __tablename__ = "rooms"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    messages = db.relationship("Message", back_populates="room")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "messages": [message.to_dict() for message in self.messages],
        }
