"""
Goal:
Introduce CPU and memory profiling.

This file builds on previous benchmarking by adding:
- CPU profiling using cProfile
- function-level timing breakdown
- memory profiling using tracemalloc
- identifying hotspots and bottlenecks

Logical sequence:
1. benchmark_timer.py
2. input_scaling_benchmark.py
3. cpu_and_memory_profiling.py
4. algorithm_comparison.py

What this file teaches:
- where time is spent (not just how much)
- how to identify bottlenecks
- how memory usage evolves during execution
"""

from __future__ import annotations

import cProfile
import pstats
import tracemalloc
from typing import List


# ----------------------------
# Example workload
# ----------------------------

def slow_fibonacci(n: int) -> int:
    """
    Intentionally slow recursive Fibonacci (exponential time).
    """
    if n <= 1:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


def fast_fibonacci(n: int) -> int:
    """
    Efficient iterative Fibonacci (linear time).
    """
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def allocate_memory(n: int) -> List[int]:
    """
    Function that allocates memory to demonstrate memory profiling.
    """
    return [i * i for i in range(n)]


# ----------------------------
# CPU Profiling
# ----------------------------

def profile_cpu(func, *args, sort_by: str = "cumtime", limit: int = 10) -> None:
    """
    Profile CPU usage of a function.

    Args:
        func: function to profile
        *args: arguments for the function
        sort_by: sorting key (e.g., 'time', 'cumtime')
        limit: number of lines to print
    """
    profiler = cProfile.Profile()
    profiler.enable()

    func(*args)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats(sort_by)

    print(f"\n--- CPU Profile ({func.__name__}) ---")
    stats.print_stats(limit)


# ----------------------------
# Memory Profiling
# ----------------------------

def profile_memory(func, *args) -> None:
    """
    Profile memory usage of a function using tracemalloc.
    """
    tracemalloc.start()

    func(*args)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\n--- Memory Profile ({func.__name__}) ---")
    print(f"Current memory usage: {current / 1024:.2f} KB")
    print(f"Peak memory usage:    {peak / 1024:.2f} KB")


# ----------------------------
# Demo
# ----------------------------

def demo() -> None:
    """
    Demonstrate CPU and memory profiling.
    """
    n_fib = 30
    n_mem = 100_000

    print("=== CPU Profiling Demo ===")
    print(f"Fibonacci input: n = {n_fib}")

    profile_cpu(slow_fibonacci, n_fib)
    profile_cpu(fast_fibonacci, n_fib)

    print("\n=== Memory Profiling Demo ===")
    print(f"Memory allocation size: n = {n_mem}")

    profile_memory(allocate_memory, n_mem)

    print("\nTakeaway:")
    print("- CPU profiling shows where time is spent.")
    print("- Recursive algorithms can explode in cost (slow_fibonacci).")
    print("- Memory profiling reveals allocation patterns.")
    print("- Optimization requires identifying real bottlenecks first.")


if __name__ == "__main__":
    demo()
