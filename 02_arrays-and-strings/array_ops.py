"""
Array / list primitives with clear APIs and edge-case handling.

This file focuses on *in-place array operations*:
- reverse_in_place
- rotate_right_in_place / rotate_left_in_place

Design choices:
- Works with any MutableSequence (e.g., list, array.array), not just list.
- Raises TypeError for non-mutable / non-indexable inputs.
- Rotations handle k < 0 and k > n by normalizing k.

Time/space:
- reverse:  O(n) time, O(1) extra space
- rotate:   O(n) time, O(1) extra space (3-reversal method)
"""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import TypeVar

T = TypeVar("T")


def _require_mutable_sequence(a: object) -> MutableSequence[T]:
    if not isinstance(a, MutableSequence):
        raise TypeError(f"Expected a mutable sequence (e.g., list). Got: {type(a).__name__}")
    return a  # type: ignore[return-value]


def _reverse_slice(a: MutableSequence[T], lo: int, hi: int) -> None:
    """
    Reverse a[lo:hi] in place, where hi is exclusive.
    """
    i, j = lo, hi - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def reverse_in_place(a: MutableSequence[T]) -> None:
    """
    Reverse the sequence in place.

    Example:
        a = [1,2,3]
        reverse_in_place(a)  # a becomes [3,2,1]
    """
    _require_mutable_sequence(a)
    _reverse_slice(a, 0, len(a))


def _normalize_k(k: int, n: int) -> int:
    """
    Normalize a rotation amount to the range [0, n).
    For n == 0, returns 0.
    """
    if n <= 0:
        return 0
    # Python's % already handles negatives the way we want:
    # -1 % 5 == 4
    return k % n


def rotate_right_in_place(a: MutableSequence[T], k: int) -> None:
    """
    Rotate the sequence to the right by k steps, in place.

    Example:
        a = [1,2,3,4,5]
        rotate_right_in_place(a, 2)  # a becomes [4,5,1,2,3]

    Edge cases:
    - empty / length-1: no-op
    - k can be negative (negative right-rotation == left-rotation)
    """
    _require_mutable_sequence(a)
    n = len(a)
    if n <= 1:
        return

    k = _normalize_k(k, n)
    if k == 0:
        return

    # 3-reversal method:
    # [A | B] where B has length k
    # reverse whole, reverse first k, reverse remaining
    _reverse_slice(a, 0, n)
    _reverse_slice(a, 0, k)
    _reverse_slice(a, k, n)


def rotate_left_in_place(a: MutableSequence[T], k: int) -> None:
    """
    Rotate the sequence to the left by k steps, in place.

    Example:
        a = [1,2,3,4,5]
        rotate_left_in_place(a, 2)  # a becomes [3,4,5,1,2]

    Implemented by converting to right-rotation.
    """
    rotate_right_in_place(a, -k)


if __name__ == "__main__":
    demo = [1, 2, 3, 4, 5]
    print("start:", demo)

    reverse_in_place(demo)
    print("reversed:", demo)

    rotate_right_in_place(demo, 2)
    print("rotate right 2:", demo)

    rotate_left_in_place(demo, 3)
    print("rotate left 3:", demo)
