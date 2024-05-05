<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TCU-ClassifAI/classifAI-engine.svg?style=for-the-badge
[contributors-url]: https://github.com/TCU-ClassifAI/classifAI-engine/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TCU-ClassifAI/classifAI-engine.svg?style=for-the-badge
[forks-url]: https://github.com/TCU-ClassifAI/classifAI-engine/network/members
[stars-shield]: https://img.shields.io/github/stars/TCU-ClassifAI/classifAI-engine.svg?style=for-the-badge
[stars-url]: https://github.com/TCU-ClassifAI/classifAI-engine/stargazers
[issues-shield]: https://img.shields.io/github/issues/TCU-ClassifAI/classifAI-engine.svg?style=for-the-badge
[issues-url]: https://github.com/TCU-ClassifAI/classifAI-engine/issues
[license-shield]: https://img.shields.io/github/license/TCU-ClassifAI/classifAI-engine.svg?style=for-the-badge
[license-url]: https://github.com/TCU-ClassifAI/classifAI-engine/blob/master/LICENSE.txt



[Flask-shield]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[OpenAI-shield]: https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/
[Torch-shield]: https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white
[Torch-url]: https://pytorch.org/
[Celery-shield]: https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white
[Celery-url]: https://docs.celeryproject.org/en/stable/index.html
[Redis-shield]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[Gemma-shield]: https://img.shields.io/badge/Gemma-8E75B2?style=for-the-badge&logo=Google-Gemini&logoColor=white
[Gemma-url]: https://ai.google.dev/gemma

[Llama-shield]: https://img.shields.io/badge/Llama-FFFFFF?style=for-the-badge&logo=meta&logoColor=0081FB
[Llama-url]: https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html

[Pegasus-shield]: https://img.shields.io/badge/Pegasus-000000?style=for-the-badge&logo=google&logoColor=white
[Pegasus-url]: https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html

[Build-shield]: https://img.shields.io/github/workflow/status/TCU-ClassifAI/classifAI-engine/deploy_docs.yml?style=for-the-badge
[Build-url]: https://github.com/TCU-ClassifAI/classifAI-engine/actions/workflows/deploy_docs.yml
[Build-shield]: https://img.shields.io/github/actions/workflow/status/TCU-ClassifAI/classifAI-engine/main.yml?branch=main&style=for-the-badge

<a name="readme-top"></a>




<br />
<div align="center">
  <a href="https://github.com/TCU-ClassifAI/classifAI-engine">
    <img src="docs/assets/logo.jpg" alt="Logo" width="128" height="128">
  </a>

<h2 align="center">ClassifAI Engine</h2>

  <p align="center">
    ClassifAI engine is a RESTful API that provides the heavy lifting for <a href="https://github.com/TCU-ClassifAI/classifAI">classifAI</a> through audio transcription, question categorization, and insights.<br>
    <br />
    <a href="https://tcu-classifai.github.io/classifAI-engine/"><strong>Explore the docs »</strong></a>
    <br /> 
    <br />
    <a href="https://github.com/TCU-ClassifAI/classifAI">Visit Portal</a>
    ·
    <a href="https://github.com/TCU-ClassifAI/classifAI-engine/issues">Report Bug</a>
    ·
    <a href="https://github.com/TCU-ClassifAI/classifAI-engine/issues">Request Feature</a>
    ·
    <a href="https://github.com/TCU-ClassifAI/classifAI/">Project Information</a>
    
  </p>
</div>




[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-License][license-shield]][license-url]
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/TCU-ClassifAI/classifAI-engine/main.yml?branch=main&style=for-the-badge)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fclassifai.tcu.edu%2F&style=for-the-badge&label=ClassifAI%20Website)





***    



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

ClassifAI engine provides the heavy lifting for classifAI. It is a RESTful API that provides the following services:

* Transcription of video and audio into text
* Categorization of questions
* Engagement insights
* Turning reports into PDFs or .docx files



### Built With
[![Flask][Flask-shield]][Flask-url]
[![Torch][Torch-shield]][Torch-url]
[![OpenAI][OpenAI-shield]][OpenAI-url]
[![Redis][Redis-shield]][Redis-url]
[![LLaMA][Llama-shield]][Llama-url]

  


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

