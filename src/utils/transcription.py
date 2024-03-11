from flask import Blueprint, make_response, current_app, request, jsonify
from typing import Optional
import time
import uuid
import json
from dataclasses import dataclass, asdict
from whisperplus import (
    ASRDiarizationPipeline,
)
from concurrent.futures import ThreadPoolExecutor


# Blueprint
transcription = Blueprint("transcription", __name__)


@transcription.route("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint.

    Returns:
        str: "OK" if the server is running.
    """
    return make_response("OK", 200)


@transcription.route("/help")
def help():
    """
    Help page.
    """
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
job_status_dict = {}


@dataclass
class TranscriptionJob:
    """
    Dataclass to store information about a transcription job.

    Args:
        job_id (str): ID of the job.
        user_id (str, optional): ID of the user who uploaded the audio file (default=None).
        model_type (str, optional): Model type to use for transcription (default='tiny.en').
        status (str, optional): Status of the job (default='in progress').
        start_time (float, optional): Start time of the job (default=time.time()).
        end_time (float, optional): End time of the job (default=None).
        duration (float, optional): Duration of the job (default=0).
        result (str, optional): Result of the job (default=None).
        error_message (str, optional): Error message of the job (default=None).

    Methods:
        to_json_string: Convert the dataclass to a JSON string.
        get_duration: Get the duration of the transcription job.
    """

    job_id: str
    user_id: str = None
    model_type: str = "openai/whisper-large-v3"
    status: str = "in progress"  # "in progress", "completed", "failed"
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


def transcribe(audio_path: str, job: TranscriptionJob, **kwargs):
    """
    Transcription of an audio file using WhisperX.

    Args:
        file (File): Audio file to be transcribed.
        job (TranscriptionJob): Transcription job object.
        model_type (str, optional): Model type to use for transcription (default='openai/whisper-large-v3').
        diarizer_model (str, optional): Speaker diarization model to use (default='pyannote/speaker-diarization').
        num_speakers (int, optional): Number of speakers in the audio (default=2).
        min_speaker (int, optional): Minimum number of speakers in the audio (default=1).
        max_speaker (int, optional): Maximum number of speakers in the audio (default=2).
        device (str, optional): Device to use for transcription (default='cuda' if available, else 'cpu').
    Returns:
        str: Path to transcription file (in JSON format).
        - Full specifications of JSON format can be found
        in docs/transcription.md
    """

    try:
        # Configuration
        device = "cuda"  # cpu or mps
        pipeline = ASRDiarizationPipeline.from_pretrained(
            asr_model="openai/whisper-large-v3",
            diarizer_model="pyannote/speaker-diarization",
            use_auth_token=False,
            chunk_length_s=30,
            device=device,
        )

        output_text = pipeline(
            audio_path, num_speakers=2, min_speaker=1, max_speaker=20
        )
        job.result = output_text
        job.status = "completed"
        job.end_time = time.time()

        job_status_dict[job.job_id] = job
        return job.to_json_string()
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        job.end_time = time.time()

        job_status_dict[job.job_id] = job
        return job.to_json_string()


@transcription.route("/check_transcription", methods=["GET"])
def check_transcription():
    """
    Check the status of a transcription job by job_id.

    Args:
        job_id (str): ID of the job to check.
    Returns:
        dict: A dictionary containing the status and result/error message.
    """
    job_id = request.args.get("job_id")
    if job_id is None:
        return jsonify({"error": "No job ID provided"}), 400

    if job_id not in job_status_dict:
        return jsonify({"error": "Invalid job ID"}), 400
    if job_id in job_status_dict:
        job_info = job_status_dict[job_id]

        job_info.duration = job_info.get_duration()

        return job_info.to_json_string()
    else:
        return {"status": "not found"}


@transcription.route("/start_transcription", methods=["POST"])
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
        else current_app.config.get("MODEL_TYPE", "openai/whisper-large-v3")
    )

    job_id = start_transcription(file, model_type)

    return make_response(job_id, 200)


def start_transcription(
    file, model_type: str = "openai/whisper-large-v3", user_id: Optional[str] = None
):
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

    # Save the file to disk (/tmp)
    file_path = f"/tmp/{job_id}.mp3"
    file.save(file_path)

    job_status_dict[job_id] = TranscriptionJob(job_id, user_id, model_type)

    executor = ThreadPoolExecutor(max_workers=80)
    executor.submit(transcribe, file_path, job_status_dict[job_id])

    return job_status_dict[job_id].to_json_string()
