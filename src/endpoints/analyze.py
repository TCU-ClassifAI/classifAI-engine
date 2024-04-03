from flask import Blueprint, request, make_response, Flask
from dotenv import load_dotenv
import os
import json
from utils.transcription.convert_utils import convert_to_mp3
from utils.transcription.download_utils import download_and_convert_to_mp3
from utils.analyze_audio import analyze_audio
from utils.queue_manager import Job, enqueue
import uuid

from config import config as settings

load_dotenv()

analyze = Blueprint("analyze", __name__)


@analyze.route("/analyze", methods=["POST"])
def analyze_endpoint():
    """Analyze a video, audio file, or YouTube link.

    Args:
        file: video or audio file to analyze. (default: None)
        url: URL of the YouTube video to analyze. (default: None)
        model_name: name of the model to use for analysis (default: large-v3)

    Returns:
        Response object with the status code.
    """

    # Check if file or URL is in request
    if "file" not in request.files and not request.json:
        return make_response(
            "No file uploaded. Please provide either a YouTube URL or a file", 400
        )

    file = request.files.get("file")  # Audio or video file
    if file:
        file = file.read()
        # Get file name
        title = file.filename
        # Get publish date
        publish_date = request.json.get("publish_date")

        # Attempt to convert to MP3 using ffmpeg
        audio_path = convert_to_mp3(file)
        if audio_path is None:
            return make_response("Error converting file to MP3", 500)
    else:
        url = request.json.get("url")
        if not url:
            return make_response("No URL provided", 400)
        audio_path, title, publish_date = download_and_convert_to_mp3(url)
        if audio_path is None:
            return make_response("Error downloading audio from YouTube", 500)

    model_name = request.json.get("model_name")
    if not model_name:
        model_name = settings.TRANSCRIPTION_MODEL
    try:
        job = Job.initialize_analysis_job(audio_path, model_name, title, publish_date)

        job_queue = enqueue("analyze", uuid.uuid4(), job)
        return make_response(f"Job {job_queue.id} enqueued for analysis", 200)
    except Exception as e:
        return make_response(str(e), 500)

    # def enqueue(job_type: str, job_id: str, job_info: dict = None):
    """
    Enqueue a job in the job queue (redis) according to the job type.

    Args:
        job_type (str): Type of the job. Required.
        job_id (str): ID of the job. If not provided, a random UUID will be generated.
        job_info (str): Information about the job in JSON format. (default: None)
            - Job info can contain the following fields:
                for transcription: {"audio_path": "path/to/audio/file",
                  "model_id": "model_id"}
                for summarization: {"text": "text to summarize"}
                for categorization: {"text": "text to categorize"}
                for other jobs: {"key": "value"}

    Returns:
        str: A message confirming the job has been enqueued.
    """
