"""
Binary Search & Bounds — lower/upper bounds (Part 2/4)

This file implements:
- lower_bound: first index i where arr[i] >= x
- upper_bound: first index i where arr[i] > x
- equal_range: (lower_bound, upper_bound)
- insert_position: where you'd insert to keep the array sorted

These are the building blocks behind:
- counting duplicates quickly
- finding first/last occurrence
- "where does x belong?" questions

Next file:
3) parametric_search.py
"""

from __future__ import annotations

from typing import Sequence, TypeVar, Tuple

T = TypeVar("T")


def lower_bound(arr: Sequence[T], x: T) -> int:
    """
    Return the first index i such that arr[i] >= x.
    If all elements are < x, returns len(arr).

    Time: O(log n)

    Equivalent to C++ std::lower_bound.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:  # type: ignore[operator]
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr: Sequence[T], x: T) -> int:
    """
    Return the first index i such that arr[i] > x.
    If all elements are <= x, returns len(arr).

    Equivalent to C++ std::upper_bound.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:  # type: ignore[operator]
            lo = mid + 1
        else:
            hi = mid
    return lo


def equal_range(arr: Sequence[T], x: T) -> Tuple[int, int]:
    """
    Return (l, r) where:
      l = lower_bound(arr, x)
      r = upper_bound(arr, x)

    Then the elements equal to x are exactly arr[l:r].
    """
    return lower_bound(arr, x), upper_bound(arr, x)


def count_with_bounds(arr: Sequence[T], x: T) -> int:
    """
    Count occurrences of x using bounds (O(log n)).
    """
    l, r = equal_range(arr, x)
    return r - l


def insert_position(arr: Sequence[T], x: T) -> int:
    """
    Return an index where x can be inserted to keep sorted order.
    This returns the *first* valid insertion position (like bisect_left).
    """
    return lower_bound(arr, x)


if __name__ == "__main__":
    a = [1, 2, 2, 2, 3, 5, 7]
    for x in [0, 2, 4, 8]:
        lb = lower_bound(a, x)
        ub = upper_bound(a, x)
        print(f"x={x}  lb={lb} ub={ub}  slice={a[lb:ub]}")