For more instructions please see the [documentation 
](https://tcu-classifai.github.io/classifAI-engine/)

### Prerequisites

* Python 3.10 (can probably work with 3.9+ but not tested)
* [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)
* [Huggingface API key token](https://huggingface.co/docs/api-inference/en/quicktour)

### Installation 

1. Clone the repo
   ```sh
   git clone https://github.com/TCU-ClassifAI/classifAI-engine.git
   cd classifAI-engine
   ```

2. [Install and run Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)
   ```sh
    sudo apt-get install redis-server 
    redis-server
   ```

3. Install Python packages (it is reccomended you use a [venv](https://docs.python.org/3/library/venv.html))
    ```sh
    pip install -r src/requirements.txt -r src/requirements-dev.txt
    ```

4. Include your [huggingface API key](https://huggingface.co/docs/api-inference/en/quicktour) in either your environment variables or in a `.env` file in the root directory
   ```sh
   HF_TOKEN=your_key_here
   ```
    You must also accept the Hugging Face terms and conditions:
    - visit hf.co/pyannote/speaker-diarization-3.1 and accept user conditions
    - visit hf.co/pyannote/segmentation-3.0 and accept user conditions

5. Launch the API 
   ```sh
    python src/app.py
   ```

6. Launch your worker (for asynchronous tasks)
   ```sh
    rq worker -c config.worker_config
   ```
   (More information on [RQ](https://python-rq.org/docs/))

7. Include your preferred summarization/categorization model through `config.py` (optional)
   ```python
    SUMMARIZATION_MODEL = "gpt4"
    CATEGORIZATION_MODEL = "gemma"
   ```
   You must launch your own model separely and include the API endpoint in your .env file
   ```sh
    LLAMA_API=your_model_endpoint
   ``` 
  For Llama, please see the repository [here](https://github.com/TCU-ClassifAI/llama-classification)

#### Testing
`curl http://localhost:5000/healthcheck` should return `OK`


<!-- USAGE EXAMPLES -->
## Usage

### Analyze an Audio File

### analyze

* **URL:** `/analyze`
* **Method:** `POST`
* **Data Params:** 
  - `file` (file)
  - `url` (string)

* Example:
  ```sh
  curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=t4yWEt0OSpg"}' http://localhost:5000/analyze
  curl -X POST -F "file=@<path_to_your_audio_file>" http://localhost:5000/analyze
  ```

* **Success Response:** 200 
```json
{
  "job_id": "0bc133cb-f519-40a1-96c6-46d2cfe9e4ad",
  "message": "Analysis started"
}
```

### Get Analysis Status

* **URL:** `/analyze/<job_id>`
* **Method:** `GET`

* Example (preferred):
  ```sh
  curl http://localhost:5000/analyze/0bc133cb-f519-40a1-96c6-46d2cfe9e4ad
  ```

* Alternative Example (legacy support):
  ```sh
  curl http://localhost:5000/analyze/?job_id=0bc133cb-f519-40a1-96c6-46d2cfe9e4ad
  ```

* **Success Response:** 200

* **Example Content:**
```json
{
  "meta": {
    "job_id": "0bc133cb-f519-40a1-96c6-46d2cfe9e4ad",
    "job_type": "analyze",
    "message": "Analysis finished",
    "progress": "finished",
    "title": "General Relativity Explained in 7 Levels of Difficulty"
  },
  "result": {
    "transcript": [
      {
        "end_time": 11149,
        "speaker": "Speaker 0",
        "start_time": 7740,
        "text": "General relativity is a physics theory invented by Albert Einstein. "
      },
    ],
    "questions": [
      {
        "question": "What is general relativity?",
        "level": 1,
      },
    ],
    "summary": "General relativity is a physics theory invented by Albert Einstein. It describes how gravity works in the universe. "
  }
}
```

_For more examples, please refer to the [Documentation](https://tcu-classifai.github.io/classifAI-engine/)_

### Summarization

#### summarize

* **URL:** `/summarize`
* **Method:** `POST`
* **Data Params:** 
  - `text` (string)

* Example:
  ```sh
  curl -X POST -H "Content-Type: application/json" -d '{"text": "This is the transcript that I want to have summarized."}' http://localhost:5000/summarize/
  ```
* **Success Response:** 200 OK

  - **Content:**
    ```json
    "This is the summary of the text that was passed in.", 200
    ```

  Alternatively, you can pass in a transcript like so: 
  ```json
  [
    {
      "end_time": 2301,
      "speaker": "Speaker 0",
      "start_time": 1260,
      "text": "Why did you bring me here? "
    },
    {
      "end_time": 4263,
      "speaker": "Main Speaker",
      "start_time": 3242,
      "text": "I dont like going out. "
    }
  ]
  ```

  So the request would look like this:
  ```sh
  curl -X POST -H "Content-Type: application/json" -d '{"transcript": [{"end_time": 2301,"speaker": "Speaker 0","start_time": 1260,"text": "Why did you bring me here? "},{"end_time": 4263,"speaker": "Main Speaker","start_time": 3242,"text": "I dont like going out. "}]}' http://localhost:5000/summarize/
  ```


<!-- ROADMAP -->
## Roadmap

- [x] Add Transcription Service
    - [x] Use Whisper for transcription
    - [x] Integrate WhisperX for faster transcription and diarization
    - [x] Use Redis for better asynchronous processing
    - [x] Add support for YouTube videos
    - [ ] Add support for more languages (unofficial)

- [x] Add Summarization Service
- [x] Add Question Categorization Service
    - [x] Update service- Using Fine-Tuned version of Llama
    - [x] Generate summaries of the transcript
    - [ ] Add support for more question types
    - [ ] Add support for more languages (works for summaries, not categorization..)
- [ ] Add Engagement Insights Service
    - [ ] Add support for more languages
    

See the [open issues](https://github.com/TCU-ClassifAI/classifAI/issues) for a full list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

### __[Instructions for Contribution](https://tcu-classifai.github.io/classifAI-engine/contribution/contributing/)__

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details. The GNU GPLv3 License is a free, copyleft license for software and other kinds of works.

Note that this license only applies *to the engine.* Please see the [classifAI portal](https://github.com/TCU-ClassifAI/classifAI) for more information on the license for the portal.

<!-- CONTACT -->
## Contact

[Learn About the Team](http://riogrande.cs.tcu.edu/2324InstructionalEffectiveness)

Project Link: [https://github.com/TCU-ClassifAI/classifAI](https://github.com/TCU-ClassifAI/classifAI)

View the Portal: [https://classifai.tcu.edu/](https://classifai.tcu.edu/)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [TCU Computer Science Department](https://cs.tcu.edu/), for funding this project
* [Our Clients](https://ai.tcu.edu/classifai), for providing us with the opportunity to work on this project and continued support
* [Dr. Bingyang Wei](https://personal.tcu.edu/bwei/), for being our faculty advisor

<p align="right">(<a href="#readme-top">back to top</a>)</p>