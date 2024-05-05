from flask import Blueprint, request, make_response, Flask, Response
from dotenv import load_dotenv
import os
import json


load_dotenv()


summarize = Blueprint("summarize", __name__)

from utils.summarize.summarize_transcript import summarize_transcript


def get_transcript_from_request():
    """
    Extract the transcript from the request. Handles both text and transcript JSON formats.

    Returns:
        str: The extracted transcript.
        tuple: Error response if no transcript is provided.
    """
    # Extract the transcript data from the request
    data = request.get_json()
    transcript = data.get("text")

    # Check if the transcript text is not provided
    if not transcript:
        transcript_json = data.get("transcript")

        # If transcript details are also not provided, return an error response
        if not transcript_json:
            return make_response("No transcript provided", 400)

        # Concatenate text entries from transcript details
        transcript = ""

        try:
            for line in transcript_json:
                transcript += line["text"] + " "
        except:
            return make_response("Invalid transcript format", 400)

    return transcript.strip()


@summarize.route("/summarize", methods=["POST"])
def summarize_endpoint():
    """Summarize the transcript using a pre-trained model (see config)
    Args:
        text: the transcript to summarize. json={"text": raw_text}
        OR json = {"transcript": [{"text": "line1"}, {"text": "line2"}]} (gets concatenated)
    Returns:
        Response object with the status code.
    """

    transcript = (
        get_transcript_from_request()
    )  # extract the transcript from the request

    if isinstance(transcript, Response):  # Check for error response
        return transcript

    summary = summarize_transcript(transcript)

    return summary


if __name__ == "__main__":  # do not use this in production
    app = Flask(__name__)
    app.register_blueprint(summarize)
    app.run(debug=True, port=5004)
