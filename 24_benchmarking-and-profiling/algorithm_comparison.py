"""
Goal:
Compare algorithms empirically and understand time/space trade-offs.

This file ties together the ideas from:
1. benchmark_timer.py
2. input_scaling_benchmark.py
3. cpu_and_memory_profiling.py
4. algorithm_comparison.py

What this file teaches:
- how to compare multiple algorithms on the same task
- how empirical performance can differ from theoretical expectations
- how preprocessing can improve query time
- how time and space trade-offs appear in practice

Example task:
Membership testing: "Is target in the data?"

Algorithms compared:
- linear search on a list
- binary search on a sorted list
- hash-based lookup using a set

Trade-offs:
- linear search: no preprocessing, slow queries
- binary search: requires sorted data
- set lookup: extra memory, usually very fast queries
"""

from __future__ import annotations

import statistics
import time
from typing import Callable, Dict, List, Sequence


def benchmark(func: Callable[..., object], *args: object, repeats: int = 5, **kwargs: object) -> Dict[str, float]:
    """
    Benchmark a function by running it multiple times.

    Returns summary timing statistics in seconds.
    """
    if repeats < 1:
        raise ValueError("repeats must be at least 1")

    timings: List[float] = []

    for _ in range(repeats):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        timings.append(end - start)

    return {
        "min": min(timings),
        "max": max(timings),
        "mean": statistics.mean(timings),
        "median": statistics.median(timings),
    }


def format_seconds(seconds: float) -> str:
    """
    Format a duration in seconds into a readable string.
    """
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    if seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    return f"{seconds:.6f} s"


def linear_search(values: Sequence[int], target: int) -> bool:
    """
    Return True if target is in values, else False.
    """
    for value in values:
        if value == target:
            return True
    return False


def binary_search(values: Sequence[int], target: int) -> bool:
    """
    Return True if target is in a sorted sequence, else False.
    """
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return True
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def set_lookup(values: set[int], target: int) -> bool:
    """
    Return True if target is in the set, else False.
    """
    return target in values


def print_comparison_table(results: List[Dict[str, object]]) -> None:
    """
    Print a comparison table for benchmark results.
    """
    print(f"{'algorithm':<18} | {'mean':>12} | {'median':>12} | {'min':>12} | {'max':>12}")
    print("-" * 78)

    for row in results:
        name = str(row["algorithm"])
        mean = format_seconds(float(row["mean"]))
        median = format_seconds(float(row["median"]))
        min_time = format_seconds(float(row["min"]))
        max_time = format_seconds(float(row["max"]))

        print(f"{name:<18} | {mean:>12} | {median:>12} | {min_time:>12} | {max_time:>12}")


def demo() -> None:
    """
    Demonstrate empirical comparison of three approaches to membership testing.
    """
    size = 1_000_000
    repeats = 20
    target = size - 1

    data = list(range(size))
    sorted_data = data
    set_data = set(data)

    print("=== Algorithm Comparison Demo ===")
    print(f"Data size: {size}")
    print(f"Target:    {target}")
    print(f"Repeats:   {repeats}")
    print()

    # correctness check
    print("Correctness check:")
    print(f"  linear_search -> {linear_search(data, target)}")
    print(f"  binary_search -> {binary_search(sorted_data, target)}")
    print(f"  set_lookup    -> {set_lookup(set_data, target)}")
    print()

    linear_results = benchmark(linear_search, data, target, repeats=repeats)
    binary_results = benchmark(binary_search, sorted_data, target, repeats=repeats)
    set_results = benchmark(set_lookup, set_data, target, repeats=repeats)

    results = [
        {"algorithm": "linear_search", **linear_results},
        {"algorithm": "binary_search", **binary_results},
        {"algorithm": "set_lookup", **set_results},
    ]

    print_comparison_table(results)
    print()

    print("Interpretation:")
    print("- Linear search uses little extra space, but query time grows with n.")
    print("- Binary search is much faster, but only works on sorted data.")
    print("- Set lookup is typically fastest, but requires extra memory.")
    print("- The best choice depends on workload, memory budget, and preprocessing cost.")


if __name__ == "__main__":
    demo()
