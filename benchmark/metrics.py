import numpy as np


def calculate_stats(values):
    values = np.array(values)

    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "p95": float(np.percentile(values, 95)),
        "p99": float(np.percentile(values, 99)),
        "std": float(np.std(values))
    }