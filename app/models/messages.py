from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_production

class Message(db.Model):
    __tablename__ = "messages"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    channel_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_production("rooms.id"))
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_production("users.id"))
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )

    room = db.relationship("Room", back_populates="messages")
    user = db.relationship("User")

    def to_dict(self, from_room=False):
        return {
            "id": self.id,
            "content": self.content,
            "room": self.room.name,
            "user": self.user.to_dict(),
            # "created_at": self.created_at.strftime("%a, %b %-d% at %-I:%M %p")
            # if self.created_at.date() != datetime.today().date()
            # else self.created_at.strftime("%-I:%M %p"),
            "created_at": self.created_at
            if from_room
            else self.created_at.strftime("%-I:%M %p"),
            "updated_at": str(self.updated_at),
        }
