"""
Two Pointers & Sliding Window — sliding window toolkit (Part 2/4)

Covers the two core window types:
- fixed-size windows (window length is constant)
- variable-size windows (expand right, shrink left while condition holds)

Functions included:
- max_sum_subarray_k (fixed-size)
- average_subarray_k (fixed-size)
- min_subarray_len_at_least (variable-size)
- longest_substring_k_distinct (variable-size)
- longest_ones_after_replacement (variable-size)

Next files:
3) patterns.py  (canonical problems combining two pointers + sliding window)
4) test_two_pointers_and_window.py
"""

from __future__ import annotations

from typing import Dict, Optional, Sequence


# ----------------------------
# Fixed-size window
# ----------------------------

def max_sum_subarray_k(nums: Sequence[int], k: int) -> int:
    """
    Return the maximum sum of any contiguous subarray of length k.
    Raises ValueError if k <= 0 or k > len(nums).

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError("k must be in [1, len(nums)]")

    window_sum = sum(nums[:k])
    best = window_sum

    for r in range(k, n):
        window_sum += nums[r] - nums[r - k]
        if window_sum > best:
            best = window_sum
    return best


def average_subarray_k(nums: Sequence[int], k: int) -> float:
    """
    Return the maximum average of any contiguous subarray of length k.
    (equivalently max_sum_subarray_k / k)

    Raises ValueError if k <= 0 or k > len(nums).
    """
    return max_sum_subarray_k(nums, k) / k


# ----------------------------
# Variable-size window
# ----------------------------

def min_subarray_len_at_least(nums: Sequence[int], target: int) -> int:
    """
    Return minimal length of a contiguous subarray with sum >= target.
    Returns 0 if no such subarray exists.

    Assumption:
      nums are non-negative (standard version of the problem).
      If negatives exist, this sliding-window approach doesn't work reliably.

    Time: O(n)
    Space: O(1)
    """
    if target <= 0:
        return 0

    n = len(nums)
    best = n + 1
    window_sum = 0
    l = 0

    for r, x in enumerate(nums):
        window_sum += x
        while window_sum >= target and l <= r:
            best = min(best, r - l + 1)
            window_sum -= nums[l]
            l += 1

    return 0 if best == n + 1 else best


def longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Return the length of the longest substring with at most k distinct characters.

    Time: O(n)
    Space: O(k)
    """
    if k <= 0:
        return 0

    freq: Dict[str, int] = {}
    l = 0
    best = 0

    for r, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1

        while len(freq) > k:
            left_ch = s[l]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            l += 1

        best = max(best, r - l + 1)

    return best


def longest_ones_after_replacement(nums: Sequence[int], k: int) -> int:
    """
    Given a binary array nums and integer k, return the length of the longest
    contiguous subarray containing only 1s after replacing at most k 0s with 1s.

    Pattern:
      Track zeros count; shrink while zeros > k.

    Time: O(n)
    Space: O(1)
    """
    if k < 0:
        raise ValueError("k must be >= 0")

    l = 0
    zeros = 0
    best = 0

    for r, x in enumerate(nums):
        if x == 0:
            zeros += 1

        while zeros > k:
            if nums[l] == 0:
                zeros -= 1
            l += 1

        best = max(best, r - l + 1)

    return best


if __name__ == "__main__":
    print(max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3))  # 9
    print(min_subarray_len_at_least([2, 3, 1, 2, 4, 3], 7))  # 2
    print(longest_substring_k_distinct("eceba", 2))  # 3 ("ece")
    print(longest_ones_after_replacement([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))  # 6
