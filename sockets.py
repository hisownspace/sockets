import os
from flask_socketio import SocketIO, emit


# origins = os.environ.get("ORIGINS")
origins = "*"


socketio = SocketIO(cors_allowed_origins=origins, logger=True)


@socketio.on("connection")
def handle_connection(data):
    print(data)


@socketio.on("chat")
def handle_chat(data):
    print("in socket")
    emit("chat", data, broadcast=True)
