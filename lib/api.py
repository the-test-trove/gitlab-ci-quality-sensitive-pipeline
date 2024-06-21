"""API module for the program."""

import requests


def get_user(user_id: int):
    """Process input."""
    base_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    response = _request_handler(base_url)

    return _response_handler(response)


def _request_handler(url):
    """Handles requests."""
    timeout = 10

    try:
        return requests.get(url, timeout=timeout)
    except requests.exceptions.Timeout:
        raise Exception("Request timed out.")
    except Exception:
        raise Exception("Request failed.")


def _response_handler(response):
    """Handles response."""
    if response.status_code != 200:
        raise ValueError("User not found.")
    else:
        return response.json()
