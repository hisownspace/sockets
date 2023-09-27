import os
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

environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

db = SQLAlchemy(metadata=metadata)


def add_prefix_for_production(attr):
    if environment == "production":
        return f"{SCHEMA}.{attr}"
    else:
        return attr


class User(db.Model, UserMixin):
    __tablename__ = "users"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(31), nullable=False)

    direct_messages = db.relationship("DirectMessage", back_populates="user")
    conversations = db.relationship(
        "Conversation", secondary="user_conversations", back_populates="members"
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, from_dm=False):
        return {
            "id": self.id,
            "username": self.username,
            "theme": self.theme,
            "conversations": [
                conversation.id if from_dm else conversation.to_dict()
                for conversation in self.conversations
            ],
        }


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


class DirectMessage(db.Model):
    __tablename__ = "direct_messages"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    conversation_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("conversations.id"))
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
