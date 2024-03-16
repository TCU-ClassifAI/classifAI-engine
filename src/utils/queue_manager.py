from utils.jobs import Job
import redis
from rq import Queue
from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
import logging
import uuid
import json
from utils.worker_manager import process_job
from utils.transcription.download_utils import download_and_convert_to_mp3
from rq.job import Job as RQJob

load_dotenv()


# Blueprint
queue_management = Blueprint("queue_management", __name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=os.getenv("REDIS_PORT"), db=0)
q = Queue('jobs', connection=r)


def enqueue_yt_transcription(job_id, url, model_name):
    """
    Enqueue a job in the job queue. Start by downloading the YouTube video and then call enqueue.

    Args:
        job_id (str): ID of the job. If not provided, a random UUID will be generated.
        url (str): URL of the
        model_name (str): Name of the model to use for transcription (default: "large-v3")
    """

    audio_path = download_and_convert_to_mp3(url)
    if audio_path is None:
        return jsonify({"error": "Error downloading audio"}), 500
    job_info = {
        "audio_path": audio_path,
        "model_id": model_name
    }
    return enqueue("transcription", job_id, job_info)





def enqueue(job_type: str, job_id: str, job_info: dict = None):
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
    # job_type = request.form.get("job_type")
    # job_id = request.form.get("job_id")
    # job_info = request.form.get("job_info")


    if job_type is None:
        return jsonify({"error": "job_type is required"}), 400
    
    if job_id is None:
        job_id = str(uuid.uuid4())

    # convert job_info to a dictionary if it is not None
    if job_info is not None and type(job_info) == str:
        try:
            job_info = json.loads(job_info)
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid job_info"}), 400     
    try:
        job = Job(type=job_type, job_id=job_id, job_info=job_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    job_pickle = job.pickle()
    description = {
        "job_type": job.type,
        "job_status": "queued",
    }
    description = json.dumps(description)
    q.enqueue(process_job, job_pickle, job_id=job.job_id, job_timeout="5m", description=description, result_ttl=-1, meta={"job_type": job.type, "job_id": job.job_id, "status": "queued"})
    logging.info(f"Job enqueued: {job.job_id}")
    return jsonify({"message": "Job enqueued", "job_id": str(job.job_id)}), 200

    

    




def get_job_status(job_id: str):
    """
    Get the status of a job by job_id.

    Args:
        job_id (str): ID of the job to check.
    Returns:
        dict: A dictionary containing the status and result/error message.
    """

    if job_id is None:
        return jsonify({"error": "No job ID provided"}), 400

    try:
        rqjob = RQJob.fetch(job_id, connection=r)
    except Exception as e:
        return jsonify({"error": "Invalid job ID: " + str(job_id)}), 400
    if rqjob is None:
        return jsonify({"error": "Invalid job ID: {job_id}"}), 400
    
    logging.info(f"Job status for {job_id}: {rqjob.get_status()}")
    print(rqjob.get_status())

    if rqjob.is_finished:

        job_unpickled = Job.unpickle(rqjob.result)
        print("Successfully unpickled job!!")

        print(Job.to_json_string(job_unpickled))
        if job_unpickled is None:
            return jsonify({"error": "Job not found"}), 400

        if job_unpickled.result is not None:
            result = Job.to_json_string(job_unpickled)
            return jsonify({"status": rqjob.get_status(), "result": result, "meta": rqjob.get_meta()}), 200
        

    return jsonify({"status": rqjob.get_status(), "meta": rqjob.get_meta()}), 200



if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(queue_management)
    app.run(port="5001", debug=True)