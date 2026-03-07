"""
Trees Basics — core types + building from level-order arrays (Part 1/4)

This file defines:
- TreeNode: binary tree node
- build_tree_level_order: build a binary tree from a level-order array (with None holes)
- tree_to_level_order: convert back to a trimmed level-order array (useful for tests)

Level-order convention (INDEX-MAPPED / array representation):
- Input is a list like [1, None, 2, None, None, None, 3]
- None means "no node at this position"
- Children are assigned by index:
    left child of i  -> 2*i + 1
    right child of i -> 2*i + 2

This matches typical "heap-style" array representations used in many problems/tests.

Next files:
2) tree_traversals.py
3) tree_utils.py
4) test_trees_basics.py
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from typing import Deque, Generic, List, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class TreeNode(Generic[T]):
    value: T
    left: Optional["TreeNode[T]"] = None
    right: Optional["TreeNode[T]"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.value!r})"


def build_tree_level_order(values: Sequence[Optional[T]]) -> Optional[TreeNode[T]]:
    """
    Build a binary tree from a level-order array using index mapping:
      left child of i  -> 2*i + 1
      right child of i -> 2*i + 2

    Examples:
      [] -> None
      [None] -> None
      [1,2,3,None,4] ->
           1
          / \
         2   3
          \
           4

      [1, None, 2, None, None, None, 3] ->
         1
          \
           2
            \
             3
    """
    if not values or values[0] is None:
        return None

    # Create node objects for non-None entries
    nodes: List[Optional[TreeNode[T]]] = [None] * len(values)
    for i, v in enumerate(values):
        if v is not None:
            nodes[i] = TreeNode(v)

    # Wire children by index
    for i, node in enumerate(nodes):
        if node is None:
            continue
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            node.left = nodes[li]
        if ri < len(nodes):
            node.right = nodes[ri]

    return nodes[0]


def tree_to_level_order(root: Optional[TreeNode[T]]) -> List[Optional[T]]:
    """
    Convert a tree to a level-order list with None placeholders, trimmed.

    Trimming rule:
      Trailing Nones are removed (since they add no structural info at the end).
    """
    if root is None:
        return []

    out: List[Optional[T]] = []
    q: Deque[Optional[TreeNode[T]]] = deque([root])

    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.value)
        # Always enqueue children to preserve shape
        q.append(node.left)
        q.append(node.right)

    # trim trailing None
    while out and out[-1] is None:
        out.pop()

    return out


if __name__ == "__main__":
    t = build_tree_level_order([1, 2, 3, None, 4])
    print("level order:", tree_to_level_order(t))

    t2 = build_tree_level_order([1, None, 2, None, None, None, 3])
    print("level order 2:", tree_to_level_order(t2))
