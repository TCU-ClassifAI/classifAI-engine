import argparse
import os

from utils.transcription.helpers import (
    wav2vec2_langs,
    filter_missing_timestamps,
    get_words_speaker_mapping,
    punct_model_langs,
    get_realigned_ws_mapping_with_punctuation,
    get_sentences_speaker_mapping,
    cleanup,
)


import whisperx
import torch
from deepmultilingualpunctuation import PunctuationModel
import re
import subprocess
import logging
from rq import get_current_job
from utils.jobs import Job
from utils.transcription.transcription_helpers import transcribe, transcribe_batched


def update_progress(progress, message):
    """Update the progress of the current job"""
    job = get_current_job()
    job.meta["progress"] = progress
    job.meta["message"] = message
    job.save_meta()


def transcribe_and_diarize(job: Job) -> list:
    """
    Transcribe and diarize an audio file.

    Args:
        job (Job): Job object containing the audio file and job information.

    Returns:
        result (list): Result of the transcription and diarization job. Speaker labels and timestamps.
    """

    logging.info("Transcribing and diarizing: ", job.job_info.get("audio_path"))
    print(f"Transcribing and diarizing: {job.job_info.get('audio_path')}")

    try:
        mtypes = {"cpu": "int8", "cuda": "float16"}

        args = argparse.Namespace()

        # add the job info to the args
        args.audio = job.job_info.get("audio_path", None)
        args.language = job.job_info.get("language", None)
        args.device = job.job_info.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )
        args.model_name = job.job_info.get("model_name", "large-v3")
        args.stemming = job.job_info.get("stemming", True)
        args.batch_size = job.job_info.get("batch_size", 6)
        args.suppress_numerals = job.job_info.get("suppress_numerals", False)

        print(args.audio)

        update_progress(
            "splitting",
            "Splitting audio into vocals and accompaniment for faster processing",
        )

        if args.stemming:
            # Isolate vocals from the rest of the audio

            return_code = os.system(
                f'python3 -m demucs.separate -n htdemucs --two-stems=vocals "{args.audio}" -o "temp_outputs"'
            )

            if return_code != 0:
                logging.warning(
                    "Source splitting failed, using original audio file. Use --no-stem argument to disable it."
                )
                vocal_target = args.audio
            else:
                vocal_target = os.path.join(
                    "temp_outputs",
                    "htdemucs",
                    os.path.splitext(os.path.basename(args.audio))[0],
                    "vocals.wav",
                )
        else:
            vocal_target = args.audio

        print("Vocal target: ", vocal_target)

        update_progress("loading-nemo", "Loading Nemo process")
        logging.info("Starting Nemo process with vocal_target: ", vocal_target)
        nemo_process = subprocess.Popen(
            [
                "python3",
                "src/utils/transcription/nemo_process.py",
                "-a",
                vocal_target,
                "--device",
                args.device,
            ],
        )
        # Transcribe the audio file

        update_progress("transcribing", "Transcribing audio")
        logging.info("Transcribing audio file: ", vocal_target)
        print("Transcribing audio file: ", vocal_target)

        if args.batch_size != 0:
            print("Batch size: ", args.batch_size)
            whisper_results, language = transcribe_batched(
                vocal_target,
                args.language,
                args.batch_size,
                args.model_name,
                mtypes[args.device],
                args.suppress_numerals,
                args.device,
            )
        else:
            whisper_results, language = transcribe(
                vocal_target,
                args.language,
                args.model_name,
                mtypes[args.device],
                args.suppress_numerals,
                args.device,
            )

        print("Aligning audio file: ", vocal_target)

        if language in wav2vec2_langs:
            update_progress("loading-align-model", "Loading alignment model")
            alignment_model, metadata = whisperx.load_align_model(
                language_code=language, device=args.device
            )
            update_progress("aligning", "Aligning audio")
            result_aligned = whisperx.align(
                whisper_results, alignment_model, metadata, vocal_target, args.device
            )
            word_timestamps = filter_missing_timestamps(
                result_aligned["word_segments"],
                initial_timestamp=whisper_results[0].get("start"),
                final_timestamp=whisper_results[-1].get("end"),
            )
            # clear gpu vram
            del alignment_model
            torch.cuda.empty_cache()
        else:
            assert (
                args.batch_size
                == 0  # TODO: add a better check for word timestamps existence
            ), (
                f"Unsupported language: {language}, use --batch_size to 0"
                " to generate word timestamps using whisper directly and fix this error."
            )
            word_timestamps = []
            # A SingleSegment consists of start, end, text (str), avg_logprob (float)
            for segment in whisper_results:
                for word in segment["words"]:
                    word_timestamps.append(
                        {"word": word[2], "start": word[0], "end": word[1]}
                    )

        # Reading timestamps <> Speaker Labels mapping
        nemo_process.communicate()
        ROOT = os.getcwd()
        temp_path = os.path.join(ROOT, "temp_outputs")

        speaker_ts = []
        with open(os.path.join(temp_path, "pred_rttms", "mono_file.rttm"), "r") as f:
            lines = f.readlines()
            for line in lines:
                line_list = line.split(" ")
                s = int(float(line_list[5]) * 1000)
                e = s + int(float(line_list[8]) * 1000)
                speaker_ts.append([s, e, int(line_list[11].split("_")[-1])])

        wsm = get_words_speaker_mapping(word_timestamps, speaker_ts, "start")

        if language in punct_model_langs:
            # restoring punctuation in the transcript to help realign the
            # sentences
            punct_model = PunctuationModel(model="kredor/punctuate-all")

            words_list = list(map(lambda x: x["word"], wsm))

            labled_words = punct_model.predict(words_list)

            ending_puncts = ".?!"
            model_puncts = ".,;:!?"

            # Check if the word is an acronym

            def is_acronym(x: str) -> bool:
                """
                Check if the word is an acronym.

                Args:
                    x (str): Word to check.

                Returns:
                    bool: True if the word is an acronym, False otherwise.
                """
                return re.fullmatch(r"\b(?:[a-zA-Z]\.){2,}", x)

            for word_dict, labeled_tuple in zip(wsm, labled_words):
                word = word_dict["word"]
                if (
                    word
                    and labeled_tuple[1] in ending_puncts
                    and (word[-1] not in model_puncts or is_acronym(word))
                ):
                    word += labeled_tuple[1]
                    if word.endswith(".."):
                        word = word.rstrip(".")
                    word_dict["word"] = word

        else:
            logging.warning(
                f"Punctuation restoration is not available for {language} language. Using the original punctuation."
            )

        wsm = get_realigned_ws_mapping_with_punctuation(wsm)
        ssm = get_sentences_speaker_mapping(wsm, speaker_ts)

        # with open(f"{os.path.splitext(args.audio)[0]}.txt", "w", encoding="utf-8-sig") as f:
        #     get_speaker_aware_transcript(ssm, f)

        # with open(f"{os.path.splitext(args.audio)[0]}.srt", "w", encoding="utf-8-sig") as srt:
        #     write_srt(ssm, srt)

        cleanup(temp_path)

        update_progress("finished", "Transcription and diarization finished")
        print("Transcription and diarization finished")
        print(ssm)

        return ssm
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

        update_progress("error", f"An error occurred: {str(e)}")
        raise e
