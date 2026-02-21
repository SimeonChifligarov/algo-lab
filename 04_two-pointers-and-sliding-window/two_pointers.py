"""
Two Pointers & Sliding Window — two pointers toolkit (Part 1/4)

This file covers the core "two pointers" variants:
- inward pointers (pair sum in sorted array)
- same-direction pointers (remove duplicates in-place)
- fast/slow pointers (move zeros, remove element)

Next files:
2) sliding_window.py  (fixed + variable window patterns)
3) patterns.py        (canonical problems built on both ideas)
4) test_two_pointers_and_window.py (unittest suite)

All functions are written to be:
- small and composable
- explicit about edge cases
- easy to unit test
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple


# ----------------------------
# Inward pointers (left/right)
# ----------------------------

def pair_sum_sorted(nums: Sequence[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Given a sorted array, return indices (i, j) with nums[i] + nums[j] == target.
    Returns None if no pair exists.

    Time: O(n)
    Space: O(1)

    Example:
        pair_sum_sorted([1,2,3,4,6], 6) -> (1,3)  # 2 + 4
    """
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return l, r
        if s < target:
            l += 1
        else:
            r -= 1
    return None


def is_palindrome_two_pointers(s: str) -> bool:
    """
    Basic palindrome check using inward pointers (no normalization).
    For normalized palindrome logic (ignore punctuation/case), handle that separately.

    Example:
        "racecar" -> True
        "Racecar" -> False (case-sensitive)
    """
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True


# ----------------------------
# Same-direction pointers
# ----------------------------

def remove_duplicates_sorted(nums: List[int]) -> int:
    """
    In-place remove duplicates from a sorted list.
    Returns the new length k such that nums[:k] are unique.

    Time: O(n)
    Space: O(1)

    Example:
        nums = [1,1,2,2,3]
        k = remove_duplicates_sorted(nums)
        nums[:k] == [1,2,3]
    """
    if not nums:
        return 0

    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def remove_element(nums: List[int], val: int) -> int:
    """
    In-place remove all occurrences of val (order NOT preserved).
    Returns new length k such that nums[:k] contains the kept elements.

    Pattern:
      Keep a 'write' boundary; when we see val, swap with last candidate.

    Time: O(n)
    Space: O(1)

    Example:
        nums=[3,2,2,3], val=3 -> k=2, nums[:2] is [2,2] (order arbitrary)
    """
    i = 0
    n = len(nums)
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1
        else:
            i += 1
    return n


# ----------------------------
# Fast/slow pointers
# ----------------------------

def move_zeros(nums: List[int]) -> None:
    """
    Move all zeros to the end, preserving relative order of non-zeros.
    Modifies nums in place.

    Time: O(n)
    Space: O(1)

    Example:
        [0,1,0,3,12] -> [1,3,12,0,0]
    """
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write] = nums[read]
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0


def remove_element_stable(nums: List[int], val: int) -> int:
    """
    In-place remove all occurrences of val, preserving order.
    Returns new length k such that nums[:k] is the filtered list.

    Time: O(n)
    Space: O(1)
    """
    write = 0
    for read in range(len(nums)):
        if nums[read] != val:
            nums[write] = nums[read]
            write += 1
    return write


if __name__ == "__main__":
    print(pair_sum_sorted([1, 2, 3, 4, 6], 6))
    print(is_palindrome_two_pointers("racecar"))

    a = [1, 1, 2, 2, 3]
    k = remove_duplicates_sorted(a)
    print("unique:", a[:k])

    b = [0, 1, 0, 3, 12]
    move_zeros(b)
    print("moved zeros:", b)
