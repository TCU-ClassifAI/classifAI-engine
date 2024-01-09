# import unittest
# from unittest.mock import patch, MagicMock
# from src.services.transcription import TranscriptionJob, transcribe, start_transcription
# from flask import Flask


# class TestTranscription(unittest.TestCase):
#     def setUp(self):
#         self.app = Flask(__name__)
#         self.client = self.app.test_client()

#     def test_transcription_job(self):
#         job = TranscriptionJob(job_id="1234", user_id="5678")
#         self.assertEqual(job.job_id, "1234")
#         self.assertEqual(job.user_id, "5678")

#     @patch("services.transcription.whisper")
#     def test_transcribe(self, mock_whisper):
#         mock_whisper.transcribe.return_value = "transcription result"
#         job = TranscriptionJob(job_id="1234", user_id="5678")
#         result = transcribe("file", job)
#         self.assertEqual(result, "transcription result")

#     @patch("services.transcription.TranscriptionJob")
#     @patch("services.transcription.transcribe")
#     def test_start_transcription(self, mock_transcribe, mock_job):
#         mock_transcribe.return_value = "transcription result"
#         mock_job.return_value = MagicMock()
#         result = start_transcription("file", "model_type", "user_id")
#         self.assertEqual(result, "transcription result")

#     def test_healthcheck_endpoint(self):
#         response = self.client.get("/healthcheck")
#         self.assertEqual(response.status_code, 200)

#     def test_help_endpoint(self):
#         response = self.client.get("/help")
#         self.assertEqual(response.status_code, 200)

#     def test_check_transcription_endpoint(self):
#         response = self.client.get("/check_transcription")
#         self.assertEqual(response.status_code, 200)

#     def test_start_transcription_endpoint(self):
#         response = self.client.post("/start_transcription")
#         self.assertEqual(response.status_code, 200)


# if __name__ == "__main__":
#     unittest.main()
