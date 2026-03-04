"""
Binary Search & Bounds — binary search on answer / parametric search (Part 3/4)

Idea:
Sometimes you can't directly binary-search an array.
Instead, you binary-search the ANSWER space because a predicate is monotonic:

  predicate(x) is False for small x, then True for large x  (or vice versa)

We implement:
- first_true(lo, hi, pred): smallest x in [lo, hi] with pred(x)=True (inclusive bounds)
- last_true(lo, hi, pred): largest x in [lo, hi] with pred(x)=True

And a few canonical applications:
- sqrt_floor(n): floor(sqrt(n)) using predicate mid*mid <= n
- min_capacity_to_ship(weights, days): classic "ship within D days" capacity problem
- min_eating_speed(piles, h): classic "Koko eating bananas" speed problem

Next file:
4) test_binary_search.py
"""

from __future__ import annotations

from typing import Callable, Iterable, List, Sequence


# ----------------------------
# Generic parametric search helpers
# ----------------------------

def first_true(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """
    Return the smallest x in [lo, hi] such that pred(x) is True.
    Assumes pred is monotonic: F F F ... T T T

    Raises ValueError if pred is False for all x in [lo, hi].
    """
    if lo > hi:
        raise ValueError("lo must be <= hi")

    left, right = lo, hi
    while left < right:
        mid = (left + right) // 2
        if pred(mid):
            right = mid
        else:
            left = mid + 1

    if not pred(left):
        raise ValueError("No True value in range")
    return left


def last_true(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """
    Return the largest x in [lo, hi] such that pred(x) is True.
    Assumes pred is monotonic: T T T ... F F F  (or equivalently last True before first False)

    Raises ValueError if pred is False for all x in [lo, hi].
    """
    if lo > hi:
        raise ValueError("lo must be <= hi")

    left, right = lo, hi
    while left < right:
        mid = (left + right + 1) // 2
        if pred(mid):
            left = mid
        else:
            right = mid - 1

    if not pred(left):
        raise ValueError("No True value in range")
    return left


# ----------------------------
# Example 1: floor sqrt
# ----------------------------

def sqrt_floor(n: int) -> int:
    """
    Return floor(sqrt(n)) for n >= 0 using binary search on answer.

    Time: O(log n)
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n

    def ok(x: int) -> bool:
        return x * x <= n

    # Find the last x with x^2 <= n in [0, n]
    return last_true(0, n, ok)


# ----------------------------
# Example 2: Ship packages within D days
# ----------------------------

def min_capacity_to_ship(weights: Sequence[int], days: int) -> int:
    """
    Given weights and days, find minimal ship capacity to ship all in order in <= days.

    Monotonic predicate:
      capacity C is feasible -> any larger capacity also feasible.

    Time: O(n log(sum(weights)))
    """
    if days <= 0:
        raise ValueError("days must be >= 1")
    if not weights:
        return 0
    if any(w <= 0 for w in weights):
        raise ValueError("weights must be positive integers")

    lo = max(weights)  # must fit the heaviest item
    hi = sum(weights)  # capacity big enough to ship all in 1 day

    def feasible(cap: int) -> bool:
        used_days = 1
        cur = 0
        for w in weights:
            if cur + w <= cap:
                cur += w
            else:
                used_days += 1
                cur = w
                if used_days > days:
                    return False
        return True

    return first_true(lo, hi, feasible)


# ----------------------------
# Example 3: Koko eating bananas
# ----------------------------

def min_eating_speed(piles: Sequence[int], h: int) -> int:
    """
    Find minimal integer speed k such that Koko can eat all piles within h hours.

    Predicate:
      speed k feasible -> any larger speed feasible.

    Time: O(n log(max(piles)))
    """
    if h <= 0:
        raise ValueError("h must be >= 1")
    if not piles:
        return 0
    if any(p <= 0 for p in piles):
        raise ValueError("piles must be positive integers")

    lo, hi = 1, max(piles)

    def hours_needed(speed: int) -> int:
        total = 0
        for p in piles:
            # ceil(p / speed) without floats
            total += (p + speed - 1) // speed
        return total

    def feasible(speed: int) -> bool:
        return hours_needed(speed) <= h

    return first_true(lo, hi, feasible)


if __name__ == "__main__":
    print("sqrt_floor(0..20):", [sqrt_floor(i) for i in range(21)])
    print("ship cap:", min_capacity_to_ship([1, 2, 3, 1, 1], 4))  # 3
    print("koko:", min_eating_speed([3, 6, 7, 11], 8))  # 4
