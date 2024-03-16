
from rq import get_current_job
from utils.jobs import Job
from utils.transcription.diarize_parallel import transcribe_and_diarize
import traceback


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

    except Exception:
        job.status = "error"
        job.result = f"Error: {traceback.format_exc()}"
        job_queue.meta["status"] = "error"
        job_queue.meta["message"] = job.result
        job_queue.save_meta()

    return job

