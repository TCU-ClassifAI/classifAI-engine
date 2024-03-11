import whisper
from dotenv import load_dotenv
import os
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import torch
import torchaudio

from download_utils import download_and_convert_to_mp3
from word_timestamp_utils import words_per_segment


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

    audio_path = download_and_convert_to_mp3(url)
    
    # Larger whisper models require a GPU to run
    if not torch.cuda.is_available():
        model_id = "tiny"

    model = whisper.load_model(model_id) # By default, large-v3 model is used

    transcript = model.transcribe(audio_path, word_timestamps=True)
    print(transcript)

    


    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HF_TOKEN")
    )

    # Load audio file into memory to speed up the diarization process
    waveform, sample_rate = torchaudio.load(audio_path)

    # GREATLY increases the speed of the diarization process by using GPU. 
    if torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))

    with ProgressHook() as hook:
        diarization_result = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)

    print(f"Diarization result: {diarization_result}")

    final_result = words_per_segment(transcript, diarization_result)

    print("Final result:")
    print("Start\tEnd\tSpeaker\tText")

    print(final_result)

    del waveform
    del sample_rate

    return final_result


if __name__ == "__main__": # Testing: do not use in prod.
    transcribe_and_diarize("court_audio.mp3")