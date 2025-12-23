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

    # 1️⃣ Validate input
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    # 2️⃣ Generate device fingerprint
    device_fingerprint = generate_fingerprint(fingerprint_data)

    # 3️⃣ Store user WITHOUT typing (done later)
    users[username] = {
        "password": password,
        "fingerprint": generate_fingerprint(fingerprint_data),
        "typing_profile": None,          # enrolled later
        "last_location": location,
        "registered_at": datetime.utcnow().isoformat()
    }

    return {
        "status": "success",
        "message": "Registered. Proceed to typing enrollment."
    }
