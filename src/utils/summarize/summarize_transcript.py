import os
import requests
from dotenv import load_dotenv
from flask import make_response

load_dotenv()



def summarize_transcript(text) -> str:
    """
    Summarize the transcript using Gemma Server
    """
    # call custom GEMMA API
    try:
        response = requests.post(
            f"{os.getenv('GEMMA_API_URL')}/summarize", json={"text": text}
        )

        response_body = (
            response.json().get("response")
            if response.status_code == 200
            else "Error Occured while accessing Gemma Summarization API"
        )

        return response_body

    except Exception as e:
        return f"Error Occured while accessing Gemma Summarization API: {str(e)}"
