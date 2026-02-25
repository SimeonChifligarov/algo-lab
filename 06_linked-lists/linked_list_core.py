"""
Linked Lists — core types and helpers (Part 1/4)

This first file builds the foundation:
- ListNode (singly linked list node)
- build_linked_list(...) from Python iterables
- linked_list_to_list(...) back to Python list
- small helper utilities for debugging and tests

Next files:
2) linked_list_ops.py       (reverse, merge, remove, pointer rewiring)
3) linked_list_patterns.py  (middle node, cycle detection, fast/slow pointers)
4) test_linked_lists.py     (unittest suite)

Design goals:
- clean, minimal APIs
- easy to test
- safe conversion helpers (including cycle-safe preview)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Optional, TypeVar, Generic, List

T = TypeVar("T")


@dataclass
class ListNode(Generic[T]):
    """
    Singly linked list node.

    Attributes:
      value: stored data
      next: next node (or None)
    """
    value: T
    next: Optional["ListNode[T]"] = None

    def __iter__(self) -> Iterator[T]:
        """
        Iterate values starting from this node until None.
        (Do not use on cyclic lists.)
        """
        cur: Optional[ListNode[T]] = self
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __repr__(self) -> str:
        # Safe-ish short preview to avoid infinite loops on cycles.
        return f"ListNode({linked_list_repr(self)})"


# ----------------------------
# Building / converting
# ----------------------------

def build_linked_list(values: Iterable[T]) -> Optional[ListNode[T]]:
    """
    Build a singly linked list from an iterable and return the head.

    Example:
      build_linked_list([1,2,3]) -> 1 -> 2 -> 3 -> None
      build_linked_list([]) -> None
    """
    head: Optional[ListNode[T]] = None
    tail: Optional[ListNode[T]] = None

    for v in values:
        node = ListNode(v)
        if head is None:
            head = node
            tail = node
        else:
            # tail is guaranteed not None if head is not None
            tail.next = node  # type: ignore[union-attr]
            tail = node
    return head


def linked_list_to_list(head: Optional[ListNode[T]], *, max_nodes: Optional[int] = None) -> List[T]:
    """
    Convert a linked list to a Python list.

    Parameters:
      head: head node (or None)
      max_nodes: optional safety cap (useful for cyclic lists)

    If max_nodes is None, traverses until None (do not use on cyclic lists).
    If max_nodes is set, stops after that many nodes.
    """
    out: List[T] = []
    cur = head
    seen = 0

    while cur is not None:
        out.append(cur.value)
        cur = cur.next
        seen += 1
        if max_nodes is not None and seen >= max_nodes:
            break
    return out


# ----------------------------
# Helper utilities
# ----------------------------

def iter_nodes(head: Optional[ListNode[T]]) -> Iterator[ListNode[T]]:
    """
    Iterate nodes (not values) from head to tail.
    (Do not use on cyclic lists.)
    """
    cur = head
    while cur is not None:
        yield cur
        cur = cur.next


def length(head: Optional[ListNode[T]]) -> int:
    """Return the number of nodes in a non-cyclic list."""
    n = 0
    cur = head
    while cur is not None:
        n += 1
        cur = cur.next
    return n


def tail_node(head: Optional[ListNode[T]]) -> Optional[ListNode[T]]:
    """Return the tail node, or None for an empty list."""
    if head is None:
        return None
    cur = head
    while cur.next is not None:
        cur = cur.next
    return cur


def node_at(head: Optional[ListNode[T]], index: int) -> ListNode[T]:
    """
    Return node at 0-based index.
    Raises IndexError if index is out of bounds or negative.
    """
    if index < 0:
        raise IndexError("index must be >= 0")

    cur = head
    i = 0
    while cur is not None:
        if i == index:
            return cur
        cur = cur.next
        i += 1
    raise IndexError("linked list index out of range")


def linked_list_repr(head: Optional[ListNode[T]], *, max_nodes: int = 20) -> str:
    """
    Return a readable preview string, cycle-safe by truncation.

    Example:
      "1 -> 2 -> 3 -> None"
      "1 -> 2 -> 3 -> ... (truncated)"
    """
    if head is None:
        return "None"

    parts: List[str] = []
    cur = head
    count = 0

    while cur is not None and count < max_nodes:
        parts.append(repr(cur.value))
        cur = cur.next
        count += 1

    if cur is None:
        return " -> ".join(parts) + " -> None"
    return " -> ".join(parts) + " -> ... (truncated)"


if __name__ == "__main__":
    head = build_linked_list([1, 2, 3, 4])
    print("head:", head)
    print("as list:", linked_list_to_list(head))
    print("length:", length(head))
    print("tail:", tail_node(head))
    print("node_at(2):", node_at(head, 2))

    empty = build_linked_list([])
    print("empty:", empty)
