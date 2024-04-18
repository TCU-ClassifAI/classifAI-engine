import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TRANSCRIPTION_MODEL = "large-v3"
CATEGORIZATION_MODEL = "gemma"  # or gpt
SUMMARIZATION_MODEL = "huggingface"  # or gpt
ENV_TYPE = "dev"
UPLOAD_FOLDER = "raw_audio/"


if os.environ.get("ENV") == "production":
    ENV_TYPE = "prod"
    # Insert any overrides here!

# You can override .env variables here

VERSION = "4.1.4"
