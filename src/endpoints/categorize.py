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

    return category

from utils.categorize.categorize_transcript import categorize_transcript

@categorize.route("/categorize_transcript", methods=["POST"])
def categorize_transcript_endpoint():
    """Categorize the transcript using GEMMA.
    Args:
        transcript: the transcript to categorize.
    Returns:
        Response object with the status code.
    """
    if "file" not in request.files:
        return make_response("No file uploaded", 400)

    file = request.files["file"]
    # PRINT FILe
    print(file)
    transcript = file.read()

    # Load the file into JSON
    json_transcript = json.loads(transcript)
    print(json_transcript)

    # convert the JSON to a dictionary
    transcript = json.loads(transcript)


    category_list = categorize_transcript(transcript)

    return category_list

@categorize.route("/")
def categorize_index():
    """Categorize endpoint. Return list of categorization endpoints."""
    return make_response(
        "Categorize endpoints: /categorize_question, /categorize_transcript", 200
    )

