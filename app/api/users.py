from flask import Blueprint, request
from ..models import User


user_routes = Blueprint("users", __name__, url_prefix="/api/users")


@user_routes.route("/search")
def search_for_user():
    search_query = request.args["user"]
    users = User.query.filter(User.username.ilike(f"%{search_query}%")).all()
    return [user.to_dict() for user in users]


@user_routes.route("")
def get_all_users():
    all_users = User.query.all()
    return [user.to_dict() for user in all_users], 200

