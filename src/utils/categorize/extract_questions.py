import json
from utils.categorize.categorize_gemma import categorize_question
from flask import Blueprint, make_response, request, Flask
import concurrent.futures
from dataclasses import dataclass
from typing import List


questions = Blueprint("questions", __name__)


@dataclass
class Question:
    """
    A dataclass to represent a question.

    Attributes:
        question (str): the question
        speaker (str): the speaker of the question (optional)
        start_time (float): the start time of the question (optional)
        end_time (float): the end time of the question (optional)
        previous_sentence (str): the sentence before the question (optional)
        two_previous_sentence (str): two sentences before the question (optional)
        level (int): the level of the question (optional)
    """

    question: str
    speaker: str = None
    start_time: float = None
    end_time: float = None
    previous_sentence: str = None
    two_previous_sentence: str = None
    level: int = None

    def get(self, key):
        return getattr(self, key)

    def set_level(self, level):
        self.level = level
        return self

    def clear_previous_sentences(self):
        self.previous_sentence = None
        self.two_previous_sentence = None
        return self

    def to_dict(self):
        """
        Convert the dataclass to a dictionary. Remove any keys with None values.
        """
        # if a value is None, don't include it in the dictionary
        # if a value is null, don't include it in the dictionary
        return {k: v for k, v in self.__dict__.items() if v is not None and v != "null"}


def extract_questions(transcript: dict) -> List[Question]:
    questions = []
    previous_text = ""  # The sentence before the question
    two_previous_text = ""  # Two sentences before the question

    print("transcript", transcript)
    # transcript = json.loads(transcript)
    for segment in transcript:
        # check if segment text exists
        if "text" not in segment:
            raise ValueError(
                "Segment does not contain text. Please ensure that the transcript is in the correct format where each segment has ['text']."
            )
        if "?" in segment["text"]:
            question = Question(
                question=segment["text"],
                speaker=segment["speaker"],
                start_time=segment["start_time"],
                end_time=segment["end_time"],
            )
            if previous_text:
                question.previous_sentence = previous_text

            if two_previous_text:
                question.two_previous_sentence = two_previous_text

            questions.append(question)
            two_previous_text = previous_text
            previous_text = segment["text"]
    return questions


@questions.route("/healthcheck")
def healthcheck():
    return make_response("OK", 200)


@questions.route("/extract_questions", methods=["POST"])
def extract_questions_in_context():
    """
    Return questions, their speaker, and the start and end time of the question
    Also include the previous and next segments for context, and the speaker of the previous and next segments

    Args:
        transcript (str): the transcript JSON (format is on documenation)

    Returns:
        list: list of dictionaries, each containing the question, speaker, start and end time, previous segment,
        next segment, previous speaker, and next speaker

    """

    data = request.json
    transcript = data["transcript"]

    questions = []
    transcript = json.loads(transcript)
    for i, segment in enumerate(transcript["result"]):
        if "?" in segment["text"]:
            question = {
                "question": segment["text"],
                "speaker": segment["speaker"],
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "previous_segment": (
                    transcript["result"][i - 1]["text"] if i > 0 else None
                ),
                "next_segment": (
                    transcript["result"][i + 1]["text"]
                    if i < len(transcript["result"]) - 1
                    else None
                ),
                "previous_speaker": (
                    transcript["result"][i - 1]["speaker"] if i > 0 else None
                ),
                "next_speaker": (
                    transcript["result"][i + 1]["speaker"]
                    if i < len(transcript["result"]) - 1
                    else None
                ),
            }
            questions.append(question)
    return questions


def categorize_all_questions() -> list:
    """
    Return questions, their speaker, and the start and end time of the question
    Also include the previous and next segments for context, and the speaker of the previous and next segments
    Also include the question type and Costa's level of reasoning for each question

    Args:
        transcript (str): the transcript JSON (format is on documenation)

    Returns:
        list: list of dictionaries, each containing the question, speaker, start and end time, previous segment, next segment,
        previous speaker, next speaker, question type, and Costa's level of reasoning

    """
    data = request.get_json()
    transcript = data.get("transcript")

    if transcript is None:
        return make_response("No transcript provided", 400)

    # Get server url
    server_url = request.url_root

    # Extract questions from the transcript

    response = requests.post(
        f"{server_url}/questions/extract_questions", json={"transcript": transcript}
    )

    questions = response.json()

    print(questions)

    # for the first question, categorize the question type and Costa's level
    # of reasoning
    question_one = questions[0]

    # categorize the question
    categorize_question_response = categorize_question(question_one)

    # for each question, categorize the question type and Costa's level of
    # reasoning

    # Using concurrent.futures.ProcessPoolExecutor() to parallelize the
    # process_question function
    with concurrent.futures.ProcessPoolExecutor() as executor:
        processed_questions = executor.map(process_question, questions)
        # Converting map object to list to access the processed questions
        processed_questions = list(processed_questions)

    print(categorize_question_response)

    return questions


def process_question(question):
    categorize_question_response = categorize_question(question)
    question["question_type"] = categorize_question_response["question_type"]
    question["question_level"] = categorize_question_response["question_level"]
    return question


# Test on log.txt
if __name__ == "__main__":
    import requests

    with open("log.txt", "r") as file:
        transcript = file.read()

    # run flaskapp
    app = Flask(__name__)
    app.register_blueprint(questions, url_prefix="/questions")

    app.run(port=5001)

    # include transcript in the request
    response = requests.post(
        "http://localhost:5001/questions/extract_questions",
        json={"transcript": transcript},
    )
    print(response.json())
