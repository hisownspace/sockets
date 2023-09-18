from sqlalchemy.sql import text
from flask.cli import AppGroup
from models import db, User

seed_commands = AppGroup("seed")


def seed_users():
    user_1 = User(username="demo_1", password="password")
    user_2 = User(username="demo_2", password="password")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()


def undo_users():
    db.session.execute(text("DELETE FROM users;"))
    db.session.commit()


@seed_commands.command("all")
def seed_all():
    seed_users()


@seed_commands.command("undo")
def undo_all():
    undo_users()
