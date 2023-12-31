from flask import Blueprint, make_response, current_app, request
from typing import Optional
import time
import uuid
import json
from dataclasses import dataclass, asdict
import whisper
from concurrent.futures import ThreadPoolExecutor
from auth import api_key_required

transcription = Blueprint("transcription", __name__)


@transcription.route("/healthcheck")
def healthcheck():
    return make_response("OK", 200)


@transcription.route("/help")
def help():
    content = """
    <h1>WhisperX API</h1>
    <h2>Endpoints</h2>
    <ul>
        <li><code>/healthcheck</code> - Healthcheck endpoint</li>
        <li><code>/help</code> - Help page</li>
        <li><code>/start_transcription</code> - Start a transcription job</li>
        <li><code>/check_transcription</code> - Check the status of a transcription job</li>
        <li><code>/config</code> - Get the current configuration</li>
    </ul>
    """
    return make_response(content, 200)


# Dictionary to store job status
job_status = {}


@dataclass
class TranscriptionJob:
    """
    Dataclass to store information about a transcription job.
    """

    job_id: str
    user_id: str = None
    model_type: str = "tiny.en"
    status: str = "in progress"  # "in progress", "completed", "failed"
    state: str = "loading model"  # "loading model", "loading audio", "transcribing", "completed", "failed"
    start_time: float = time.time()
    end_time: float = None
    duration: float = 0  # in seconds
    result: str = None
    error_message: str = None

    def to_json_string(self) -> str:
        """
        Convert the dataclass to a JSON string. Remove any fields with None values.

        Args:
            None (self)
        Returns:
            str: JSON string representation of the dataclass.
        """
        data_dict = asdict(self)
        filtered_dict = {
            key: value for key, value in data_dict.items() if value is not None
        }
        return json.dumps(filtered_dict)

    def get_duration(self) -> float:
        """
        Get the duration of the transcription job.

        Args:
            None (self)
        Returns:
            float: Duration of the transcription job in seconds.
        """
        if self.start_time is None:
            return None
        elif self.end_time is None:
            return time.time() - self.start_time
        else:
            return self.end_time - self.start_time


def transcribe(file, job: TranscriptionJob):
    """
    Transcription of an audio file using WhisperX.

    Args:
        file (File): Audio file to be transcribed.
        job (TranscriptionJob): Transcription job object.
    Returns:
        str: Path to transcription file (in JSON format).
        - Full specifications of JSON format can be found
        in docs/transcription.md
    """

    model = whisper.load_model(job.model_type)

    try:
        audio = whisper.load_audio(file)
    except Exception as e:
        return f"Error loading audio: {e}"

    try:
        result = whisper.transcribe(model, audio, refine_whisper_precision=0.1)
        job.result = result
        job.status = job.state = "completed"
        job.end_time = time.time()

        job_status[job.job_id] = job
        return job.to_json_string()
    except Exception as e:
        job.state = job.status = "failed"
        job.error_message = str(e)
        job.end_time = time.time()

        job_status[job.job_id] = job
        return job.to_json_string()


@transcription.route("/check_transcription", methods=["GET"])
@api_key_required
def check_transcription(job_id):
    """
    Check the status of a transcription job by job_id.

    Args:
        job_id (str): ID of the job to check.
    Returns:
        dict: A dictionary containing the status and result/error message.
    """
    if job_id in job_status:
        job_info = job_status[job_id]
        job_info.duration = job_info.get_duration()

        return job_info.to_json_string()
    else:
        return {"status": "not found"}


@transcription.route("/start_transcription", methods=["POST"])
@api_key_required
def start_transcription_endpoint():
    if "file" not in request.files:
        return make_response("No file uploaded", 400)

    file = request.files["file"]

    print(current_app.config.get("MODEL_TYPE"))
    # print the file name
    print(file.filename)

    model_type = (
        request.form["model_type"]
        if "model_type" in request.form
        else current_app.config.get("MODEL_TYPE", "tiny.en")
    )

    job_id = start_transcription(file, model_type)

    return make_response(job_id, 200)


def start_transcription(file, model_type: str, user_id: Optional[str] = None):
    """
    Start transcription of an audio file using Whisper.
    Use ThreadPoolExecutor to run in the background.
    Args:
        file (File): Audio file to be transcribed.
        model_type (str): Model type to use for transcription (e.g. 'large', 'tiny.en')
        user_id (str, optional): ID of the user who uploaded the audio file (default=None).
    Returns:
        str: JSON string representation of a TranscriptionJob object.
    """
    job_id = str(uuid.uuid4())  # Generate a job ID using uuid

    job_status[job_id] = TranscriptionJob(job_id, user_id, model_type)

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(transcribe, file, user_id, job_id, model_type)

    return job_status[job_id].to_json_string()
