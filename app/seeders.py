import os
from datetime import datetime, timedelta
from random import random
from sqlalchemy.sql import text
from flask.cli import AppGroup
from .models import db, User, Room, Message


def random_date_2024():
    # start_date = datetime(2024, 1, 1)
    start_date = datetime.now() - timedelta(7)
    end_date = datetime.now()
    time_elapsed = end_date - start_date
    random_time = time_elapsed * random()
    random_date = start_date + random_time
    return random_date



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
    message_1 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_2 = Message( # type: ignore
        content="We have done the impossible, and that makes us mighty.",
        room=rooms["persephone"],
        user=users["mal"],
    )
    message_3 = Message( # type: ignore
        content="I believe that woman's plannin' to shoot me again.",
        room=rooms["serenity"],
        user=users["mal"],
    )
    message_4 = Message( # type: ignore
        content="I'm very sorry if she tipped off anyone about your cunningly concealed herd of cows.",
        room=rooms["persephone"],
        user=users["simon"],
    )
    message_5 = Message( # type: ignore
        content="This place gives me an uncomfortableness...",
        room=rooms["miranda"],
        user=users["jayne"],
    )
    message_6 = Message( # type: ignore
        content="It's been a big day, what with the abduction and all.",
        room=rooms["serenity"],
        user=users["simon"],
    )
    message_7 = Message( # type: ignore
        content="It's good to be home",
        room=rooms["serenity"],
        user=users["book"],
    )
    message_8 = Message( # type: ignore
        content="Someone ever tries to kill you, you try to kill 'em right back!",
        room=rooms["miranda"],
        user=users["mal"],
    )
    message_9 = Message( # type: ignore
        content="Every planet has its own weird customs. About a year before we met, I spent six weeks on a moon where the principal form of recreation was juggling geese. My hand to God. Baby geese. Goslings. They were juggled.",
        room=rooms["persephone"],
        user=users["wash"],
    )
    message_10 = Message( # type: ignore
        content="The hero of Canton, the man they call 'me'.",
        room=rooms["miranda"],
        user=users["jayne"],
    )
    message_11 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["persephone"],
        user=users["kaylee"],
    )
    message_12 = Message( # type: ignore
        content="Sometimes a thing gets broke, can't be fixed.",
        room=rooms["serenity"],
        user=users["kaylee"],
    )
    message_13 = Message( # type: ignore
        content="Two by two, hands of blue... two by two, hands of blue...",
        room=rooms["miranda"],
        user=users["river"],
    )
    message_14 = Message( # type: ignore
        content="They don't like it when you shoot at 'em. I worked that out myself.",
        room=rooms["miranda"],
        user=users["mal"],
    )
    message_15 = Message( # type: ignore
        content="Nothing worse than a monster who thinks he's right with God.",
        room=rooms["miranda"],
        user=users["mal"],
    )
    message_16 = Message( # type: ignore
        content="It's just an object. It doesn't mean what you think.",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_17 = Message( # type: ignore
        content="Something ain't right...",
        room=rooms["serenity"],
        user=users["zoe"],
    )
    message_18 = Message( # type: ignore
        content="Sweetie, we're crooks, if everything was right, we'd be in jail.",
        room=rooms["serenity"],
        user=users["wash"],
    )
    message_19 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_20 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_21 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_22 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_23 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_24 = Message( # type: ignore
        content="No power in the 'verse can stop me!",
        room=rooms["serenity"],
        user=users["river"],
    )
    message_25 = Message( # type: ignore
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

    for idx, message in enumerate(messages):
        random_date = random_date_2024()
        message.created_at = random_date
        message.created_at = random_date
        if idx == 17:
            message.created_at = messages[idx-1].created_at + timedelta(seconds=30)
        db.session.add(message)

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
    users = seed_users()
    rooms = seed_rooms()
    seed_messages(users, rooms)


@seed_commands.command("undo")
def undo_all():
    undo_rooms()
    undo_users()
    undo_messages()
