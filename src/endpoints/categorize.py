from flask import Blueprint, request, make_response
from dotenv import load_dotenv
import os
import json


load_dotenv()


categorize = Blueprint("categorize", __name__)

from utils.categorize.categorize_gemma import categorize_question


@categorize.route("/categorize_question", methods=["POST"])
def categorize_question_endpoint():
    """Categorize the question using GEMMA.
    Args:
        question: the question to categorize.
    Returns:
        Response object with the status code.
    """
    # See if question is in request JSON

    question = request.get_json()["question"]
    if not question:
        return make_response("No question provided", 400)

    category = categorize_question(question)

    return make_response(json.dumps({"category": category}), 200)


from utils.categorize.categorize_transcript import categorize_transcript


@categorize.route("/categorize_transcript", methods=["POST"])
def categorize_transcript_endpoint():
    """Categorize the transcript using GEMMA.
    Args:
        transcript: the transcript to categorize.
    Returns:
        Response object with the status code.
    """
    if "file" not in request.files and not request.json:
        return make_response("No file uploaded", 400)

    file = request.files.get("file")
    if file:
        transcript = file.read()
        transcript = json.loads(transcript)
    else:
        transcript = request.json

    print("=====================================")
    print(transcript)

    # PRINT FILe
    # print(file)
    # transcript = file.read()

    # convert the JSON to a dictionary

    category_list = categorize_transcript(transcript)

    return category_list


@categorize.route("/")
def categorize_index():
    """Categorize endpoint. Return list of categorization endpoints."""
    return make_response(
        "Categorize endpoints: /categorize_question, /categorize_transcript", 200
    )
