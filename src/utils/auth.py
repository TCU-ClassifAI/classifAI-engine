from flask import request, make_response


def api_key_required(func):
    """
    Decorator to check for API key in request header.
    @param func: Function to decorate

    @return: Wrapper function
    """

    def wrapper(*args, **kwargs):
        api_key = request.headers.get("API-Key")

        # Check if API key is present in the environment or any other desired
        # validation
        if api_key and validate_api_key(api_key):
            # If the API key is valid, proceed with the decorated function
            return func(*args, **kwargs)
        else:
            # If the API key is not valid, return a 401 Unauthorized response
            return make_response(
                "Unauthorized. Pleae add a header with the key API-Key and your secret key.",
                401,
            )

    return wrapper


def validate_api_key(api_key):
    """
    Validate the API key. Currently it has a basic functionality

    @param api_key: API key to validate
    @return: True if the API key is valid, False otherwise
    """
    return api_key == "secret_key"
