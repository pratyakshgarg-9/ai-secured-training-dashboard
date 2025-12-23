from fastapi import APIRouter
from database import sessions

router = APIRouter()

@router.get("/portfolio")
def portfolio(username: str):
    session = sessions.get(username)

    if not session:
        return {"locked": True}

    if session["access"] == "PARTIAL" and not session["verified"]:
        return {"locked": True}

    return {
        "locked": False,
        "balance": "₹4,25,000",
        "stocks": ["INFY", "TCS", "RELIANCE"]
    }
@router.get("/session")
def get_session(username: str):
    return sessions.get(username, {})

