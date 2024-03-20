import requests
from dotenv import load_dotenv
import os


load_dotenv()
def categorize_question(question: str) -> int:
    """
    Categorize the question using GEMMA
    """
    # call GEMMA API
    response = requests.post(f"{os.getenv('GEMMA_API_URL')}/categorize", json={"question": question})

    # return the category
    return response.json()