from rq import get_current_job
from utils.queueing.jobs import Job
from utils.transcription.download_utils import download_and_convert_to_mp3
from typing import List
from utils.categorize.extract_questions import Question
from collections import OrderedDict
from pytube.exceptions import AgeRestrictedError, VideoRegionBlocked, VideoUnavailable
from config import config
from utils.queueing.update_rq import update_job_status
import os


def handle_yt_exception(job: Job, message: str, exception: Exception):
    """Handle YouTube exceptions"""
    job.status = "error"
    job.result = f"Error: {message}"
    update_job_status("error", message)
    raise Exception(message)


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

    # URL handling

    if job_info.get("url"):
        update_job_status("downloading", "Downloading YouTube and converting to mp3")

        try:
            # if we are in the src folder, we need to go up one level
            if os.path.basename(os.getcwd()) == "src":
                os.chdir("..")

            audio_path, title, date = download_and_convert_to_mp3(
                url=job_info["url"],
                output_path=config.UPLOAD_FOLDER,
                filename=job.job_id,
            )

        except AgeRestrictedError as e:
            handle_yt_exception(job, "Age-restricted video", e)
        except VideoRegionBlocked as e:
            handle_yt_exception(job, "Video region blocked", e)
        except VideoUnavailable as e:
            handle_yt_exception(job, "Video unavailable", e)
        except Exception as e:
            handle_yt_exception(
                job, f"Error downloading and converting to mp3: {str(e)}", e
            )

        job_info["audio_path"] = audio_path
        job_info["title"] = title
        job_info["date"] = date

        rq_job = get_current_job()
        if rq_job:
            rq_job.meta["title"] = title
        update_job_status("start_transcribing", "Starting transcription")

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
