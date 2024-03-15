
from rq import get_current_job
import json
import time
from utils.jobs import Job
from utils.transcription.transcribe_and_diarize_threaded import transcribe_and_diarize
import traceback
import logging




# queue_names = ('queued_jobs', 'in_progress_jobs', 'finished_jobs')

# queues = [Queue(queue_name, connection=r) for queue_name in queue_names]

# def update_job_in_queue(job: Job, queue: Queue):
#     """
#     Update the job in the queue.

#     Args:
#         job (Job): The job to update.
#         queue (Queue): The queue in which the job is located.

#     Returns:
#         None
#     """

#     job_pickle = job.pickle()
#     job_id = job.job_id

#     # See all jobs in the queue
#     job_strings = queue.job_ids


def process_job(job_pickle: str):
    """
    Process a job from the queue.

    Args:
        job_pickle (str): The pickled job object.

    Returns:
        job_pickle (str): The pickled job object, updated with the result of the job.
    """

    job_queue = get_current_job()
    print(f"Current job: {job_queue.id}")

    # unpickle the job
    job = Job.unpickle(job_pickle)

    job_queue.meta["job_type"] = job.type
    job_queue.meta["job_id"] = job.job_id
    job_queue.meta["status"] = "in progress"
    job_queue.save_meta()

    try:
        if job.type == "transcription":
            # Perform the transcription
            result = transcribe_and_diarize(job)
            return result   
        if job.type == "summarization":
            # Perform the summarization
            pass

        if job.type == "categorization":
            # Perform the categorization
            pass

    except Exception as e:
        job.status = "error"
        job.result = f"Error: {traceback.format_exc()}"
        job_queue.meta["status"] = "error"
        job_queue.meta["message"] = job.result
        job_queue.save_meta()

    return job


# def process_job(job_pickle: str):
#     """
#     Process a job from the queue.

#     Args:
#         job_pickle (str): The pickled job object.

#     Returns:
#         job_pickle (str): The pickled job object, updated with the result of the job.
#     """

#     try:
#         source_queue  = queues[0]
#         in_progress_queue = queues[1]

#         job_string = source_queue.remove(job_pickle)
#         # unpickle, set status to in progress, pickle, and push to in progress queue
#         job = Job.unpickle(job_string)
#         job.status = "in progress"
#         job_pickle = job.pickle()
        
#         in_progress_queue.enqueue(job_id=job.job_id, job_pickle=job_pickle)
#     except Exception as e:
#         print(f"Error moving job from source queue to in progress queue: {e}")
#         logging.error(f"Error moving job from source queue to in progress queue: {e}")

    
#     print(f"Processing job: {job_string}")
#     logging.info(f"Processing job: {job_string}")

#     # Convert the job string to a Job object
#     job = Job.unpickle(job_string)

#     print(f"Current job processing: {job.to_json_string()}")

#     try:
        
#         update_progress(job)  # Update job status in queue

#         if job.type == "transcription":
#             # Perform the transcription
#             print(f"Transcribing job: {job_string}")
#             result = transcribe_and_diarize(job, r) # should be blocking
#             job.status = "completed"
#             job.result = result
#             update_progress(job)

#         if job.type == "summarization":
#             # Perform the summarization
#             pass

#         if job.type == "categorization":
#             # Perform the categorization
#             pass

#     except Exception as e:
#         job.status = "error"
#         job.result = f"Error: {traceback.format_exc()}"
#         update_progress(job)

#     return job


# if __name__ == '__main__':
#     # Print all jobs in the queue
#     # job_strings = r.lrange("jobs", 0, -1)
#     # for job_string in job_strings:
#     #     print(job_string)

#     while True:
#         # Get the job from the queue
#         job_string = r.rpop("jobs")

#         if job_string:
#             # convert the job string to a Job object
#             job = Job.from_json_string(job_string)

#             print(f"Current job: {job_string}")

#             if job.status == "queued":
#                 # Process the job
#                 r.lpush("in_progress_jobs", job_string)

#                 print(f"Processing job: {job_string}")

#                 finished_job = process_job(job_string)

#                 # Remove an in progress job from the queue if it is there
#                 in_progress_jobs = r.lrange("in_progress_jobs", 0, -1)
#                 for in_progress_job_string in in_progress_jobs:
#                     in_progress_job = Job.from_json_string(in_progress_job_string)
#                     if in_progress_job.job_id == job.job_id:
#                         r.lrem("in_progress_jobs", 0, in_progress_job_string)

#                 # Add the finished job to the finished jobs queue

#                 r.lpush("finished_jobs", finished_job.to_json_string())

#             else: # if the job is not queued, send it to the back of the queue
#                 print(f"Job {job.job_id} is not queued. Sending it to the back of the queue.")
#                 r.lpush("jobs", job_string)

#         time.sleep(5)


