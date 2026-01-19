from typing import List, Dict
import statistics

def monthly_average(records: List[Dict]) -> float:
    if not records:
        return 0.0
    vals = [r["value"] for r in records]
    return statistics.mean(vals)

def moving_average(records: List[Dict], window: int = 3) -> List[float]:
    vals = [r["value"] for r in records]
    if window <= 0:
        raise ValueError("window must be >= 1")
    if len(vals) < window:
        return []
    ma = []
    for i in range(len(vals) - window + 1):
        ma.append(sum(vals[i:i+window]) / window)
    return ma

def month_over_month_change(records: List[Dict]) -> List[float]:
    vals = [r["value"] for r in records]
    changes = []
    for prev, cur in zip(vals, vals[1:]):
        if prev == 0:
            changes.append(float("inf"))
        else:
            changes.append((cur - prev) / prev * 100.0)
    return changes
