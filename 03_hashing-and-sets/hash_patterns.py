"""
Hashing & Sets — classic algorithm patterns (Part 3/4)

Includes:
- two_sum_indices: hash map lookup for complements
- group_anagrams: bucket by "signature"
- longest_consecutive: set-based scan with O(n) expected time
- intersection_unique: unique intersection using sets
- has_duplicate: membership trick

These are the patterns you see constantly in interviews and real code.
"""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Sequence, Tuple


def two_sum_indices(nums: Sequence[int], target: int) -> Tuple[int, int]:
    """
    Return indices (i, j) such that nums[i] + nums[j] == target.
    Assumes exactly one solution exists.
    Raises ValueError if no solution.

    Pattern:
      seen[value] = index
      for each x: check if (target-x) is in seen
    """
    seen: Dict[int, int] = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return seen[need], i
        # store after check to avoid using same element twice
        seen[x] = i
    raise ValueError("No two-sum solution")


def group_anagrams(words: Iterable[str]) -> List[List[str]]:
    """
    Group words that are anagrams.

    Signature choice:
      tuple(sorted(word))  (simple and clear)
    Time:
      O(total_chars * log word_length) due to sorting each word.

    Alternative (faster for lowercase a-z):
      26-count signature.
    """
    buckets: DefaultDict[Tuple[str, ...], List[str]] = defaultdict(list)
    for w in words:
        sig = tuple(sorted(w))
        buckets[sig].append(w)
    return list(buckets.values())


def longest_consecutive(nums: Iterable[int]) -> int:
    """
    Return length of the longest run of consecutive integers.

    Expected O(n):
      - Put all numbers into a set
      - Only start counting from numbers that are "starts" (x-1 not in set)
    """
    s = set(nums)
    best = 0
    for x in s:
        if (x - 1) not in s:  # start of a run
            length = 1
            y = x + 1
            while y in s:
                length += 1
                y += 1
            if length > best:
                best = length
    return best


def intersection_unique(a: Iterable[int], b: Iterable[int]) -> List[int]:
    """
    Unique intersection of two sequences, returned as a list.
    Order is arbitrary (set order).
    """
    return list(set(a) & set(b))


def has_duplicate(items: Iterable[object]) -> bool:
    """
    Return True if any element appears at least twice.
    """
    seen = set()
    for x in items:
        if x in seen:
            return True
        seen.add(x)
    return False


if __name__ == "__main__":
    print(two_sum_indices([2, 7, 11, 15], 9))
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))
    print(intersection_unique([1, 2, 2, 3], [2, 2, 4]))
    print(has_duplicate([1, 2, 3, 2]))
