from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from dataclasses import dataclass
import uuid


auth = Blueprint("auth", __name__)


@dataclass
class User(object):
    username: str
    password: str
    id: str = str(uuid.uuid4())


# Use a dictionary with usernames as keys in userid_table
userid_table = {
    "admin": User(username="admin", password="admin")
}  # Replace with a database


def authenticate(username, password):
    user = userid_table.get(username, None)
    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)


@auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = authenticate(username, password)

    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    print(username)
    print(password)
    return jsonify({"msg": "Bad username or password"}), 401


@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"msg": "Success!"}), 200
