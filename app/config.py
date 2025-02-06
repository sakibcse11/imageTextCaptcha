import os
from dotenv import load_dotenv
from nopecha.api.urllib import UrllibAPIClient

load_dotenv()


# Get the absolute path of the project's root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current file's directory
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # Move up to root

PASS_KEY_PATH = os.path.join(ROOT_DIR, "pass.key")

API_KEY_PATH = os.path.join(ROOT_DIR, "api.key")
DOT_ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Load API keys from file
def load_api_keys():

    with open(API_KEY_PATH, "r") as f:
        content = f.read().strip()
        return content.split(",") if content else []

# Save API keys to file
def save_api_keys(api_keys):
    with open(API_KEY_PATH, "w") as f:
        f.write(",".join(api_keys))

def get_pass_key():
    with open(PASS_KEY_PATH, "r") as f:
        pass_key = f.read().strip()
        return pass_key

def get_fresh_client():
    """Get a fresh API client with current key"""
    load_dotenv(dotenv_path=DOT_ENV_PATH, override=True)
    current_api_key = os.getenv("NOPECHA_API_KEY", "")
    return UrllibAPIClient(current_api_key)

def check_status(api_key):
    """Check status with direct client"""
    client = UrllibAPIClient(api_key)
    try:
        return client.status()
    except Exception as e:
        print(f"Error checking status for key {api_key}: {str(e)}")
        return {"credit": 0, "status": "Error", "ttl": 0}


def active_api_key():
    """Find the best API key using direct client"""
    api_keys = load_api_keys()
    ttl = 99604281
    active_key = None

    for api_key in api_keys:
        api_key = api_key.strip()
        status = check_status(api_key)

        if status['credit'] > 0 and status['status'] == 'Active':
            if status["ttl"] < ttl:
                ttl = status["ttl"]
                active_key = api_key
    return active_key

def regenerate_active_api_key():
    """Update active key using direct client approach"""
    active_key = active_api_key()
    if active_key:
        # Read and update the .env file
        with open(DOT_ENV_PATH, "r") as file:
            lines = file.readlines()

        with open(DOT_ENV_PATH, "w") as file:
            for line in lines:
                if line.startswith("NOPECHA_API_KEY"):
                    file.write(f'NOPECHA_API_KEY = "{active_key}"\n')
                else:
                    file.write(line)

        # Force reload environment
        load_dotenv(dotenv_path=DOT_ENV_PATH, override=True)

        # Verify with new client
        client = get_fresh_client()
        status = client.status()
        print(f"Regenerated key status: {status}")
        return True
    else:
        raise Exception("No active key found")













