from flask import Blueprint, request, make_response, Flask
from dotenv import load_dotenv
import os
import json
from utils.auth import api_key_required

from config import config as settings

load_dotenv()

server_info = Blueprint("server", __name__)


@server_info.route("/", methods=["GET"])
def index():
    """Gives a brief description of the API, version, config, and healthcheck. Welcome page"""

    description = "ClassifAI Engine"
    version = "2.0.4"
    config = settings.SETTINGS_TYPE
    healthcheck = "OK"
    documentation = "https://tcu-classifai.github.io/classifAI-engine/"

    return "<h1>{}</h1><p>Version: {}</p><p>Config: {}</p><p>Healthcheck: {}</p><a href='{}'>Documentation</a>".format(
        description, version, config, healthcheck, documentation
    )


@server_info.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for API

    Returns: OK
    """
    return make_response("OK", 200)


@server_info.route("/config", methods=["GET"])
def config():
    return make_response(str(settings.SETTINGS_TYPE), 200)


@server_info.route("/auth", methods=["GET"])
@api_key_required
def secure():
    return make_response("OK", 200)
