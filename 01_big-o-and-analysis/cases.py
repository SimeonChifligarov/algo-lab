"""
Benchmark "cases" (algorithms) that tend to exhibit familiar growth shapes.

Each Case provides:
- name: identifier used by the CLI/report
- make_input(n): builds an input object of size n
- func(x): the function to benchmark (should NOT mutate x)
- default_ns: reasonable n values to try (kept conservative for slower cases)

Important:
Our benchmark runner reuses the same input object for repeated timings at a given n.
So each func here is written to avoid mutating the provided input.
"""

from __future__ import annotations

from dataclasses import dataclass
import bisect
from typing import Any, Callable, Dict, List, Sequence


@dataclass(frozen=True)
class Case:
    name: str
    description: str
    make_input: Callable[[int], Any]
    func: Callable[[Any], Any]
    default_ns: Sequence[int]


# ----------------------------
# Helper generators
# ----------------------------

def geometric_ns(start: int, factor: int, steps: int) -> List[int]:
    """
    Generate sizes like: start, start*factor, start*factor^2, ...
    """
    ns: List[int] = []
    n = start
    for _ in range(steps):
        ns.append(int(n))
        n *= factor
    return ns


# ----------------------------
# Cases
# ----------------------------

def _make_list(n: int) -> List[int]:
    return list(range(n))


def _case_constant_index() -> Case:
    def make_input(n: int) -> List[int]:
        return _make_list(n)

    def func(xs: List[int]) -> int:
        # O(1): single indexed lookup
        return xs[len(xs) // 2]

    return Case(
        name="constant_index",
        description="O(1) list index lookup",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(10_000, 2, 6),
    )


def _case_binary_search() -> Case:
    def make_input(n: int) -> List[int]:
        # sorted list
        return _make_list(n)

    def func(xs: List[int]) -> int:
        # O(log n): binary search using bisect
        target = len(xs) - 1
        return bisect.bisect_left(xs, target)

    return Case(
        name="binary_search",
        description="O(log n) bisect on a sorted list",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(50_000, 2, 6),
    )


def _case_linear_sum() -> Case:
    def make_input(n: int) -> List[int]:
        return _make_list(n)

    def func(xs: List[int]) -> int:
        # O(n): sum
        return sum(xs)

    return Case(
        name="linear_sum",
        description="O(n) sum over a list",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(20_000, 2, 6),
    )


def _case_n_log_n_sort() -> Case:
    def make_input(n: int) -> List[int]:
        # Reverse order to make it "non-trivial", but Python's Timsort is adaptive.
        # Still commonly fits close-ish to n log n over typical ranges.
        return list(range(n, 0, -1))

    def func(xs: List[int]) -> List[int]:
        # O(n log n): return a sorted copy (does not mutate xs)
        return sorted(xs)

    return Case(
        name="sort",
        description="~O(n log n) sorted(xs) (Timsort; adaptive in practice)",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(5_000, 2, 6),
    )


def _case_quadratic_pairs() -> Case:
    def make_input(n: int) -> int:
        # For pure-loop cases, the input can just be n itself.
        return n

    def func(n: int) -> int:
        # O(n^2): double loop doing tiny constant work
        acc = 0
        for i in range(n):
            for j in range(n):
                acc += (i ^ j) & 1
        return acc

    return Case(
        name="quadratic_pairs",
        description="O(n^2) nested loops with tiny work",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(200, 2, 6),
    )


def _case_cubic_triples() -> Case:
    def make_input(n: int) -> int:
        return n

    def func(n: int) -> int:
        # O(n^3): triple loop; keep n small or it explodes fast
        acc = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    acc += (i + j + k) & 1
        return acc

    return Case(
        name="cubic_triples",
        description="O(n^3) triple loops (VERY slow; small n only)",
        make_input=make_input,
        func=func,
        default_ns=geometric_ns(25, 2, 6),  # 25, 50, 100, 200, 400, 800 (800^3 is too big!)
    )


# Note: cubic default above can still get huge quickly. We'll clamp in the CLI later.
# Keeping the values here makes it obvious how quickly n^3 grows.


DEFAULT_CASES: List[Case] = [
    _case_constant_index(),
    _case_binary_search(),
    _case_linear_sum(),
    _case_n_log_n_sort(),
    _case_quadratic_pairs(),
    _case_cubic_triples(),
]

_CASE_MAP: Dict[str, Case] = {c.name: c for c in DEFAULT_CASES}


def list_cases() -> List[str]:
    return [c.name for c in DEFAULT_CASES]


def get_case(name: str) -> Case:
    try:
        return _CASE_MAP[name]
    except KeyError as e:
        raise KeyError(f"Unknown case '{name}'. Available: {', '.join(list_cases())}") from e


if __name__ == "__main__":
    for c in DEFAULT_CASES:
        print(f"{c.name:15s}  {c.description}")
        print(f"  ns: {list(c.default_ns)}")
