from rq import get_current_job
from utils.queueing.jobs import Job
from utils.transcription.transcribe_full import transcribe_and_diarize
from utils.transcription.download_utils import download_and_convert_to_mp3
from utils.analyze.analyze_audio import analyze_audio
import traceback
import logging


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
    logging.info(f"Processing job: {job_queue.id}")

    # unpickle the job
    job: Job = Job.unpickle(job_pickle)

    job_queue.meta["job_type"] = job.type
    job_queue.meta["job_id"] = job.job_id
    job_queue.meta["progress"] = "assigning_worker"
    job_queue.meta["message"] = "Job assigned to worker"
    # try to get job info
    try:
        job_info = job.job_info
    except Exception:
        job.status = "error"
        job.result = f"Error: {traceback.format_exc()}"
        job_queue.meta["status"] = "error"
        job_queue.meta["message"] = job.result
        job_queue.save_meta()
        raise Exception(f"Error: {traceback.format_exc()}")

    # if job info has title or data, save it to the job
    if "title" in job_info:
        job_queue.meta["title"] = job_info["title"]
    if "data" in job_info:
        job_queue.meta["data"] = job_info["data"]

    job_queue.save_meta()

    try:
        if job.type == "transcription":
            # Perform the transcription
            if job_info.get("url"):
                rq_job = get_current_job()
                rq_job.meta["progress"] = "downloading"
                rq_job.meta["message"] = "Downloading YouTube and converting to mp3"
                rq_job.save_meta()

                audio_path, title, date = download_and_convert_to_mp3(
                    job_info["url"], "raw_audio", job.job_id
                )
                job_info["audio_path"] = audio_path
                job_info["title"] = title
                job_info["date"] = date

                rq_job.meta["progress"] = "transcribing"
                rq_job.meta["message"] = "Transcribing audio"
                rq_job.save_meta()

                job.job_info = job_info
            result = transcribe_and_diarize(job)
            return result

        if job.type == "summarization":
            # result = summarize_transcript(job)
            # return result
            pass

        if job.type == "categorization":
            # result = categorize_transcript(job)
            # return result
            pass
        if job.type == "analyze":
            result = analyze_audio(job)
            return result

    except Exception:
        job.status = "error"
        job.result = f"Error: {traceback.format_exc()}"
        job_queue.meta["status"] = "error"
        job_queue.meta["message"] = job.result
        job_queue.save_meta()
        raise Exception(f"Error: {traceback.format_exc()}")
