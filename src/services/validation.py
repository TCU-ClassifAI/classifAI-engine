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
    if not query_string:
        return ValidationResponse(False, "Query string is empty.")

    # Split the query string into key-value pairs
    query_params = query_string.split("&")

    if not query_params:
        return ValidationResponse(
            False, "Query string is invalid: no key-value pairs found."
        )

    parameter_names = [param.split("=")[0] for param in query_params]
    if "path" not in parameter_names:
        return ValidationResponse(
            False, "Query string is invalid: parameter path is required."
        )

    # Check if the query string has the required parameters (path is required)
    if "path" not in query_string:
        return ValidationResponse(
            False, "Query string is invalid: parameter path is required."
        )

    return ValidationResponse(True)

    # Check to ensure path is in the database
