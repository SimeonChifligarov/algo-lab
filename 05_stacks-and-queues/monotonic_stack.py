"""
Stacks & Queues — monotonic stack patterns (Part 2/4)

This file focuses on classic monotonic-stack problems:
- next_greater_elements       (monotonic decreasing stack)
- daily_temperatures          (days until warmer temperature)
- largest_rectangle_area      (histogram max rectangle)
- stock_span                  (online-style span query in batch form)

Why monotonic stacks?
They let us answer "next/previous greater/smaller" questions in O(n)
by keeping the stack ordered (monotonic increasing/decreasing).

Next files:
3) queue_basics.py
4) test_stacks_queues.py
"""

from __future__ import annotations

from typing import List, Sequence, Tuple


# ----------------------------
# Next greater element (right side)
# ----------------------------

def next_greater_elements(nums: Sequence[int]) -> List[int]:
    """
    For each index i, return the next greater value to the RIGHT of nums[i],
    or -1 if no greater value exists.

    Example:
      [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]

    Pattern:
      Keep a decreasing stack of indices.
      When current value is larger, it resolves previous indices.
    """
    n = len(nums)
    ans = [-1] * n
    st: List[int] = []  # indices, nums[st] decreasing

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            j = st.pop()
            ans[j] = x
        st.append(i)

    return ans


def next_greater_indices(nums: Sequence[int]) -> List[int]:
    """
    Same idea as next_greater_elements, but returns the INDEX of the next greater
    element to the right, or -1 if none exists.

    Example:
      [2, 1, 2, 4, 3] -> [3, 2, 3, -1, -1]
    """
    n = len(nums)
    ans = [-1] * n
    st: List[int] = []

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            j = st.pop()
            ans[j] = i
        st.append(i)

    return ans


# ----------------------------
# Daily Temperatures
# ----------------------------

def daily_temperatures(temps: Sequence[int]) -> List[int]:
    """
    Return, for each day, how many days until a warmer temperature.
    If none, return 0 for that day.

    Example:
      [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]

    Pattern:
      Monotonic decreasing stack of indices (by temperature).
    """
    n = len(temps)
    ans = [0] * n
    st: List[int] = []  # indices of unresolved days, temps decreasing

    for i, t in enumerate(temps):
        while st and temps[st[-1]] < t:
            j = st.pop()
            ans[j] = i - j
        st.append(i)

    return ans


# ----------------------------
# Largest Rectangle in Histogram
# ----------------------------

def largest_rectangle_area(heights: Sequence[int]) -> int:
    """
    Return the area of the largest rectangle in a histogram.

    Example:
      [2,1,5,6,2,3] -> 10

    Pattern:
      Monotonic increasing stack of (start_index, height).
      When a lower bar arrives, pop taller bars and compute areas.

    Time: O(n)
    Space: O(n)
    """
    best = 0
    st: List[Tuple[int, int]] = []  # (start_index, height), heights increasing

    for i, h in enumerate(heights):
        start = i
        # Current bar closes rectangles formed by taller bars.
        while st and st[-1][1] > h:
            idx, height = st.pop()
            best = max(best, height * (i - idx))
            start = idx  # current shorter bar can extend back to idx
        st.append((start, h))

    n = len(heights)
    # Flush remaining bars (they extend to the end)
    while st:
        idx, height = st.pop()
        best = max(best, height * (n - idx))

    return best


# ----------------------------
# Stock Span (batch version)
# ----------------------------

def stock_span(prices: Sequence[int]) -> List[int]:
    """
    For each day i, return the stock span:
    number of consecutive days up to i (inclusive) where price <= prices[i].

    Example:
      [100, 80, 60, 70, 60, 75, 85] -> [1, 1, 1, 2, 1, 4, 6]

    Pattern:
      Monotonic decreasing stack of indices by price.
    """
    spans = [0] * len(prices)
    st: List[int] = []  # indices, prices[st] strictly decreasing

    for i, p in enumerate(prices):
        while st and prices[st[-1]] <= p:
            st.pop()

        prev_greater_idx = st[-1] if st else -1
        spans[i] = i - prev_greater_idx
        st.append(i)

    return spans


if __name__ == "__main__":
    print("next greater values:", next_greater_elements([2, 1, 2, 4, 3]))
    print("next greater idxs:", next_greater_indices([2, 1, 2, 4, 3]))
    print("daily temps:", daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    print("largest histogram:", largest_rectangle_area([2, 1, 5, 6, 2, 3]))
    print("stock span:", stock_span([100, 80, 60, 70, 60, 75, 85]))
