from utils.jobs import Job
import redis
from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
import os
import logging

load_dotenv()


# Blueprint
queue_management = Blueprint("queue_management", __name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=os.getenv("REDIS_PORT"), db=0)



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

    if job_type is None or job_id is None:
        return jsonify({"error": "job_type and job_id are required"}), 400
    
    try:
        #Create a job object
        job = Job(type=job_type, job_id=job_id)

        r.lpush("jobs", job.to_json_string())


        logging.info(f"Job enqueued: {job.to_json_string()}")
        print(f"Job enqueued: {job.to_json_string()}")
        return jsonify({"message": "Job enqueued"}), 200


    except redis.exceptions.RedisError as e:
        return jsonify({"Redis error": str(e)}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

    job_strings = r.lrange("jobs", 0, -1) # Get all jobs from the queue 

    for job_string in job_strings:
        job = Job.from_json_string(job_string)
        if job.job_id == job_id:
            return job.to_json_string(), 200

    if job is None:
        return jsonify({"error": "Invalid job ID"}), 400

    return job.to_json_string(), 200


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(queue_management)
    app.run(port="5001", debug=True)