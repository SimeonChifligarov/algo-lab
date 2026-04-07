"""
Goal:
Implement Randomized Quickselect to find the k-th smallest element.

Key ideas:
- Random pivot selection
- Partitioning (like Quicksort)
- Expected O(n) time

Notes:
- This implementation modifies the list in-place
- A safe wrapper is provided to avoid modifying input
"""

from __future__ import annotations

import random
from typing import List, MutableSequence, TypeVar

T = TypeVar("T")


def partition(arr: MutableSequence[T], left: int, right: int, pivot_index: int) -> int:
    """
    Partition arr[left:right+1] around the pivot value.

    Returns:
        Final index of the pivot.
    """
    pivot_value = arr[pivot_index]

    # Move pivot to end
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]

    store_index = left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store_index], arr[i] = arr[i], arr[store_index]
            store_index += 1

    # Move pivot to its final place
    arr[right], arr[store_index] = arr[store_index], arr[right]
    return store_index


def randomized_quickselect(arr: MutableSequence[T], k: int) -> T:
    """
    In-place Randomized Quickselect.

    Args:
        arr: mutable sequence
        k: zero-based index (k-th smallest)

    Returns:
        k-th smallest element

    Raises:
        ValueError: empty input
        IndexError: invalid k
    """
    if not arr:
        raise ValueError("Cannot select from an empty sequence")

    if k < 0 or k >= len(arr):
        raise IndexError(f"k={k} out of range for length {len(arr)}")

    left = 0
    right = len(arr) - 1

    while True:
        if left == right:
            return arr[left]

        pivot_index = random.randint(left, right)
        pivot_index = partition(arr, left, right, pivot_index)

        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1


def kth_smallest(values: List[T], k: int) -> T:
    """
    Safe wrapper (does NOT modify input list).
    """
    copied = list(values)
    return randomized_quickselect(copied, k)


def demo() -> None:
    """
    Demonstration of usage.
    """
    data = [9, 1, 7, 3, 8, 2, 6, 5, 4]
    k = 4  # zero-based → 5th smallest

    print("Data:", data)
    print(f"k = {k}")

    result = kth_smallest(data, k)

    print("k-th smallest element:", result)
    print("Sorted (reference):   ", sorted(data))


if __name__ == "__main__":
    random.seed()
    demo()
