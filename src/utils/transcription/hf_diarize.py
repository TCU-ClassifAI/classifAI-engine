import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook
import pydub
import uuid

# instantiate the pipeline
from pyannote.audio import Pipeline


pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1", use_auth_token=True
)


pipeline.to(torch.device("cuda"))


def diarize_audio(audio_path: str, output_path: str) -> bytes:
    """
    Diarize an audio file using the Pyannote pipeline.

    Args:
      audio_path (str): Path to the audio file.
      output_path (str): Path to save the diarization output.

    Returns:
      bytes: The diarization output.

    """



    # confirm the audio file exists
    try:
        with open(audio_path, "rb") as f:
            pass
    except FileNotFoundError:
        raise FileNotFoundError(f"File {audio_path} not found.")



    # Torchaudio does not support m4a files, so convert them to wav

    # If audio path is not mp3 or wav, convert it to wav

    # get ending of the audio file
    audio_ending = audio_path.split(".")[-1]

    # if the audio file is not mp3 or wav, convert it to wav
    if audio_ending not in ["mp3", "wav"]:
        audio = pydub.AudioSegment.from_file(audio_path)
        audio_base_path = audio_path.split(".")[0]
        audio_path = f"{audio_base_path}.wav"
        audio.export(audio_path, format="wav")

    waveform, sample_rate = torchaudio.load(audio_path)

    with ProgressHook() as hook:
        diarization = pipeline(
            {"waveform": waveform, "sample_rate": sample_rate}, hook=hook
        )

    # dump the diarization output to disk using RTTM format
    with open(output_path, "w") as rttm:
        diarization.write_rttm(rttm)

    with open(output_path, "rb") as f:
        return f.read()


# Test
if __name__ == "__main__":
    print(diarize_audio("D601 Day 1 Audio Only.wav", "audio.rttm"))
