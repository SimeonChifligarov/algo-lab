"""
Binary Search Trees — core types + basic operations (Part 1/4)

This file provides the BST foundation:
- BSTNode: node structure
- insert, search
- build_bst (from iterable)
- inorder_values (sorted view)

Next files:
2) bst_delete.py        (delete operation + helpers)
3) bst_queries.py       (is_bst, LCA, kth smallest, range queries)
4) test_bst.py          (unittest suite)

Conventions:
- BST stores comparable values (supports < and >).
- Duplicates policy: duplicates go to the RIGHT subtree.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar, List

T = TypeVar("T")


@dataclass
class BSTNode(Generic[T]):
    value: T
    left: Optional["BSTNode[T]"] = None
    right: Optional["BSTNode[T]"] = None

    def __repr__(self) -> str:
        return f"BSTNode({self.value!r})"


# ----------------------------
# Basic operations
# ----------------------------

def search(root: Optional[BSTNode[T]], x: T) -> Optional[BSTNode[T]]:
    """
    Return the node containing x, or None if not found.
    """
    cur = root
    while cur is not None:
        if x == cur.value:
            return cur
        if x < cur.value:  # type: ignore[operator]
            cur = cur.left
        else:
            cur = cur.right
    return None


def insert(root: Optional[BSTNode[T]], x: T) -> BSTNode[T]:
    """
    Insert x into the BST and return the (possibly new) root.
    Duplicates go to the right subtree.
    """
    if root is None:
        return BSTNode(x)

    cur = root
    while True:
        if x < cur.value:  # type: ignore[operator]
            if cur.left is None:
                cur.left = BSTNode(x)
                break
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = BSTNode(x)
                break
            cur = cur.right
    return root


def build_bst(values: Iterable[T]) -> Optional[BSTNode[T]]:
    """
    Build a BST by inserting values in order.
    Returns the root (or None for empty iterable).
    """
    root: Optional[BSTNode[T]] = None
    for v in values:
        root = insert(root, v)
    return root


# ----------------------------
# Traversal (sorted view)
# ----------------------------

def inorder_values(root: Optional[BSTNode[T]]) -> List[T]:
    """
    Inorder traversal returns values in sorted order for a valid BST.
    """
    out: List[T] = []

    def dfs(node: Optional[BSTNode[T]]) -> None:
        if node is None:
            return
        dfs(node.left)
        out.append(node.value)
        dfs(node.right)

    dfs(root)
    return out


def inorder_iter(root: Optional[BSTNode[T]]) -> Iterator[T]:
    """
    Iterative inorder generator (sorted stream for a BST).
    """
    stack: List[BSTNode[T]] = []
    cur = root
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        yield cur.value
        cur = cur.right


if __name__ == "__main__":
    r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
    print("inorder:", inorder_values(r))
    print("search 6:", search(r, 6))
    print("search 10:", search(r, 10))
