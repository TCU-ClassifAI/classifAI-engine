from flask import Blueprint, request, make_response, Flask, jsonify
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
    version = settings.VERSION
    env_type = settings.ENV_TYPE
    healthcheck = "OK"
    documentation = "https://tcu-classifai.github.io/classifAI-engine/"

    return "<h1>{}</h1><p>Version: {}</p><p>Environment: {}</p><p>Healthcheck: {}</p><a href='{}'>Documentation</a>".format(
        description, version, env_type, healthcheck, documentation
    )


@server_info.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for API

    Returns: OK
    """
    return make_response("OK", 200)


@server_info.route("/config", methods=["GET"])
def config():
    """Get the configuration settings for the API

    Returns: JSON object with the configuration settings
    """
    config_settings = {}
    for key in dir(settings):
        # Skip over built-in attributes and private attributes (start with '_')
        if key.isupper():
            value = getattr(settings, key)
            config_settings[key] = value
    
    # Return the settings as a JSON response
    return make_response(jsonify(config_settings), 200)


@server_info.route("/auth", methods=["GET"])
@api_key_required
def secure():
    return make_response("OK", 200)
