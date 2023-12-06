from flask import Flask, make_response, redirect
import os
from dotenv import load_dotenv
from services.transcription.profile import profile
from services.transcription.views import transcription
from services.auth import api_key_required, validate_api_key
# from flask_api_key import APIKeyManager
import secrets

load_dotenv()  # Load environment variables from .env file

# Load settings based on environment
if os.environ.get("ENV") == "production":
    from config import production as settings
else:
    from config import development as settings

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(transcription, url_prefix="/transcription")
# app.register_blueprint(auth, url_prefix="/auth")

# # Initialize JWT Manager
# app.config["JWT_SECRET_KEY"] = secrets.token_urlsafe(
#     32
# )  # This dynamically generates a secure key at runtime
# jwt = JWTManager(app)

# key_manager = APIKeyManager(app)




@app.route("/help", methods=["GET"])
def help():
    """Forwards to the documentation page (https://tcu-classifai.github.io/classifAI-engine/)"""
    return redirect("https://tcu-classifai.github.io/classifAI-engine/", code=302)


@app.route("/", methods=["GET"])
def index():
    """Gives a brief description of the API, version, config, and healthcheck. Welcome page"""

    description = "ClassifAI Engine"
    version = "1.0.0"
    config = settings.SETTINGS_TYPE
    healthcheck = "OK"
    documentation = "https://tcu-classifai.github.io/classifAI-engine/"

    return "<h1>{}</h1><p>Version: {}</p><p>Config: {}</p><p>Healthcheck: {}</p><a href='{}'>Documentation</a>".format(
        description, version, config, healthcheck, documentation
    )


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for API

    Returns: OK
    """
    return make_response("OK", 200)


@app.route("/config", methods=["GET"])
def config():
    return make_response(str(settings.SETTINGS_TYPE), 200)


@app.route("/secure", methods=["GET"])
@api_key_required
def secure():
    return make_response("OK", 200)


def create_app():
    return app

# @app.route("/create_key", methods=["GET"])
# def create_key():
#     key = key_manager.create("HelloWorld")
#     return print(key.secret)

if __name__ == "__main__":
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True)
    # my_key = key_manager.create("HellowWorld")

    # print(my_key)
