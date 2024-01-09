# import unittest
# from unittest.mock import patch
# from services.auth import validate_api_key, api_key_required
# from flask import Flask


# class TestAuth(unittest.TestCase):
#     def setUp(self):
#         self.app = Flask(__name__)
#         self.client = self.app.test_client()

#     @patch("services.auth.validate_api_key")
#     def test_api_key_required(self, mock_validate_api_key):
#         @self.app.route("/")
#         @api_key_required
#         def dummy_route():
#             return "Success", 200

#         # Test with valid API key
#         mock_validate_api_key.return_value = True
#         response = self.client.get("/", headers={"API-Key": "secret_key"})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data.decode(), "Success")

#         # Test with invalid API key
#         mock_validate_api_key.return_value = False
#         response = self.client.get("/", headers={"API-Key": "wrong_key"})
#         self.assertEqual(response.status_code, 401)
#         self.assertIn("Unauthorized", response.data.decode())

#     def test_validate_api_key(self):
#         # Test with valid API key
#         self.assertTrue(validate_api_key("secret_key"))
