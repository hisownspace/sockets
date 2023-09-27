import os
from sqlalchemy.sql import text
from flask.cli import AppGroup
from models import db, User, Room

environment = "development" if int(os.environ.get("FLASK_DEBUG")) else "production"

seed_commands = AppGroup("seed")


def seed_rooms():
    room_1 = Room(name="Serenity")
    room_2 = Room(name="Miranda")
    room_3 = Room(name="Persephone")
    db.session.add(room_1)
    db.session.add(room_2)
    db.session.add(room_3)
    db.session.commit()


def undo_rooms():
    db.session.execute(text("DELETE FROM rooms;"))
    db.session.commit()


def seed_users():
    user_1 = User(username="Mal", password="password", theme="#7B6859")
    user_2 = User(username="Zoe", password="password", theme="#ACACA2")
    user_3 = User(username="Wash", password="password", theme="#C8A680")
    user_4 = User(username="Inara", password="password", theme="#457E89")
    user_5 = User(username="Jayne", password="password", theme="#E76D2D")
    user_6 = User(username="River", password="password", theme="#969249")
    user_7 = User(username="Kaylee", password="password", theme="#A7AF9D")
    user_8 = User(username="Simon", password="password", theme="#6A9DA1")
    user_9 = User(username="Book", password="password", theme="#7B6859")

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)
    db.session.add(user_5)
    db.session.add(user_6)
    db.session.add(user_7)
    db.session.add(user_8)
    db.session.add(user_9)
    db.session.commit()


def undo_users():
    db.session.execute(text("DELETE FROM users;"))
    db.session.commit()


def undo_messages():
    db.session.execute(text("DELETE FROM messages;"))
    db.session.commit()


def undo_conversations():
    db.session.execute(text("DELETE FROM conversations;"))


def undo_user_conversations():
    db.session.execute(text("DELETE FROM user_conversations;"))


def undo_direct_messages():
    db.session.execute(text("DELETE FROM direct_messages;"))


@seed_commands.command("all")
def seed_all():
    if environment == "production":
        undo_rooms()
        undo_users()
        undo_messages()
        undo_direct_messages()
        undo_user_conversations()
        undo_conversations()
    seed_users()
    seed_rooms()


@seed_commands.command("undo")
def undo_all():
    undo_rooms()
    undo_users()
    undo_messages()
