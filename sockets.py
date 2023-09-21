import os
from flask_socketio import SocketIO, emit, join_room
from models import db, Message


# origins = os.environ.get("ORIGINS")
origins = "*"


socketio = SocketIO(cors_allowed_origins=origins, logger=True)


@socketio.on("join")
def handle_join(room_id):
    print(f"Joining room {room_id}")
    join_room(room_id)


@socketio.on("connection")
def handle_connection(data):
    print(data)


@socketio.on("chat")
def handle_chat(data):
    room_id = data["room_id"]
    content = data["content"]
    user_id = data["user_id"]
    print(data)
    new_message = Message(channel_id=room_id, content=content, user_id=user_id)
    db.session.add(new_message)
    db.session.commit()
    emit("chat", new_message.to_dict(from_room=False), broadcast=True, to=room_id)
