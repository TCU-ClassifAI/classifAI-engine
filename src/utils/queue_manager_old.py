import queue
import threading 
from utils.transcription.transcribe_and_diarize_threaded import transcribe_and_diarize  # Load your function
from time import sleep  # Just for simulating work duration 
from datetime import datetime
import json
from dataclasses import dataclass, asdict


job_queue = queue.Queue()
progress_tracker = {} 

@dataclass
class TranscriptionJob:
    """
    Dataclass to store information about a transcription job.

    Attributes:
        job_id: Unique ID of the transcription job.
        user_id: ID of the user who started the transcription job (default: None).
        model_type: Name of the model used for transcription (default: "large-v3").
        status: Status of the transcription job (default: "transcribing").
        start_time: Start time of the transcription job (datetime) (default: current time).
        end_time: End time of the transcription job (default: None).
        duration: Duration of the transcription job in milliseconds (default: 0).
        result: List of transcription segments (default: None).
        error_message: Error message of the transcription job (default: None).
    """

    job_id: str
    user_id: str = None
    model_type: str = "large-v3"
    status: str = "transcribing"  # "transcribing", "diarizing", "punctuating", "completed", "failed"
    start_time: datetime = datetime.now()
    end_time: datetime = None
    duration: float = 0  # in milliseconds
    result: list = None
    error_message: str = None
    title: str = None # Title of Youtube or other video

    def to_json_string(self) -> str:
        """
        Convert the dataclass to a JSON string. Remove any fields with None values.

        Args:
            None (self)
        Returns:
            str: JSON string representation of the dataclass.
        """

        # Helper function to format the datetime
        def format_datetime(datetime_obj) -> str:
            return (
                datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                if datetime_obj
                else None
            )

        # Get current duration if the job is still not "completed" or "failed"
        if self.status not in ["completed", "failed"]:
            self.duration = self.get_duration()

        data_dict = asdict(self)

        # Ensure result is formatted correctly
        if self.result is not None:
            data_dict["result"] = [asdict(segment) for segment in self.result]

        filtered_dict = {
            key: value for key, value in data_dict.items() if value is not None
        }

        if filtered_dict.get("start_time") is not None:
            filtered_dict["start_time"] = format_datetime(filtered_dict["start_time"])

        if filtered_dict.get("end_time") is not None:
            filtered_dict["end_time"] = format_datetime(filtered_dict["end_time"])

        return json.dumps(filtered_dict, default=str)

    def get_duration(self) -> int:
        """
        Get the duration of the transcription job.

        Args:
            None (self) (accesses the start_time and end_time datetime attributes of the dataclass)
        Returns:
            int: Duration of the transcription job in milliseconds.
        """
        if self.start_time is not None and self.end_time is not None:
            return int((self.end_time - self.start_time).total_seconds() * 1000)
        if self.start_time is not None:
            return int((datetime.now() - self.start_time).total_seconds() * 1000)
        return 0



def enqueue_transcription(job_id, url, model_id):
    job_queue.put((job_id, url, model_id))
    progress_tracker[job_id] = {"state": "queued", "message": "Waiting in queue"}

def get_transcription_status(job_id):
    """Get the status of a transcription job by its job ID."""
    if job_id in progress_tracker:
        return progress_tracker[job_id]
    else:
        return {"error": "Job ID not found"}
    

def enqueue_yt_transcription(job_id, url, model_id):
    job_queue.put((job_id, url, model_id))
    progress_tracker[job_id] = {"state": "queued", "message": "Waiting in queue"}



def worker_thread():
    while True:
        job_id, url, model_id = job_queue.get()
        try:
            progress_tracker[job_id]["state"] = "processing"
            progress_tracker[job_id]["message"] = "In progress"

            result = transcribe_and_diarize(url, model_id)  # Update to use your real functions
            sleep(5)  # Simulate transcription and diarization time

            progress_tracker[job_id]["state"] = "complete"
            progress_tracker[job_id]["message"] = result 
        except Exception as e:
            progress_tracker[job_id]["state"] = "error"
            progress_tracker[job_id]["message"] = str(e)
        finally:
            job_queue.task_done() 

threading.Thread(target=worker_thread, daemon=True).start()
