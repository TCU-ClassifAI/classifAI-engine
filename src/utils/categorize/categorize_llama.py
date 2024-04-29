import requests
from dotenv import load_dotenv
import os
import random as rand

load_dotenv()


def categorize_question(question: str) -> int:
    """
    Categorize the question using GEMMA
    """
    # call GEMMA API

    try:
        response = requests.post(
            f"{os.getenv('GEMMA_API_URL')}/categorize", json={"question": question}
        )

    except Exception as e:
        # return random category
        return rand.randint(0, 3)
    

    print(response.json())

    # return the category
    return int(response.json().get("response"))
