"""
Heaps & Priority Queues — small adapters + comparison with heapq (Part 3/4)

Why this file exists:
- In real Python code, you'll often use heapq (a min-heap on a list).
- Sometimes you want a max-heap or a "priority queue" with (priority, item).

This module provides:
- MaxHeap wrapper (via negation)
- PriorityQueue wrapper (min-priority first)
- heapq reference helpers

Next file:
4) test_heaps.py
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Generic, Iterable, List, Optional, Tuple, TypeVar

try:
    from .min_heap import MinHeap
except ImportError:
    from min_heap import MinHeap

T = TypeVar("T")


# ----------------------------
# MaxHeap wrapper (ints)
# ----------------------------

class MaxHeap:
    """
    Max-heap for ints implemented using MinHeap of negated values.
    Educational convenience wrapper.
    """

    def __init__(self, items: Optional[Iterable[int]] = None):
        self._h = MinHeap[int]()
        if items is not None:
            self._h.heapify([-x for x in items])

    def __len__(self) -> int:
        return len(self._h)

    def __bool__(self) -> bool:
        return bool(self._h)

    def peek(self) -> int:
        return -self._h.peek()

    def push(self, x: int) -> None:
        self._h.push(-x)

    def pop(self) -> int:
        return -self._h.pop()


# ----------------------------
# PriorityQueue wrapper
# ----------------------------

@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T


class PriorityQueue(Generic[T]):
    """
    Min-priority-first queue.
    Lower priority value == comes out first.

    Internally uses our MinHeap of PrioritizedItem (orderable via dataclass).
    """

    def __init__(self, items: Optional[Iterable[Tuple[int, T]]] = None):
        self._h: MinHeap[PrioritizedItem[T]] = MinHeap()
        if items is not None:
            self._h.heapify([PrioritizedItem(p, it) for p, it in items])

    def __len__(self) -> int:
        return len(self._h)

    def push(self, priority: int, item: T) -> None:
        self._h.push(PrioritizedItem(priority, item))

    def pop(self) -> Tuple[int, T]:
        x = self._h.pop()
        return x.priority, x.item

    def peek(self) -> Tuple[int, T]:
        x = self._h.peek()
        return x.priority, x.item


# ----------------------------
# heapq reference helpers (optional)
# ----------------------------

def heapq_top_k_largest(nums: Iterable[int], k: int) -> List[int]:
    """
    Reference: use Python's heapq to compute top-k largest (descending).
    """
    if k <= 0:
        return []
    h: List[int] = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        else:
            if x > h[0]:
                heapq.heapreplace(h, x)
    return sorted(h, reverse=True)


def heapq_k_way_merge(lists: List[List[int]]) -> List[int]:
    """
    Reference: merge k sorted lists with heapq.
    """
    h: List[Tuple[int, int, int]] = []
    for li, arr in enumerate(lists):
        if arr:
            h.append((arr[0], li, 0))
    heapq.heapify(h)

    out: List[int] = []
    while h:
        val, li, ei = heapq.heappop(h)
        out.append(val)
        nxt = ei + 1
        if nxt < len(lists[li]):
            heapq.heappush(h, (lists[li][nxt], li, nxt))
    return out


if __name__ == "__main__":
    mh = MaxHeap([3, 1, 9, 2])
    while mh:
        print("max pop:", mh.pop())

    pq = PriorityQueue[str]([(2, "low"), (1, "high"), (3, "later")])
    while len(pq):
        print("pq pop:", pq.pop())

    print("heapq top 3:", heapq_top_k_largest([5, 1, 9, 2, 7, 3], 3))
    print("heapq merge:", heapq_k_way_merge([[1, 4, 7], [2, 5], [3, 6, 9]]))
