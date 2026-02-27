"""
Recursion & Backtracking — recursion fundamentals (Part 1/4)

This file focuses on recursion "building blocks" you should feel comfortable with:
- recursion on sequences (sum, max, binary search)
- divide-and-conquer patterns (merge sort)
- simple recursion on trees (depth / traversal) with a tiny TreeNode type

Next files:
2) backtracking_subsets_perms.py  (subsets, permutations, combinations)
3) backtracking_constraints.py    (N-Queens + pruning patterns)
4) test_recursion_backtracking.py (unittest suite)

All code is standard-library-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


# ----------------------------
# Recursion on sequences
# ----------------------------

def recursive_sum(nums: Sequence[int]) -> int:
    """Return sum(nums) using recursion."""

    def helper(i: int) -> int:
        if i == len(nums):
            return 0
        return nums[i] + helper(i + 1)

    return helper(0)


def recursive_max(nums: Sequence[int]) -> int:
    """
    Return max(nums) using recursion.
    Raises ValueError on empty input.
    """
    if not nums:
        raise ValueError("recursive_max() arg is an empty sequence")

    def helper(i: int) -> int:
        if i == len(nums) - 1:
            return nums[i]
        m = helper(i + 1)
        return nums[i] if nums[i] > m else m

    return helper(0)


def recursive_binary_search(nums: Sequence[int], target: int) -> int:
    """
    Return index of target in sorted nums, or -1 if not found.
    Uses recursive binary search.

    Time: O(log n)
    Space: O(log n) recursion depth
    """

    def helper(lo: int, hi: int) -> int:
        if lo >= hi:
            return -1
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return helper(mid + 1, hi)
        return helper(lo, mid)

    return helper(0, len(nums))


# ----------------------------
# Divide and conquer (merge sort)
# ----------------------------

def merge_sort(nums: Sequence[int]) -> List[int]:
    """
    Return a sorted copy of nums using merge sort (recursive).

    Time: O(n log n)
    Space: O(n)
    """
    n = len(nums)
    if n <= 1:
        return list(nums)

    mid = n // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return _merge(left, right)


def _merge(a: List[int], b: List[int]) -> List[int]:
    i = j = 0
    out: List[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


# ----------------------------
# Recursion on trees
# ----------------------------

@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def tree_depth(root: Optional[TreeNode]) -> int:
    """Return max depth of a binary tree (0 for empty)."""
    if root is None:
        return 0
    return 1 + max(tree_depth(root.left), tree_depth(root.right))


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Return inorder traversal values."""
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.value] + inorder_traversal(root.right)


def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Return preorder traversal values."""
    if root is None:
        return []
    return [root.value] + preorder_traversal(root.left) + preorder_traversal(root.right)


def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Return postorder traversal values."""
    if root is None:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.value]


if __name__ == "__main__":
    print("sum:", recursive_sum([1, 2, 3, 4]))
    print("max:", recursive_max([1, 9, 3, 7]))
    print("bs:", recursive_binary_search([1, 3, 5, 7, 9], 7))
    print("merge_sort:", merge_sort([5, 2, 4, 6, 1, 3]))

    t = TreeNode(2, left=TreeNode(1), right=TreeNode(3))
    print("depth:", tree_depth(t))
    print("inorder:", inorder_traversal(t))
