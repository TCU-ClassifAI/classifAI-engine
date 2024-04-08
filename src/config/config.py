import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TRANSCRIPTION_MODEL = "large-v3"
CATEGORIZATION_MODEL = "gemma"
SUMMARIZATION_MODEL = "huggingface"
ENV_TYPE = "dev"


if os.environ.get("ENV") == "production":
    ENV_TYPE = "prod"
    # Insert any overrides here!


VERSION = "3.0.3"
