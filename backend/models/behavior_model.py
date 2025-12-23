def behavior_score(baseline, current):
    diff = abs(baseline["avg"] - current["avg"])
    return min(diff / 300, 1.0)
