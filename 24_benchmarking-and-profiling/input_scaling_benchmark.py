"""
Goal:
Learn how performance changes as input size grows.

This file builds on benchmark_timer.py by adding:
- benchmarks across multiple input sizes
- empirical scaling analysis
- comparison between two algorithms
- a simple tabular report

Logical sequence:
1. benchmark_timer.py
2. input_scaling_benchmark.py
3. cpu_and_memory_profiling.py
4. algorithm_comparison.py

What this file teaches:
- single benchmarks can be misleading
- input scaling often reveals algorithmic differences
- empirical data helps connect theory and practice
"""

from __future__ import annotations

import statistics
import time
from typing import Any, Callable, Dict, List, Sequence


def benchmark(func: Callable[..., Any], *args: Any, repeats: int = 5, **kwargs: Any) -> Dict[str, float]:
    """
    Benchmark a function by running it multiple times.

    Returns summary statistics in seconds.
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


def linear_search(values: Sequence[int], target: int) -> int:
    """
    Return the index of target if found, otherwise -1.
    """
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def binary_search(values: Sequence[int], target: int) -> int:
    """
    Return the index of target in a sorted sequence if found, otherwise -1.
    """
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def run_scaling_benchmark(
        func: Callable[..., Any],
        sizes: Sequence[int],
        input_builder: Callable[[int], tuple[Any, ...]],
        repeats: int = 5,
) -> List[Dict[str, float]]:
    """
    Benchmark a function across multiple input sizes.

    Args:
        func: function to benchmark
        sizes: input sizes to test
        input_builder: builds argument tuple from each input size
        repeats: number of repeated runs per size

    Returns:
        A list of dictionaries containing benchmark results.
    """
    results: List[Dict[str, float]] = []

    for size in sizes:
        args = input_builder(size)
        timing = benchmark(func, *args, repeats=repeats)
        results.append(
            {
                "size": float(size),
                "min": timing["min"],
                "max": timing["max"],
                "mean": timing["mean"],
                "median": timing["median"],
            }
        )

    return results


def print_scaling_report(title: str, results: List[Dict[str, float]]) -> None:
    """
    Print a simple scaling report table.
    """
    print(title)
    print(f"{'size':>10} | {'mean':>12} | {'median':>12} | {'min':>12} | {'max':>12}")
    print("-" * 70)

    for row in results:
        size = int(row["size"])
        mean = format_seconds(row["mean"])
        median = format_seconds(row["median"])
        min_time = format_seconds(row["min"])
        max_time = format_seconds(row["max"])
        print(f"{size:>10} | {mean:>12} | {median:>12} | {min_time:>12} | {max_time:>12}")


def demo() -> None:
    """
    Demonstrate scaling benchmarks for linear search vs binary search.
    """
    sizes = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000]
    repeats = 10

    def build_search_input(size: int) -> tuple[list[int], int]:
        data = list(range(size))
        target = size - 1  # worst case for linear search, valid case for binary search
        return data, target

    print("=== Input Scaling Benchmark Demo ===")
    print(f"Sizes:   {sizes}")
    print(f"Repeats: {repeats}")
    print()

    linear_results = run_scaling_benchmark(
        linear_search,
        sizes,
        build_search_input,
        repeats=repeats,
    )

    binary_results = run_scaling_benchmark(
        binary_search,
        sizes,
        build_search_input,
        repeats=repeats,
    )

    print_scaling_report("Linear Search", linear_results)
    print()
    print_scaling_report("Binary Search", binary_results)
    print()

    print("Takeaway:")
    print("- Linear search tends to grow roughly in proportion to n.")
    print("- Binary search grows much more slowly, roughly like log2(n).")
    print("- Input scaling benchmarks help reveal algorithmic complexity in practice.")


if __name__ == "__main__":
    demo()
