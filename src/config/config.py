import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "production":
    # Production settings
    TRANSCRIPTION_MODEL = "large-v3"
    CATEGORIZATION_MODEL = "gemma"  # or "gpt"
    SUMMARIZATION_MODEL = "huggingface"  # or "gpt"
    SETTINGS_TYPE = "prod"

else:
    # Development settings
    TRANSCRIPTION_MODEL = "large-v3"  # or "tiny.en"
    CATEGORIZATION_MODEL = "gemma"  # or "gpt"
    SUMMARIZATION_MODEL = "huggingface"  # or "gpt"
    SETTINGS_TYPE = "dev"

VERSION = "3.0.1"