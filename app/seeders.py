import os
from datetime import datetime
from random import random
from app.models.messages import Message
from sqlalchemy.sql import text
from flask.cli import AppGroup
from .models import db, User, Room


def random_date_2024():
    start_date = datetime(2024, 1, 1)
    end_date = datetime.now()
    time_elapsed = end_date - start_date
    random_time = time_elapsed * random()
    random_date = start_date + random_time
    return random_date


environment = os.environ.get("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

seed_commands = AppGroup("seed")


def seed_rooms():
    rooms = {
        "serenity": Room(name="Serenity"),
        "miranda": Room(name="Miranda"),
        "persephone": Room(name="Persephone"),
    }
    for room in rooms.values():
        db.session.add(room)
    db.session.commit()

    return rooms


def undo_rooms():
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.rooms RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM rooms;"))
    db.session.commit()


def seed_users():
    users = {
        "mal": User(username="Mal", password="password", theme="#7B6859"),
        "zoe": User(username="Zoe", password="password", theme="#ACACA2"),
        "wash": User(username="Wash", password="password", theme="#C8A680"),
        "inara": User(username="Inara", password="password", theme="#457E89"),
        "jayne": User(username="Jayne", password="password", theme="#E76D2D"),
        "river": User(username="River", password="password", theme="#969249"),
        "kaylee": User(username="Kaylee", password="password", theme="#A7AF9D"),
        "simon": User(username="Simon", password="password", theme="#6A9DA1"),
        "book": User(username="Book", password="password", theme="#7B6859"),
    }

    for user in users.values():
        db.session.add(user)
    db.session.commit()
    return users


def undo_users():
    if environment == "production":
        db.session.execute(
            text(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
        )
    else:
        db.session.execute(text("DELETE FROM users;"))
    db.session.commit()


def seed_messages(users, rooms):
    message_1 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_2 = Message(
        content="We have done the impossible, and that makes us mighty.",
        room=rooms["persephone"],
        user=users["mal"],
    )
    message_3 = Message(
        content="I believe that woman's plannin' to shoot me again.",
        room=rooms["serenity"],
        user=users["mal"],
    )
    message_4 = Message(
        content="I'm very sorry if she tipped off anyone about your cunningly concealed herd of cows.",
        room=rooms["persephone"],
        user=users["simon"],
    )
    message_5 = Message(
        content="This place gives me an uncomfortableness...",
        room=rooms["miranda"],
        user=users["jayne"],
    )
    message_6 = Message(
        content="It's been a big day, what with the abduction and all.",
        room=rooms["serenity"],
        user=users["simon"],
    )
    message_7 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_8 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_9 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_10 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_11 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_12 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_13 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_14 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_15 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_16 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_17 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_18 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_19 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_20 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_21 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_22 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_23 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_24 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_25 = Message(
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )

    messages = [
        message_1,
        message_2,
        message_3,
        message_4,
        message_5,
        message_6,
        message_7,
        message_8,
        message_9,
        message_10,
        message_11,
        message_12,
        message_13,
        message_14,
        message_15,
        message_16,
        message_17,
        message_18,
        message_19,
        message_20,
        message_21,
        message_22,
        message_23,
        message_24,
        message_25,
    ]

    for message in messages:
        random_date = random_date_2024()
        message.created_at = random_date
        message.created_at = random_date


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
    users = seed_users()
    rooms = seed_rooms()
    seed_messages(users, rooms)


@seed_commands.command("undo")
def undo_all():
    undo_rooms()
    undo_users()
    undo_messages()
