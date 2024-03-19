#!/usr/bin/env python
from redis import Redis
from rq import Worker
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_PORT = os.getenv("REDIS_PORT")

# Preload libraries
from utils.worker_manager import process_job # noqa: F401
from utils.transcription.diarize_parallel import transcribe_and_diarize # noqa: F401

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default'], connection=Redis(host="localhost", port=REDIS_PORT))
w.work()