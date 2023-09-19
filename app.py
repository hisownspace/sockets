from flask import Flask, request
from flask_migrate import Migrate
from flask_login import LoginManager, login_user
from flask_wtf.csrf import generate_csrf
from config import Config
from models import db, User, Message, Room
from forms import LoginForm
from seeders import seed_commands

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)

app.cli.add_command(seed_commands)


@app.route("/")
def test():
    return "App Deployed"


@app.route("/api/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    print(form.data)
    if form.validate_on_submit():
        username = form.data["username"]
        print(username)
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return {"user": user.to_dict()}
    return form.errors, 401


@app.route("/api/users")
def get_all_users():
    all_users = User.query.all()
    print(all_users)
    return [user.to_dict() for user in all_users], 200


@app.route("/api/rooms")
def get_all_rooms():
    all_rooms = Room.query.all()
    return [room.to_dict() for room in all_rooms], 200


@app.route("/api/rooms/<int:roomId>")
def get_single_room(roomId):
    room = Room.query.get(roomId)
    return room.to_dict(), 200


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        "csrf_token",
        generate_csrf(),
        secure=False,
        samesite=None,
        httponly=True,
    )
    return response


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
