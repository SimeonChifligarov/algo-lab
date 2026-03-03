"""
Binary Search & Bounds — core searches (Part 1/4)

This file covers:
- classic binary search on sorted arrays (iterative + recursive)
- variants that handle duplicates (first/last occurrence)

Next files:
2) bounds.py                 (lower_bound / upper_bound and helpers)
3) parametric_search.py      (binary search on answer)
4) test_binary_search.py     (unittest suite)

Conventions:
- All functions assume `arr` is sorted in non-decreasing order.
- Returns indices, or -1 when "not found" (for find-style functions).
"""

from __future__ import annotations

from typing import Sequence, TypeVar, Optional, Callable

T = TypeVar("T")


def binary_search(arr: Sequence[T], target: T) -> int:
    """
    Classic iterative binary search.
    Returns index of target, or -1 if not found.

    Time: O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(arr)  # [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:  # type: ignore[operator]
            lo = mid + 1
        else:
            hi = mid
    return -1


def binary_search_recursive(arr: Sequence[T], target: T) -> int:
    """
    Recursive binary search (educational).
    """

    def helper(lo: int, hi: int) -> int:
        if lo >= hi:
            return -1
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:  # type: ignore[operator]
            return helper(mid + 1, hi)
        return helper(lo, mid)

    return helper(0, len(arr))


def first_occurrence(arr: Sequence[T], target: T) -> int:
    """
    Return the first index i where arr[i] == target, or -1 if not found.
    Works with duplicates.

    Pattern:
      when we find target, keep searching left.
    """
    lo, hi = 0, len(arr)
    ans = -1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid
            hi = mid
        elif arr[mid] < target:  # type: ignore[operator]
            lo = mid + 1
        else:
            hi = mid
    return ans


def last_occurrence(arr: Sequence[T], target: T) -> int:
    """
    Return the last index i where arr[i] == target, or -1 if not found.
    Works with duplicates.

    Pattern:
      when we find target, keep searching right.
    """
    lo, hi = 0, len(arr)
    ans = -1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            ans = mid
            lo = mid + 1
        elif arr[mid] < target:  # type: ignore[operator]
            lo = mid + 1
        else:
            hi = mid
    return ans


def count_occurrences(arr: Sequence[T], target: T) -> int:
    """
    Return how many times target appears in arr.

    Uses first/last occurrence (O(log n)).
    """
    first = first_occurrence(arr, target)
    if first == -1:
        return 0
    last = last_occurrence(arr, target)
    return last - first + 1


if __name__ == "__main__":
    data = [1, 2, 2, 2, 3, 5, 7]
    print("binary_search 2:", binary_search(data, 2))
    print("first 2:", first_occurrence(data, 2))
    print("last 2:", last_occurrence(data, 2))
    print("count 2:", count_occurrences(data, 2))
