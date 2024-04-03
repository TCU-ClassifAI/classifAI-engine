from flask import Blueprint, request, make_response, Flask
from dotenv import load_dotenv
import os
import json


load_dotenv()


summarize = Blueprint("summarize", __name__)

from utils.summarize.summarize_transcript import summarize_transcript


@summarize.route("/", methods=["POST"])
def summarize_transcript_endpoint():
    """Summarize the transcript using GEMMA.
    Args:
        text: the transcript to summarize. json={"text": text}
    Returns:
        Response object with the status code.
    """
    transcript = request.get_json()["text"]
    if not transcript:
        transcript_json = request.get_json()["transcript"]
        if not transcript_json:
            return make_response("No transcript provided", 400)
        transcript = ""
        for line in transcript_json:
            transcript += line["text"] + " "

    print("=====================================")
    print(transcript)
    summary = summarize_transcript(transcript)

    return summary


@summarize.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for API

    Returns: OK
    """
    return make_response("OK", 200)


if __name__ == "__main__":  # do not use this in production
    app = Flask(__name__)
    app.register_blueprint(summarize, url_prefix="/summarize")
    app.run(debug=True, port=5004)
