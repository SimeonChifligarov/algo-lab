"""
Big-O & Analysis mini-tool (CLI)

This script ties everything together:
- pick an algorithm "case" (or run all)
- benchmark across input sizes n
- fit measured runtimes against growth models:
    1, log n, n, n log n, n^2, n^3
- print a small report (and optionally save CSV)

Run examples:
    python main.py --list
    python main.py --case linear_sum
    python main.py --case sort --ns 2000,4000,8000,16000,32000
    python main.py --all
    python main.py --case quadratic_pairs --start 150 --factor 2 --steps 6
    python main.py --case sort --csv out.csv

Files expected with this one:
    growth_models.py
    bench.py
    cases.py
"""

from __future__ import annotations

import argparse
import csv
import sys
from typing import Iterable, List, Optional, Sequence, Tuple

from bench import BenchConfig, benchmark_series, to_xy
from cases import DEFAULT_CASES, get_case, list_cases, geometric_ns
from growth_models import fit_all_models, best_model


def _parse_ns_csv(s: str) -> List[int]:
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if not parts:
        raise ValueError("Empty --ns list")
    ns: List[int] = []
    for p in parts:
        n = int(p)
        if n <= 0:
            raise ValueError("All n must be positive")
        ns.append(n)
    return ns


def _fmt_sec(x: float) -> str:
    # human-ish compact formatting
    if x == 0:
        return "0"
    if x < 1e-6:
        return f"{x * 1e9:.2f} ns"
    if x < 1e-3:
        return f"{x * 1e6:.2f} µs"
    if x < 1:
        return f"{x * 1e3:.2f} ms"
    return f"{x:.3f} s"


def _clamp_ns_for_case(case_name: str, ns: Sequence[int]) -> Tuple[List[int], Optional[str]]:
    """
    Safety clamps for very slow cases.
    Returns (possibly adjusted ns, optional warning message).
    """
    ns2 = list(ns)

    if case_name == "cubic_triples":
        # n^3 blows up fast: clamp fairly aggressively
        max_n = 120
        before = ns2[:]
        ns2 = [n for n in ns2 if n <= max_n]
        if not ns2:
            ns2 = [min(max_n, min(before))]
        if before != ns2:
            return ns2, f"Clamped n for cubic_triples to <= {max_n} to avoid extremely long runs."
    return ns2, None


def _print_table(rows: List[Tuple[int, float, int]]) -> None:
    # rows: (n, seconds, loops)
    print("Measurements (median per-call):")
    print(f"{'n':>10}  {'time':>12}  {'loops':>8}")
    print("-" * 36)
    for n, sec, loops in rows:
        print(f"{n:>10d}  {_fmt_sec(sec):>12}  {loops:>8d}")
    print()


def _report_fit(ns: List[int], ys: List[float]) -> None:
    results = fit_all_models(ns, ys)
    top = results[:3]
    winner = top[0]

    print("Best fit:")
    print(f"  model: {winner.model.name}")
    print(f"  y ≈ a*f(n) + b with a={winner.a:.6e}, b={winner.b:.6e}")
    print(f"  R²={winner.r2:.6f}, RMSE={winner.rmse:.6e} seconds")
    print()

    print("Top 3 models:")
    for r in top:
        print(f"  {r.model.name:7s}  R²={r.r2:.6f}  RMSE={r.rmse:.6e}")
    print()


def _run_one_case(
        case_name: str,
        ns: Sequence[int],
        cfg: BenchConfig,
        csv_path: Optional[str] = None,
) -> None:
    case = get_case(case_name)

    ns2, warn = _clamp_ns_for_case(case.name, ns)
    if warn:
        print(f"[note] {warn}\n")

    print("=" * 72)
    print(f"Case: {case.name}")
    print(f"Desc: {case.description}")
    print(f"ns:   {list(ns2)}")
    print("=" * 72)

    results = benchmark_series(case.func, case.make_input, ns2, cfg)
    rows = [(r.n, r.seconds, r.loops) for r in results]
    _print_table(rows)

    n_values, y_values = to_xy(results)
    _report_fit(n_values, y_values)

    if csv_path:
        # If running multiple cases to the same CSV, we'll append and write a header once.
        write_header = False
        try:
            with open(csv_path, "r", newline=""):
                pass
        except FileNotFoundError:
            write_header = True

        with open(csv_path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["case", "n", "median_seconds", "loops"])
            for r in results:
                w.writerow([case.name, r.n, f"{r.seconds:.12e}", r.loops])

        print(f"Wrote CSV rows to: {csv_path}\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Big-O intuition tool: benchmark + fit growth models.")
    p.add_argument("--list", action="store_true", help="List available cases and exit.")
    p.add_argument("--case", type=str, help="Case name to run (see --list).")
    p.add_argument("--all", action="store_true", help="Run all cases.")
    p.add_argument("--ns", type=str, help="Comma-separated n values, e.g. 1000,2000,4000")
    p.add_argument("--start", type=int, default=0, help="Generate geometric ns: start (with --factor/--steps).")
    p.add_argument("--factor", type=int, default=2, help="Geometric factor for generated ns.")
    p.add_argument("--steps", type=int, default=0, help="Number of ns points to generate.")
    p.add_argument("--warmups", type=int, default=2, help="Warmup runs per n (unmeasured).")
    p.add_argument("--repeats", type=int, default=7, help="Recorded repeats per n (median taken).")
    p.add_argument("--min-time", type=float, default=0.02, help="Minimum seconds per repeat via looping.")
    p.add_argument("--csv", type=str, default=None, help="Optional CSV path to append results.")

    args = p.parse_args(argv)

    if args.list:
        print("Available cases:")
        for c in DEFAULT_CASES:
            print(f"  {c.name:15s}  {c.description}")
        return 0

    if not args.case and not args.all:
        # default: run one reasonable example so the user gets output immediately
        args.case = "linear_sum"

    cfg = BenchConfig(
        warmup_runs=max(0, args.warmups),
        repeats=max(3, args.repeats),
        min_time_per_repeat=max(0.0, args.min_time),
        collect_distribution=False,
    )

    def choose_ns_for(case_name: str) -> List[int]:
        if args.ns:
            return _parse_ns_csv(args.ns)
        if args.start > 0 and args.steps > 0:
            return geometric_ns(args.start, max(2, args.factor), args.steps)
        # default from case
        return list(get_case(case_name).default_ns)

    if args.all:
        for c in DEFAULT_CASES:
            ns = choose_ns_for(c.name)
            _run_one_case(c.name, ns, cfg, csv_path=args.csv)
        return 0

    # single case
    case_name = args.case
    try:
        ns = choose_ns_for(case_name)
        _run_one_case(case_name, ns, cfg, csv_path=args.csv)
        return 0
    except KeyError as e:
        print(str(e), file=sys.stderr)
        print("Tip: use --list to see available cases.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
