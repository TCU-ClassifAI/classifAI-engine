#!/bin/bash

# Make sure we're in the right directory
cd /home/classgpu/classifAI-engine/src

# make sure we're in the right virtual environment
source /home/classgpu/classifAI-engine/venv-3.10/bin/activate

function is_running() {
  ps aux | grep "$1" | grep -v grep > /dev/null
}

# see if there is already a gunicorn process running
if ! is_running gunicorn; then
  echo "Starting gunicorn..."
  gunicorn -w 3 --bind 0.0.0.0:5000 app:app &
fi

# see if there is already a RQ worker process running
if ! is_running rq; then
  echo "Starting RQ worker..."
  rq worker jobs &
fi

# run the startup script for the web server
/home/classgpu/gemma-classification-1/run.sh

