import requests
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

API_URL = os.getenv("LLAMA_API_URL")


def summarize_llama(text):
    """
    Summarize the transcript using the LLAMA API.

    Args:
        text: the transcript to summarize.

    Returns:
        str: The summarized transcript.
    """
    try:
        response = requests.post(f"{API_URL}/summarize", json={"text": text})

        response_body = (
            response.json().get("response")
            if response.status_code == 200
            else "Error Occured while accessing Summarization API"
        )

        return response_body

    except Exception as e:
        return f"Error Occured while accessing Summarization API: {str(e)}"
