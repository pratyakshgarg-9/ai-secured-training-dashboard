from fastapi import APIRouter
from database import login_history

router = APIRouter()

@router.get("/admin/logins")
def get_login_history():
    return login_history
