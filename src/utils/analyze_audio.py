from flask import Response
from utils.jobs import Job
import logging
from rq import get_current_job
from flask import make_response
from utils.analyze.extraction_utils import (
    get_audio_path_from_url_or_file,
    get_raw_transcript,
    combine_results,
)
from utils.analyze.update_rq import update_job_status
from utils.transcription.diarize_parallel import transcribe_and_diarize
from utils.categorize.extract_questions import extract_questions
from utils.categorize.categorize_transcript import categorize_list_of_questions
from utils.summarize.summarize_transcript import summarize_transcript


def analyze_audio(job: Job) -> dict:
    """
    Analyze an audio file by transcribing, categorizing, and summarizing it.

    Args:
        audio_path (str): Path to the audio file.
        url (str): URL to the audio file.
        model_name (str): Model name for transcription. Defaults to "large-v3".

    Returns:
        result (dict): Result
    """

    try:
        # 1. Extract the file audio path. If it's URL, download and convert to mp3.
        job = get_audio_path_from_url_or_file(job)
    except Exception as e:
        return "Error: Unable to download and convert the audio file: " + str(e)

    # 2. Transcribe the audio file.
    update_job_status("start_transcribing", "Transcribing audio")
    transcription = transcribe_and_diarize(job)

    # 3. Extract the transcription questions from the transcription.
    update_job_status("extracting_questions", "Extracting questions from transcription")
    questions_with_context = extract_questions(transcription)

    # 4. Categorize the transcription questions by Costa's level.
    update_job_status("categorizing_questions", "Categorizing questions")
    categorized_questions = categorize_list_of_questions(questions_with_context)

    # 5. Summarize the transcription.
    update_job_status("summarizing", "Summarizing transcription")
    raw_transcript = get_raw_transcript(transcription)
    summary = summarize_transcript(raw_transcript)

    # 5. Combine the results into a single dictionary.
    update_job_status("combining_results", "Combining results")
    combined_result = combine_results(transcription, categorized_questions, summary)

    update_job_status("completed", "Analysis completed")

    # 6. Return the result.
    return combined_result
