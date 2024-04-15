from flask import Blueprint, request, make_response, Flask
from dotenv import load_dotenv
import os
import json
from utils.transcription.convert_utils import convert_to_mp3
from utils.transcription.download_utils import download_and_convert_to_mp3

# from utils.analyze_audio import analyze_audio
from utils.queue_manager import Job, enqueue
import uuid

from config import config as settings
from utils.queue_manager import get_job_status
from flask import jsonify
import logging
import tempfile

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
        print("Hi")
        title = file.filename
        publish_date = None
        url = None
        print(title)
        print("Bue")

        # Save the file to the server - Convert to MP3 Later - using temp file

        file_suffix = title.split(".")[-1]
        file_descriptor, audio_path = tempfile.mkstemp(suffix=f".{file_suffix}")
        # save the file to the server

        print(audio_path)

        try:
            file.save(audio_path)
        except Exception as e:
            return make_response(
                f"Could not save file to server: {str(e)}. Audio path is {audio_path}",
                500,
            )

    else:
        url = request.json.get("url")
        audio_path = None
        publish_date = request.json.get("publish_date")
        if not url:
            return make_response("No URL or Audio File provided", 400)
        title = url

    model_name = settings.TRANSCRIPTION_MODEL
    try:
        job = Job.initialize_analysis_job(
            Job(job_id=str(uuid.uuid4()), type="analyze"),
            audio_path=audio_path,
            model_type=model_name,
            title=title,
            publish_date=publish_date,
            url=url,
        )

        print(job.job_info)

        job_queue = enqueue("analyze", job.job_id, job.job_info)

        return job_queue
    except Exception as e:
        return make_response(str(e), 500)


@analyze.route("/analyze", methods=["GET"])
def analyze_status():
    job_id = request.args.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id parameter is required"}), 400

    return get_job_status(job_id)
