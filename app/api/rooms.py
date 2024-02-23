from flask import Blueprint
from ..models import Room

room_routes = Blueprint("rooms", __name__, url_prefix="/api/rooms")

@room_routes.route("")
def get_all_rooms():
    """Returns a list of all the chat rooms. Right now, since create is
    not implemented for this application, it willl always return the same
    three rooms (as defined in the seeder file)"""
    all_rooms = Room.query.all()
    return [room.to_dict() for room in all_rooms], 200


@room_routes.route("/<int:room_id>")
def get_single_room(room_id):
    """Returns information about a specific room."""
    room = Room.query.get(room_id)
    return room.to_dict(), 200

