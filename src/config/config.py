import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TRANSCRIPTION_MODEL = "large-v3"
CATEGORIZATION_MODEL = "gemma"  # or gpt
SUMMARIZATION_MODEL = "huggingface"  # or gpt
ENV_TYPE = "dev"

# File upload settings

# Audio file upload settings
UPLOAD_FOLDER = "raw_audio/"

ALLOWED_EXTENSIONS = {
    "wav",
    "mp3",
    "mp4",
    "m4a",
    "flac",
    "aac",
    "wma",
    "ogg",
    "oga",
    "webm",
    "mov",
} # Others are probably supported as well but not tested.

# Includes vocal separation outputs and diarization rich transcription time marked (rttm) files
TEMP_FOLDER = "temp_outputs/"  

if os.environ.get("ENV") == "production":
    ENV_TYPE = "prod"
    # Insert any overrides here!

# You can override .env variables here

VERSION = "4.1.4"
