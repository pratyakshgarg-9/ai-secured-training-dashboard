def otp_score(req):
    return 1.0 if req > 5 else req * 0.1
