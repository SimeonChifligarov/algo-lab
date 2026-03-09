"""
Binary Search Trees — delete operation (Part 2/4)

Implements:
- delete(root, x): remove one occurrence of value x (duplicates go right)
- helper: find_min_node (inorder successor)
- helper: remove_min_node (delete the minimum node in a subtree)

Delete cases:
1) node not found -> tree unchanged
2) node is a leaf -> remove it
3) node has 1 child -> replace node with its child
4) node has 2 children -> replace node's value with inorder successor,
   then delete successor in right subtree

Next files:
3) bst_queries.py
4) test_bst.py
"""

from __future__ import annotations

from typing import Optional, TypeVar, Tuple

from bst_core import BSTNode

T = TypeVar("T")


def find_min_node(root: BSTNode[T]) -> BSTNode[T]:
    """Return the node with minimum value in this subtree."""
    cur = root
    while cur.left is not None:
        cur = cur.left
    return cur


def delete(root: Optional[BSTNode[T]], x: T) -> Optional[BSTNode[T]]:
    """
    Delete ONE occurrence of x from the BST and return the new root.
    If x is not found, returns the original root.

    Duplicates policy reminder:
      duplicates were inserted into the right subtree, so deletion will remove
      the first match found along the search path.
    """
    if root is None:
        return None

    if x < root.value:  # type: ignore[operator]
        root.left = delete(root.left, x)
        return root
    if x > root.value:  # type: ignore[operator]
        root.right = delete(root.right, x)
        return root

    # Found node to delete: root.value == x
    if root.left is None and root.right is None:
        return None
    if root.left is None:
        return root.right
    if root.right is None:
        return root.left

    # Two children: replace with inorder successor (min in right subtree)
    succ = find_min_node(root.right)
    root.value = succ.value
    root.right = delete(root.right, succ.value)
    return root


if __name__ == "__main__":
    from bst_core import build_bst, inorder_values

    r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
    print("inorder:", inorder_values(r))
    r = delete(r, 7)
    print("after delete 7:", inorder_values(r))
    r = delete(r, 5)
    print("after delete 5:", inorder_values(r))
