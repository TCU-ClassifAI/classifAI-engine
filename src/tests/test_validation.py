# import unittest
# import sys
# from services.transcription.validation import validate_query_for_transcription

# sys.path.append("..")

# # Print out sys.path to see if the path to the src folder is correct
# print(sys.path)


# class TestValidation(unittest.TestCase):
#     def test_empty_query_string(self):
#         response = validate_query_for_transcription(None)
#         self.assertFalse(response.is_valid)
#         self.assertEqual(response.error_message, "Query string is empty.")

#     def test_missing_path_parameter(self):
#         response = validate_query_for_transcription("foo=bar")
#         self.assertFalse(response.is_valid)
#         self.assertEqual(
#             response.error_message,
#             "Query string is invalid: parameter path is required.",
#         )

#     def test_valid_query_string(self):
#         response = validate_query_for_transcription("path=/foo/bar")
#         self.assertTrue(response.is_valid)
#         self.assertIsNone(response.error_message)


# if __name__ == "__main__":
#     unittest.main()
