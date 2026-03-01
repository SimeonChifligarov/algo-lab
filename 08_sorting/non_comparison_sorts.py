"""
Design: Sorting — non-comparison sorts (Part 2/4)

This file includes sorting algorithms that don't rely on comparisons:
- counting_sort (stable)
- radix_sort_lsd (stable) for non-negative integers

These demonstrate different assumptions:
- Counting sort assumes keys are integers in a reasonably small range.
- Radix sort assumes integers with bounded digit length; it uses counting sort per digit.

Next file:
3) sorting_analysis.py
"""

from __future__ import annotations

from typing import List, Sequence


# ----------------------------
# Counting sort
# ----------------------------

def counting_sort(nums: Sequence[int], *, min_value: int | None = None, max_value: int | None = None) -> List[int]:
    """
    Stable counting sort for integers.

    Parameters:
      nums: sequence of ints
      min_value/max_value: optional bounds to avoid scanning nums twice.
        If not provided, we compute them.

    Returns:
      new sorted list (stable)

    Time: O(n + R) where R = max_value - min_value + 1
    Space: O(R)

    Notes:
      Works with negatives by offsetting indices.
    """
    a = list(nums)
    if not a:
        return []

    if min_value is None:
        min_value = min(a)
    if max_value is None:
        max_value = max(a)
    if min_value > max_value:
        return []

    rng = max_value - min_value + 1
    if rng < 0:
        raise ValueError("Invalid range")
    # counts[i] counts occurrences of value (i + min_value)
    counts = [0] * rng
    for x in a:
        counts[x - min_value] += 1

    # prefix sums -> positions (stable output)
    for i in range(1, rng):
        counts[i] += counts[i - 1]

    out = [0] * len(a)
    # traverse input from right to left for stability
    for x in reversed(a):
        idx = x - min_value
        counts[idx] -= 1
        out[counts[idx]] = x
    return out


# ----------------------------
# Radix sort (LSD)
# ----------------------------

def radix_sort_lsd(nums: Sequence[int], *, base: int = 10) -> List[int]:
    """
    LSD radix sort for NON-NEGATIVE integers. Stable.

    Parameters:
      base: digit base (10 is typical). Higher bases reduce passes.

    Raises:
      ValueError if any number is negative or base < 2.

    Time: O(d * (n + base)) where d is number of digits/passes.
    Space: O(n + base)
    """
    a = list(nums)
    if not a:
        return []
    if base < 2:
        raise ValueError("base must be >= 2")
    if any(x < 0 for x in a):
        raise ValueError("radix_sort_lsd supports only non-negative integers")

    exp = 1  # base^digit
    max_num = max(a)

    while max_num // exp > 0:
        a = _counting_sort_by_digit(a, exp, base)
        exp *= base

    return a


def _counting_sort_by_digit(a: List[int], exp: int, base: int) -> List[int]:
    """
    Stable counting sort by the digit at (exp) place.
    digit = (x // exp) % base
    """
    n = len(a)
    counts = [0] * base

    for x in a:
        d = (x // exp) % base
        counts[d] += 1

    for i in range(1, base):
        counts[i] += counts[i - 1]

    out = [0] * n
    for x in reversed(a):  # stability
        d = (x // exp) % base
        counts[d] -= 1
        out[counts[d]] = x

    return out


if __name__ == "__main__":
    print("counting:", counting_sort([3, -1, 2, 2, 5, 0, -1]))
    print("radix:", radix_sort_lsd([170, 45, 75, 90, 802, 24, 2, 66]))
