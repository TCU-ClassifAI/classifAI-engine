import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Engine settings
VERSION = "4.4.5"

# Model settings
TRANSCRIPTION_MODEL = "large-v3"
CATEGORIZATION_MODEL = "llama"  # or gpt
SUMMARIZATION_MODEL = "llama"  # or gpt # or huggingface

# Audio file upload settings
UPLOAD_FOLDER = "raw_audio/"
TEMP_FOLDER = "temp_outputs/"  # Includes vocal separation outputs and rttm files
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
}  # Others are (probably) supported as well but not tested.

# Environment settings

ENV_TYPE = "dev"

if os.environ.get("ENV") == "production":
    ENV_TYPE = "prod"
    # Insert any overrides here!

# You can override .env variables here
