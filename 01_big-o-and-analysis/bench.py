"""
Lightweight benchmarking utilities.

This module measures runtimes for a function under different input sizes n.
It tries to be "honest enough" without becoming a full benchmarking framework:

- Uses time.perf_counter() for high-resolution timing.
- Supports warmups (to reduce one-time effects like imports/caches/branch training).
- Uses repeats and takes a robust summary (median) to reduce noise.
- Can adapt the number of loop iterations so each measurement is long enough
  (avoids "timer resolution dominated" results).

Design:
- You provide a callable `make_input(n)` to build inputs of size n.
- You provide a callable `func(x)` to benchmark on that input.
"""

from __future__ import annotations

from dataclasses import dataclass
import statistics
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class BenchConfig:
    warmup_runs: int = 2  # runs done once per n (not recorded)
    repeats: int = 7  # recorded measurements per n
    min_time_per_repeat: float = 0.02  # seconds; ensure each repeat is "long enough"
    max_loops: int = 1_000_000  # safety cap so we don't loop forever
    collect_distribution: bool = False  # if True, keep per-repeat timing samples


@dataclass
class BenchResult:
    n: int
    seconds: float  # representative runtime (median seconds per single call)
    loops: int  # number of loops used per repeat
    samples: Optional[List[float]] = None  # per-repeat per-call seconds, if collected


def _time_call(func: Callable[[], Any], loops: int) -> float:
    """
    Time `loops` executions of func() and return total seconds.
    """
    start = time.perf_counter()
    for _ in range(loops):
        func()
    end = time.perf_counter()
    return end - start


def _choose_loops(func: Callable[[], Any], cfg: BenchConfig) -> int:
    """
    Choose a loop count so that total time is at least cfg.min_time_per_repeat
    (unless the function is extremely slow already).

    Strategy:
    - Start with 1 loop.
    - Exponentially increase until threshold reached or max_loops.
    """
    loops = 1
    total = _time_call(func, loops)
    if total <= 0:
        total = 1e-12

    # If one call already exceeds the threshold, stick to loops=1
    if total >= cfg.min_time_per_repeat:
        return 1

    while total < cfg.min_time_per_repeat and loops < cfg.max_loops:
        loops *= 2
        total = _time_call(func, loops)
        if total <= 0:
            total = 1e-12

    return min(loops, cfg.max_loops)


def benchmark_one_n(
        func: Callable[[Any], Any],
        make_input: Callable[[int], Any],
        n: int,
        cfg: BenchConfig = BenchConfig(),
) -> BenchResult:
    """
    Benchmark `func` for a single input size n.

    Returns a BenchResult where `seconds` is median seconds per single func(input).
    """
    x = make_input(n)

    def thunk() -> Any:
        return func(x)

    # Warmup runs (unmeasured)
    for _ in range(max(0, cfg.warmup_runs)):
        thunk()

    loops = _choose_loops(thunk, cfg)

    per_call_samples: List[float] = []
    for _ in range(max(1, cfg.repeats)):
        total = _time_call(thunk, loops)
        per_call = total / loops
        per_call_samples.append(per_call)

    median = statistics.median(per_call_samples)

    return BenchResult(
        n=n,
        seconds=median,
        loops=loops,
        samples=per_call_samples if cfg.collect_distribution else None,
    )


def benchmark_series(
        func: Callable[[Any], Any],
        make_input: Callable[[int], Any],
        n_values: Sequence[int],
        cfg: BenchConfig = BenchConfig(),
) -> List[BenchResult]:
    """
    Benchmark `func` across many n values.
    """
    results: List[BenchResult] = []
    for n in n_values:
        results.append(benchmark_one_n(func, make_input, n, cfg))
    return results


def to_xy(results: Sequence[BenchResult]) -> Tuple[List[int], List[float]]:
    """
    Convert BenchResult list into (n_values, seconds_values).
    """
    ns = [r.n for r in results]
    ys = [r.seconds for r in results]
    return ns, ys


# Small demo
if __name__ == "__main__":
    # Example: sum of a list (O(n))
    def make_list(n: int) -> list[int]:
        return list(range(n))


    def f(xs: list[int]) -> int:
        return sum(xs)


    ns = [10_000, 20_000, 40_000, 80_000, 160_000]
    cfg = BenchConfig(warmup_runs=2, repeats=9, min_time_per_repeat=0.03)
    res = benchmark_series(f, make_list, ns, cfg)

    for r in res:
        print(f"n={r.n:<7d} median={r.seconds:.6e}s loops={r.loops}")
