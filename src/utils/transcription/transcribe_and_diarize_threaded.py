import whisper
from dotenv import load_dotenv
import os
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import torch
import torchaudio
import threading
import time
import logging

from download_utils import download_and_convert_to_mp3
from word_timestamp_utils import words_per_segment

progress_status = {
    "state": "idle",
    "message": ""
}

progress_lock = threading.Lock()

def update_progress(state: str, message: str):
    """Update the progress status with the given state and message.

    Args:
        state (str): The state of the progress
        message (str): The message to display
    """
    progress_lock.acquire()
    progress_status["state"] = state
    progress_status["message"] = message
    progress_lock.release()


def transcribe_and_diarize(audio_path: str, model_id: str = "large-v3") -> dict:
    """Transcribe and diarize a given audio file using the whisper library and pyannote library.

    Args:
        audio_path (str): The path to the audio file
        model_id (str): The model id to use for transcription (default: "openai/whisper-large-v3")

    Returns:
        dict: A dictionary containing the transcribed and diarized result
    """
        
    load_dotenv()
    url = "https://www.youtube.com/watch?v=UVzLd304keA"
    update_progress("downloading", "Downloading and converting to mp3")
    
    try:
        audio_path = download_and_convert_to_mp3(url)

        # make sure model_id is a valid model
        if model_id not in whisper.available_models():
            model_id = "large-v3"  # Default to large-v3 if invalid model id is provided
        
        # Larger whisper models require a GPU to run
        if not torch.cuda.is_available():
            model_id = "tiny"

        update_progress("load-model", f"Loading model: {model_id}")

        model = whisper.load_model(model_id) # By default, large-v3 model is used
        update_progress("transcribing", "Transcribing audio")

        transcript = model.transcribe(audio_path, word_timestamps=True)
        
        logging.info(transcript)
        update_progress("load-diarization", "Loading diarization pipeline")

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HF_TOKEN")
        )

        # Load audio file into memory to speed up the diarization process
        waveform, sample_rate = torchaudio.load(audio_path)

        # GREATLY increases the speed of the diarization process by using GPU. 
        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))

        update_progress("diarizing", "Diarizing audio")

        with ProgressHook() as hook:
            diarization_result = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)

        logging.info(f"Diarization result: {diarization_result}")

        update_progress("finalizing", "Finalizing result")

        final_result = words_per_segment(transcript, diarization_result)


        logging.info(final_result)

        update_progress("complete", final_result)

        del waveform
        del sample_rate
    except Exception as e:
        update_progress("error", f"An error occurred: {str(e)}")
        final_result = None

    return final_result


def check_progress():
    """Returns the current progress status"""
    progress_lock.acquire()
    status_copy = progress_status.copy()  # Avoid issues if the status changes mid-check
    progress_lock.release()
    return status_copy

if __name__ == "__main__": # Testing: do not use in prod.
    transcribe_and_diarize("court_audio.mp3")