from fastapi import APIRouter, HTTPException, Request
import random, time

from database import users, sessions, otp_tracker, login_history
from utils.fingerprint import fingerprint_match
from utils.geo import geo_risk
from utils.ip_utils import get_client_ip
from utils.ip_geo import ip_to_geo
from models.otp_model import otp_score
from models.fusion_engine import final_decision

router = APIRouter()

@router.post("/generate-otp")
def generate_otp(data: dict):
    username = data.get("username")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    otp = random.randint(100000, 999999)

    otp_tracker[username] = {
        "otp": otp,
        "count": otp_tracker.get(username, {}).get("count", 0) + 1,
        "time": time.time()
    }

    login_history.append({
        "user": username,
        "otp": otp,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })

    if otp_tracker[username]["count"] > 5:
        return {"status": "blocked"}

    return {"status": "otp_generated"}


@router.post("/login")
def login(data: dict, request: Request):
    username = data.get("username")
    password = data.get("password")
    otp = data.get("otp")
    incoming_fp = data.get("fingerprint")

    user = users.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401)

    otp_data = otp_tracker.get(username)
    if not otp_data or otp_data["otp"] != otp:
        raise HTTPException(status_code=401)

    ip = get_client_ip(request)
    location = ip_to_geo(ip)

    last_location = user.get("last_location")
    geo = geo_risk(last_location, location, 24)

    stored_fp = user.get("fingerprint")
    if not stored_fp:
        match_score = 1.0
        user["fingerprint"] = incoming_fp
    else:
        match_score = fingerprint_match(incoming_fp, stored_fp)

    device_risk = 0.6 if match_score < 0.7 else 0.0
    otp_risk = otp_score(otp_data["count"])

    decision, risk = final_decision(
        0.0,
        geo,
        otp_risk,
        device_risk
    )

    sessions[username] = {
        "access": decision,
        "verified": match_score >= 0.7
    }

    user["last_location"] = location
    otp_tracker.pop(username, None)

    login_history[-1]["risk"] = risk
    login_history[-1]["decision"] = decision

    return {
        "access": decision,
        "risk": risk
    }
