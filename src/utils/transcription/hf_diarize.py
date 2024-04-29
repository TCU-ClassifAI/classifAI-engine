import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook
import pydub
import uuid
import logging

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

        
    # Update the speaker names in the RTTM file
    update_speaker_names_rttm(output_path)

    return output_path
    


def update_speaker_names_rttm(rttm_path):
    """Update the speaker names in an RTTM file, so that 'SPEAKER_00' is the person speaking the most, 'SPEAKER_01' is the second most, etc.

    Args:
        rttm_path (str): Path to the RTTM file.

    Returns:
        str: The original RTTM file path (overwritten with updated speaker names)
    """

    # read the RTTM file
    with open(rttm_path, "r") as f:
        rttm_lines = f.readlines()



    # Example of RTTM line: 
    # Type File Channel Start Duration <NA> <NA> Speaker_Name Confidence <NA>
    # SPEAKER waveform 1 295.390 0.543 <NA> <NA> SPEAKER_00 <NA> <NA>

    # Get the speaker names
    speaker_names = []
    for line in rttm_lines:
        speaker_name = line.split(" ")[7]
        if speaker_name not in speaker_names:
            speaker_names.append(speaker_name)

    # Get the total duration of each speaker
    speaker_durations = {}
    for speaker_name in speaker_names:
        speaker_durations[speaker_name] = 0

    for line in rttm_lines:
        speaker_name = line.split(" ")[7]
        duration = float(line.split(" ")[4])
        speaker_durations[speaker_name] += duration

    # Sort the speakers by duration
    sorted_speakers = sorted(speaker_durations, key=speaker_durations.get, reverse=True)

    # Update the speaker names, overwrite the original RTTM file


    with open(rttm_path, "w") as f:
        for line in rttm_lines:
            speaker_name = line.split(" ")[7]
            speaker_index = sorted_speakers.index(speaker_name)
            updated_speaker_name = f"SPEAKER_{str(speaker_index).zfill(2)}"
            updated_line = line.replace(speaker_name, updated_speaker_name)
            f.write(updated_line)

    logging.info(f"Updated RTTM file saved to {rttm_path}")

    return rttm_path

        





# Test
if __name__ == "__main__":
    print(diarize_audio("D601 Day 1 Audio Only.wav", "audio.rttm"))
    update_speaker_names_rttm("audio.rttm")



