from flask import Blueprint
from ..models import Room

room_routes = Blueprint("rooms", __name__, url_prefix="/api/rooms")

@room_routes.route("")
def get_all_rooms():
    all_rooms = Room.query.all()
    return [room.to_dict() for room in all_rooms], 200


@room_routes.route("/<int:room_id>")
def get_single_room(room_id):
    room = Room.query.get(room_id)
    return room.to_dict(), 200

