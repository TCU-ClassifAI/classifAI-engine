# Installation

## Requirements


* [Python 3.10 or higher](https://www.python.org/downloads/)
* Docker is required to run this project. You can download it [here](https://www.docker.com/products/docker-desktop).
* [ffmpeg](https://ffmpeg.org/download.html) is required to run this project. You can download it [here](https://ffmpeg.org/download.html).

## Installation

1. Clone the repo

   ```sh
   git clone https://github.com/TCU-Instructional-AI/classifAI-engine.git
    cd classifAI-engine
    ```

2. Install Python packages

    ```sh
     pip install -r src/requirements.txt -r src/requirements-dev.txt
     ```

3. Install ffmpeg

    ```sh
     sudo apt install ffmpeg # Ubuntu
     brew install ffmpeg # MacOS
     ```

4. Launch the API

    ```sh
     python src/app.py
     ```


### Test: 
`curl http://localhost:5000/healthcheck` should return `OK`


More usage can be found in the [API Documentation](api.md).
