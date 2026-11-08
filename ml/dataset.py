import random
import numpy as np
import pandas as pd
from engine.metrics import run_all

DISK_SIZE = 200


def make_workload():
    n = random.randint(5, 30)
    head = random.randint(0, DISK_SIZE - 1)
    kind = random.choice(["uniform", "clustered", "one_side", "both_ends"])

    if kind == "uniform":
        reqs = [random.randint(0, DISK_SIZE - 1) for _ in range(n)]
    elif kind == "clustered":
        center = random.randint(20, DISK_SIZE - 20)
        reqs = [min(DISK_SIZE - 1, max(0, int(random.gauss(center, 10)))) for _ in range(n)]
    elif kind == "one_side":
        reqs = [random.randint(head, DISK_SIZE - 1) for _ in range(n)]
    else:
        reqs = [random.choice([random.randint(0, 30), random.randint(DISK_SIZE - 31, DISK_SIZE - 1)]) for _ in range(n)]
    return reqs, head


def extract_features(reqs, head):
    arr = np.array(reqs)
    return {
        "n": len(reqs),
        "head": head,
        "mean": arr.mean(),
        "std": arr.std(),
        "spread": arr.max() - arr.min(),
        "dist_to_mean": abs(arr.mean() - head),
        "frac_right": (arr >= head).mean(),
    }


def build_dataset(samples=3000, seed=42):
    random.seed(seed)
    rows = []
    for _ in range(samples):
        reqs, head = make_workload()
        summary = run_all(reqs, head, DISK_SIZE)
        best = min(summary, key=lambda a: summary[a]["total_seek"])
        row = extract_features(reqs, head)
        row["best"] = best
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build_dataset()
    df.to_csv("data/dataset.csv", index=False)
    print(df["best"].value_counts())