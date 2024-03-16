from flask import Blueprint, make_response, jsonify
from dotenv import load_dotenv
import os
load_dotenv()

# config
if os.environ.get("ENV") == "production":
    from config import production as settings
else:
    from config import config as settings

categorize = Blueprint("categorize", __name__)