from rq import get_current_job
from utils.jobs import Job
from utils.transcription.download_utils import download_and_convert_to_mp3
from typing import List
from utils.categorize.extract_questions import Question
from collections import OrderedDict


def get_audio_path_from_url_or_file(job: Job):
    """
    Get the audio path from either a URL or a file.

    Args:
        job (Job): Job object containing the audio file URL or file.

    Returns:
        job (Job): Job object with the audio path added.
        Also adds the title and date of the audio file, if YouTube URL

    Raises:
        Exception: If there is an error downloading the audio file.
    """
    job_info = job.job_info

    print(job_info)

    if job_info.get("url"):
        rq_job = get_current_job()
        rq_job.meta["progress"] = "downloading"
        rq_job.meta["message"] = "Downloading YouTube and converting to mp3"
        rq_job.save_meta()

        try:
            audio_path, title, date = download_and_convert_to_mp3(
                job_info["url"], "raw_audio", job.job_id
            )
        except Exception as e:
            job.status = "error"
            job.result = f"Error: {str(e)}"
            rq_job.meta["status"] = "error"
            rq_job.meta["message"] = job.result
            rq_job.save_meta()
            raise Exception(str(e))

        job_info["audio_path"] = audio_path
        job_info["title"] = title
        job_info["date"] = date

        rq_job.meta["progress"] = "transcribing"
        rq_job.meta["message"] = "Transcribing audio"
        rq_job.meta["title"] = title
        rq_job.save_meta()

        job.job_info = job_info

    return job


def get_raw_transcript(transcript: list) -> str:
    """
    Get the raw transcript from the transcription results.

    Args:
        transcript (list): List of transcription results.

    Returns:
        str: Raw transcript
    """
    return " ".join([line["text"] for line in transcript])


def combine_results(
    transcript: list, categories: List[Question], summary: str
) -> OrderedDict:
    """
    Combine the transcription, summary, and categories into a single result.

    Args:
        transcript (list): List of transcription results.
        summary (str): Summary of the transcription.
        categories (list): List of Question objects.

    Returns:
        dict: Combined results
    """
    result = OrderedDict()
    result["transcript"] = transcript
    result["questions"] = [category.to_dict() for category in categories]
    result["summary"] = summary

    return result
