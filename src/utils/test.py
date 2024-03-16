from whisperplus import ASRDiarizationPipeline
import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook
import numpy as np


# start timer:
import time

start = time.time()


audio_path = "output/court_audio.mp3"

device = "cuda"  # cpu or mps
pipeline = ASRDiarizationPipeline.from_pretrained(
    asr_model="openai/whisper-large-v3",
    diarizer_model="pyannote/speaker-diarization-3.1",
    use_auth_token=False,
    chunk_length_s=30,
    device=device,
)


waveform, sample_rate = torchaudio.load(audio_path)

# Downmix audio to mono if it is multi-channel
if waveform.shape[0] > 1:
    waveform = torch.mean(waveform, dim=0, keepdim=True)

# Convert the Tensor to a NumPy array of type float32
waveform_np = waveform.numpy().astype(np.float32)

# Optionally handle stride if needed (for CTC models)
# stride = {"left": int, "right": int}

with ProgressHook() as hook:
    output_text = pipeline(
        {"raw": waveform_np.squeeze(), "sampling_rate": sample_rate}, hook=hook
    )

# end timer:
end = time.time()
print(end - start)

print(output_text)
