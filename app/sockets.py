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
    latest_message = (
        Message.query.filter(Message.channel_id == room_id)
        .order_by(Message.id.desc())
        .first()
    )
    # code to store chat message in database
    new_message = Message(channel_id=room_id, content=content, user_id=user_id)
    db.session.add(new_message)
    db.session.commit()
    chat_message = new_message.to_dict(from_room=False)
    if (
        latest_message is None
        or latest_message.created_at.date() != new_message.created_at.date()
    ):
        chat_message["new_day"] = "Today"
    # end db code

    # # message formatted to work without database
    # chat_message = {
    #     "content": content,
    #     "user": User.query.get(user_id).to_dict(),
    #     "created_at": datetime.now().strftime("%-I:%M %p"),
    #     "new_day": None
    #     if latest_message.created_at.date() == datetime.now().date()
    #     else "Today",
    # }
    # # end db-less code
    emit("chat", chat_message, broadcast=True, to=room_id)
