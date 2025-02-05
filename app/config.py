from dotenv import load_dotenv
import os
import nopecha
from nopecha.api.requests import RequestsAPIClient


load_dotenv()
import os

# Get the absolute path of the project's root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current file's directory
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Move up to root

PASS_KEY_PATH = os.path.join(ROOT_DIR, "pass.key")

API_KEY_FILE = os.path.join(ROOT_DIR, "api.key")
ENV_FILE = os.path.join(ROOT_DIR, ".env")

# Load API keys from file
def load_api_keys():

    with open(API_KEY_FILE, "r") as f:
        content = f.read().strip()
        return content.split(",") if content else []

# Save API keys to file
def save_api_keys(api_keys):
    with open(API_KEY_FILE, "w") as f:
        f.write(",".join(api_keys))

def get_pass_key():
    with open(PASS_KEY_PATH, "r") as f:
        pass_key = f.read().strip()
        return pass_key

def check_status(api_key = "23u6q79gd11xje0j"):
    client = RequestsAPIClient(api_key)
    status = client.status()
    return status


def active_api_key():
    api_keys = load_api_keys()
    for api_key in api_keys:
        api_key = api_key.strip()
        status = check_status(api_key)
        if status['credit'] > 0 and status['status'] == 'Active':
            return api_key
    return None
def regenerate_env_api_key():
    active_key = active_api_key()
    if active_key:
        # Read and update the .env file
        with open(ENV_FILE, "r") as file:
            lines = file.readlines()

        with open(ENV_FILE, "w") as file:
            for line in lines:
                if line.startswith("NOPECHA_API_KEY="):
                    file.write(f'NOPECHA_API_KEY="{active_key}"\n')
                else:
                    file.write(line)

        print("Replacement done!")
    else:
        print("No active API key found.")
regenerate_env_api_key()


