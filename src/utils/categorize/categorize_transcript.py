from typing import List
from utils.categorize.extract_questions import extract_questions


def categorize_transcript(transcript: str) -> List[int]:
    """
    Categorize the transcript using GEMMA
    """
    # Extract all questions from the transcript
    questions = extract_questions(transcript)
    for question in questions:
        # Categorize each question using GEMMA
        category = categorize_question(question)
        question["category"] = category

    return questions