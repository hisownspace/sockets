from flask import Blueprint, request
from flask_login import current_user, login_user, logout_user
from ..forms import LoginForm
from ..models import User

auth_routes = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_routes.route("")
def authenticate():
    if current_user.is_authenticated:  # type: ignore
        return current_user.to_dict(), 200  # type: ignore
    return {"errors": ["Unauthorized"]}, 401


@auth_routes.route("/unauthorized")
def unauthorized():
    return {"errors": ["Unauthorized!"]}


@auth_routes.route("/login", methods=["POST"])  # type: ignore
def login():
    form = LoginForm()
    print(form.data)
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        username = form.data["username"]
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return user.to_dict()
    return form.errors, 401


@auth_routes.route("/logout")
def logout():
    logout_user()
    return {"message": "Logout Successful!"}
