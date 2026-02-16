# main.py
"""
Big-O & Analysis mini-tool (interactive)

This is the same "tie everything together" script, but instead of CLI arguments
it uses input() prompts.

Files expected next to this one:
  - growth_models.py
  - bench.py
  - cases.py
"""

from __future__ import annotations

import csv
from typing import List, Optional, Sequence, Tuple

from bench import BenchConfig, benchmark_series, to_xy
from cases import DEFAULT_CASES, get_case, list_cases, geometric_ns
from growth_models import fit_all_models


def _parse_ns_csv(s: str) -> List[int]:
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if not parts:
        raise ValueError("Empty n list")
    ns: List[int] = []
    for p in parts:
        n = int(p)
        if n <= 0:
            raise ValueError("All n must be positive")
        ns.append(n)
    return ns


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


def _clamp_ns_for_case(case_name: str, ns: Sequence[int]) -> Tuple[List[int], Optional[str]]:
    ns2 = list(ns)
    if case_name == "cubic_triples":
        max_n = 120
        before = ns2[:]
        ns2 = [n for n in ns2 if n <= max_n]
        if not ns2:
            ns2 = [min(max_n, min(before))]
        if before != ns2:
            return ns2, f"Clamped n for cubic_triples to <= {max_n} to avoid extremely long runs."
    return ns2, None


def _print_table(rows: List[Tuple[int, float, int]]) -> None:
    print("Measurements (median per-call):")
    print(f"{'n':>10}  {'time':>12}  {'loops':>8}")
    print("-" * 36)
    for n, sec, loops in rows:
        print(f"{n:>10d}  {_fmt_sec(sec):>12}  {loops:>8d}")
    print()


def _report_fit(ns: List[int], ys: List[float]) -> None:
    results = fit_all_models(ns, ys)
    winner = results[0]
    top = results[:3]

    print("Best fit:")
    print(f"  model: {winner.model.name}")
    print(f"  y ≈ a*f(n) + b with a={winner.a:.6e}, b={winner.b:.6e}")
    print(f"  R²={winner.r2:.6f}, RMSE={winner.rmse:.6e} seconds")
    print()

    print("Top 3 models:")
    for r in top:
        print(f"  {r.model.name:7s}  R²={r.r2:.6f}  RMSE={r.rmse:.6e}")
    print()


def _append_csv(csv_path: str, case_name: str, results) -> None:
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
            w.writerow([case_name, r.n, f"{r.seconds:.12e}", r.loops])


def _run_one_case(case_name: str, ns: Sequence[int], cfg: BenchConfig, csv_path: Optional[str]) -> None:
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
        _append_csv(csv_path, case.name, results)
        print(f"Wrote CSV rows to: {csv_path}\n")


# ----------------------------
# Interactive helpers
# ----------------------------

def _ask(prompt: str, default: Optional[str] = None) -> str:
    if default is None:
        s = input(prompt).strip()
        return s
    s = input(f"{prompt} [{default}]: ").strip()
    return s if s else default


def _ask_int(prompt: str, default: int, min_value: Optional[int] = None) -> int:
    while True:
        s = _ask(prompt, str(default))
        try:
            v = int(s)
            if min_value is not None and v < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")


def _ask_float(prompt: str, default: float, min_value: Optional[float] = None) -> float:
    while True:
        s = _ask(prompt, str(default))
        try:
            v = float(s)
            if min_value is not None and v < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid number.")


def _ask_yes_no(prompt: str, default_yes: bool) -> bool:
    default = "y" if default_yes else "n"
    while True:
        s = _ask(prompt + " (y/n)", default).lower().strip()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please enter y or n.")


def _choose_ns(case_name: str) -> List[int]:
    case = get_case(case_name)
    print("\nChoose n-values mode:")
    print("  1) Use case default ns")
    print("  2) Enter comma-separated ns")
    print("  3) Generate geometric ns (start, factor, steps)")
    mode = _ask("Mode", "1").strip()

    if mode == "2":
        while True:
            try:
                s = _ask("Enter ns like 1000,2000,4000", ",".join(str(x) for x in case.default_ns))
                return _parse_ns_csv(s)
            except Exception as e:
                print(f"Invalid ns: {e}")

    if mode == "3":
        start = _ask_int("start", int(case.default_ns[0]), min_value=1)
        factor = _ask_int("factor", 2, min_value=2)
        steps = _ask_int("steps", len(case.default_ns), min_value=2)
        return geometric_ns(start, factor, steps)

    return list(case.default_ns)


def main() -> None:
    print("Big-O & Analysis: benchmark + fit growth models")
    print("-" * 60)

    print("\nAvailable cases:")
    for i, c in enumerate(DEFAULT_CASES, start=1):
        print(f"  {i:2d}) {c.name:15s}  {c.description}")

    run_all = _ask_yes_no("\nRun all cases?", default_yes=False)

    # Benchmark config
    print("\nBenchmark settings:")
    warmups = _ask_int("Warmup runs per n (unmeasured)", 2, min_value=0)
    repeats = _ask_int("Recorded repeats per n (median taken)", 7, min_value=3)
    min_time = _ask_float("Min seconds per repeat via looping", 0.02, min_value=0.0)

    cfg = BenchConfig(
        warmup_runs=warmups,
        repeats=repeats,
        min_time_per_repeat=min_time,
        collect_distribution=False,
    )

    csv_path = _ask("Optional CSV output path (blank = none)", "").strip() or None

    if run_all:
        for c in DEFAULT_CASES:
            ns = _choose_ns(c.name)
            _run_one_case(c.name, ns, cfg, csv_path=csv_path)
        return

    # Run one case
    while True:
        choice = _ask("\nPick a case by number or name", "linear_sum").strip()
        # accept number
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(DEFAULT_CASES):
                case_name = DEFAULT_CASES[idx - 1].name
                break
            print("Invalid number.")
            continue
        # accept name
        if choice in list_cases():
            case_name = choice
            break
        print("Unknown case. Try again.")

    ns = _choose_ns(case_name)
    _run_one_case(case_name, ns, cfg, csv_path=csv_path)


if __name__ == "__main__":
    main()
