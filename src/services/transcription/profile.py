from flask import Blueprint, make_response

profile = Blueprint("profile", __name__)


@profile.route("/<username>")
def get_profile(username):
    return make_response(f"Hello {username}", 200)
