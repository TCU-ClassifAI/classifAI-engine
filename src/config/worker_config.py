from dotenv import load_dotenv
import os

load_dotenv()

# Redis port should be 11110 (not the default 6379) \
# to avoid conflicts with other services
REDIS_URL = f'redis://localhost:{os.getenv("REDIS_PORT")}/0'


# Queues to listen on
QUEUES = ["jobs"]


# To start a worker up from the terminal:
# rq worker -c config.worker_config
