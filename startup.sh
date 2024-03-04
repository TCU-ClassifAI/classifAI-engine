#!/bin/bash

# change to the directory where the script is located
cd /home/classgpu/classifAI-engine

# if there is a nohup.out file, remove it
if [ -f nohup.out ]; then
    rm nohup.out
fi


# activate the virtual environment (in /home/classgpu/classifAI-engine)
source bin/activate

# Start the server
gunicorn --bind 0.0.0.0:5000 --chdir src/ wsgi:app