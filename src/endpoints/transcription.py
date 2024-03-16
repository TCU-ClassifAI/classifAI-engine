from flask import Flask, request, jsonify, Blueprint, make_response
import uuid
import logging

from utils.queue_manager import (
    enqueue_yt_transcription,
    enqueue as enqueue_transcription,
    get_job_status as get_transcription_status,
)


transcription = Blueprint("transcription", __name__)


@transcription.route("/transcribe_yt")
def start_yt_transcription():
    """Start the transcription process for a YouTube video by creating a new thread to run the process. Either a GET or POST request can be used.

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

    logging.info(
        f"Starting transcription for YouTube video {url} with model large-v3")

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

    job_id = str(uuid.uuid4())  # Generate a job ID using uuid

    job_info = {"audio_path": file, "model_id": model_name}

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
