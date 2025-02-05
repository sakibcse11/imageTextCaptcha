from fastapi import APIRouter, HTTPException, Query
from app.config import load_api_keys, save_api_keys, get_pass_key, check_status, regenerate_active_api_key

router = APIRouter()
pass_key = get_pass_key()

# API Key Management

@router.post("/api-keys/add/")
def add_api_key(api_key: str, password: str):
    if not password== pass_key:
        raise HTTPException(status_code=404, detail="Your password is incorrect")
    api_keys = load_api_keys()
    if api_key in api_keys:
        raise HTTPException(status_code=400, detail="API key already exists")
    status = check_status(api_key)
    if status['credit'] > 0 and status['status'] == 'Active':
        api_keys.append(api_key)
        save_api_keys(api_keys)
        regenerate_active_api_key()
        return {"message": "API key added successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired API key")
@router.delete("/api-keys/remove/")
def remove_api_key(api_key: str):
    api_keys = load_api_keys()
    if api_key in api_keys:
        api_keys.remove(api_key)
    save_api_keys(api_keys)
    regenerate_active_api_key()
    return {"message": "API key removed successfully"}

@router.get("/api-keys/refresh/")
def refresh_api_key_list():
    api_keys = load_api_keys()
    if not api_keys:
        return {"message": "API key not found"}
    valid_api_key_status = []
    for api_key in api_keys:
        status = check_status(api_key)
        if status['credit'] == 0 or status['status'] == 'Expired':
            remove_api_key(api_key)
        if  status['credit'] > 0 and status['status'] == 'Active':
            valid_api_key_status.append(status)
    regenerate_active_api_key()
    return {"message":valid_api_key_status}
