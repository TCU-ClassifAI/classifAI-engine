from flask import Blueprint
from dotenv import load_dotenv
import os

load_dotenv()

# config
if os.environ.get("ENV") == "production":
    pass
else:
    pass

categorize = Blueprint("categorize", __name__)
