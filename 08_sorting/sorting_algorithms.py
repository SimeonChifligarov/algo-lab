"""
Design: Sorting — classic algorithms (Part 1/4)

This file contains implementations of several classic sorting algorithms.
We keep them small, readable, and correct, and we aim to preserve a consistent API:

- sorting functions return a NEW sorted list by default (pure functions)
- *_in_place variants mutate the list in place

Algorithms included here (comparison-based):
- insertion_sort
- selection_sort
- bubble_sort
- merge_sort (stable)
- quick_sort (average O(n log n), worst O(n^2))

Next files:
2) non_comparison_sorts.py  (counting sort / radix sort)
3) sorting_analysis.py      (properties table, tiny benchmark helper)
4) test_sorting.py          (unittest suite)

All standard-library-only.
"""

from __future__ import annotations

from typing import Callable, List, Sequence, TypeVar, Optional

T = TypeVar("T")


# ----------------------------
# Utility
# ----------------------------

def _key_fn(key: Optional[Callable[[T], object]]) -> Callable[[T], object]:
    return key if key is not None else (lambda x: x)


# ----------------------------
# Insertion sort (stable)
# ----------------------------

def insertion_sort(nums: Sequence[T], *, key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Stable insertion sort. Returns a new sorted list.

    Time:
      - best: O(n) (already sorted)
      - avg/worst: O(n^2)
    Space: O(1) extra (besides output copy)
    """
    keyf = _key_fn(key)
    a = list(nums)
    for i in range(1, len(a)):
        x = a[i]
        kx = keyf(x)
        j = i - 1
        while j >= 0 and keyf(a[j]) > kx:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def insertion_sort_in_place(a: List[T], *, key: Optional[Callable[[T], object]] = None) -> None:
    """In-place insertion sort (stable)."""
    keyf = _key_fn(key)
    for i in range(1, len(a)):
        x = a[i]
        kx = keyf(x)
        j = i - 1
        while j >= 0 and keyf(a[j]) > kx:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


# ----------------------------
# Selection sort (not stable)
# ----------------------------

def selection_sort(nums: Sequence[T], *, key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Selection sort. Returns a new sorted list.

    Time: O(n^2)
    Space: O(1) extra (besides output copy)
    Stability: generally NOT stable
    """
    keyf = _key_fn(key)
    a = list(nums)
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            if keyf(a[j]) < keyf(a[min_i]):
                min_i = j
        a[i], a[min_i] = a[min_i], a[i]
    return a


def selection_sort_in_place(a: List[T], *, key: Optional[Callable[[T], object]] = None) -> None:
    keyf = _key_fn(key)
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            if keyf(a[j]) < keyf(a[min_i]):
                min_i = j
        a[i], a[min_i] = a[min_i], a[i]


# ----------------------------
# Bubble sort (stable if implemented with adjacent swaps only)
# ----------------------------

def bubble_sort(nums: Sequence[T], *, key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Bubble sort. Returns a new sorted list.

    Time: O(n^2) worst/avg, O(n) best with early exit.
    Space: O(1) extra (besides output copy)
    Stability: stable with adjacent swaps
    """
    keyf = _key_fn(key)
    a = list(nums)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if keyf(a[j]) > keyf(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def bubble_sort_in_place(a: List[T], *, key: Optional[Callable[[T], object]] = None) -> None:
    keyf = _key_fn(key)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if keyf(a[j]) > keyf(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break


# ----------------------------
# Merge sort (stable)
# ----------------------------

def merge_sort(nums: Sequence[T], *, key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Stable merge sort. Returns a new sorted list.

    Time: O(n log n)
    Space: O(n)
    """
    keyf = _key_fn(key)
    a = list(nums)
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], key=key)
    right = merge_sort(a[mid:], key=key)
    return _merge(left, right, keyf)


def _merge(left: List[T], right: List[T], keyf: Callable[[T], object]) -> List[T]:
    out: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        # <= keeps stability (left element wins ties)
        if keyf(left[i]) <= keyf(right[j]):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ----------------------------
# Quick sort (not stable)
# ----------------------------

def quick_sort(nums: Sequence[T], *, key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Quick sort (3-way partition). Returns a new sorted list.

    Average: O(n log n)
    Worst: O(n^2) (rare with decent pivoting, but possible)
    Space: O(log n) recursion (plus new lists due to functional style here)
    Stability: not stable
    """
    keyf = _key_fn(key)
    a = list(nums)
    if len(a) <= 1:
        return a

    pivot = a[len(a) // 2]
    kp = keyf(pivot)

    less: List[T] = []
    equal: List[T] = []
    greater: List[T] = []

    for x in a:
        kx = keyf(x)
        if kx < kp:
            less.append(x)
        elif kx > kp:
            greater.append(x)
        else:
            equal.append(x)

    return quick_sort(less, key=key) + equal + quick_sort(greater, key=key)


if __name__ == "__main__":
    data = [5, 2, 4, 6, 1, 3]
    print("insertion:", insertion_sort(data))
    print("selection:", selection_sort(data))
    print("bubble:", bubble_sort(data))
    print("merge:", merge_sort(data))
    print("quick:", quick_sort(data))
