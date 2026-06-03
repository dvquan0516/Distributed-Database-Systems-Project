import numpy as np


def calculate_stats(values):
    values = np.array(values)

    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "p99": float(np.percentile(values, 99)),
        "std": float(np.std(values))
    }