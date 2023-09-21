from pprint import pprint
from datetime import datetime
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


suffixes = {
    "11": "th",
    "12": "th",
    "13": "th",
    "1": "st",
    "2": "nd",
    "3": "rd",
    "4": "th",
    "5": "th",
    "6": "th",
    "7": "th",
    "8": "th",
    "9": "th",
    "0": "th",
}

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(31), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "theme": self.theme}


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    channel_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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


class Room(db.Model):
    __tablename__ = "rooms"
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
        pprint(message_dicts)

        return {
            "id": self.id,
            "name": self.name,
            "messages": message_dicts,
        }
