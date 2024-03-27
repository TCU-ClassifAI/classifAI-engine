from flask import Blueprint, request, make_response
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
        return make_response("No transcript provided", 400)
    
    summary = summarize_transcript(transcript)

    return make_response(json.dumps({"summary": summary}), 200)

@summarize.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for API

    Returns: OK
    """
    return make_response("OK", 200)


    