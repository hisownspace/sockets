from .db import db, environment, SCHEMA
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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

