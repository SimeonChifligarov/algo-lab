"""
Two Pointers & Sliding Window — canonical problems (Part 3/4)

This file contains common interview-style problems built on:
- two pointers
- sliding window

Included:
- reverse_vowels (two pointers inward on a string)
- squares_sorted (two pointers inward on sorted array with negatives)
- container_with_most_water (two pointers inward)
- is_subsequence (same-direction pointers)
- longest_substring_without_repeating (variable sliding window)
- min_window_substring (variable sliding window; classic)

Next file:
4) test_two_pointers_and_window.py
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Sequence, Tuple


# ----------------------------
# Two pointers
# ----------------------------

def reverse_vowels(s: str) -> str:
    """
    Reverse only the vowels in s.

    Example:
      "hello" -> "holle"
    """
    vowels = set("aeiouAEIOU")
    chars = list(s)
    l, r = 0, len(chars) - 1

    while l < r:
        while l < r and chars[l] not in vowels:
            l += 1
        while l < r and chars[r] not in vowels:
            r -= 1
        if l < r:
            chars[l], chars[r] = chars[r], chars[l]
            l += 1
            r -= 1

    return "".join(chars)


def squares_sorted(nums: Sequence[int]) -> List[int]:
    """
    Given a sorted array (may include negatives), return sorted squares.

    Pattern:
      largest square must come from either end.
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    out = [0] * n
    l, r = 0, n - 1
    write = n - 1

    while l <= r:
        left_sq = nums[l] * nums[l]
        right_sq = nums[r] * nums[r]
        if left_sq > right_sq:
            out[write] = left_sq
            l += 1
        else:
            out[write] = right_sq
            r -= 1
        write -= 1

    return out


def container_with_most_water(heights: Sequence[int]) -> int:
    """
    Classic "Container With Most Water".

    Pattern:
      Two pointers inward; move the smaller height pointer.
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(heights) - 1
    best = 0
    while l < r:
        h = min(heights[l], heights[r])
        best = max(best, h * (r - l))
        if heights[l] < heights[r]:
            l += 1
        else:
            r -= 1
    return best


def is_subsequence(s: str, t: str) -> bool:
    """
    Return True if s is a subsequence of t.

    Same-direction pointers:
      advance i on matches; always advance j
    """
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)


# ----------------------------
# Sliding window
# ----------------------------

def longest_substring_without_repeating(s: str) -> int:
    """
    Return length of the longest substring without repeating characters.

    Pattern:
      window with last-seen index map; jump left pointer forward.
    Time: O(n)
    Space: O(distinct chars)
    """
    last: Dict[str, int] = {}
    l = 0
    best = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            l = last[ch] + 1
        last[ch] = r
        best = max(best, r - l + 1)
    return best


def min_window_substring(s: str, t: str) -> str:
    """
    Return the minimum window in s which contains all chars of t (with multiplicity).
    Returns "" if no such window exists.

    Classic variable-window:
      - expand right until valid
      - then shrink left to minimal while keeping valid

    Time: O(|s| + |t|)
    Space: O(|alphabet|)
    """
    if not t:
        return ""
    if len(t) > len(s):
        return ""

    need = Counter(t)
    missing = len(t)  # total chars still missing (counts multiplicity)
    l = 0

    best_len = float("inf")
    best_range: Optional[Tuple[int, int]] = None  # inclusive-exclusive [start, end)

    for r, ch in enumerate(s):
        if ch in need:
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1

        # When we've satisfied all requirements, try to shrink.
        while missing == 0:
            window_len = r - l + 1
            if window_len < best_len:
                best_len = window_len
                best_range = (l, r + 1)

            left_ch = s[l]
            if left_ch in need:
                need[left_ch] += 1
                if need[left_ch] > 0:
                    missing += 1
            l += 1

    if best_range is None:
        return ""
    return s[best_range[0]:best_range[1]]


if __name__ == "__main__":
    print(reverse_vowels("hello"))
    print(squares_sorted([-4, -1, 0, 3, 10]))
    print(container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]))
    print(is_subsequence("abc", "ahbgdc"))
    print(longest_substring_without_repeating("abcabcbb"))
    print(min_window_substring("ADOBECODEBANC", "ABC"))
