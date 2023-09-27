import os
from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_wtf.csrf import generate_csrf
from config import Config
from models import db, User, Message, Room, Conversation, DirectMessage
from forms import LoginForm, DirectMessageForm
from flask_socketio import emit
from sockets import socketio
from seeders import seed_commands

app = Flask(__name__, static_folder="../react-app/dist", static_url_path="/")
app.config.from_object(Config)
db.init_app(app)
Migrate(app, db)
socketio.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

app.cli.add_command(seed_commands)

CORS(app, expose_headers=["Access-Control-Allow-Origin", "content-length"])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/api/auth")
def authenticate():
    if current_user.is_authenticated:
        return current_user.to_dict(), 200
    return {"errors": "Unauthorized"}, 401


@app.route("/api/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        username = form.data["username"]
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return user.to_dict()
    return form.errors, 401


@app.route("/api/logout")
def logout():
    logout_user()
    return {"Message": "Logout Successful!"}


@app.route("/api/users")
def get_all_users():
    all_users = User.query.all()
    return [user.to_dict() for user in all_users], 200


@app.route("/api/rooms")
def get_all_rooms():
    all_rooms = Room.query.all()
    return [room.to_dict() for room in all_rooms], 200


@app.route("/api/rooms/<int:roomId>")
def get_single_room(roomId):
    room = Room.query.get(roomId)
    return room.to_dict(), 200


@app.route("/api/conversations")
def get_all_conversations():
    my_conversations = current_user.conversations
    print(current_user)
    return [conversation.to_dict() for conversation in my_conversations], 200


@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    users = request.get_json()["users"]
    user_objs = []
    for user in users:
        user_obj = User.query.get(user["id"])
        user_objs.append(user_obj)
    all_conversations = Conversation.query.all()
    new_conversation = Conversation()
    new_conversation.members = user_objs

    # def check_conversation_exists(new_conversation, all_conversations):
    #     same_conversations = []
    #     for conversation in all_conversations:
    #         did_break = False
    #         # print(conversation.members)
    #         for member in conversation.members:
    #             if member not in new_conversation.members:
    #                 same_conversations.append(True)
    #                 did_break = True
    #                 break
    #         if did_break:
    #             continue
    #         for member in new_conversation.members:
    #             if member not in conversation.members:
    #                 same_conversations.append(True)
    #                 did_break = True
    #                 break
    #         if did_break:
    #             continue
    #         same_conversations.append(False)
    #     return (
    #         all_conversations[same_conversations.index(False)]
    #         if not all(same_conversations)
    #         else False
    #     )

    def check_conversation_exists(new_conversation, all_conversations):
        new_conversation_members = set(new_conversation.members)
        for conversation in all_conversations:
            conversation_members = set(conversation.members)
            if conversation_members == new_conversation_members:
                return conversation
        return False

    conversation_exists = check_conversation_exists(new_conversation, all_conversations)

    if conversation_exists:
        return conversation_exists.to_dict()
    else:
        db.session.add(new_conversation)
        db.session.commit()
        return new_conversation.to_dict(), 201


@app.route("/api/conversations/<int:conversation_id>/messages", methods=["POST"])
def send_dm(conversation_id):
    form = DirectMessageForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        content = form.data["content"]
        user = current_user
        new_dm = DirectMessage(
            content=content, user=user, conversation_id=conversation_id
        )
        db.session.add(new_dm)
        db.session.commit()
        print(new_dm.to_dict())
        socketio.emit(
            "dm", new_dm.to_dict(), namespace="/", to=f"conversation/{conversation_id}"
        )
        return new_dm.to_dict(), 201
    print(form.errors)
    return {"errors": form.errors}, 500


@app.route("/api/users/search")
def search_for_user():
    search_query = request.args["user"]
    users = User.query.filter(User.username.ilike(f"%{search_query}%")).all()
    return [user.to_dict() for user in users]


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


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == "favicon.ico":
        return app.send_from_directory("public", "favicon.ico")
    return app.send_static_file("index.html")


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")


if __name__ == "__main__":
    socketio.run(app)
