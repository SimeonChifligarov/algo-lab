"""
Tests for Heaps & Priority Queues toolkit (Part 4/4)

Run:
  python test_heaps.py

or:
  python -m unittest test_heaps.py

Covers:
- MinHeap core ops (push/pop/peek/heapify/replace/pushpop)
- Heap patterns (top-k, k-way merge, running median)
- PriorityQueue + MaxHeap wrappers
- Cross-checks against Python's sorted / expected behavior
"""

from __future__ import annotations

import sys
from pathlib import Path
import random
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from min_heap import MinHeap
from heap_patterns import top_k_largest, k_way_merge_sorted, RunningMedian
from pq_wrappers import MaxHeap, PriorityQueue, heapq_top_k_largest, heapq_k_way_merge


class TestMinHeap(unittest.TestCase):
    def test_push_pop_peek(self) -> None:
        h = MinHeap[int]()
        with self.assertRaises(IndexError):
            h.peek()
        with self.assertRaises(IndexError):
            h.pop()

        for x in [5, 3, 8, 1, 2]:
            h.push(x)

        self.assertEqual(h.peek(), 1)

        popped = [h.pop() for _ in range(5)]
        self.assertEqual(popped, [1, 2, 3, 5, 8])

        self.assertEqual(len(h), 0)

    def test_heapify(self) -> None:
        h = MinHeap([5, 3, 8, 1, 2])
        popped = []
        while h:
            popped.append(h.pop())
        self.assertEqual(popped, [1, 2, 3, 5, 8])

        h.heapify([])
        self.assertEqual(len(h), 0)

    def test_replace(self) -> None:
        h = MinHeap([2, 5, 7])
        old = h.replace(6)
        self.assertEqual(old, 2)
        self.assertEqual([h.pop(), h.pop(), h.pop()], [5, 6, 7])

        with self.assertRaises(IndexError):
            MinHeap().replace(1)

    def test_pushpop(self) -> None:
        h = MinHeap([2, 5, 7])
        # x smaller than min -> x returned, heap unchanged
        self.assertEqual(h.pushpop(1), 1)
        self.assertEqual([h.pop(), h.pop(), h.pop()], [2, 5, 7])

        h = MinHeap([2, 5, 7])
        # x larger than min -> old min returned, x inserted
        self.assertEqual(h.pushpop(6), 2)
        self.assertEqual([h.pop(), h.pop(), h.pop()], [5, 6, 7])

        # empty heap -> returns x
        h2 = MinHeap[int]()
        self.assertEqual(h2.pushpop(10), 10)
        self.assertEqual(len(h2), 0)


class TestHeapPatterns(unittest.TestCase):
    def test_top_k_largest(self) -> None:
        data = [5, 1, 9, 2, 7, 3]
        self.assertEqual(top_k_largest(data, 0), [])
        self.assertEqual(top_k_largest(data, 1), [9])
        self.assertEqual(top_k_largest(data, 3), [9, 7, 5])
        self.assertEqual(top_k_largest(data, 10), sorted(data, reverse=True))

        with self.assertRaises(ValueError):
            top_k_largest(data, -1)

    def test_k_way_merge_sorted(self) -> None:
        lists = [[1, 4, 7], [2, 5], [3, 6, 9]]
        self.assertEqual(k_way_merge_sorted(lists), [1, 2, 3, 4, 5, 6, 7, 9])
        self.assertEqual(k_way_merge_sorted([]), [])
        self.assertEqual(k_way_merge_sorted([[]]), [])

    def test_running_median(self) -> None:
        rm = RunningMedian()
        with self.assertRaises(IndexError):
            rm.median()

        seq = [5, 15, 1, 3]
        expected = [5.0, 10.0, 5.0, 4.0]
        got = []
        for x in seq:
            rm.add(x)
            got.append(rm.median())
        self.assertEqual(got, expected)
        self.assertEqual(len(rm), 4)

        # Random cross-check vs sorting
        rng = random.Random(0)
        rm2 = RunningMedian()
        seen = []
        for _ in range(25):
            x = rng.randrange(-50, 50)
            rm2.add(x)
            seen.append(x)
            s = sorted(seen)
            m = len(s)
            if m % 2 == 1:
                expected_median = float(s[m // 2])
            else:
                expected_median = (s[m // 2 - 1] + s[m // 2]) / 2.0
            self.assertEqual(rm2.median(), expected_median)


class TestPQWrappers(unittest.TestCase):
    def test_max_heap(self) -> None:
        mh = MaxHeap([3, 1, 9, 2])
        out = []
        while mh:
            out.append(mh.pop())
        self.assertEqual(out, [9, 3, 2, 1])

    def test_priority_queue(self) -> None:
        pq = PriorityQueue[str]([(2, "low"), (1, "high"), (3, "later")])
        self.assertEqual(pq.peek(), (1, "high"))
        self.assertEqual(pq.pop(), (1, "high"))
        self.assertEqual(pq.pop(), (2, "low"))
        self.assertEqual(pq.pop(), (3, "later"))

    def test_heapq_reference_helpers(self) -> None:
        data = [5, 1, 9, 2, 7, 3]
        self.assertEqual(heapq_top_k_largest(data, 3), [9, 7, 5])

        lists = [[1, 4, 7], [2, 5], [3, 6, 9]]
        self.assertEqual(heapq_k_way_merge(lists), [1, 2, 3, 4, 5, 6, 7, 9])


if __name__ == "__main__":
    unittest.main(verbosity=2)
