import whisper_timestamped as whisper

# from celery import Celery, Task
# from settings.development import MODEL


# @app.task
def transcribe(path: str) -> str:
    """Transcription of audio file using Whisper.
     Use Celery to run in background.

    Args:
        path (str): Path to audio file.
        language (str): Language of audio file.
        user_id (int): ID of user who uploaded audio file.
        job_id (int): ID of job.
    Returns:
        str: Path to transcription file (in JSON format).
        - Full specifications of JSON format can be found
        in docs/transcription.md
    """

    model = whisper.load_model("tiny.en")
    audio = whisper.load_audio(path)
    print(whisper.transcribe_timestamped(model, audio))
