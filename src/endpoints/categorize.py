from flask import Blueprint, request, make_response
from dotenv import load_dotenv
import os


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
def categorize_transcript():
    """Categorize the transcript using GEMMA.
    Args:
        transcript: the transcript to categorize.
    Returns:
        Response object with the status code.
    """
    if "transcript" not in request.form:
        return make_response("No transcript provided", 400)

    transcript = request.form["transcript"]

    category_list = categorize_transcript(transcript)

    return category_list

