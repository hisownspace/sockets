from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from models import User


class LoginForm(FlaskForm):
    username = StringField("Username: ", [InputRequired()])
    password = PasswordField("Password: ", [InputRequired(), Length(min=8)])

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError("User does not exist")

    def validate_password(form, field):
        user = User.query.filter_by(username=form.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("Invalid username/password combo")


class DirectMessageForm(FlaskForm):
    content = StringField(
        "Content",
        [InputRequired(message="Cannot send an empty message"), Length(max=2000)],
    )
