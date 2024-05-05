from typing import List
from utils.categorize.extract_questions import extract_questions, Question
import multiprocessing

from config.config import CATEGORIZATION_MODEL

if CATEGORIZATION_MODEL == "gemma":
    from utils.categorize.categorize_gemma import categorize_question
elif CATEGORIZATION_MODEL == "llama":
    from utils.categorize.categorize_llama import categorize_question
else:
    raise ValueError("Invalid categorization model selected, please check config.py")


def process_question(question: Question) -> Question:
    question_text = build_question_text(question)

    print("Question text: ", question_text)
    level = categorize_question(question_text)
    print(level)
    question = question.set_level(level)
    question = question.clear_previous_sentences()
    return question


def categorize_list_of_questions(questions: List[Question]) -> List[Question]:
    try:
        with multiprocessing.Pool() as pool:  # Create a process pool
            results = pool.map(
                process_question, questions
            )  # Map the function to the list of questions
            print(results)
        return results
    except Exception as e:
        raise "Could not categorize questions. Error: " + str(e)


def categorize_transcript(transcript: dict) -> List[int]:
    """
    Categorize the transcript using GEMMA
    """

    # Extract all questions from the transcript
    questions = extract_questions(transcript)
    with multiprocessing.Pool() as pool:  # Create a process pool
        results = pool.map(
            process_question, questions
        )  # Map the function to the list of questions
    # for question in questions:
    #     question_text = build_question_text(question)
    #     print(question_text)
    #     # Categorize each question using GEMMA
    #     level = categorize_question(question_text)
    #     question= question.set_level(level)
    #     question = question.clear_previous_sentences()
    #     # convert the question to a dictionary
    #     question = question.to_dict()

    return questions


def build_question_text(question: Question) -> str:
    """Builds a question text string, omitting empty or None values."""
    parts = [
        part
        for part in (
            question.get("two_previous_sentence"),
            question.get("previous_sentence"),
            question.get("question"),
        )
        if part
    ]
    return " ".join(parts)
