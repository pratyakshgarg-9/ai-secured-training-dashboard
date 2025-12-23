import numpy as np

def extract_features(samples):
    delays = []
    for s in samples:
        delays.extend(np.diff(s))
    return {
        "avg": float(np.mean(delays)),
        "std": float(np.std(delays))
    }
