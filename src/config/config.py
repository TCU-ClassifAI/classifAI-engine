import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "production":
    MODEL_TYPE = "large-v3"
    SETTINGS_TYPE = "prod"


else:
    MODEL_TYPE = "tiny.en"
    SETTINGS_TYPE = "dev"
