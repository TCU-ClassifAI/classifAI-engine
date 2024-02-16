import os
import wget
from omegaconf import OmegaConf
import json
import shutil
import whisperx
import torch
from pydub import AudioSegment
from nemo.collections.asr.models.msdd_models import NeuralDiarizer
from deepmultilingualpunctuation import PunctuationModel
import re
import logging
import nltk
from whisperx.alignment import DEFAULT_ALIGN_MODELS_HF, DEFAULT_ALIGN_MODELS_TORCH
from whisperx.utils import LANGUAGES, TO_LANGUAGE_CODE

import unidecode
from unidecode import unidecode
from pathlib import Path

from flask import Flask, request, jsonify, Blueprint, make_response
import threading
from typing import TextIO
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TranscriptionJob:
    """
    Dataclass to store information about a transcription job.

    Attributes:
        job_id: Unique ID of the transcription job.
        user_id: ID of the user who started the transcription job (default: None).
        model_type: Name of the model used for transcription (default: "large-v3").
        status: Status of the transcription job (default: "in progress").
        state: State of the transcription job (default: "transcribing").
        start_time: Start time of the transcription job (datetime) (default: current time).
        end_time: End time of the transcription job (default: None).
        duration: Duration of the transcription job in milliseconds (default: 0).
        result: List of transcription segments (default: None).
        error_message: Error message of the transcription job (default: None).
    """

    job_id: str
    user_id: str = None
    model_type: str = "large-v3"
    status: str = "in progress"  # "in progress", "completed", "failed"
    progress: str = "transcribing"  # "transcribing", "diarizing", "punctuating", "completed", "failed
    start_time: datetime = datetime.now()
    end_time: datetime = None
    duration: float = 0  # in milliseconds
    result: list = None
    error_message: str = None

    def to_json_string(self) -> str:
        """
        Convert the dataclass to a JSON string. Remove any fields with None values.

        Args:
            None (self)
        Returns:
            str: JSON string representation of the dataclass.
        """

        # Helper function to format the datetime
        def format_datetime(datetime_obj) -> str:
            return (
                datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                if datetime_obj
                else None
            )

        # Get current duration if the job is still in progress
        if self.status == "in progress":
            self.duration = self.get_duration()

        data_dict = asdict(self)

        # Ensure result is formatted correctly
        if self.result is not None:
            data_dict["result"] = [asdict(segment) for segment in self.result]

        filtered_dict = {
            key: value for key, value in data_dict.items() if value is not None
        }

        if filtered_dict.get("start_time") is not None:
            filtered_dict["start_time"] = format_datetime(filtered_dict["start_time"])

        if filtered_dict.get("end_time") is not None:
            filtered_dict["end_time"] = format_datetime(filtered_dict["end_time"])

        return json.dumps(filtered_dict, default=str)

    def get_duration(self) -> int:
        """
        Get the duration of the transcription job.

        Args:
            None (self) (accesses the start_time and end_time datetime attributes of the dataclass)
        Returns:
            int: Duration of the transcription job in milliseconds.
        """
        if self.start_time is not None and self.end_time is not None:
            return int((self.end_time - self.start_time).total_seconds() * 1000)
        if self.start_time is not None:
            return int((datetime.now() - self.start_time).total_seconds() * 1000)
        return 0


@dataclass
class TranscriptionSegment:
    """
    Dataclass to store information about a transcription segment.

    Attributes:
        List of:
            speaker: Speaker label
            start_time: Start time of the segment (0 is the start of the audio file)
            end_time: End time of the segment
            text: Transcribed text of the segment
            confidence: Confidence of the transcription of the segment
    """

    speaker: str
    start_time: float
    end_time: float
    text: str


transcription = Blueprint("transcription", __name__)

# We could possibly use a database to store the job status and create the method get_job_status_from_db(job_id) to retrieve the job status from the database
job_status = {}


