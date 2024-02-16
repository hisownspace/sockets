from wtforms import StringField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm



class DirectMessageForm(FlaskForm):
    content = StringField(
        "Content",
        [InputRequired(message="Cannot send an empty message"), Length(max=2000)],
    )
