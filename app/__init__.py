from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf
from .config import Config
from .models import db, User
from .sockets import socketio
from .seeders import seed_commands
from .api import auth_routes, user_routes, room_routes, conversation_routes

app = Flask(__name__, static_folder="../react-app/dist", static_url_path="/")
app.config.from_object(Config)
db.init_app(app)
Migrate(app, db)
socketio.init_app(app)

app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(room_routes, url_prefix="/api/rooms")
app.register_blueprint(conversation_routes, url_prefix="/api/conversations")



login_manager = LoginManager()

login_manager.init_app(app)

app.cli.add_command(seed_commands)

CORS(app, expose_headers=["Access-Control-Allow-Origin", "content-length"])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



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
