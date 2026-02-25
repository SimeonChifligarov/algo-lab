"""
Linked Lists — pointer rewiring operations (Part 2/4)

This file focuses on classic pointer-manipulation tasks:
- reverse_list                 (iterative in-place reversal)
- merge_sorted_lists          (merge two sorted lists, reusing nodes)
- remove_first_value          (remove first matching node)
- remove_all_values           (remove all matching nodes)
- remove_nth_from_end         (remove nth node from end; two-pass version)

Notes:
- These functions *rewire existing nodes* (they do not clone the list).
- They return the (possibly new) head.
- Edge cases are handled carefully (empty list, removing head, etc.).

Next file:
3) linked_list_patterns.py  (middle node, cycle detection, fast/slow pointers)
"""

from __future__ import annotations

from typing import Optional, TypeVar

from linked_list_core import ListNode, linked_list_repr

T = TypeVar("T")


# ----------------------------
# Reverse
# ----------------------------

def reverse_list(head: Optional[ListNode[T]]) -> Optional[ListNode[T]]:
    """
    Reverse a singly linked list in place and return the new head.

    Example:
      1 -> 2 -> 3 -> None
      becomes
      3 -> 2 -> 1 -> None

    Time: O(n)
    Space: O(1)
    """
    prev: Optional[ListNode[T]] = None
    cur = head

    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    return prev


# ----------------------------
# Merge (sorted)
# ----------------------------

def merge_sorted_lists(
        a: Optional[ListNode[T]],
        b: Optional[ListNode[T]],
) -> Optional[ListNode[T]]:
    """
    Merge two already-sorted linked lists into one sorted list.
    Reuses the existing nodes (no new nodes allocated except local pointers).

    Assumes node values support <= comparison.

    Example:
      a: 1 -> 3 -> 5
      b: 2 -> 4 -> 6
      -> 1 -> 2 -> 3 -> 4 -> 5 -> 6

    Time: O(n + m)
    Space: O(1) extra
    """
    if a is None:
        return b
    if b is None:
        return a

    # Pick initial head
    if a.value <= b.value:  # type: ignore[operator]
        head = a
        a = a.next
    else:
        head = b
        b = b.next

    tail = head

    while a is not None and b is not None:
        if a.value <= b.value:  # type: ignore[operator]
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a is not None else b
    return head


# ----------------------------
# Remove by value
# ----------------------------

def remove_first_value(head: Optional[ListNode[T]], target: T) -> tuple[Optional[ListNode[T]], bool]:
    """
    Remove the first node whose value == target.
    Returns (new_head, removed_flag).

    Example:
      1 -> 2 -> 3, target=2  -> (1 -> 3, True)
      1 -> 2 -> 3, target=9  -> (unchanged, False)
    """
    if head is None:
        return None, False

    if head.value == target:
        return head.next, True

    prev = head
    cur = head.next
    while cur is not None:
        if cur.value == target:
            prev.next = cur.next
            return head, True
        prev = cur
        cur = cur.next

    return head, False


def remove_all_values(head: Optional[ListNode[T]], target: T) -> Optional[ListNode[T]]:
    """
    Remove all nodes whose value == target.
    Returns the new head.

    Example:
      1 -> 2 -> 2 -> 3, target=2  -> 1 -> 3

    Time: O(n)
    Space: O(1)
    """
    # Drop matching nodes from the front first
    while head is not None and head.value == target:
        head = head.next

    cur = head
    while cur is not None and cur.next is not None:
        if cur.next.value == target:
            cur.next = cur.next.next
        else:
            cur = cur.next

    return head


# ----------------------------
# Remove nth node from end
# ----------------------------

def remove_nth_from_end(head: Optional[ListNode[T]], n: int) -> Optional[ListNode[T]]:
    """
    Remove the nth node from the end (1-based) and return the new head.

    This version is intentionally two-pass (length first), so file 3 can focus on
    fast/slow pointer patterns separately.

    Examples:
      [1,2,3,4,5], n=2 -> [1,2,3,5]
      [1], n=1 -> []

    Raises:
      ValueError if n <= 0
      IndexError if n > length of list
    """
    if n <= 0:
        raise ValueError("n must be >= 1")

    # First pass: length
    length = 0
    cur = head
    while cur is not None:
        length += 1
        cur = cur.next

    if n > length:
        raise IndexError("n is larger than the linked list length")

    # Remove (length - n)-th node from start (0-based)
    remove_index = length - n

    if remove_index == 0:
        # remove head
        return head.next if head is not None else None

    prev = head
    for _ in range(remove_index - 1):
        # prev exists because bounds are valid
        prev = prev.next  # type: ignore[assignment]

    # prev is node before the one to delete
    if prev is not None and prev.next is not None:
        prev.next = prev.next.next

    return head


if __name__ == "__main__":
    from linked_list_core import build_linked_list

    h = build_linked_list([1, 2, 3, 4])
    print("original: ", linked_list_repr(h))
    h = reverse_list(h)
    print("reversed: ", linked_list_repr(h))

    a = build_linked_list([1, 3, 5])
    b = build_linked_list([2, 4, 6])
    m = merge_sorted_lists(a, b)
    print("merged:   ", linked_list_repr(m))

    x = build_linked_list([1, 2, 2, 3, 2])
    x = remove_all_values(x, 2)
    print("rm all 2: ", linked_list_repr(x))

    y = build_linked_list([10, 20, 30, 40, 50])
    y = remove_nth_from_end(y, 2)
    print("rm 2nd end:", linked_list_repr(y))
