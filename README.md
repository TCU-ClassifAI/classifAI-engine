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
[MongoDB-shield]: https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/
[Pydantic-shield]: https://img.shields.io/badge/Pydantic-2B7AFD?style=for-the-badge&logo=pydantic&logoColor=white
[Pydantic-url]: https://pydantic-docs.helpmanual.io/


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


[![GitHub contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


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
[![Celery][Celery-shield]][Celery-url]
[![Redis][Redis-shield]][Redis-url]
[![MongoDB for Python][MongoDB-shield]][MongoDB-url]
[![Pydantic][Pydantic-shield]][Pydantic-url]
  


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up this API locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* Python 3.10 (will probably work with 3.11+)
* ffmpeg


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/TCU-ClassifAI/classifAI-engine.git
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
    python src/run.py
   ```


`curl http://localhost:5000/healthcheck` should return `OK`


<!-- USAGE EXAMPLES -->
## Usage

### Transcription

#### start_transcription

* **URL:** `/transcription/start_transcription`
* **Method:** `POST`
* **Data Params:** (Request with file)

#### get_transcription

* **URL:** `/transcription/get_transcription`
* **Method:** `GET`
* **Data Params:** 
  - `job_id` (string)
* **Success Response:** 200 OK
  - **Content:**
    ```json
    {
      "status": "completed",
      "transcription_link": "https://example.com/transcription-file"
    }
    ```
* **Error Response:** 404 Not Found
  - **Content:**
    ```json
    {
      "status": "error",
      "message": "Transcription job not found"
    }
    ```


<!-- Get request to /get_transcription with job_id should return a status and a link to the transcription file (if relevant) -->

_For more examples, please refer to the [Documentation](https://tcu-classifai.github.io/classifAI-engine/)_




<!-- ROADMAP -->
## Roadmap

- [x] Add Transcription Service
    - [x] Use Whisper for transcription
    - [ ] Integrate WhisperX for faster transcription and diarization
    - [ ] Use Celery for better asynchronous processing
    - [ ] Use Redis for better asynchronous processing
    - [ ] Ensemble different models for better transcription
- [ ] Add Question Categorization Service
- [ ] Add Question Categorization Service
- [ ] Add Engagement Insights Service



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

View the Portal: [http://classifai.tcu.edu/](http://classifai.tcu.edu/)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [TCU Computer Science Department](https://cs.tcu.edu/), for funding this project
* [Our Clients](https://ai.tcu.edu/#/ai4edu), for providing us with the opportunity to work on this project and continued support
* [Dr. Bingyang Wei](https://personal.tcu.edu/bwei/), for being our faculty advisor
* [Dr. Michael Denkowski](https://www.mjdenkowski.com/), for advising us on our NLP models

<p align="right">(<a href="#readme-top">back to top</a>)</p>




