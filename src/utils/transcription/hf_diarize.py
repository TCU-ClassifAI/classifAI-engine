import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook

# instantiate the pipeline
from pyannote.audio import Pipeline



pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.1",
  use_auth_token=True)



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

  waveform, sample_rate = torchaudio.load(audio_path)

  with ProgressHook() as hook:
    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)


  # dump the diarization output to disk using RTTM format
  with open(output_path, "w") as rttm:
      diarization.write_rttm(rttm)

  with open(output_path, "rb") as f:
    return f.read()

# Test
if __name__ == "__main__":
  print(diarize_audio("D601 Day 1 Audio Only.wav", "audio.rttm"))


  

