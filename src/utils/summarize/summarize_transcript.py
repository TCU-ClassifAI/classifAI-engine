import os
import openai
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

def summarize_transcript(text) -> str:
    """
    Summarize the transcript using Gemma Server
    """
    # call custom GEMMA API
    response = requests.post(f"{os.getenv('GEMMA_API_URL')}/summarize", json={"text": text})
