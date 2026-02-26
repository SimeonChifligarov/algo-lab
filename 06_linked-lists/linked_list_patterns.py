"""
Linked Lists — fast/slow pointer patterns (Part 3/4)

This file focuses on classic "tortoise and hare" linked-list problems:
- middle_node                 (find middle; choose second middle on even length)
- has_cycle                   (Floyd cycle detection)
- cycle_entry                 (find cycle start if one exists)
- kth_from_end                (one-pass two-pointer pattern)
- is_palindrome_list          (reverse second half, compare, restore)

Notes:
- Functions are written for singly linked lists.
- `is_palindrome_list` restores the list before returning (nice for tests/debugging).

Next file:
4) test_linked_lists.py
"""

from __future__ import annotations

from typing import Optional, TypeVar

from linked_list_core import ListNode, linked_list_repr

T = TypeVar("T")


# ----------------------------
# Basic fast/slow patterns
# ----------------------------

def middle_node(head: Optional[ListNode[T]]) -> Optional[ListNode[T]]:
    """
    Return the middle node of the list.
    If there are two middles (even length), returns the SECOND middle.

    Examples:
      [1,2,3] -> node(2)
      [1,2,3,4] -> node(3)
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    return slow


def kth_from_end(head: Optional[ListNode[T]], k: int) -> ListNode[T]:
    """
    Return the k-th node from the end (1-based), using one pass.

    Example:
      [10,20,30,40,50], k=2 -> node(40)

    Raises:
      ValueError if k <= 0
      IndexError if k > length
    """
    if k <= 0:
        raise ValueError("k must be >= 1")

    fast = head
    for _ in range(k):
        if fast is None:
            raise IndexError("k is larger than the linked list length")
        fast = fast.next

    slow = head
    while fast is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next

    if slow is None:
        raise IndexError("k is larger than the linked list length")
    return slow


# ----------------------------
# Cycle detection (Floyd)
# ----------------------------

def has_cycle(head: Optional[ListNode[T]]) -> bool:
    """
    Return True if the list contains a cycle, else False.
    """
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def cycle_entry(head: Optional[ListNode[T]]) -> Optional[ListNode[T]]:
    """
    If the list has a cycle, return the entry node of the cycle.
    Otherwise return None.

    Floyd's algorithm:
      1) Detect meeting point (slow/fast)
      2) Start one pointer at head and one at meeting point
      3) Advance both 1 step; they meet at cycle entry
    """
    slow = head
    fast = head

    # Phase 1: find meeting point
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle

    # Phase 2: find entry
    p1 = head
    p2 = slow
    while p1 is not p2:
        p1 = p1.next  # type: ignore[assignment]
        p2 = p2.next  # type: ignore[assignment]
    return p1


# ----------------------------
# Palindrome linked list
# ----------------------------

def is_palindrome_list(head: Optional[ListNode[T]]) -> bool:
    """
    Return True if the linked list values form a palindrome.

    Approach:
    - Find middle with fast/slow
    - Reverse second half
    - Compare first half and reversed second half
    - Restore second half before returning

    Works for odd/even lengths.
    Time: O(n)
    Space: O(1) extra
    """
    if head is None or head.next is None:
        return True

    # 1) Find end of first half
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next

    # Now slow is end of first half (for odd length, exact middle-left)
    second_start = _reverse(slow.next)

    # 2) Compare halves
    p1 = head
    p2 = second_start
    ok = True
    while p2 is not None:
        if p1.value != p2.value:
            ok = False
            break
        p1 = p1.next  # type: ignore[assignment]
        p2 = p2.next

    # 3) Restore
    slow.next = _reverse(second_start)
    return ok


def _reverse(head: Optional[ListNode[T]]) -> Optional[ListNode[T]]:
    prev: Optional[ListNode[T]] = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


if __name__ == "__main__":
    from linked_list_core import build_linked_list, node_at

    h = build_linked_list([1, 2, 3, 4, 5])
    print("middle:", middle_node(h))
    print("kth from end (2):", kth_from_end(h, 2))

    p = build_linked_list([1, 2, 3, 2, 1])
    print("palindrome:", is_palindrome_list(p), linked_list_repr(p))  # list restored

    c = build_linked_list([10, 20, 30, 40, 50])
    # make cycle: tail -> node(30)
    tail = node_at(c, 4)
    entry = node_at(c, 2)
    tail.next = entry
    print("has cycle:", has_cycle(c))
    print("cycle entry:", cycle_entry(c))
