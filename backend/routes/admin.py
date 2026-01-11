from fastapi import APIRouter
from database import login_history

router = APIRouter()

@router.get("/admin/logs")
def get_login_history():
    return login_history
