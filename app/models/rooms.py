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
        messages = [message for message in self.messages]
        message_dicts = [{"new_day": None} for _ in messages]
        for idx in range(len(messages)):
            this_message = messages[idx].to_dict(from_room=True)
            if idx == 0:
                message_dicts[idx] = this_message
                if messages[idx].created_at.date() == datetime.today().date():
                    message_dicts[idx]["new_day"] = "Today"
                else:
                    message_dicts[idx]["new_day"] = this_message["created_at"].strftime(
                        "%A, %B %-d"
                    )
            if (
                idx + 1 < len(messages)
                and messages[idx].to_dict(from_room=True)["created_at"].date()
                != messages[idx + 1].to_dict(from_room=True)["created_at"].date()
            ):
                next_message = messages[idx + 1].to_dict(from_room=True)
                message_dicts[idx + 1] = next_message
                if next_message["created_at"].date() == datetime.today().date():
                    message_dicts[idx + 1]["new_day"] = "Today"
                else:
                    message_dicts[idx + 1]["new_day"] = next_message[
                        "created_at"
                    ].strftime("%A, %B %-d")
            elif idx + 1 < len(messages):
                message_dicts[idx + 1] = messages[idx + 1].to_dict(from_room=True)
            message_dicts[idx]["created_at"] = message_dicts[idx][
                "created_at"
            ].strftime("%-I:%M %p")

        return {
            "id": self.id,
            "name": self.name,
            "messages": message_dicts,
        }

