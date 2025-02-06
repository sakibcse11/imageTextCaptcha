import os
from app.config import regenerate_active_api_key, get_fresh_client
from app.routes.api import remove_api_key

from nopecha.api.types import RecognitionRequest
import typing


def solve_image(image):
    """Solve captcha using direct client"""
    # Get fresh client
    client = get_fresh_client()
    current_api_key = client.key
    print(f"Using key: {client.key}")

    status = client.status()
    print(f"Status for key {client.key}: {status}")

    if status['credit'] == 0 or status['status'] == 'Expired':
        remove_api_key(current_api_key)
        client = get_fresh_client()

    for i in range(2):
        try:
            # Create request dict
            request = {
                "type": "textcaptcha",
                "image_urls": [image]
            }
            # Use client directly
            response = client.recognize_raw(typing.cast(RecognitionRequest, request))
            if response and isinstance(response, dict) and "data" in response and response["data"]:
                captcha_solution = response["data"][0]
                return captcha_solution
        except RuntimeError:
            regenerate_active_api_key()
            client = get_fresh_client()
            print(f"New key after regeneration: {client.key}")
