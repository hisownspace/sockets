from flask import Flask
from flask_login import login_user

app = Flask(__name__)


@app.route("/")
def test():
    return "App Deployed"


@app.route("/api/login", methods=["GET", "POST"])
def login():
    print("Hitting route!")
    return "hello"


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
