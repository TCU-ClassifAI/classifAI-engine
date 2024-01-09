import unittest
from flask import Flask


class TestCategorization(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    # def test_categorize_question(self):
    #     question = "What is the capital of the United States?"
    #     result = categorize_question(question)
    #     self.assertEqual(result, "Knowledge")

    def test_healthcheck_endpoint(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
