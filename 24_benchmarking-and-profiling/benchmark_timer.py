"""
Goal:
Introduce basic benchmarking by measuring execution time.

This is the first file in a logical sequence for benchmarking and profiling:
1. benchmark_timer.py
2. input_scaling_benchmark.py
3. cpu_and_memory_profiling.py
4. algorithm_comparison.py

What this file teaches:
- how to measure execution time
- why repeated runs matter
- how to summarize timing results
- how to avoid modifying benchmarked code too much

Notes:
- This uses time.perf_counter(), which is appropriate for benchmarking
- Benchmarks are noisy, so we run a function multiple times
- This is a simple educational benchmark, not a full benchmarking framework
"""

from __future__ import annotations

import statistics
import time
from typing import Any, Callable, Dict, List


def benchmark(func: Callable[..., Any], *args: Any, repeats: int = 5, **kwargs: Any) -> Dict[str, float]:
    """
    Benchmark a function by running it multiple times.

    Args:
        func: function to benchmark
        *args: positional arguments for the function
        repeats: number of times to run the function
        **kwargs: keyword arguments for the function

    Returns:
        A dictionary with summary timing statistics in seconds:
        - min
        - max
        - mean
        - median

    Raises:
        ValueError: if repeats is less than 1
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


def print_benchmark_report(name: str, results: Dict[str, float]) -> None:
    """
    Print benchmark results in a readable way.
    """
    print(f"Benchmark: {name}")
    print(f"  min:    {format_seconds(results['min'])}")
    print(f"  max:    {format_seconds(results['max'])}")
    print(f"  mean:   {format_seconds(results['mean'])}")
    print(f"  median: {format_seconds(results['median'])}")


def sum_of_squares(n: int) -> int:
    """
    Example function to benchmark.

    Computes:
        1^2 + 2^2 + ... + n^2
    """
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


def sum_of_squares_formula(n: int) -> int:
    """
    Faster mathematical version for comparison.
    """
    return n * (n + 1) * (2 * n + 1) // 6


def demo() -> None:
    """
    Demonstrate basic benchmarking on two implementations of the same task.
    """
    n = 100_000
    repeats = 10

    print("=== Basic Benchmarking Demo ===")
    print(f"Input size: n = {n}")
    print(f"Repeats:    {repeats}")
    print()

    iterative_results = benchmark(sum_of_squares, n, repeats=repeats)
    formula_results = benchmark(sum_of_squares_formula, n, repeats=repeats)

    print_benchmark_report("sum_of_squares (iterative)", iterative_results)
    print()
    print_benchmark_report("sum_of_squares_formula", formula_results)
    print()

    iterative_value = sum_of_squares(n)
    formula_value = sum_of_squares_formula(n)

    print("Correctness check:")
    print(f"  iterative result == formula result -> {iterative_value == formula_value}")
    print()

    print("Takeaway:")
    print("- Benchmarking helps compare implementations empirically.")
    print("- Running multiple repeats reduces the effect of timing noise.")
    print("- Faster code is not always better if it uses more memory or is harder to maintain.")


if __name__ == "__main__":
    demo()
