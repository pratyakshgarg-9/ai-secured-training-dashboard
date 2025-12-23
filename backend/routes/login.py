from fastapi import APIRouter, HTTPException
import random
import time

from database import users, sessions, otp_tracker
from utils.fingerprint import generate_fingerprint, fingerprint_match
from utils.geo import geo_risk
from models.otp_model import otp_score
from models.fusion_engine import final_decision

router = APIRouter()


# -------------------------
# GENERATE OTP
# -------------------------
@router.post("/generate-otp")
def generate_otp(data: dict):
    username = data.get("username")

    if not username or username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    otp = random.randint(100000, 999999)

    otp_tracker[username] = {
        "otp": otp,
        "count": otp_tracker.get(username, {}).get("count", 0) + 1,
        "time": time.time()
    }

    if otp_tracker[username]["count"] > 5:
        return {"status": "blocked"}

    # Demo mode: return OTP
    return {"status": "otp_sent", "otp": otp}


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    otp = data.get("otp")
    fingerprint_data = data.get("fingerprint")
    location = data.get("location")
    hours = data.get("hours", 24)

    # -------------------------
    # BASIC VALIDATION
    # -------------------------
    if not username or not password or not otp:
        raise HTTPException(status_code=400, detail="Missing fields")

    user = users.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # -------------------------
    # OTP CHECK
    # -------------------------
    otp_data = otp_tracker.get(username)
    if not otp_data or otp_data["otp"] != otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    if time.time() - otp_data["time"] > 300:
        raise HTTPException(status_code=401, detail="OTP expired")

    # -------------------------
    # DEVICE FINGERPRINT CHECK
    # -------------------------
    incoming_fp = generate_fingerprint(fingerprint_data)
    stored_fp = user.get("fingerprint")

    if not stored_fp:
        # First ever login device → trust & store it
        match_score = 1.0
        user["fingerprint"] = incoming_fp
    else:
        match_score = fingerprint_match(incoming_fp, stored_fp)

    device_risk = 0.6 if match_score < 0.7 else 0.0

    # -------------------------
    # GEO CHECK
    # -------------------------
    geo = geo_risk(user.get("last_location"), location, hours)
    if geo == 1.0:
        return {"access": "BLOCK"}

    # -------------------------
    # OTP MISUSE RISK
    # -------------------------
    otp_risk = otp_score(otp_data["count"])

    # -------------------------
    # FINAL DECISION
    # -------------------------
    # -------------------------
# FINAL ACCESS DECISION
# -------------------------

# STRONG TRUST: same device + safe geo
    if match_score >= 0.7 and geo == 0.0:
        decision = "ALLOW"
        risk = 0.0
    else:
        decision, risk = final_decision(
        0.0,        # behavior risk
        geo,
        otp_risk,
        device_risk
    )


    # -------------------------
    # SESSION STORE
    # -------------------------
    sessions[username] = {
        "access": decision,
        "verified": decision == "ALLOW"
    }

    otp_tracker.pop(username, None)


    return {
        "access": decision,
        "risk": risk,
        "device_match": match_score >= 0.7
    }
    print("MATCH:", match_score, "GEO:", geo, "DEVICE_RISK:", device_risk)

