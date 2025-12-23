from fastapi import APIRouter, HTTPException
from database import users, sessions
from utils.fingerprint import generate_fingerprint

router = APIRouter()

@router.post("/verify-device")
def verify_device(data: dict):
    username = data.get("username")
    fingerprint_data = data.get("fingerprint")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    session = sessions.get(username)
    if not session or session["access"] != "VERIFY":
        raise HTTPException(status_code=403, detail="Verification not allowed")

    # Trust this device AFTER verification
    users[username]["fingerprint"] = generate_fingerprint(fingerprint_data)

    # Mark session verified
    sessions[username]["verified"] = True
    sessions[username]["access"] = "ALLOW"

    return {"status": "verified"}
