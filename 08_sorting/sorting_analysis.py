"""
Design: Sorting — properties + tiny measurement helper (Part 3/4)

This module provides:
- A structured "properties table" for the algorithms in this lab
- A lightweight timing helper (median-of-repeats)
- A simple comparator that runs each algorithm on the same datasets and prints results

It is intentionally small (not a full benchmarking suite).
Use it to build intuition:
- stability differences (when sorting decorated records)
- performance differences across input shapes (sorted, reversed, random, many duplicates)

Next file:
4) test_sorting.py
"""

from __future__ import annotations

from dataclasses import dataclass
import random
import statistics
import time
from typing import Callable, Dict, List, Sequence, Tuple, Any, Optional

from sorting_algorithms import (
    insertion_sort,
    selection_sort,
    bubble_sort,
    merge_sort,
    quick_sort,
)
from non_comparison_sorts import counting_sort, radix_sort_lsd


@dataclass(frozen=True)
class SortProps:
    name: str
    stable: bool
    in_place: bool
    avg_time: str
    worst_time: str
    extra_space: str
    notes: str = ""


PROPERTIES: List[SortProps] = [
    SortProps("insertion_sort", stable=True, in_place=True, avg_time="O(n^2)", worst_time="O(n^2)", extra_space="O(1)",
              notes="Fast on nearly-sorted"),
    SortProps("selection_sort", stable=False, in_place=True, avg_time="O(n^2)", worst_time="O(n^2)", extra_space="O(1)",
              notes="Few swaps; not stable"),
    SortProps("bubble_sort", stable=True, in_place=True, avg_time="O(n^2)", worst_time="O(n^2)", extra_space="O(1)",
              notes="Educational; early-exit best O(n)"),
    SortProps("merge_sort", stable=True, in_place=False, avg_time="O(n log n)", worst_time="O(n log n)",
              extra_space="O(n)", notes="Stable; great worst-case"),
    SortProps("quick_sort", stable=False, in_place=False, avg_time="O(n log n)", worst_time="O(n^2)",
              extra_space="O(log n)", notes="Fast average; pivot-sensitive"),
    SortProps("counting_sort", stable=True, in_place=False, avg_time="O(n+R)", worst_time="O(n+R)", extra_space="O(R)",
              notes="Ints in small range"),
    SortProps("radix_sort_lsd", stable=True, in_place=False, avg_time="O(d(n+b))", worst_time="O(d(n+b))",
              extra_space="O(n+b)", notes="Non-negative ints"),
]

# Map algorithm name -> callable
SORTERS: Dict[str, Callable[[Sequence[Any]], List[Any]]] = {
    "insertion_sort": lambda a: insertion_sort(a),
    "selection_sort": lambda a: selection_sort(a),
    "bubble_sort": lambda a: bubble_sort(a),
    "merge_sort": lambda a: merge_sort(a),
    "quick_sort": lambda a: quick_sort(a),
    "counting_sort": lambda a: counting_sort(a),  # expects ints
    "radix_sort_lsd": lambda a: radix_sort_lsd(a),  # expects non-negative ints
}


# ----------------------------
# Tiny timing helper
# ----------------------------

def time_function(func: Callable[[], Any], *, warmups: int = 2, repeats: int = 7) -> float:
    """
    Return median runtime (seconds) over `repeats` runs.
    """
    for _ in range(max(0, warmups)):
        func()

    samples: List[float] = []
    for _ in range(max(1, repeats)):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        samples.append(t1 - t0)

    return statistics.median(samples)


def _fmt_sec(x: float) -> str:
    if x == 0:
        return "0"
    if x < 1e-6:
        return f"{x * 1e9:.2f} ns"
    if x < 1e-3:
        return f"{x * 1e6:.2f} µs"
    if x < 1:
        return f"{x * 1e3:.2f} ms"
    return f"{x:.3f} s"


# ----------------------------
# Dataset generators
# ----------------------------

def make_datasets(n: int, *, seed: int = 0) -> Dict[str, List[int]]:
    """
    Create a few standard datasets for intuition.
    """
    rng = random.Random(seed)
    base = [rng.randrange(0, n * 2) for _ in range(n)]
    return {
        "random": base,
        "sorted": sorted(base),
        "reversed": sorted(base, reverse=True),
        "many_dupes": [rng.randrange(0, 10) for _ in range(n)],
    }


# ----------------------------
# Comparison runner (print)
# ----------------------------

def compare_sorts(
        n: int = 2000,
        *,
        which: Optional[Sequence[str]] = None,
        seed: int = 0,
        warmups: int = 1,
        repeats: int = 5,
) -> List[Tuple[str, str, float]]:
    """
    Run each sorter on each dataset and print a small timing table.
    Returns list of (sorter_name, dataset_name, seconds).

    Note:
      O(n^2) sorts become slow quickly; keep n modest (e.g., <= 5000).
    """
    datasets = make_datasets(n, seed=seed)
    names = list(which) if which is not None else list(SORTERS.keys())

    results: List[Tuple[str, str, float]] = []

    print(f"\nComparing sorts at n={n} (median of {repeats} runs)")
    print("-" * 72)
    print(f"{'algorithm':18s} {'dataset':12s} {'time':>12s}")
    print("-" * 72)

    for alg in names:
        sorter = SORTERS[alg]
        for ds_name, data in datasets.items():
            # Some sorts have constraints
            if alg == "radix_sort_lsd" and any(x < 0 for x in data):
                continue

            # Each run should see the same input (copy)
            def run() -> None:
                sorter(list(data))

            sec = time_function(run, warmups=warmups, repeats=repeats)
            results.append((alg, ds_name, sec))
            print(f"{alg:18s} {ds_name:12s} {_fmt_sec(sec):>12s}")

    return results


def print_properties() -> None:
    """
    Print the properties table.
    """
    print("\nAlgorithm properties")
    print("-" * 110)
    print(f"{'name':16s} {'stable':6s} {'in_place':8s} {'avg':10s} {'worst':10s} {'space':8s} notes")
    print("-" * 110)
    for p in PROPERTIES:
        print(
            f"{p.name:16s} {str(p.stable):6s} {str(p.in_place):8s} {p.avg_time:10s} {p.worst_time:10s} {p.extra_space:8s} {p.notes}")
    print()


if __name__ == "__main__":
    print_properties()
    compare_sorts(n=1500, repeats=3)
