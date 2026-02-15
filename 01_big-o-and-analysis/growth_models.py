"""
Growth models + tiny least-squares fitter for Big-O intuition.

We fit measured runtimes (y) against a single-feature model f(n):

    y ≈ a * f(n) + b

For each candidate model (1, log n, n, n log n, n^2, n^3), we compute:
- slope a, intercept b (ordinary least squares)
- R^2 (higher is better)
- RMSE (lower is better)

This file is intentionally dependency-free (standard library only).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Iterable, List, Sequence, Tuple


# ----------------------------
# Model definitions
# ----------------------------

def _safe_log2(n: float) -> float:
    # Avoid log(0) and log(1)=0 issues. For benchmarking, n>=1,
    # but we still guard so the fitter never explodes.
    return math.log2(max(2.0, float(n)))


def f_const(n: float) -> float:
    return 1.0


def f_log_n(n: float) -> float:
    return _safe_log2(n)


def f_n(n: float) -> float:
    return float(n)


def f_n_log_n(n: float) -> float:
    nn = float(n)
    return nn * _safe_log2(nn)


def f_n2(n: float) -> float:
    nn = float(n)
    return nn * nn


def f_n3(n: float) -> float:
    nn = float(n)
    return nn * nn * nn


@dataclass(frozen=True)
class Model:
    name: str
    f: Callable[[float], float]


DEFAULT_MODELS: Tuple[Model, ...] = (
    Model("1", f_const),
    Model("log n", f_log_n),
    Model("n", f_n),
    Model("n log n", f_n_log_n),
    Model("n^2", f_n2),
    Model("n^3", f_n3),
)


# ----------------------------
# Fit results
# ----------------------------

@dataclass(frozen=True)
class FitResult:
    model: Model
    a: float
    b: float
    r2: float
    rmse: float

    def predict(self, n: float) -> float:
        return self.a * self.model.f(n) + self.b


# ----------------------------
# Least squares fitting
# ----------------------------

def _ols_fit_affine(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    """
    Fit y ≈ a*x + b via ordinary least squares.

    Returns (a, b). If variance of x is ~0, fall back to a=0 and b=mean(y).
    """
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(xs) < 2:
        raise ValueError("Need at least 2 points to fit a line")

    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n

    sxx = 0.0
    sxy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mean_x
        sxx += dx * dx
        sxy += dx * (y - mean_y)

    if abs(sxx) < 1e-30:
        # Degenerate: x doesn't vary; best affine is constant at mean_y
        return 0.0, mean_y

    a = sxy / sxx
    b = mean_y - a * mean_x
    return a, b


def _r2_and_rmse(xs: Sequence[float], ys: Sequence[float], a: float, b: float) -> Tuple[float, float]:
    """
    Compute R^2 and RMSE for predictions y_hat = a*x + b.
    """
    n = len(xs)
    mean_y = sum(ys) / n

    ss_res = 0.0
    ss_tot = 0.0
    for x, y in zip(xs, ys):
        y_hat = a * x + b
        err = y - y_hat
        ss_res += err * err

        dy = y - mean_y
        ss_tot += dy * dy

    rmse = math.sqrt(ss_res / n)

    # If ys are (almost) constant, define R^2 as 1 if perfect, else 0.
    if abs(ss_tot) < 1e-30:
        r2 = 1.0 if ss_res < 1e-30 else 0.0
    else:
        r2 = 1.0 - (ss_res / ss_tot)

    return r2, rmse


def fit_model(n_values: Sequence[int], y_values: Sequence[float], model: Model) -> FitResult:
    """
    Fit runtime measurements y_values vs n_values using y ≈ a*f(n) + b.
    """
    if len(n_values) != len(y_values):
        raise ValueError("n_values and y_values must have the same length")
    if len(n_values) < 2:
        raise ValueError("Need at least 2 points to fit a model")

    xs = [model.f(float(n)) for n in n_values]
    ys = list(map(float, y_values))

    a, b = _ols_fit_affine(xs, ys)
    r2, rmse = _r2_and_rmse(xs, ys, a, b)

    return FitResult(model=model, a=a, b=b, r2=r2, rmse=rmse)


def fit_all_models(
        n_values: Sequence[int],
        y_values: Sequence[float],
        models: Iterable[Model] = DEFAULT_MODELS,
) -> List[FitResult]:
    """
    Fit all candidate models and return a list of FitResult sorted by:
      1) higher R^2
      2) lower RMSE
    """
    results = [fit_model(n_values, y_values, m) for m in models]
    results.sort(key=lambda r: (r.r2, -r.rmse), reverse=True)  # rmse sign flipped; see below fix
    # The above sort is slightly awkward because we want:
    #   r2 descending, rmse ascending.
    # We'll re-sort correctly for clarity.
    results.sort(key=lambda r: (-r.r2, r.rmse))
    return results


def best_model(
        n_values: Sequence[int],
        y_values: Sequence[float],
        models: Iterable[Model] = DEFAULT_MODELS,
) -> FitResult:
    """
    Return the best-fitting model by (R^2 desc, RMSE asc).
    """
    return fit_all_models(n_values, y_values, models=models)[0]


# ----------------------------
# Small demo (optional)
# ----------------------------

if __name__ == "__main__":
    # Fake data that roughly follows n log n
    ns = [100, 200, 400, 800, 1600]
    # pretend runtime in seconds
    ys = [n * math.log2(n) * 2e-7 + 2e-4 for n in ns]

    results = fit_all_models(ns, ys)
    print("Top fits:")
    for r in results[:3]:
        print(f"  {r.model.name:7s}  R^2={r.r2:.6f}  RMSE={r.rmse:.6e}  a={r.a:.3e}  b={r.b:.3e}")
