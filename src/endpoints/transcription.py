from flask import Flask, request, jsonify, Blueprint, make_response
import uuid
import logging
from pydub import AudioSegment
import os

# Manually add FFMPEG to the PATH
os.environ["PATH"] += os.pathsep + "/usr/bin/"
print(os.environ["PATH"])

from utils.queueing.queue_manager import (
    enqueue_yt_transcription,
    enqueue as enqueue_transcription,
    get_job_status as get_transcription_status,
)


transcription = Blueprint("transcription", __name__)


@transcription.route("/transcribe_yt")
def start_yt_transcription():
    """Start the transcription process for a YouTube video by creating a new thread to run the process.
    Either a GET or POST request can be used.

    Args:
        url: URL of the YouTube video to transcribe.
        model_name: name of the model to use for transcription (default: large-v3)

    Returns:
        Response object with the status code.
    """
    if request.method == "GET":
        url = request.args.get("url")
        if url is None:
            return jsonify({"error": "No URL provided"}), 400
        model_name = request.args.get("model_name")
    if request.method == "POST":
        url = request.form.get("url")
        if url is None:
            return jsonify({"error": "No URL provided"}), 400
        model_name = request.form.get("model_name")

    logging.info(f"Starting transcription for YouTube video {url} with model large-v3")

    job_id = str(uuid.uuid4())  # Generate a job ID using uuid

    return enqueue_yt_transcription(job_id, url, model_name)


@transcription.route("/transcribe", methods=["POST"])
def start_transcription():
    """Start the transcription process for an audio file by creating a new thread to run the process.

    Args:
        file: audio file to transcribe.
        model_name: name of the model to use for transcription (default: large-v3)

    Returns:
        Response object with the status code.
    """
    if "file" not in request.files:
        return make_response("No file uploaded", 400)

    file = request.files["file"]

    model_name = request.form.get("model_name")

    logging.info(
        f"Starting transcription for audio file {file.filename} with model {model_name}"
    )
    print(
        f"Starting transcription for audio file {file.filename} with model {model_name}"
    )
    job_id = str(uuid.uuid4())  # Generate a job ID using uuid

    try:
        audio = AudioSegment.from_file(file)
        # save the file to the disk as mp3
        file_path = f"audio_files/{job_id}.mp3"
        # if the directory does not exist, create it
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        audio.export(file_path, format="mp3")
        print(f"File saved to {file_path}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    job_info = {"audio_path": file_path, "model_id": model_name}

    return enqueue_transcription("transcription", job_id, job_info)


@transcription.route("/get_transcription_status")
def get_status():
    job_id = request.args.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id parameter is required"}), 400

    return get_transcription_status(job_id)


if __name__ == "__main__":  # do not use this in production
    app = Flask(__name__)
    app.register_blueprint(transcription)
    app.run(debug=True)
