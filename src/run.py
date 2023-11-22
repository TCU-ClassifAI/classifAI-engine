from flask import Flask, make_response
import os
from dotenv import load_dotenv
from services.transcription.profile import profile
from services.transcription.views import transcription

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


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return make_response("OK", 200)


@app.route("/config", methods=["GET"])
def config():
    return make_response(str(settings.SETTINGS_TYPE), 200)


if __name__ == "__main__":
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True)
