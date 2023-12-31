import os
from sqlalchemy.sql import text
from flask.cli import AppGroup
from models import db, User, Room

environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

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
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.rooms RESTART IDENTITY CASCADE;")
        )
    else:
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
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM users;"))
    db.session.commit()


def undo_messages():
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.messages RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM messages;"))
    db.session.commit()


def undo_conversations():
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.conversations RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM conversations;"))
    db.session.commit()


def undo_user_conversations():
    if environment == "production":
        db.session.execute(
            text(
                f"TRUNCATE table {SCHEMA}.user_conversations RESTART IDENTITY CASCADE;"
            )
        )
    else:
        db.session.execute(text("DELETE FROM user_conversations;"))
    db.session.commit()


def undo_direct_messages():
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.direct_messages RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM direct_messages;"))
    db.session.commit()


@seed_commands.command("all")
def seed_all():
    if environment == "production":
        undo_direct_messages()
        undo_user_conversations()
        undo_conversations()
        undo_rooms()
        undo_users()
        undo_messages()
    seed_users()
    seed_rooms()


@seed_commands.command("undo")
def undo_all():
    undo_rooms()
    undo_users()
    undo_messages()
