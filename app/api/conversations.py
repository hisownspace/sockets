from flask import Blueprint, request
from flask_login import current_user
from ..sockets import socketio
from ..models import db, User, Conversation, DirectMessage
from ..forms import DirectMessageForm

conversation_routes = Blueprint("conversations", __name__, url_prefix="/api/conversations")

@conversation_routes.route("")
def get_all_conversations():
    """Returns a response object with all of the DM conversations that the
    current user is a part of."""
    if current_user.is_authenticated: # type: ignore
        my_conversations = current_user.conversations # type: ignore
        return [conversation.to_dict() for conversation in my_conversations], 200
    else:
        return { "errors": ["Unauthorized!"] }


@conversation_routes.route("", methods=["POST"])
def create_conversation():
    """Handles a request for the creation of a conversation. It is not connected
    to a socket, so the other users in the conversation are only informed of the
    new conversation when a message is created in the conversation."""
    users = request.get_json()["users"]
    user_objs = []
    for user in users:
        user_obj = User.query.get(user["id"])
        user_objs.append(user_obj)
    all_conversations = Conversation.query.all()
    new_conversation = Conversation()
    new_conversation.members = user_objs

    def check_conversation_exists(new_conversation, all_conversations):
        new_conversation_members = set(new_conversation.members)
        for conversation in all_conversations:
            conversation_members = set(conversation.members)
            if conversation_members == new_conversation_members:
                return conversation
        return False

    conversation_exists = check_conversation_exists(new_conversation, all_conversations)

    if conversation_exists:
        return conversation_exists.to_dict()
    else:
        db.session.add(new_conversation)
        db.session.commit()
        return new_conversation.to_dict(), 201


@conversation_routes.route("/<int:conversation_id>/messages", methods=["POST"])
def send_dm(conversation_id):
    """This route handles a request from a user and returns an http response.
    It also emits to the dm listener, so other users in the conversation
    immediately receive the message. One benefit of structuring your data flow
    this way is that it allows access to wtforms validators."""
    form = DirectMessageForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        content = form.data["content"]
        user = current_user
        new_dm = DirectMessage(  # type: ignore[call-arg]
            content=content, user=user, conversation_id=conversation_id
        )
        db.session.add(new_dm)
        db.session.commit()
        print(new_dm.to_dict())
        socketio.emit(
            "dm", new_dm.to_dict(), namespace="/"
        )
        return new_dm.to_dict(), 201
    errors = {**form.errors}
    if "content" in form.errors and "csrf_token" in form.errors.keys():
        print("deleting...")
        del errors["csrf_token"]
        return errors, 400
    print(errors)
    return errors, 403

