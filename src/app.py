from flask import Flask, make_response
import os
from dotenv import load_dotenv
from services.auth import api_key_required
from services.transcribe import transcription

load_dotenv()  # Load environment variables from .env file

# Load settings based on environment
if os.environ.get("ENV") == "production":
    from config import production as settings
else:
    from config import development as settings

# Initialize Flask app
app = Flask(__name__)
# app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(transcription, url_prefix="/transcription")


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


@app.route("/auth", methods=["GET"])
@api_key_required
def secure():
    return make_response("OK", 200)


def create_app():
    return app


if __name__ == "__main__":
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True, host="0.0.0.0")
