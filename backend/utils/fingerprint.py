import hashlib
import json

def generate_fingerprint(fp_data: dict) -> str:
    raw = json.dumps(fp_data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def fingerprint_match(fp1: str, fp2: str) -> float:
    if not fp1 or not fp2:
        return 0.0
    return 1.0 if fp1 == fp2 else 0.0


