import os
import logging
from config.config import SUMMARIZATION_MODEL

from utils.summarize.summarize_llama import summarize_llama


def summarize_transcript(text: str) -> str:
    """
    Summarize the transcript using a custom summarization API.

    Args:
        text: the transcript to summarize.

    Returns:
        str: The summarized transcript.
    """

    try:
        if SUMMARIZATION_MODEL == "gpt":
            # TODO: Implement GPT summarization model
            # return summarize_gpt(text)
            return "GPT summarization model is not supported yet."
        elif SUMMARIZATION_MODEL == "huggingface":
            # TODO: Implement Huggingface summarization model
            # return summarize_huggingface(text)
            return "Huggingface summarization model is not supported yet."
        elif SUMMARIZATION_MODEL == "llama":
            return summarize_llama(text)
        else:
            return "Invalid summarization model selected, please check config.py"
    except Exception as e:
        logging.error(f"Error Occured while accessing Summarization API: {str(e)}")
        return f"Error Occured while accessing Summarization API: {str(e)}"
