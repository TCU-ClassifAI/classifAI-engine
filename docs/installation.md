# Installation

## Requirements


* [Python 3.10 or higher](https://www.python.org/downloads/)
* Docker is required to run this project. You can download it [here](https://www.docker.com/products/docker-desktop).
* [ffmpeg](https://ffmpeg.org/download.html) is required to run this project. You can download it [here](https://ffmpeg.org/download.html).

## Installation

1. Clone the repo

```sh
git clone https://github.com/TCU-ClassifAI/classifAI-engine.git
cd classifAI-engine
```

2. Install Python packages

```sh
pip install -r src/requirements.txt -r src/requirements-dev.txt
```

3. Install required system packages 

```sh
# Install ffmpeg
sudo apt install ffmpeg # Ubuntu
brew install ffmpeg # MacOS
# install Redis
sudo apt install redis-server # Ubuntu
brew install redis # MacOS
# start Redis
sudo redis-server # Ubuntu
```
4. Accept the Hugging Face terms and conditions
- 1. visit hf.co/pyannote/speaker-diarization-3.1 and accept user conditions
- 2. visit hf.co/pyannote/segmentation-3.0 and accept user conditions
- 3. visit hf.co/settings/tokens to create an access token


4. Set up the environment variables and ins

- Create a `.env` file in the root directory of the project. The `.env` file should contain the following environment variables:

```sh
# .env
HF_TOKEN=your_hugging_face_token # Get a token from https://hf.co/settings/tokens
REDIS_PORT=6379 #(default port for Redis, can be changed)
REDIS_HOST=localhost #(default host for Redis, can be changed)
REDIS_DB=0 #(default db for Redis, can be changed)
OPENAI_API_KEY=your_openai_api_key # Get a token from https://platform.openai.com/account/api-keys
```


4. Launch the API

```sh
python src/app.py
```


## Test
`curl http://localhost:5000/healthcheck` should return `OK`


More usage can be found in the [API Documentation](api/api_transcription.md).


## Installation on the GPU Server

Currently, it is run as a Systemd service. The service file is located at `/etc/systemd/system/classifai.service`. The service can be started, stopped, and restarted using the following commands:

```sh
sudo systemctl start classifai
sudo systemctl stop classifai
sudo systemctl restart classifai
```

The logs can be viewed using the following command:

```sh
sudo journalctl -u classifai
```

Below is the startup script that is used to start the server. It is located at `/home/classgpu/classifAI-engine/startup.sh`.
```sh
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
```