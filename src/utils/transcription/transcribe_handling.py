from download_utils import download_and_convert_to_mp3
from transcribe_and_diarize_threaded import transcribe_and_diarize


def youtube_transcribe_and_diarize(url: str, model_id: str = "large-v3"):
    """Transcribe and diarize a given YouTube video using the whisper library and pyannote library."""
    try:
        audio_path = download_and_convert_to_mp3(url)
        result = transcribe_and_diarize(audio_path, model_id)
        return result
    except Exception as e:
        return {"error": str(e)}


# I'm pretty sure this is unused code.
