#!/usr/bin/env python
from redis import Redis
from rq import Worker
import os
from dotenv import load_dotenv
import sys

load_dotenv()
REDIS_PORT = os.getenv("REDIS_PORT")

# add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Preload libraries
from utils.worker_manager import process_job # noqa: F401
from utils.transcription.diarize_parallel import transcribe_and_diarize # noqa: F401

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default'], connection=Redis(host="localhost", port=REDIS_PORT))
w.work()