import requests
from dotenv import load_dotenv
import os
import random as rand
import logging


load_dotenv()


def categorize_question(question: str) -> int:
    """
    Categorize the question using LLAMA
    """
    # call GEMMA API

    try:
        response = requests.post(
            f"{os.getenv('LLAMA_API_URL')}/categorize", json={"question": question}
        )

    except Exception as e:
        logging.error(f"Error Occured while accessing LLAMA API: {str(e)}")
        # return random category
        return rand.randint(0, 3)

    print(f"Response for question: {question} is {response.json().get('response')}")

    # return the category
    return int(response.json().get("response"))
