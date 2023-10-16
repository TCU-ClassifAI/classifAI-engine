# This file include validation functions for the API. It checks if the input is valid or not. Specifically for query parameters.


class ValidationResponse:
    def __init__(self, is_valid, error_message=None):
        self.is_valid = is_valid
        self.error_message = error_message


def validate_query_for_transcription(query_string: str):
    """
    Validates the query string for transcription endpoint.

    Args:
        query_string (str): Query string of the request.

    Returns:
        ValidationResponse: Validation response object.
    """
    # Check if the query string is empty
    if query_string is None:
        return ValidationResponse(False, "Query string is empty.")

    # Split the query string into key-value pairs
    query_params = query_string.split("&")
    if len(query_params) < 1:
        return ValidationResponse(
            False, "Query string is invalid: no key-value pairs found."
        )

    # Check if the query string has the required parameters (path is required)
    if "path" not in query_string:
        return ValidationResponse(
            False, "Query string is invalid: parameter path is required."
        )

    # Check to ensure path is in the database
