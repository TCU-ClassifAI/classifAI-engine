from flask import Blueprint, request, make_response
from dotenv import load_dotenv

# from utils.analyze_audio import analyze_audio
from utils.queueing.queue_manager import enqueue, get_job_status
from utils.queueing.jobs import Job
import uuid

from config import config as settings
from flask import jsonify
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
        title = file.filename
        publish_date = None
        url = None

        # Write the file to a temporary file - convert to mp3, if necessary, later

        file_suffix = title.split(".")[-1]
        file_descriptor, audio_path = tempfile.mkstemp(suffix=f".{file_suffix}")

        try:
            file.save(audio_path)
        except Exception as e:
            return make_response(
                f"Could not save file to server: {str(e)}. Audio path is {audio_path}",
                500,
            )

    else:  # URL
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
