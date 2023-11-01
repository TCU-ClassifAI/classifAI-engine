# Style Guide

## Linting

We follow black and flake8 for our style guide. We use black to format our code and flake8 to check for style errors. We use pre-commit to run black and flake8 before every commit.

Please see [the pre-commit setup instructions](instructions_for_pre-commit.md) for more information on how to set up pre-commit.

## Docstrings

Docstrings are reccomended for most functions and classes. You are not required to do them for the smallest classes, etc. but please do them for anything that is not obvious.
- We use [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

```py
def start_transcription(file: File, model_type: str, user_id: Optional[str] = None):
    """
    Start transcription of an audio file using Whisper.
    Use ThreadPoolExecutor to run in the background.
    Args:
        file (File): Audio file to be transcribed.
        model_type (str): Model type to use for transcription (e.g. 'large', 'tiny.en')
        user_id (str, optional): ID of the user who uploaded the audio file (default=None).
    Returns:
        str: JSON string representation of a TranscriptionJob object.
    """
```

## Testing

Please write tests for your code. We use pytest for our testing framework. 

## Type Hints

We encourage type hints for all functions and classes. Please see [PEP 484](https://www.python.org/dev/peps/pep-0484/) for more information on type hints.

## Other

Please be sure to use good code practices. Some things to especially keep in mind:

* Use descriptive variable names
* DRY (Don't Repeat Yourself)
* Use comments when necessary
* Break up long functions into smaller functions

We do not strictly adhere to the google styleguide, but we encourage you to follow it:  [https://google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)