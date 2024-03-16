import pytest
from flask import Flask
from unittest.mock import patch

from endpoints.transcription import transcription  # Import your blueprint

# Fixtures for setting up the Flask app
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(transcription)
    app.testing = True  # Set testing mode
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# --- Tests for '/transcribe_yt' endpoint ---

@patch('utils.queue_manager.enqueue_yt_transcription')  # Mock the queueing function
def test_start_yt_transcription_get(mock_enqueue, client):
    response = client.get('/transcribe_yt?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    assert response.status_code == 200
    assert response.json == {'job_id': mock_enqueue.return_value}
    mock_enqueue.assert_called_once_with(  # Assert the mock was called correctly
        mock_enqueue.return_value, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', None
    )


# Add similar tests for POST requests and error scenarios for '/transcribe_yt'


# --- Tests for '/transcribe' endpoint ---

@patch('utils.queue_manager.enqueue_transcription')
def test_start_transcription(mock_enqueue, client):
    with open('sample_audio.mp3', 'rb') as file:
        response = client.post(
            '/transcribe', 
            data={'file': (file, 'sample_audio.mp3')},
            content_type='multipart/form-data'
        )

    assert response.status_code == 200
    assert response.json == {'job_id': mock_enqueue.return_value}
    # ... (Assert mock_enqueue is called with correct arguments)


# Add tests for missing file, error scenarios for '/transcribe'


# --- Tests for '/get_transcription_status' endpoint ---

@patch('utils.queue_manager.get_transcription_status')
def test_get_transcription_status(mock_get_status, client):
    mock_get_status.return_value = {'status': 'completed', 'result': '...'}
    response = client.get('/get_transcription_status?job_id=test_job_id')

    assert response.status_code == 200
    assert response.json == {'status': 'completed', 'result': '...'}
    mock_get_status.assert_called_once_with('test_job_id')

# Add tests for error scenarios in '/get_transcription_status'
