from fastapi import APIRouter, HTTPException, Request
import random, time

from database import users, sessions, otp_tracker, login_history
from utils.fingerprint import generate_fingerprint, fingerprint_match
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

    # store OTP to admin log table (demo)
    login_history.append({
        "user": username,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "otp": otp,
        "risk": None,
        "decision": None
    })

    if otp_tracker[username]["count"] > 5:
        return {"status": "blocked"}

    # IMPORTANT: do NOT return OTP here
    return {"status": "otp_generated"}


@router.post("/login")
def login(data: dict, request: Request):
    username = data.get("username")
    password = data.get("password")
    otp = data.get("otp")
    fp_data = data.get("fingerprint")

    user = users.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    otp_data = otp_tracker.get(username)
    if not otp_data:
        raise HTTPException(status_code=401, detail="OTP not generated")
    if otp_data["otp"] != otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # expire OTP after 5 minutes
    if time.time() - otp_data["time"] > 300:
        raise HTTPException(status_code=401, detail="OTP expired")

    # device check
    incoming_fp = generate_fingerprint(fp_data or {})
    stored_fp = user.get("fingerprint")

    match_score = fingerprint_match(incoming_fp, stored_fp)
    device_risk = 0.6 if match_score < 0.7 else 0.0

    # geo check using IP lookup
    ip = get_client_ip(request)
    location = ip_to_geo(ip)

    geo = geo_risk(user.get("last_location"), location, 24)
    if geo == 1.0:
        decision, risk = "BLOCK", 1.0
        sessions[username] = {"access": "BLOCK", "verified": False}
        return {"access": "BLOCK", "risk": 1.0}

    # otp abuse risk
    otp_risk = otp_score(otp_data["count"])

    decision, risk = final_decision(
        0.0,
        geo,
        otp_risk,
        device_risk
    )

    # IMPORTANT SESSION RULE:
    # if device mismatch → allow dashboard but lock portfolio
    verified = match_score >= 0.7
    if not verified and decision == "ALLOW":
        decision = "PARTIAL"

    sessions[username] = {
        "access": decision,
        "verified": verified
    }

    # update last location
    user["last_location"] = location

    # clear otp
    otp_tracker.pop(username, None)

    # update last admin record
    login_history[-1]["risk"] = risk
    login_history[-1]["decision"] = decision

    return {"access": decision, "risk": risk}
