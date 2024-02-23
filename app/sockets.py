import os
from datetime import datetime
from flask_socketio import SocketIO, emit, join_room
from flask_login import current_user
from .models import db, Message, Room, User


environment = os.environ.get("FLASK_ENV")
if environment == "development":
    origins = "*"
else:
    origins = [
        "http://serenity-chat.onrender.com",
        "https://serenity-chat.onrender.com",
    ]


socketio = SocketIO(cors_allowed_origins=origins, logger=True)


@socketio.on("join")
def handle_join(room_id):
    """This socket handles emits that are sent out every time a user joins a
    room. Now this user will receive emits from the backend whenever other users
    in that room send a message"""
    print(f"Joining room {room_id}")
    join_room(room_id)

@socketio.on("chat")
def handle_chat(data):
    """This socket handles emits for user submitted messages. There is basic
    error handling for length. If the message is within the required length
    requirements, the message is broadcasted to all users currently in
    the room from which the message was sent"""
    room_id = data["room_id"]
    content = data["content"]
    user_id = data["user_id"]
    if not content:
        print("in error block")
        emit("chat", { "errors": "Cannot send an empty message" }, broadcast=False, to=room_id)
    elif len(content) > 2000:
        emit("chat", { "errors": "Messages must be less than 2000 characters." }, broadcast=False, to=room_id)
    else:
        new_message = Message(channel_id=room_id, content=content, user_id=user_id)
        db.session.add(new_message)
        db.session.commit()
        emit("chat", new_message.to_dict(), broadcast=True, to=room_id)
