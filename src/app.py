from flask import Flask
import os
from dotenv import load_dotenv


# Import blueprints for endpoints
from endpoints import (
    categorize,
    summarize,
    transcription,
    analyze,
    server_info,
)


load_dotenv()  # Load environment variables from .env file


# Initialize Flask app
app = Flask(__name__)

# Register blueprints for endpoints

# Transcription Blueprint (transcribe audio or video files)
app.register_blueprint(transcription)

# Categorize Blueprint (categorize transcripts or questions by costa's level)
app.register_blueprint(categorize)

# Summarize Blueprint (text summarization)
app.register_blueprint(summarize)

# Analysis Blueprint (all-in-one transcription, categorization, and summarization)
app.register_blueprint(analyze)  # run on index route

# Server Blueprint (server information, healthcheck, and configuration)
app.register_blueprint(server_info)  # run on index route


def create_app():
    return app


if __name__ == "__main__":  # DO NOT RUN IN PRODUCTION
    local = True if os.environ.get("ENV") == "development" else False
    app.run(debug=True, port=5001, host="0.0.0.0")
