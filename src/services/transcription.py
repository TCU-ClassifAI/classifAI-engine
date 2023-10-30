import whisper_timestamped as whisper
from concurrent.futures import ThreadPoolExecutor
import time
import uuid

# Dictionary to store job status
job_status = {}


def transcribe(file, user_id, job_id, model_type):
    """
    Transcription of an audio file using Whisper.
    Use Celery to run in the background.

    Args:
        file (File): Audio file to be transcribed.
        user_id (str): ID of the user who uploaded the audio file.
        job_id (str): ID of the job.
        model_type (str): Model type to use for transcription (e.g. 'large', 'tiny.en')
    Returns:
        str: Path to transcription file (in JSON format).
        - Full specifications of JSON format can be found
        in docs/transcription.md
    """

    model = whisper.load_model(model_type)

    try:
        audio = whisper.load_audio(file)
    except Exception as e:
        return f"Error loading audio: {e}"

    try:
        result = whisper.transcribe_timestamped(
            model, audio, refine_whisper_precision=0.1
        )
        # Store the result in job_status using the job_id as a key
        job_status[job_id] = {
            "status": "completed",
            "result": result,
            "start_time": job_status[job_id]["start_time"],
            "end_time": time.time(),
        }
        return result
    except Exception as e:
        # Update job status with an error message
        job_status[job_id] = {
            "status": "failed",
            "error_message": str(e),
            "start_time": job_status[job_id]["start_time"],
            "end_time": time.time(),
        }
        return str(e)


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
        status = job_info["status"]
        result_info = {"status": status}
        if status == "completed" or status == "failed":
            result_info["result"] = (
                job_info["result"]
                if status == "completed"
                else job_info["error_message"]
            )
            result_info["duration"] = job_info["end_time"] - job_info["start_time"]

        if status == "in progress":
            result_info["duration"] = time.time() - job_info["start_time"]
        return result_info
    else:
        return {"status": "not found"}


def start_transcription(file, model_type, user_id=None):
    """
    Start transcription of an audio file using Whisper.
    Use ThreadPoolExecutor to run in the background.

    Args:
        file (File): Audio file to be transcribed.
        model_type (str): Model type to use for transcription (e.g. 'large', 'tiny.en')
        user_id (str, optional): ID of the user who uploaded the audio file (default=None).
    Returns:
        str: The job ID for the transcription task.
    """
    job_id = str(uuid.uuid4())  # Generate a job ID using uuid
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(transcribe, file, user_id, job_id, model_type)

    # Create a job status entry with "in progress" status
    job_status[job_id] = {"status": "in progress", "start_time": time.time()}

    return job_id  # Return the job ID immediately


# Example usage:
if __name__ == "__main__":
    job_id = start_transcription("court_audio.mp3", "tiny.en", user_id=123)
    print(f"Started transcription job with ID: {job_id}")

    # Check the progress every 5 seconds until the job is completed
    while True:
        result = check_transcription(job_id)
        print(result)
        print(f"Job Status: {result['status']}")
        if result["status"] == "completed":
            print(f"Result: {result['result']}")
        # if duration is available, print it
        if "duration" in result:
            print(f"Duration: {result['duration']} seconds")
        if result["status"] == "completed" or result["status"] == "failed":
            break
        time.sleep(5)
