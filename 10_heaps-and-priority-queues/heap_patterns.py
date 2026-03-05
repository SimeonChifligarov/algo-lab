"""
Heaps & Priority Queues — common heap patterns (Part 2/4)

This file builds classic algorithms on top of MinHeap (our implementation):
- top_k_largest            (keep a min-heap of size k)
- k_way_merge_sorted       (merge k sorted lists using a heap)
- RunningMedian            (two-heaps technique: max-heap + min-heap)

Notes:
- For the max-heap, we store negated values in a MinHeap.
- These implementations are educational and keep APIs clean/testable.

Next files:
3) pq_wrappers.py
4) test_heaps.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

from min_heap import MinHeap


# ----------------------------
# Pattern 1: Top-K largest
# ----------------------------

def top_k_largest(nums: Iterable[int], k: int) -> List[int]:
    """
    Return the k largest elements from nums (in descending order).
    Uses a min-heap of size k.

    Time: O(n log k)
    Space: O(k)
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return []

    heap = MinHeap[int]()
    for x in nums:
        if len(heap) < k:
            heap.push(x)
        else:
            # If x is larger than the smallest in the heap, it belongs in top-k.
            if x > heap.peek():
                heap.replace(x)

    # heap contains k largest, but unsorted. Pop gives ascending, so reverse.
    out: List[int] = []
    while heap:
        out.append(heap.pop())
    out.reverse()
    return out


# ----------------------------
# Pattern 2: K-way merge of sorted lists
# ----------------------------

def k_way_merge_sorted(lists: Sequence[Sequence[int]]) -> List[int]:
    """
    Merge k sorted lists into one sorted list.

    Time: O(N log k) where N is total number of elements.
    Space: O(k) for the heap + output.

    Implementation:
      Push (value, list_index, element_index) into the heap.
    """
    heap: MinHeap[Tuple[int, int, int]] = MinHeap()

    for li, arr in enumerate(lists):
        if arr:
            heap.push((arr[0], li, 0))

    out: List[int] = []
    while heap:
        val, li, ei = heap.pop()
        out.append(val)
        nxt = ei + 1
        if nxt < len(lists[li]):
            heap.push((lists[li][nxt], li, nxt))

    return out


# ----------------------------
# Pattern 3: Running median (two heaps)
# ----------------------------

class RunningMedian:
    """
    Maintain the median of a stream of numbers.

    Invariants:
    - low (max-heap) contains the smaller half
    - high (min-heap) contains the larger half
    - len(low) == len(high) or len(low) == len(high) + 1
      (we keep low having the extra when odd count)

    Median:
    - if odd: max(low)
    - if even: average of max(low) and min(high)

    Max-heap is simulated by storing negatives in a MinHeap.
    """

    def __init__(self):
        self._low = MinHeap[int]()  # max-heap via negatives
        self._high = MinHeap[int]()  # min-heap
        self._count = 0

    def add(self, x: int) -> None:
        if self._count == 0:
            self._low.push(-x)
            self._count = 1
            return

        # Decide which heap gets x
        if -self._low.peek() >= x:
            self._low.push(-x)
        else:
            self._high.push(x)

        self._count += 1
        self._rebalance()

    def median(self) -> float:
        if self._count == 0:
            raise IndexError("median of empty stream")

        if len(self._low) > len(self._high):
            return float(-self._low.peek())

        # even count
        return (-self._low.peek() + self._high.peek()) / 2.0

    def __len__(self) -> int:
        return self._count

    def _rebalance(self) -> None:
        # Ensure size invariant
        if len(self._low) < len(self._high):
            self._low.push(-self._high.pop())
        elif len(self._low) > len(self._high) + 1:
            self._high.push(-self._low.pop())


if __name__ == "__main__":
    print("top 3:", top_k_largest([5, 1, 9, 2, 7, 3], 3))
    print("merge:", k_way_merge_sorted([[1, 4, 7], [2, 5], [3, 6, 9]]))

    rm = RunningMedian()
    for x in [5, 15, 1, 3]:
        rm.add(x)
        print("added", x, "median:", rm.median())
