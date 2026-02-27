"""
Recursion & Backtracking — generating subsets/permutations/combinations (Part 2/4)

This file is about the "generate all possibilities" toolkit:
- subsets                  (power set)
- subsets_with_dup         (handles duplicates in input)
- permutations             (all orderings)
- permutations_unique      (handles duplicates)
- combinations_n_choose_k  (choose k from 1..n)
- combination_sum          (classic "choose numbers that sum to target", reuse allowed)

Patterns:
- Choose / explore / un-choose (backtracking)
- Sorting + skip duplicates
- Early pruning (e.g., if partial sum exceeds target)

Next file:
3) backtracking_constraints.py (N-Queens + pruning patterns)
"""

from __future__ import annotations

from typing import List, Sequence


# ----------------------------
# Subsets
# ----------------------------

def subsets(nums: Sequence[int]) -> List[List[int]]:
    """
    Return all subsets (the power set).
    Input treated as distinct elements.

    Time: O(2^n)
    """
    out: List[List[int]] = []
    path: List[int] = []

    def dfs(i: int) -> None:
        if i == len(nums):
            out.append(path.copy())
            return
        # exclude
        dfs(i + 1)
        # include
        path.append(nums[i])
        dfs(i + 1)
        path.pop()

    dfs(0)
    return out


def subsets_with_dup(nums: Sequence[int]) -> List[List[int]]:
    """
    Return all unique subsets when nums may contain duplicates.

    Trick:
      Sort, then in the "include/exclude" style, skipping duplicates is awkward.
      Instead, use a for-loop backtracking where you choose next elements,
      and skip equal neighbors at the same recursion level.
    """
    nums_sorted = sorted(nums)
    out: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int) -> None:
        out.append(path.copy())
        for i in range(start, len(nums_sorted)):
            if i > start and nums_sorted[i] == nums_sorted[i - 1]:
                continue
            path.append(nums_sorted[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return out


# ----------------------------
# Permutations
# ----------------------------

def permutations(nums: Sequence[int]) -> List[List[int]]:
    """
    Return all permutations (assumes distinct elements).

    Time: O(n!)
    """
    out: List[List[int]] = []
    path: List[int] = []
    used = [False] * len(nums)

    def dfs() -> None:
        if len(path) == len(nums):
            out.append(path.copy())
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return out


def permutations_unique(nums: Sequence[int]) -> List[List[int]]:
    """
    Return all unique permutations when nums may contain duplicates.

    Trick:
      Sort and skip duplicates *only when the previous duplicate hasn't been used*
      at the current depth.
    """
    nums_sorted = sorted(nums)
    out: List[List[int]] = []
    path: List[int] = []
    used = [False] * len(nums_sorted)

    def dfs() -> None:
        if len(path) == len(nums_sorted):
            out.append(path.copy())
            return
        for i in range(len(nums_sorted)):
            if used[i]:
                continue
            if i > 0 and nums_sorted[i] == nums_sorted[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums_sorted[i])
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return out


# ----------------------------
# Combinations
# ----------------------------

def combinations_n_choose_k(n: int, k: int) -> List[List[int]]:
    """
    Return all combinations of k numbers chosen from 1..n.

    Example:
      n=4, k=2 -> [ [1,2],[1,3],[1,4],[2,3],[2,4],[3,4] ]
    """
    if k < 0 or n < 0:
        raise ValueError("n and k must be non-negative")
    if k > n:
        return []

    out: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int) -> None:
        # Prune: if remaining numbers are insufficient to fill k
        if len(path) + (n - start + 1) < k:
            return
        if len(path) == k:
            out.append(path.copy())
            return
        for x in range(start, n + 1):
            path.append(x)
            dfs(x + 1)
            path.pop()

    dfs(1)
    return out


def combination_sum(candidates: Sequence[int], target: int) -> List[List[int]]:
    """
    Return unique combinations where numbers sum to target.
    Each candidate can be used unlimited times.

    Assumptions:
      candidates are positive integers.

    Example:
      candidates=[2,3,6,7], target=7 -> [[2,2,3],[7]]
    """
    if target < 0:
        return []

    nums = sorted(candidates)
    out: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path.copy())
            return
        for i in range(start, len(nums)):
            x = nums[i]
            if x > remaining:
                break  # pruning
            path.append(x)
            dfs(i, remaining - x)  # reuse allowed
            path.pop()

    dfs(0, target)
    return out


if __name__ == "__main__":
    print("subsets([1,2]):", subsets([1, 2]))
    print("subsets_with_dup([1,2,2]):", subsets_with_dup([1, 2, 2]))
    print("permutations([1,2,3]) size:", len(permutations([1, 2, 3])))
    print("permutations_unique([1,1,2]):", permutations_unique([1, 1, 2]))
    print("nCk:", combinations_n_choose_k(4, 2))
    print("comb_sum:", combination_sum([2, 3, 6, 7], 7))
