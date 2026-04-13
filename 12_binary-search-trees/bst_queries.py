"""
Binary Search Trees — validation and common queries (Part 3/4)

Implements:
- is_bst: validate BST invariant using bounds
- lca_bst: lowest common ancestor in a BST (BST-specific, O(h))
- kth_smallest: kth smallest element (1-based) using inorder (iterative)
- range_query: return all values in [lo, hi] (inclusive) in sorted order

Duplicates policy:
- duplicates go to the RIGHT subtree.

Next file:
4) test_bst.py
"""

from __future__ import annotations

from typing import List, Optional, TypeVar

try:
    from .bst_core import BSTNode
except ImportError:
    from bst_core import BSTNode

T = TypeVar("T")


def is_bst(root: Optional[BSTNode[T]]) -> bool:
    """
    Validate BST property using recursive bounds.

    With duplicates going RIGHT, the invariant is:
      left subtree: values < node.value
      right subtree: values >= node.value
    """

    def dfs(node: Optional[BSTNode[T]], lo: Optional[T], hi: Optional[T]) -> bool:
        if node is None:
            return True

        v = node.value
        # lower bound: v must be >= lo
        if lo is not None and v < lo:  # type: ignore[operator]
            return False
        # upper bound: v must be < hi (strict), so duplicates can't appear on the left
        if hi is not None and v >= hi:  # type: ignore[operator]
            return False

        return dfs(node.left, lo, v) and dfs(node.right, v, hi)

    return dfs(root, None, None)


def lca_bst(root: Optional[BSTNode[T]], a: T, b: T) -> Optional[BSTNode[T]]:
    """
    Lowest Common Ancestor in a BST (BST-specific).

    Returns None if root is None.
    Note: does not require that a and b exist in the tree.
    """
    if root is None:
        return None

    x, y = (a, b) if a <= b else (b, a)  # type: ignore[operator]
    cur = root
    while cur is not None:
        if y < cur.value:  # type: ignore[operator]
            cur = cur.left
        elif x > cur.value:  # type: ignore[operator]
            cur = cur.right
        else:
            return cur
    return None


def kth_smallest(root: Optional[BSTNode[T]], k: int) -> T:
    """
    Return the kth smallest value (1-based) in the BST.
    """
    if k <= 0:
        raise ValueError("k must be >= 1")

    i = 0
    for v in inorder_iter(root):
        i += 1
        if i == k:
            return v
    raise IndexError("k is larger than number of nodes")


def range_query(root: Optional[BSTNode[T]], lo: T, hi: T) -> List[T]:
    """
    Return all values in [lo, hi] inclusive, in sorted order.

    BST pruning:
      - if node.value < lo -> skip left, go right
      - if node.value > hi -> skip right, go left

    IMPORTANT with duplicates-go-right:
      - if node.value == hi, duplicates equal to hi may still exist in the RIGHT subtree,
        so we must allow exploring right when node.value <= hi (not strictly < hi).
    """
    # Normalize bounds if lo > hi
    if lo > hi:  # type: ignore[operator]
        lo, hi = hi, lo  # type: ignore[misc]

    out: List[T] = []

    def dfs(node: Optional[BSTNode[T]]) -> None:
        if node is None:
            return

        if node.value > lo:  # type: ignore[operator]
            dfs(node.left)

        if lo <= node.value <= hi:  # type: ignore[operator]
            out.append(node.value)

        # FIX: allow right traversal when node.value == hi to capture duplicates of hi
        if node.value <= hi:  # type: ignore[operator]
            dfs(node.right)

    dfs(root)
    return out


if __name__ == "__main__":
    from bst_core import build_bst

    r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
    print(range_query(r, 4, 7))  # [4, 5, 6, 7, 7]
