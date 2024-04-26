from flask import Blueprint, request, make_response
from dotenv import load_dotenv
import json

load_dotenv()

categorize = Blueprint("categorize", __name__)

from utils.categorize.categorize_gemma import categorize_question
from utils.categorize.categorize_transcript import categorize_transcript


@categorize.route("/categorize/question", methods=["POST"])
def categorize_question_endpoint():
    """Categorize the question using a pre-trained model (see config)
    Args:
        question: the question to categorize. String.
    Returns:
        Response object with the status code.
    """
    # See if question is in request JSON

    question = request.get_json()["question"]
    if not question:
        return make_response("No question provided", 400)

    category = categorize_question(question)

    return make_response(json.dumps({"category": category}), 200)


@categorize.route("/categorize/transcript", methods=["POST"])
def categorize_transcript_endpoint():
    """Categorize the transcript using a pre-trained model (see config)
    Args:
        transcript: the transcript to categorize (JSON format or file upload)
    Returns:
        Response object with the status code.
    """

    # Handle file upload
    if "file" not in request.files and not request.json:
        return make_response("No file uploaded", 400)

    file = request.files.get("file")
    if file:
        transcript = file.read()
        transcript = json.loads(transcript)
    else:
        transcript = request.json


    category_list = categorize_transcript(transcript)

    return make_response(json.dumps({"categories": category_list}), 200)


@categorize.route("/categorize")
def categorize_index():
    """Categorize endpoint. Return list of categorization endpoints."""
    return make_response(
        "Categorize endpoints: /categorize/question, /categorize/transcript", 200
    )
