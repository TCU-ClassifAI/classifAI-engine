# Installation

## Requirements


* [Python 3.10 or higher](https://www.python.org/downloads/)
* Docker is required to run this project. You can download it [here](https://www.docker.com/products/docker-desktop).
* [ffmpeg](https://ffmpeg.org/download.html) is required to run this project. You can download it [here](https://ffmpeg.org/download.html).
* [Redis](https://redis.io/download) is required to run this project. You can download it with `sudo apt install redis`.
* [Hugging Face token](https://hf.co/settings/tokens) is required to use the Hugging Face models. You can get a token [here](https://hf.co/settings/tokens). You must also accept the terms and conditions for the models you want to use ([here](https://hf.co/pyannote/speaker-diarization-3.1) and [here](https://hf.co/pyannote/segmentation-3.0)).

## Installation

1. Clone the repo

```sh
git clone https://github.com/TCU-ClassifAI/classifAI-engine.git
cd classifAI-engine
```

2. Install Python packages (it is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html))

```sh
pip install -r src/requirements.txt
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


5. Set up the environment variables

- For a full list of environment variables, see the [Configuration](configuration.md) documentation. This guide will cover a minimal set of environment variables to get the server running.

- Create a `.env` file in the root directory of the project. The `.env` file should contain the following environment variables:

```sh
# .env
HF_TOKEN=your_hugging_face_token # Get a token from https://hf.co/settings/tokens
REDIS_PORT=6379 #(default port for Redis, can be changed), the URL can also be changed (see config)
LLAMA_API_URL=http://localhost:5003 # URL for the LLAMA API
```
5. (Optional) Set up configuration for the API

- Edit values in `src/config/config.py` to match your environment.

6. Launch the API

```sh
python src/app.py
```

7. Run your RQ worker (you can do this through [supervisor](https://python-rq.org/patterns/supervisor/) or [another process manager](https://python-rq.org/patterns/systemd/))

```sh
rq worker -c config.worker_config
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