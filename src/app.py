from flask import Flask
import os
from dotenv import load_dotenv

# Import blueprints for endpoints
from endpoints import (
    categorize,
    summarize,
    transcription,
    # analyze,
    server_info,
)


load_dotenv()  # Load environment variables from .env file


# Initialize Flask app
app = Flask(__name__)

# Register blueprints for endpoints

# Transcription Blueprint
app.register_blueprint(transcription, url_prefix="/transcription")

# Categorize Blueprint
app.register_blueprint(categorize, url_prefix="/categorize")

# Summarize Blueprint
app.register_blueprint(summarize, url_prefix="/summarize")

# Analysis Blueprint
# app.register_blueprint(analyze) # run on index route

# Server Blueprint
# Server information, healthcheck, and configuration
app.register_blueprint(server_info)  # run on index route


def create_app():
    return app


if __name__ == "__main__":  # DO NOT RUN IN PRODUCTION
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True, port=5000, host="0.0.0.0")
