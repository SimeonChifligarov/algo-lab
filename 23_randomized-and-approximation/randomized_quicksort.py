"""
Goal:
Implement Randomized Quicksort and expose the core idea behind its
expected O(n log n) performance.

Key ideas:
- Random pivot selection
- Divide-and-conquer sorting
- In-place partitioning
- Better expected behavior than always choosing a fixed pivot

Notes:
- This implementation sorts in-place
- A safe wrapper is provided to return a sorted copy
- The demo compares the original data and the sorted result
"""

from __future__ import annotations

import random
from typing import List, MutableSequence, TypeVar

T = TypeVar("T")


def partition(arr: MutableSequence[T], left: int, right: int, pivot_index: int) -> int:
    """
    Partition arr[left:right+1] around the pivot value.

    After partitioning:
    - elements < pivot are on the left
    - pivot is in its final sorted position
    - elements >= pivot are on the right

    Returns:
        Final index of the pivot.
    """
    pivot_value = arr[pivot_index]

    # Move pivot to the end temporarily.
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]

    store_index = left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store_index], arr[i] = arr[i], arr[store_index]
            store_index += 1

    # Move pivot into its final place.
    arr[right], arr[store_index] = arr[store_index], arr[right]
    return store_index


def _randomized_quicksort(arr: MutableSequence[T], left: int, right: int) -> None:
    """
    Recursive helper for in-place randomized Quicksort.
    """
    if left >= right:
        return

    pivot_index = random.randint(left, right)
    pivot_index = partition(arr, left, right, pivot_index)

    _randomized_quicksort(arr, left, pivot_index - 1)
    _randomized_quicksort(arr, pivot_index + 1, right)


def randomized_quicksort(arr: MutableSequence[T]) -> None:
    """
    Sort a mutable sequence in-place using Randomized Quicksort.

    Args:
        arr: mutable sequence of comparable elements

    Returns:
        None
    """
    if len(arr) <= 1:
        return

    _randomized_quicksort(arr, 0, len(arr) - 1)


def sorted_copy(values: List[T]) -> List[T]:
    """
    Return a sorted copy of the input without modifying the original list.
    """
    copied = list(values)
    randomized_quicksort(copied)
    return copied


def demo() -> None:
    """
    Demonstration of Randomized Quicksort.
    """
    data = [9, 1, 7, 3, 8, 2, 6, 5, 4, 3, 7]

    print("Original data: ", data)

    result = sorted_copy(data)

    print("Sorted result: ", result)
    print("Python sorted: ", sorted(data))
    print("Original unchanged after sorted_copy():", data)


if __name__ == "__main__":
    random.seed()
    demo()
