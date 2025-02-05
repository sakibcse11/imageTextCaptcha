import os
from dotenv import load_dotenv
import nopecha

from app.config import regenerate_active_api_key
from app.routes.api import remove_api_key

def solve_image(image):
    load_dotenv(override=True)
    current_api_key = os.getenv("NOPECHA_API_KEY", "")
    status = nopecha.Balance.get()
    print(status)
    if status['credit'] == 0 or status['status'] == 'Expired':
        remove_api_key(current_api_key)
        regenerate_active_api_key()
    for i in range(2):
        try:
            response = nopecha.Recognition.solve(
                type='textcaptcha',
                image_urls=[image]
            )
            if response and isinstance(response, dict) and "data" in response and response["data"]:
                captcha_solution = response["data"][0]
                return captcha_solution
        except RuntimeError:
            regenerate_active_api_key()
    return False





