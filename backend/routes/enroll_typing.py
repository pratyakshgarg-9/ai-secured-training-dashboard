from fastapi import APIRouter, HTTPException
from database import users
from utils.typing_metrics import extract_features

router = APIRouter()


@router.post("/enroll-typing")
def enroll_typing(data: dict):
    username = data.get("username")
    typing_samples = data.get("typing_samples")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if not typing_samples or len(typing_samples) != 3:
        raise HTTPException(
            status_code=400,
            detail="Exactly 3 typing samples required"
        )

    users[username]["typing_profile"] = extract_features(typing_samples)

    return {
        "status": "success",
        "message": "Typing behavior enrolled"
    }
