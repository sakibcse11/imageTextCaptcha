from dotenv import load_dotenv
import os
import nopecha
from nopecha.api.requests import RequestsAPIClient


load_dotenv()

API_KEY_FILE = "api.key"

# Load API keys from file
def load_api_keys():
    if not os.path.exists(API_KEY_FILE):
        return []
    with open(API_KEY_FILE, "r") as f:
        content = f.read().strip()
        return content.split(",") if content else []

# Save API keys to file
def save_api_keys(api_keys):
    with open(API_KEY_FILE, "w") as f:
        f.write(",".join(api_keys))

def get_pass_key():
    with open("pass.key", "r") as f:
        pass_key = f.read().strip()
        return pass_key
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
        with open(".env", "r") as file:
            lines = file.readlines()

        with open(".env", "w") as file:
            for line in lines:
                if line.startswith("NOPECHA_API_KEY="):
                    file.write(f'NOPECHA_API_KEY="{active_key}"\n')
                else:
                    file.write(line)

        print("Replacement done!")
    else:
        print("No active API key found.")

def check_status(api_key = "23u6q79gd11xje0j"):
    client = RequestsAPIClient(api_key)
    status = client.status()
    return status
print(check_status())

