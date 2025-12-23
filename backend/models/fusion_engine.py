def final_decision(b, g, o, d):
    risk = 0.4*b + 0.3*g + 0.2*o + 0.1*d
    if g == 1.0:
        return "BLOCK", risk
    if risk > 0.8:
        return "BLOCK", risk
    if risk > 0.6:
        return "PARTIAL", risk
    return "FULL", risk
