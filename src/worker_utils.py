# Command line options:
#    --kill: Kill all workers
#    --restart: Kill all workers and restart them


# activate the virtual environment
import os

os.system("source /home/classgpu/classifAI-engine/venv-3.10/bin/activate")

#!/usr/bin/env python
from redis import Redis
from rq import Worker, Queue
import os
from dotenv import load_dotenv
import sys
import argparse


# This file is intended to tell information about all the workers that are running in the system.
# It can also kill workers, and restart them.


load_dotenv()
REDIS_PORT = os.getenv("REDIS_PORT")

# add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


# Returns all workers registered in this connection
redis = Redis(host="localhost", port=REDIS_PORT)

queue = Queue("jobs", connection=redis)
workers = Worker.all(queue=queue)

print(f"Number of workers: {len(workers)}")

for worker in workers:
    print(f"Worker: {worker.name}")
    print(f"Host: {worker.hostname}")
    print(f"PID: {worker.pid}")
    print(f"State: {worker.state}")
    print(f"Current job: {worker.get_current_job()}")
    print(f"Birth: {worker.birth_date}")
    print(f"Queues: {worker.queue_names()}")
    print(f"Successful jobs: {worker.successful_job_count}")
    print(f"Failed jobs: {worker.failed_job_count}")
    print(f"Total working time: {worker.total_working_time}")  # In seconds
    print("")

print("To restart all workers, run: sudo python3 src/worker_utils.py --restart")


# if sys argument kill=True, kill all workers in the system

# use argparse to parse the arguments
if len(sys.argv) > 1:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kill", action="store_true", help="Kill all workers")
    parser.add_argument(
        "--restart", action="store_true", help="Kill all workers and restart them"
    )
    args = parser.parse_args()

    if args.kill:
        for worker in workers:
            worker_name = worker.name
            pid = worker.pid
            os.system(f"kill {pid}")  # send SIGTERM to the worker
            os.system(
                f"kill {pid}"
            )  # Send twice to not let the worker finish the current job
            print(f"Worker {worker_name} with PID {pid} killed")

    print("All workers killed")

    # if sys argument restart=True, kill all workers in the system, and restart them\
    if args.restart:
        print("Restarting workers...")
        for worker in workers:
            worker_name = worker.name
            pid = worker.pid
            os.system(f"kill {pid}")
            os.system(f"kill {pid}")
            print(f"Worker {worker_name} with PID {pid} killed")

        print("All workers killed. Restarting workers...")
        # Create one worker according to worker_config.py

        # ensure we're in the right directory
        os.chdir("/home/classgpu/classifAI-engine")
        # Change the virtual environment
        os.system("source /home/classgpu/classifAI-engine/venv-3.10/bin/activate")

        # Run the worker in background
        os.system("rq worker --config worker_config &")

        print("Workers restarted")
