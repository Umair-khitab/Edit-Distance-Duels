# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 02:28:25 2025

@author: khita
"""

# benchmark_complexity.py
import time
from edit_distance import edit_distance_steps

def benchmark_pair(s1, s2, runs=50):
    """
    Measure average runtime (in ms) of edit_distance_steps(s1, s2)
    over `runs` repetitions.
    """
    start = time.perf_counter()
    for _ in range(runs):
        dist, dp, steps = edit_distance_steps(s1, s2)
    end = time.perf_counter()

    avg_ms = (end - start) / runs * 1000  # convert to milliseconds
    n, m = len(s1), len(s2)
    operations = (n + 1) * (m + 1)  # number of DP cells filled

    return {
        "s1": s1,
        "s2": s2,
        "n": n,
        "m": m,
        "distance": dist,
        "avg_ms": avg_ms,
        "operations": operations,
    }

def main():
    test_cases = [
        ("cat", "cut"),
        ("kitten", "sitting"),
        ("abcdef", "azced"),
        ("algorithm", "rhythm"),
        ("transformation", "transportation"),
    ]

    print(f"{'Word 1':15s} {'Word 2':15s} {'(n,m)':10s} {'Dist':6s} {'Avg time (ms)':15s} {'DP cells':10s}")
    print("-" * 80)

    for s1, s2 in test_cases:
        result = benchmark_pair(s1, s2, runs=100)
        print(f"{result['s1']:15s} "
              f"{result['s2']:15s} "
              f"({result['n']},{result['m']})   "
              f"{result['distance']:<6d} "
              f"{result['avg_ms']:<15.4f} "
              f"{result['operations']:<10d}")

if __name__ == "__main__":
    main()
