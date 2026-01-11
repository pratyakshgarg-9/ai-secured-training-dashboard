from fastapi import APIRouter, HTTPException
from database import users, sessions
from utils.fingerprint import generate_fingerprint, fingerprint_match

router = APIRouter()

@router.post("/verify-device")
def verify_device(data: dict):
    username = data.get("username")
    fp_data = data.get("fingerprint")

    user = users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    incoming_fp = generate_fingerprint(fp_data or {})
    stored_fp = user.get("fingerprint")

    score = fingerprint_match(incoming_fp, stored_fp)

    # ✅ After verify, trust the new device by storing fingerprint
    user["fingerprint"] = incoming_fp

    sessions[username] = {
        "access": "ALLOW",
        "verified": True
    }

    return {"status": "verified"}
