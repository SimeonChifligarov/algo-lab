"""
Trees Basics — utilities + BFS/DFS patterns (Part 3/4)

Includes:
- size (number of nodes)
- height (max depth)
- invert (mirror a tree)
- are_equal (structural + value equality)
- is_same_values_multiset (counts values via DFS)
- max_path_sum_root_to_leaf (classic DFS pattern)
- has_path_sum (DFS backtracking / early exit)
- is_valid_bst (BST validation via bounds)

Next file:
4) test_trees_basics.py
"""

from __future__ import annotations

from collections import Counter, deque
from typing import Deque, Optional, TypeVar, Generic, Tuple

from tree_core import TreeNode

T = TypeVar("T")


def size(root: Optional[TreeNode[T]]) -> int:
    """Number of nodes in the tree."""
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)


def height(root: Optional[TreeNode[T]]) -> int:
    """
    Height / max depth of the tree.
    Returns 0 for empty tree, 1 for single node.
    """
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def invert(root: Optional[TreeNode[T]]) -> Optional[TreeNode[T]]:
    """
    Invert (mirror) the tree in-place and return root.
    """
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert(root.left)
    invert(root.right)
    return root


def are_equal(a: Optional[TreeNode[T]], b: Optional[TreeNode[T]]) -> bool:
    """
    Structural + value equality.
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    return a.value == b.value and are_equal(a.left, b.left) and are_equal(a.right, b.right)


def is_same_values_multiset(a: Optional[TreeNode[T]], b: Optional[TreeNode[T]]) -> bool:
    """
    Compare trees by the multiset of their values (ignores structure).
    Useful to show "DFS scan + frequency counts" pattern.
    """

    def count(root: Optional[TreeNode[T]]) -> Counter:
        c = Counter()
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            c[node.value] += 1
            stack.append(node.left)
            stack.append(node.right)
        return c

    return count(a) == count(b)


def max_path_sum_root_to_leaf(root: Optional[TreeNode[int]]) -> int:
    """
    Return maximum root-to-leaf sum.
    For empty tree, returns 0.
    """
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return root.value
    return root.value + max(
        max_path_sum_root_to_leaf(root.left),
        max_path_sum_root_to_leaf(root.right),
    )


def has_path_sum(root: Optional[TreeNode[int]], target_sum: int) -> bool:
    """
    Return True if there's a root-to-leaf path with sum == target_sum.
    Uses DFS with early exit.
    """
    if root is None:
        return False
    if root.left is None and root.right is None:
        return root.value == target_sum
    rem = target_sum - root.value
    return has_path_sum(root.left, rem) or has_path_sum(root.right, rem)


def is_valid_bst(root: Optional[TreeNode[int]]) -> bool:
    """
    Validate BST property using recursive bounds:
      left < node < right for all nodes.
    """

    def dfs(node: Optional[TreeNode[int]], lo: Optional[int], hi: Optional[int]) -> bool:
        if node is None:
            return True
        v = node.value
        if lo is not None and v <= lo:
            return False
        if hi is not None and v >= hi:
            return False
        return dfs(node.left, lo, v) and dfs(node.right, v, hi)

    return dfs(root, None, None)


if __name__ == "__main__":
    from tree_core import build_tree_level_order, tree_to_level_order

    t = build_tree_level_order([4, 2, 7, 1, 3, 6, 9])
    print("size:", size(t))
    print("height:", height(t))
    print("valid bst:", is_valid_bst(t))
    print("max root->leaf sum:", max_path_sum_root_to_leaf(t))
    print("has path sum 7:", has_path_sum(t, 7))

    invert(t)
    print("inverted:", tree_to_level_order(t))
