from dataclasses import dataclass, asdict
import time
import json
from typing import Optional
import redis

@dataclass
class Job:
    """
    Dataclass to store information about a job

    Args:
        job_id (str): ID of the job.
        type (str): Type of the job. 'transcription', 'summarization', or 'categorization'.
        user_id (str, optional): ID of the user who uploaded the audio file (default=None).
        status (str, optional): Status of the job 'queued', 'in progress', 'completed', or 'failed'.
        subtask (str, optional): List of subtasks that are part of the job. (loading_model, transcribing, diarizing, etc.)
        subtask_message (str, optional): Message for the subtask (default=None).
        submit_time (float, optional): Time when the job was submitted (default=time.time()).
        start_time (float, optional): Start time of the job from the queue (default=None).
        end_time (float, optional): End time of the job (default=None).
        duration (float, optional): Duration of the job from submission to completion (default=0).
        result (str, optional): Result of the job, if any (default=None).
        error_message (str, optional): Error message of the job, if any (default=None).
        job_info (dict, optional): Additional information about the job used by the worker, like the audio file path, model_type, etc. (default=None).

    Methods:
        to_json_string: Convert the dataclass to a JSON string.
        get_duration: Get the duration of the transcription job.
        enqueue: Enqueue the job in the job queue according to the job type.
        dequeue: A worker dequeues the job from the job queue and starts processing it.
    """

    job_id: str
    type: str
    user_id: str = None
    status: str = "queued"
    subtask: str = None
    subtask_message: str = None
    submit_time: float = time.time()
    start_time: float = None
    end_time: float = None
    duration: float = 0
    result: str = None
    error_message: str = None
    job_info: dict = None

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
    
    def from_json_string(json_string: str):
        """
        Convert a JSON string to a Job object.

        Args:
            json_string (str): JSON string representation of the dataclass.
        Returns:
            Job: Job object created from the JSON string.
        """
        data_dict = json.loads(json_string)
        for key, value in data_dict.items():
            if value is None:
                data_dict[key] = None
        return Job(**data_dict)
    
    def initialize_transcription_job(self, audio_path: str, model_type: str = "large-v3", title: str = None):
        """
        Initialize a transcription job with the audio file path and model type.

        Args:
            audio_path (str): Path to the audio file.
            model_type (str): Name of the model used for transcription (default: "large-v3").
            title (str, optional): Title of Youtube or other video (default: None).
        Returns:
            None
        """
        self.job_info = {
            "audio_path": audio_path, # Path to the audio file, downloaded before processing
            "model_type": model_type, # Name of the model used for transcription (default: "large-v3")
            "title": title,
        }

    def initialize_categorization_job(self, transcript: str):
        """
        Initialize a categorization job with the transcript.

        Args:
            transcript (str): Transcript of the audio file.
        Returns:
            None
        """
        self.job_info = {
            "transcript": transcript, # Transcript of the audio file to be categorized
        }

    def initialize_summarization_job(self, transcript: str):
        """
        Initialize a summarization job with the transcript.

        Args:
            transcript (str): Transcript of the audio file.
        Returns:
            None
        """
        self.job_info = {
            "transcript": transcript, # Transcript of the audio file to be summarized
        }
    
    def get_duration(self) -> float:
        """
        Get the duration of the job.

        Args:
            None (self)
        Returns:
            float: Duration of the job in seconds.
        """
        if self.start_time is None:
            return None
        return self.end_time - self.start_time
    
    # def enqueue(self, r):
    #     """
    #     Enqueue the job in the job queue (redis) according to the job type.

    #     Args:
    #         r (redis.Redis): Redis connection object.
    #     Returns:
    #         None
    #     """
    #     # Connect to Redis
    #     # Enqueue the job
    #     r.lpush(self.type, self.to_json_string())

    # def dequeue(self, r):
    #     """
    #     A worker dequeues the job from the job queue and starts processing it.

    #     Args:
    #         r (redis.Redis): Redis connection object.
    #     Returns:
    #         The job object that was dequeued. (Job)
    #     """
    #     # Connect to Redis

    #     # Dequeue the job
    #     job_string = r.rpop(self.type)
    #     # Convert the job string to a Job object
    #     job = Job(**json.loads(job_string))
    #     # Update the status of the job
    #     job.status = "in progress"
    #     job.start_time = time.time()
    #     # Update the job in the queue
    #     r.lpush(self.type, job.to_json_string())
    #     return job


# job = Job("123", "transcription", "user1", "queued", "loading_model", "large-v3", time.time(), None, None, 0, None, None)


