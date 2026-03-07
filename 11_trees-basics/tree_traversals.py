"""
Trees Basics — traversals (Part 2/4)

Implements:
- preorder / inorder / postorder (recursive and iterative)
- level_order (BFS)
- level_order_levels (BFS grouped by level)

Next files:
3) tree_utils.py
4) test_trees_basics.py
"""

from __future__ import annotations

from collections import deque
from typing import Deque, List, Optional, Sequence, TypeVar

from tree_core import TreeNode

T = TypeVar("T")


# ----------------------------
# DFS traversals (recursive)
# ----------------------------

def preorder_recursive(root: Optional[TreeNode[T]]) -> List[T]:
    if root is None:
        return []
    return [root.value] + preorder_recursive(root.left) + preorder_recursive(root.right)


def inorder_recursive(root: Optional[TreeNode[T]]) -> List[T]:
    if root is None:
        return []
    return inorder_recursive(root.left) + [root.value] + inorder_recursive(root.right)


def postorder_recursive(root: Optional[TreeNode[T]]) -> List[T]:
    if root is None:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.value]


# ----------------------------
# DFS traversals (iterative)
# ----------------------------

def preorder_iterative(root: Optional[TreeNode[T]]) -> List[T]:
    """
    Root, Left, Right using a stack.
    """
    if root is None:
        return []
    out: List[T] = []
    st: List[TreeNode[T]] = [root]
    while st:
        node = st.pop()
        out.append(node.value)
        # push right first so left is processed first
        if node.right is not None:
            st.append(node.right)
        if node.left is not None:
            st.append(node.left)
    return out


def inorder_iterative(root: Optional[TreeNode[T]]) -> List[T]:
    """
    Left, Root, Right using a stack and a pointer.
    """
    out: List[T] = []
    st: List[TreeNode[T]] = []
    cur = root
    while cur is not None or st:
        while cur is not None:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        out.append(cur.value)
        cur = cur.right
    return out


def postorder_iterative(root: Optional[TreeNode[T]]) -> List[T]:
    """
    Left, Right, Root iterative.

    Common trick:
      Do a modified preorder: Root, Right, Left then reverse.
    """
    if root is None:
        return []
    out: List[T] = []
    st: List[TreeNode[T]] = [root]
    while st:
        node = st.pop()
        out.append(node.value)
        if node.left is not None:
            st.append(node.left)
        if node.right is not None:
            st.append(node.right)
    out.reverse()
    return out


# ----------------------------
# BFS traversals
# ----------------------------

def level_order(root: Optional[TreeNode[T]]) -> List[T]:
    """
    Return level-order traversal as a flat list.
    """
    if root is None:
        return []
    out: List[T] = []
    q: Deque[TreeNode[T]] = deque([root])
    while q:
        node = q.popleft()
        out.append(node.value)
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
    return out


def level_order_levels(root: Optional[TreeNode[T]]) -> List[List[T]]:
    """
    Return level-order traversal grouped by depth.
    """
    if root is None:
        return []
    out: List[List[T]] = []
    q: Deque[TreeNode[T]] = deque([root])

    while q:
        level_size = len(q)
        level: List[T] = []
        for _ in range(level_size):
            node = q.popleft()
            level.append(node.value)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        out.append(level)

    return out


if __name__ == "__main__":
    from tree_core import build_tree_level_order

    t = build_tree_level_order([1, 2, 3, None, 4, 5])
    print("pre rec:", preorder_recursive(t))
    print("in rec:", inorder_recursive(t))
    print("post rec:", postorder_recursive(t))
    print("pre it:", preorder_iterative(t))
    print("in it:", inorder_iterative(t))
    print("post it:", postorder_iterative(t))
    print("level:", level_order(t))
    print("levels:", level_order_levels(t))
