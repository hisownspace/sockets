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
        "http://websockets-testing.onrender.com",
        "https://websockets-testing.onrender.com",
    ]


socketio = SocketIO(cors_allowed_origins=origins, logger=True)


@socketio.on("join")
def handle_join(room_id):
    """This socket handles emits that are sent out every time a user joins a
    room. Now this user will receive emits from the backend whenever other users
    in that room send a message."""
    print(f"Joining room {room_id}")
    join_room(room_id)


@socketio.on("connection")
def handle_connection(data):
    """This socket is purely for informative purposes. It prints """
    print("PRINTING SOCKET CONNECTION DATA:")
    print(data)


@socketio.on("chat")
def handle_chat(data):
    room_id = data["room_id"]
    content = data["content"]
    user_id = data["user_id"]
    new_message = Message(channel_id=room_id, content=content, user_id=user_id)
    db.session.add(new_message)
    db.session.commit()
    emit("chat", new_message.to_dict(), broadcast=True, to=room_id)
