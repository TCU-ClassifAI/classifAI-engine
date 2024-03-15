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
from rq.job import Job as RQJob

load_dotenv()


# Blueprint
queue_management = Blueprint("queue_management", __name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=os.getenv("REDIS_PORT"), db=0)
q = Queue('jobs', connection=r)


@queue_management.route("/enqueue", methods=["POST"])
def enqueue():
    """
    Enqueue a job in the job queue (redis) according to the job type.

    Args:
        job_type (str): Type of the job.
        job_id (str): ID of the job.
    Returns:
        str: A message confirming the job has been enqueued.
    """
    job_type = request.form.get("job_type")
    job_id = request.form.get("job_id")
    job_info = request.form.get("job_info")


    if job_type is None:
        return jsonify({"error": "job_type is required"}), 400
    
    if job_id is None:
        job_id = str(uuid.uuid4())

    # convert job_info to a dictionary if it is not None
    if job_info is not None:
        try:
            job_info = json.loads(job_info)
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid job_info"}), 400
        
    try:

        # create a job object from the request parameters
        job = Job(type=job_type, job_id=job_id, job_info=job_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    job_pickle = job.pickle()

    description = {
        "job_type": job.type,
        "job_status": "queued",
    }

    description = json.dumps(description)

    q.enqueue(process_job, job_pickle, job_id=job.job_id, job_timeout="5m", description=description, result_ttl=-1)

    logging.info(f"Job enqueued: {job.job_id}")

    return jsonify({"message": "Job enqueued", "job_id": str(job.job_id)}), 200

    

    



@queue_management.route("/get_job_status", methods=["GET"])
def get_job_status():
    """
    Get the status of a job by job_id.

    Args:
        job_id (str): ID of the job to check.
    Returns:
        dict: A dictionary containing the status and result/error message.
    """
    job_id = request.args.get("job_id")
    if job_id is None:
        return jsonify({"error": "No job ID provided"}), 400

    rqjob = RQJob.fetch(job_id, connection=r)
    if rqjob is None:
        return jsonify({"error": "Invalid job ID"}), 400
    
    logging.info(f"Job status for {job_id}: {rqjob.get_status()}")

    if rqjob.is_finished:
        
        result = Job.to_json_string(Job.unpickle(rqjob.result))

        return jsonify({"status": rqjob.get_status(), "result": result, "meta": rqjob.get_meta()}), 200
        

    return jsonify({"status": rqjob.get_status(), "meta": rqjob.get_meta()}), 200



if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(queue_management)
    app.run(port="5001", debug=True)