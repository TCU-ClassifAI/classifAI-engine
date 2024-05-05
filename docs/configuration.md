# Configuration

## Configuration files

There are a few server configuration files that you can use to customize the server. These files are located in the `config` directory of the server.

### config.py
This has things like the Flask app configuration.

Here is an example of the `config.py` file:

```python
TRANSCRIPTION_MODEL = "large-v3"
CATEGORIZATION_MODEL = "gemma" # You can also use "gpt" but that involves setting up your API key
SUMMARIZATION_MODEL = "huggingface" # You can also use "gpt"
ENV_TYPE = "dev"
UPLOAD_FOLDER = "raw_audio/"
```

More information about how to set up your API key for the GPT models can be found in the [OpenAI documentation](https://github.com/openai/openai-python)
Note that using GPT requires MONEYS.

Note that `UPLOAD_FOLDER` is the directory where the raw audio files are stored. This is relative to `root` so the default is `classifAI-engine/raw_audio/`.

## Server configuration

This runs on a few different services, so there are diffierent ways to view logs. 

To view the logs for ClassifAI-engine, the flask server, you can run the following command:

```bash
sudo journalctl -u classifai
```

The Flask server service file is located at `/etc/systemd/system/classifai.service`.
You can see it through `sudo systemctl cat classifai`.

To view the logs for the Redis queue worker, you can run the following command:

```bash
sudo supervisorctl tail -5000 procname stderr
sudo supervisorctl tail -f procname stdout
```

This is also run through the supervisor service file located at `/etc/supervisor/supervisord.conf`.
Commands are imported through the `src` directory.

## Environment variables

There's a `.env` file in the root directory of the server that you can use to set environment variables. 

This has ENV, REDIS_PORT, and GEMMA_API_URL.

Here is an example of the `.env` file:

```bash
ENV=development # This overrides whatever is in src/config/config.py. You can delete this line if you want to use the config.py file
REDIS_PORT=6379 # This is the default port for Redis
GEMMA_API_URL=http://localhost:5001 # Notice that the ClassifAI-engine Flask app is running on port 5000 by default, so the GEMMA API is running on port 5001
LLAMA_API_URL=http://localhost:5003 # This is the URL for the LLAMA API
HF_TOKEN=YOUR_HUGGINGFACE_API_KEY # This is the API key for the HuggingFace API
OPENAI_API_KEY=YOUR_OPENAI_API_KEY # This is the API key for the OpenAI API (Optional)
```
Recall that a the ENV variable is set in the `config.py` file, so if you set it in the `.env` file, it will override the `config.py` file. 

Furthermore, if you are using the GPT models, you will need to set the `OPENAI_API_KEY` variable in the `.env` file. Otherwise, it will not work.

## Cronjobs

There's one cronjob that runs every day to remove old audio files. This is simple enough that it's just in the `crontab` file.

We permanently store audio_files in the web server, so there's no need to keep them in the raw_audio directory for more than a few days.
To edit the cronjobs, you can run the following command:

```bash
sudo crontab -e
# Below is the cronjob, if you're interested:
5 3 * * * find /home/classgpu/classifAI-engine/src/raw_audio/ -mtime +3 -type f -delete
# This will delete all files in the raw_audio directory that are older than 3 days, every day at 3:05 AM
```

## Supervisor

The server uses Supervisor to manage the Redis queue worker. The configuration file is located at `/etc/supervisor/supervisord.conf`.

More information about Supervisor can be found in the [Supervisor documentation](http://supervisord.org/).