@transcription.route("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint.

    Returns:
        str: "OK" if the server is running.
    """
    return make_response("OK", 200)


@transcription.route("/start_transcription", methods=["POST"])
def start_transcription():
    """
    Start the transcription process for an audio file by creating a new thread to run the process.

    Args:
        audio_file: audio file to transcribe.
        model_name: name of the model to use for transcription (default: large-v3)

    Returns:
        Response object with the status code.
    """
    print("Starting transcription")

    audio_file = request.files.get("file")

    # Check if the file is present
    if audio_file is None:
        print(request.files)  # This should not be empty if the file is sent correctly
        return jsonify({"error": "No file part"}), 400

    print("File retrieved")

    # Input validation
    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    print(f"File name: {audio_file.filename}")

    # Get model name from the request
    model_name = request.form.get("model_name", "large-v3")
    if model_name not in [
        "tiny.en",
        "tiny",
        "base.en",
        "base",
        "small.en",
        "small",
        "medium.en",
        "medium",
        "large-v1",
        "large-v2",
        "large-v3",
        "large",
    ]:
        return jsonify({"error": "Invalid model name"}), 400

    # Check if the file is a valid audio file and if not, return an error
    if audio_file and audio_file.filename.split(".")[-1] not in [
        "wav",
        "mp3",
        "ogg",
        "flac",
    ]:
        return jsonify({"error": "Invalid file type"}), 400

    print(f"Starting transcription for audio file with model {model_name}")

    if audio_file:
        file_extension = audio_file.filename.split(".")[-1]
        uuid_audio_file = uuid.uuid4().hex
        secure_filename = f"{uuid_audio_file}.{file_extension}"

        # Make "tmp" directory in the current directory if it doesn't exist
        tmp_dir = os.path.join(os.getcwd(), "tmp")
        os.makedirs(tmp_dir, exist_ok=True)

        # change directory to tmp (required because of audio_file.save() function) (its weird)
        os.chdir(tmp_dir)

        # Save the audio file to the temporary path
        audio_file.save(secure_filename)

        # change directory back to the original directory
        os.chdir("..")

        audio_file_path = os.path.join(tmp_dir, secure_filename)

        print("File saved to temporary location")
        print(f"File path: {audio_file_path}")

        # Create job in job_status
        job_status[uuid_audio_file] = TranscriptionJob(
            uuid_audio_file, model_type=model_name
        )

        # Start the transcription process in a new thread
        thread = threading.Thread(
            target=transcribe_and_generate_files,
            args=(audio_file_path, model_name, uuid_audio_file),
        )
        thread.start()

        return jsonify(
            {"message": "Transcription started", "job_id": uuid_audio_file}
        ), 200

    return jsonify({"error": "Invalid request"}), 400


@transcription.route("/get_transcription_status", methods=["GET"])
def get_transcription_status():
    """
    Get the status of a transcription job.

    Args:
        job_id: ID of the transcription job.

    Returns:
        Response object with the status code.
    """
    job_id = request.args.get("job_id")
    if job_id is None:
        return jsonify({"error": "No job ID provided"}), 400

    if job_id not in job_status:
        return make_response(jsonify({"error": "Invalid job ID"}), 400)

    return make_response(job_status[job_id].to_json_string(), 200)


def transcribe_and_generate_files(
    audio_path: str, model_name="large-v3", job_id=None
) -> TextIO:
    """
    Transcribe and diarize an audio file and update the status of the transcription job.

    Args:
        audio_path: Path to the audio file to transcribe (str) (required) (possible formats: wav, mp3, ogg, flac)
        model_name: Name of the model to use for transcription (default: large-v3).
        job_id: ID of the transcription job (default: None). Used to update the status of the transcription job.

    Returns:
        None
    """

    # List of languages supported by the punctuation model (https://huggingface.co/kredor/punctuate-all)
    punct_model_langs = [
        "en",
        "fr",
        "de",
        "es",
        "it",
        "nl",
        "pt",
        "bg",
        "pl",
        "cs",
        "sk",
        "sl",
    ]
    wav2vec2_langs = list(DEFAULT_ALIGN_MODELS_TORCH.keys()) + list(
        DEFAULT_ALIGN_MODELS_HF.keys()
    )

    whisper_langs = sorted(LANGUAGES.keys()) + sorted(
        [k.title() for k in TO_LANGUAGE_CODE.keys()]
    )

    def create_config(output_dir, DOMAIN_TYPE="telephonic"):
        # DOMAIN_TYPE: can be meeting, telephonic, or general based on domain type of the audio file
        CONFIG_FILE_NAME = f"diar_infer_{DOMAIN_TYPE}.yaml"
        CONFIG_URL = f"https://raw.githubusercontent.com/NVIDIA/NeMo/main/examples/speaker_tasks/diarization/conf/inference/{CONFIG_FILE_NAME}"
        MODEL_CONFIG = os.path.join(output_dir, CONFIG_FILE_NAME)
        if not os.path.exists(MODEL_CONFIG):
            MODEL_CONFIG = wget.download(CONFIG_URL, output_dir)

        config = OmegaConf.load(MODEL_CONFIG)

        data_dir = os.path.join(output_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        meta = {
            "audio_filepath": os.path.join(output_dir, "mono_file.wav"),
            "offset": 0,
            "duration": None,
            "label": "infer",
            "text": "-",
            "rttm_filepath": None,
            "uem_filepath": None,
        }
        with open(os.path.join(data_dir, "input_manifest.json"), "w") as fp:
            json.dump(meta, fp)
            fp.write("\n")

        pretrained_vad = "vad_multilingual_marblenet"
        pretrained_speaker_model = "titanet_large"
        config.num_workers = (
            0  # Workaround for multiprocessing hanging with ipython issue
        )
        config.diarizer.manifest_filepath = os.path.join(
            data_dir, "input_manifest.json"
        )
        config.diarizer.out_dir = (
            output_dir  # Directory to store intermediate files and prediction outputs
        )

        config.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
        config.diarizer.oracle_vad = (
            False  # compute VAD provided with model_path to vad config
        )
        config.diarizer.clustering.parameters.oracle_num_speakers = False

        # Here, we use our in-house pretrained NeMo VAD model
        config.diarizer.vad.model_path = pretrained_vad
        config.diarizer.vad.parameters.onset = 0.8
        config.diarizer.vad.parameters.offset = 0.6
        config.diarizer.vad.parameters.pad_offset = -0.05
        config.diarizer.msdd_model.model_path = (
            "diar_msdd_telephonic"  # Telephonic speaker diarization model
        )

        return config

    def get_word_ts_anchor(s, e, option="start"):
        if option == "end":
            return e
        elif option == "mid":
            return (s + e) / 2
        return s

    def get_words_speaker_mapping(wrd_ts, spk_ts, word_anchor_option="start"):
        s, e, sp = spk_ts[0]
        wrd_pos, turn_idx = 0, 0
        wrd_spk_mapping = []
        for wrd_dict in wrd_ts:
            ws, we, wrd = (
                int(wrd_dict["start"] * 1000),
                int(wrd_dict["end"] * 1000),
                wrd_dict["word"],
            )
            wrd_pos = get_word_ts_anchor(ws, we, word_anchor_option)
            while wrd_pos > float(e):
                turn_idx += 1
                turn_idx = min(turn_idx, len(spk_ts) - 1)
                s, e, sp = spk_ts[turn_idx]
                if turn_idx == len(spk_ts) - 1:
                    e = get_word_ts_anchor(ws, we, option="end")
            wrd_spk_mapping.append(
                {"word": wrd, "start_time": ws, "end_time": we, "speaker": sp}
            )
        return wrd_spk_mapping

    sentence_ending_punctuations = ".?!"

    def get_first_word_idx_of_sentence(word_idx, word_list, speaker_list, max_words):
        is_word_sentence_end = (
            lambda x: x >= 0 and word_list[x][-1] in sentence_ending_punctuations
        )
        left_idx = word_idx
        while (
            left_idx > 0
            and word_idx - left_idx < max_words
            and speaker_list[left_idx - 1] == speaker_list[left_idx]
            and not is_word_sentence_end(left_idx - 1)
        ):
            left_idx -= 1

        return left_idx if left_idx == 0 or is_word_sentence_end(left_idx - 1) else -1

    def get_last_word_idx_of_sentence(word_idx, word_list, max_words):
        is_word_sentence_end = (
            lambda x: x >= 0 and word_list[x][-1] in sentence_ending_punctuations
        )
        right_idx = word_idx
        while (
            right_idx < len(word_list)
            and right_idx - word_idx < max_words
            and not is_word_sentence_end(right_idx)
        ):
            right_idx += 1

        return (
            right_idx
            if right_idx == len(word_list) - 1 or is_word_sentence_end(right_idx)
            else -1
        )

    def get_realigned_ws_mapping_with_punctuation(
        word_speaker_mapping, max_words_in_sentence=50
    ):
        is_word_sentence_end = (
            lambda x: x >= 0
            and word_speaker_mapping[x]["word"][-1] in sentence_ending_punctuations
        )
        wsp_len = len(word_speaker_mapping)

        words_list, speaker_list = [], []
        for k, line_dict in enumerate(word_speaker_mapping):
            word, speaker = line_dict["word"], line_dict["speaker"]
            words_list.append(word)
            speaker_list.append(speaker)

        k = 0
        while k < len(word_speaker_mapping):
            line_dict = word_speaker_mapping[k]
            if (
                k < wsp_len - 1
                and speaker_list[k] != speaker_list[k + 1]
                and not is_word_sentence_end(k)
            ):
                left_idx = get_first_word_idx_of_sentence(
                    k, words_list, speaker_list, max_words_in_sentence
                )
                right_idx = (
                    get_last_word_idx_of_sentence(
                        k, words_list, max_words_in_sentence - k + left_idx - 1
                    )
                    if left_idx > -1
                    else -1
                )
                if min(left_idx, right_idx) == -1:
                    k += 1
                    continue

                spk_labels = speaker_list[left_idx : right_idx + 1]
                mod_speaker = max(set(spk_labels), key=spk_labels.count)
                if spk_labels.count(mod_speaker) < len(spk_labels) // 2:
                    k += 1
                    continue

                speaker_list[left_idx : right_idx + 1] = [mod_speaker] * (
                    right_idx - left_idx + 1
                )
                k = right_idx

            k += 1

        k, realigned_list = 0, []
        while k < len(word_speaker_mapping):
            line_dict = word_speaker_mapping[k].copy()
            line_dict["speaker"] = speaker_list[k]
            realigned_list.append(line_dict)
            k += 1

        return realigned_list

    def get_sentences_speaker_mapping(word_speaker_mapping, spk_ts):
        sentence_checker = (
            nltk.tokenize.PunktSentenceTokenizer().text_contains_sentbreak
        )
        s, e, spk = spk_ts[0]
        prev_spk = spk

        snts = []
        snt = {"speaker": f"Speaker {spk}", "start_time": s, "end_time": e, "text": ""}

        for wrd_dict in word_speaker_mapping:
            wrd, spk = wrd_dict["word"], wrd_dict["speaker"]
            s, e = wrd_dict["start_time"], wrd_dict["end_time"]
            if spk != prev_spk or sentence_checker(snt["text"] + " " + wrd):
                snts.append(snt)
                snt = {
                    "speaker": f"Speaker {spk}",
                    "start_time": s,
                    "end_time": e,
                    "text": "",
                }
            else:
                snt["end_time"] = e
            snt["text"] += wrd + " "
            prev_spk = spk

        snts.append(snt)
        return snts

    def get_speaker_aware_transcript(sentences_speaker_mapping, f):
        previous_speaker = sentences_speaker_mapping[0]["speaker"]
        f.write(f"{previous_speaker}: ")

        for sentence_dict in sentences_speaker_mapping:
            speaker = sentence_dict["speaker"]
            sentence = sentence_dict["text"]

            # If this speaker doesn't match the previous one, start a new paragraph
            if speaker != previous_speaker:
                f.write(f"\n\n{speaker}: ")
                previous_speaker = speaker

            # No matter what, write the current sentence
            f.write(sentence + " ")

    def format_timestamp(
        milliseconds: float,
        always_include_hours: bool = False,
        decimal_marker: str = ".",
    ):
        assert milliseconds >= 0, "non-negative timestamp expected"

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"

    def find_numeral_symbol_tokens(tokenizer):
        numeral_symbol_tokens = [
            -1,
        ]
        for token, token_id in tokenizer.get_vocab().items():
            has_numeral_symbol = any(c in "0123456789%$£" for c in token)
            if has_numeral_symbol:
                numeral_symbol_tokens.append(token_id)
        return numeral_symbol_tokens

    def _get_next_start_timestamp(word_timestamps, current_word_index):
        # if current word is the last word
        if current_word_index == len(word_timestamps) - 1:
            return word_timestamps[current_word_index]["start"]

        next_word_index = current_word_index + 1
        while current_word_index < len(word_timestamps) - 1:
            if word_timestamps[next_word_index].get("start") is None:
                # if next word doesn't have a start timestamp
                # merge it with the current word and delete it
                word_timestamps[current_word_index]["word"] += (
                    " " + word_timestamps[next_word_index]["word"]
                )

                word_timestamps[next_word_index]["word"] = None
                next_word_index += 1

            else:
                return word_timestamps[next_word_index]["start"]

    def filter_missing_timestamps(word_timestamps):
        # handle the first and last word
        if word_timestamps[0].get("start") is None:
            word_timestamps[0]["start"] = 0
            word_timestamps[0]["end"] = _get_next_start_timestamp(word_timestamps, 0)

        result = [
            word_timestamps[0],
        ]

        for i, ws in enumerate(word_timestamps[1:], start=1):
            # if ws doesn't have a start and end
            # use the previous end as start and next start as end
            if ws.get("start") is None and ws.get("word") is not None:
                ws["start"] = word_timestamps[i - 1]["end"]
                ws["end"] = _get_next_start_timestamp(word_timestamps, i)

            if ws["word"] is not None:
                result.append(ws)
        return result

    def cleanup(path: str):
        """path could either be relative or absolute."""
        # check if file or directory exists
        if os.path.isfile(path) or os.path.islink(path):
            # remove file
            os.remove(path)
        elif os.path.isdir(path):
            # remove directory and all its content
            shutil.rmtree(path)
        else:
            raise ValueError("Path {} is not a file or dir.".format(path))

    def process_language_arg(language: str, model_name: str):
        """
        Process the language argument to make sure it's valid and convert language names to language codes.
        """
        if language is not None:
            language = language.lower()
        if language not in LANGUAGES:
            if language in TO_LANGUAGE_CODE:
                language = TO_LANGUAGE_CODE[language]
            else:
                raise ValueError(f"Unsupported language: {language}")

        if model_name.endswith(".en") and language != "en":
            if language is not None:
                logging.warning(
                    f"{model_name} is an English-only model but received '{language}'; using English instead."
                )
            language = "en"
        return language

    def transcribe(
        audio_file: str,
        language: str,
        model_name: str,
        compute_dtype: str,
        suppress_numerals: bool,
        device: str,
    ):
        from faster_whisper import WhisperModel
        from helpers import find_numeral_symbol_tokens, wav2vec2_langs

        # Faster Whisper non-batched
        # Run on GPU with FP16
        whisper_model = WhisperModel(
            model_name, device=device, compute_type=compute_dtype
        )

        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        # model = WhisperModel(model_size, device="cpu", compute_type="int8")

        if suppress_numerals:
            numeral_symbol_tokens = find_numeral_symbol_tokens(
                whisper_model.hf_tokenizer
            )
        else:
            numeral_symbol_tokens = None

        if language is not None and language in wav2vec2_langs:
            word_timestamps = False
        else:
            word_timestamps = True

        segments, info = whisper_model.transcribe(
            audio_file,
            language=language,
            beam_size=5,
            word_timestamps=word_timestamps,  # TODO: disable this if the language is supported by wav2vec2
            suppress_tokens=numeral_symbol_tokens,
            vad_filter=True,
        )
        whisper_results = []
        for segment in segments:
            whisper_results.append(segment._asdict())
        # clear gpu vram
        del whisper_model
        torch.cuda.empty_cache()
        return whisper_results, language

    def transcribe_batched(
        audio_file: str,
        language: str,
        batch_size: int,
        model_name: str,
        compute_dtype: str,
        suppress_numerals: bool,
        device: str,
    ):
        import whisperx

        # Faster Whisper batched
        whisper_model = whisperx.load_model(
            model_name,
            device,
            compute_type=compute_dtype,
            asr_options={"suppress_numerals": suppress_numerals},
        )
        audio = whisperx.load_audio(audio_file)
        result = whisper_model.transcribe(
            audio, language=language, batch_size=batch_size
        )
        del whisper_model
        torch.cuda.empty_cache()
        return result["segments"], result["language"]

    # no space, punctuation, accent in lower string
    def cleanString(string):
        cleanString = unidecode(string)
        # cleanString = re.sub('\W+','_', cleanString)
        cleanString = re.sub(r"[^\w\s]", "", cleanString)
        cleanString = cleanString.replace(" ", "_")
        return cleanString.lower()

    # rename audio filename to get name without accent, no space, in lower case
    def rename_file(filepath):
        suffix = Path(filepath).suffix
        if str(Path(filepath).parent) != ".":
            new_filepath = (
                str(Path(filepath).parent)
                + cleanString(filepath.replace(suffix, ""))
                + suffix
            )
        else:
            new_filepath = cleanString(filepath.replace(suffix, "")) + suffix
        os.rename(filepath, new_filepath)
        return new_filepath

    # rename audio filename if necessary to get string without accent, space, in lower case
    audio_path = rename_file(audio_path)

    # (Option) Whether to enable music removal from speech, helps increase diarization quality but uses alot of ram
    enable_stemming = False

    whisper_model_name = model_name  # Set via the function argument

    # replaces numerical digits with their pronounciation, increases diarization accuracy
    suppress_numerals = True

    batch_size = 8

    language = None  # autodetect language

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if enable_stemming:
        # Isolate vocals from the rest of the audio

        return_code = os.system(
            f'python3 -m demucs.separate -n htdemucs --two-stems=vocals "{audio_path}" -o "temp_outputs"'
        )

        if return_code != 0:
            logging.warning("Source splitting failed, using original audio file.")
            vocal_target = audio_path
        else:
            vocal_target = os.path.join(
                "temp_outputs",
                "htdemucs",
                os.path.splitext(os.path.basename(audio_path))[0],
                "vocals.wav",
            )
    else:
        vocal_target = audio_path

    if device == "cuda":
        compute_type = "float16"
    # or run on GPU with INT8
    # compute_type = "int8_float16"
    # or run on CPU with INT8
    else:
        compute_type = "int8"

    if batch_size != 0:
        whisper_results, language = transcribe_batched(
            vocal_target,
            language,
            batch_size,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )
    else:
        whisper_results, language = transcribe(
            vocal_target,
            language,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )

    # Change job status to diarizing
    if job_id is not None:
        job_status[job_id].progress = "diarizing"

    if language in wav2vec2_langs:
        device = "cuda"
        alignment_model, metadata = whisperx.load_align_model(
            language_code=language, device=device
        )
        result_aligned = whisperx.align(
            whisper_results, alignment_model, metadata, vocal_target, device
        )
        word_timestamps = filter_missing_timestamps(result_aligned["word_segments"])

        # clear gpu vram
        del alignment_model
        torch.cuda.empty_cache()
    else:
        assert (
            batch_size == 0
        ), (  # TODO: add a better check for word timestamps existence
            f"Unsupported language: {language}, use --batch_size to 0"
            " to generate word timestamps using whisper directly and fix this error."
        )
        word_timestamps = []
        for segment in whisper_results:
            for word in segment["words"]:
                word_timestamps.append(
                    {"word": word[2], "start": word[0], "end": word[1]}
                )

    # Convert audio to mono for nemo compatibility

    sound = AudioSegment.from_file(vocal_target).set_channels(1)
    ROOT = os.getcwd()
    temp_path = os.path.join(ROOT, "temp_outputs")
    os.makedirs(temp_path, exist_ok=True)
    sound.export(os.path.join(temp_path, "mono_file.wav"), format="wav")

    # Run diarization using NeMo MSDD model

    msdd_model = NeuralDiarizer(
        cfg=create_config(temp_path, DOMAIN_TYPE="telephonic")
    ).to("cuda")
    msdd_model.diarize()  # Takes about 1 minute for 1 hour of audio

    del msdd_model
    torch.cuda.empty_cache()

    # Change job status to aligning
    if job_id is not None:
        job_status[job_id].progress = "aligning"

    # Map speaker labels to speaker names
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
        # restoring punctuation in the transcript to help realign the sentences
        punct_model = PunctuationModel(model="kredor/punctuate-all")

        words_list = list(map(lambda x: x["word"], wsm))

        labled_words = punct_model.predict(words_list)

        ending_puncts = ".?!"
        model_puncts = ".,;:!?"

        # We don't want to punctuate U.S.A. with a period. Right?
        is_acronym = lambda x: re.fullmatch(r"\b(?:[a-zA-Z]\.){2,}", x)

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

    print("Transcription complete")

    print(ssm)

    # Convert SSM into a list of TranscriptionSegment objects
    ssm_objects = list(
        map(
            lambda x: TranscriptionSegment(
                speaker=x["speaker"],
                start_time=x["start_time"],
                end_time=x["end_time"],
                text=x["text"],
            ),
            ssm,
        )
    )

    # print first 5 segments
    print(ssm_objects[:5])

    if job_id is not None:
        job_status[job_id] = TranscriptionJob(
            job_id=job_id,
            status="completed",
            progress="completed",
            result=ssm_objects,
            end_time=datetime.now(),
            duration=job_status[job_id].get_duration(),
        )

    return None


# Testing the transcription process (in production, this is a service endpoint)
if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(transcription, url_prefix="/transcription")

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    app.run(debug=True, host="0.0.0.0")
