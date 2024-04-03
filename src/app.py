from flask import Flask, make_response
import os
from dotenv import load_dotenv
from utils.auth import api_key_required

from config import config as settings


# Import blueprints for endpoints
# TO DO: Refactor to use settings dynamically
if settings.CATEGORIZATION_MODEL == "gemma":
    from endpoints.categorize import categorize as categorize
elif settings.CATEGORIZATION_MODEL == "gpt":
    from endpoints.categorize import categorize as categorize
if settings.SUMMARIZATION_MODEL == "gpt":
    from endpoints.summarize import summarize as summarize
elif settings.SUMMARIZATION_MODEL == "huggingface":
    from endpoints.summarize import summarize as summarize

from endpoints.transcription import transcription as transcription
# from endpoints.analyze import analyze
from endpoints.server_info import server


load_dotenv()  # Load environment variables from .env file


# Initialize Flask app
app = Flask(__name__)
# app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(transcription, url_prefix="/transcription")
app.register_blueprint(categorize, url_prefix="/categorize")
app.register_blueprint(summarize, url_prefix="/summarize")
# app.register_blueprint(analyze)
app.register_blueprint(server) # Server information, healthcheck, and config



def create_app():
    return app


if __name__ == "__main__":
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True, port=5000, host="0.0.0.0")
