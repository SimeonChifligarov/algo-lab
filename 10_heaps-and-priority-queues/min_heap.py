"""
Heaps & Priority Queues — minimal binary min-heap (Part 1/4)

This file implements a small binary MIN-heap from scratch to build intuition.
It supports:
- push(x)
- pop() -> smallest
- peek() -> smallest (without removing)
- heapify(iterable)
- replace(x) (pop+push in one)
- pushpop(x) (push then pop, optimized)

Next files:
2) heap_patterns.py       (top-k, k-way merge, running median)
3) pq_wrappers.py         (tiny adapters + comparisons vs heapq)
4) test_heaps.py          (unittest suite)

Notes:
- This is educational. Python's heapq is faster and battle-tested.
- Indexing: parent=(i-1)//2, children=2i+1,2i+2
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None):
        self._a: List[T] = []
        if items is not None:
            self._a = list(items)
            self._heapify()

    def __len__(self) -> int:
        return len(self._a)

    def __bool__(self) -> bool:
        return bool(self._a)

    def __iter__(self) -> Iterator[T]:
        return iter(self._a)

    def __repr__(self) -> str:
        return f"MinHeap({self._a!r})"

    # ----------------------------
    # Core operations
    # ----------------------------

    def peek(self) -> T:
        if not self._a:
            raise IndexError("peek from empty heap")
        return self._a[0]

    def push(self, x: T) -> None:
        self._a.append(x)
        self._sift_up(len(self._a) - 1)

    def pop(self) -> T:
        if not self._a:
            raise IndexError("pop from empty heap")
        a = self._a
        root = a[0]
        last = a.pop()
        if a:
            a[0] = last
            self._sift_down(0)
        return root

    def heapify(self, items: Iterable[T]) -> None:
        self._a = list(items)
        self._heapify()

    # ----------------------------
    # Convenience ops (like heapq)
    # ----------------------------

    def replace(self, x: T) -> T:
        """
        Pop and return smallest, then push x.
        More efficient than pop()+push().
        """
        if not self._a:
            raise IndexError("replace on empty heap")
        root = self._a[0]
        self._a[0] = x
        self._sift_down(0)
        return root

    def pushpop(self, x: T) -> T:
        """
        Push x, then pop and return smallest.
        Optimized: if x is smaller than current min, x is popped immediately.
        """
        if not self._a:
            return x
        if x <= self._a[0]:  # type: ignore[operator]
            return x
        # x is bigger than min; replace min with x, then return old min
        root = self._a[0]
        self._a[0] = x
        self._sift_down(0)
        return root

    # ----------------------------
    # Internals
    # ----------------------------

    def _heapify(self) -> None:
        # Bottom-up heapify in O(n)
        n = len(self._a)
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        a = self._a
        while i > 0:
            p = (i - 1) // 2
            if a[p] <= a[i]:  # type: ignore[operator]
                break
            a[p], a[i] = a[i], a[p]
            i = p

    def _sift_down(self, i: int) -> None:
        a = self._a
        n = len(a)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i

            if l < n and a[l] < a[smallest]:  # type: ignore[operator]
                smallest = l
            if r < n and a[r] < a[smallest]:  # type: ignore[operator]
                smallest = r

            if smallest == i:
                break
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest


if __name__ == "__main__":
    h = MinHeap([5, 3, 8, 1, 2])
    print("heap:", h)
    while h:
        print("pop:", h.pop())
