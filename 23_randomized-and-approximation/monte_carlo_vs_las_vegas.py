"""
Goal:
Show the difference between Monte Carlo and Las Vegas randomized algorithms.

Key ideas:
- Monte Carlo algorithms have bounded running time, but may return an incorrect result
- Las Vegas algorithms always return a correct result, but their running time is random

This file includes:
1. A Monte Carlo estimator for pi
2. A Las Vegas search for a target value in a list
3. A demo that compares their behavior
"""

from __future__ import annotations

import math
import random
from typing import Optional, Sequence


def estimate_pi(num_samples: int) -> float:
    """
    Estimate pi using a Monte Carlo method.

    Idea:
    - Randomly sample points in the unit square [0, 1] x [0, 1]
    - Count how many fall inside the quarter-circle x^2 + y^2 <= 1
    - The ratio approximates pi / 4

    Args:
        num_samples: number of random points to sample

    Returns:
        Approximate value of pi

    Raises:
        ValueError: if num_samples is not positive
    """
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")

    inside_circle = 0

    for _ in range(num_samples):
        x = random.random()
        y = random.random()

        if x * x + y * y <= 1.0:
            inside_circle += 1

    return 4.0 * inside_circle / num_samples


def las_vegas_search(values: Sequence[int], target: int) -> Optional[int]:
    """
    Las Vegas randomized search for a target value.

    Behavior:
    - Repeatedly pick a random untested index
    - If the target is found, return its index
    - If all positions are exhausted, return None

    Why this is Las Vegas:
    - The answer is always correct
    - The running time depends on luck

    Args:
        values: sequence to search
        target: value to find

    Returns:
        An index where target appears, or None if not found
    """
    remaining_indices = list(range(len(values)))

    while remaining_indices:
        position = random.randrange(len(remaining_indices))
        index = remaining_indices.pop(position)

        if values[index] == target:
            return index

    return None


def describe_monte_carlo_result(estimate: float) -> str:
    """
    Build a short explanation string for the pi estimation result.
    """
    error = abs(math.pi - estimate)
    return (
        f"Monte Carlo estimate of pi: {estimate:.6f}\n"
        f"Actual pi:                  {math.pi:.6f}\n"
        f"Absolute error:             {error:.6f}"
    )


def describe_las_vegas_result(values: Sequence[int], target: int, result: Optional[int]) -> str:
    """
    Build a short explanation string for the Las Vegas search result.
    """
    if result is None:
        return (
            f"Las Vegas search did not find target {target}.\n"
            "This is correct: the target is not in the sequence."
        )

    return (
        f"Las Vegas search found target {target} at index {result}.\n"
        f"Verification: values[{result}] = {values[result]}"
    )


def demo() -> None:
    """
    Demonstrate Monte Carlo vs Las Vegas behavior.
    """
    print("=== Monte Carlo example: estimating pi ===")
    samples = 100_000
    pi_estimate = estimate_pi(samples)
    print(f"Samples used: {samples}")
    print(describe_monte_carlo_result(pi_estimate))

    print("\n=== Las Vegas example: randomized search ===")
    data = [12, 7, 3, 19, 5, 8, 14, 3, 21]
    target = 14
    result = las_vegas_search(data, target)

    print("Data:   ", data)
    print("Target: ", target)
    print(describe_las_vegas_result(data, target, result))

    print("\n=== Missing-target example ===")
    missing_target = 99
    missing_result = las_vegas_search(data, missing_target)
    print("Target: ", missing_target)
    print(describe_las_vegas_result(data, missing_target, missing_result))

    print("\n=== Summary ===")
    print("Monte Carlo: fixed amount of work, approximate answer.")
    print("Las Vegas: always correct answer, random amount of work.")


if __name__ == "__main__":
    random.seed()
    demo()
