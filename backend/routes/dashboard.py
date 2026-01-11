from fastapi import APIRouter
from database import sessions

router = APIRouter()

@router.get("/session")
def session(username: str):
    return sessions.get(username, {"access": "PARTIAL", "verified": False})

@router.get("/portfolio")
def portfolio(username: str):
    sess = sessions.get(username)
    if not sess:
        return {"locked": True}

    # ✅ lock portfolio in PARTIAL mode
    if sess["access"] == "PARTIAL" and not sess.get("verified", False):
        return {"locked": True}

    return {"locked": False}
