from fastapi import APIRouter, HTTPException
from datetime import datetime

from database import users
from utils.fingerprint import generate_fingerprint

router = APIRouter()

@router.post("/register")
def register(data: dict):
    username = data.get("username")
    password = data.get("password")
    fingerprint_data = data.get("fingerprint")
    location = data.get("location")

    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[username] = {
        "password": password,
        "fingerprint": generate_fingerprint(fingerprint_data or {}),
        "typing_profile": None,
        "last_location": location,   # may be None at register
        "registered_at": datetime.utcnow().isoformat()
    }

    return {
        "status": "success",
        "message": "Registered successfully. Proceed to typing enrollment."
    }
