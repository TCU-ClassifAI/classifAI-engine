from flask import Flask, make_response
import os

from services.transcription.profile import profile
from services.transcription.views import transcription


if os.environ.get("ENV") == "production":
    from config import production as settings
else:
    from config import development as settings

app = Flask(__name__)
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(transcription, url_prefix="/transcription")


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return make_response("OK", 200)


@app.route("/config", methods=["GET"])
def config():
    return make_response(str(settings.SETTINGS_TYPE), 200)


@app.errorhandler(404)
def not_found(error):
    return make_response("Route not found", 404)


if __name__ == "__main__":
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True)
