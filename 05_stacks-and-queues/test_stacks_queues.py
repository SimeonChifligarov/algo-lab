"""
Tests for Stacks & Queues toolkit (Part 4/4)

Run:
  python test_stacks_queues.py

or:
  python -m unittest test_stacks_queues.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stack_basics import Stack, is_valid_brackets, simplify_path, eval_rpn
from monotonic_stack import (
    next_greater_elements,
    next_greater_indices,
    daily_temperatures,
    largest_rectangle_area,
    stock_span,
)
from queue_basics import (
    Queue,
    CircularQueue,
    MovingAverage,
    RecentCounter,
    bfs_shortest_path_grid,
)


class TestStackBasics(unittest.TestCase):
    def test_stack_class(self) -> None:
        s = Stack[int]()
        self.assertTrue(s.is_empty())

        s.push(10)
        s.push(20)
        self.assertEqual(len(s), 2)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)
        self.assertTrue(s.is_empty())

        with self.assertRaises(IndexError):
            s.pop()
        with self.assertRaises(IndexError):
            s.peek()

    def test_is_valid_brackets(self) -> None:
        self.assertTrue(is_valid_brackets("([]){}"))
        self.assertTrue(is_valid_brackets("abc(def)[x]{y}"))  # ignores non-brackets
        self.assertFalse(is_valid_brackets("([)]"))
        self.assertFalse(is_valid_brackets("("))
        self.assertTrue(is_valid_brackets(""))

    def test_simplify_path(self) -> None:
        self.assertEqual(simplify_path("/a/./b/../../c/"), "/c")
        self.assertEqual(simplify_path("/../"), "/")
        self.assertEqual(simplify_path("a/b/../c"), "a/c")
        self.assertEqual(simplify_path(""), ".")
        self.assertEqual(simplify_path("a//b///c"), "a/b/c")
        self.assertEqual(simplify_path("../../a"), "../../a")

    def test_eval_rpn(self) -> None:
        self.assertEqual(eval_rpn(["2", "1", "+", "3", "*"]), 9)
        self.assertEqual(eval_rpn(["4", "13", "5", "/", "+"]), 6)
        self.assertEqual(eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22)
        self.assertEqual(eval_rpn(["-7", "2", "/"]), -3)  # trunc toward zero

        with self.assertRaises(ZeroDivisionError):
            eval_rpn(["1", "0", "/"])
        with self.assertRaises(ValueError):
            eval_rpn(["2", "+"])
        with self.assertRaises(ValueError):
            eval_rpn(["2", "x", "+"])


class TestMonotonicStack(unittest.TestCase):
    def test_next_greater_elements(self) -> None:
        nums = [2, 1, 2, 4, 3]
        self.assertEqual(next_greater_elements(nums), [4, 2, 4, -1, -1])
        self.assertEqual(next_greater_indices(nums), [3, 2, 3, -1, -1])
        self.assertEqual(next_greater_elements([]), [])
        self.assertEqual(next_greater_indices([5]), [-1])

    def test_daily_temperatures(self) -> None:
        self.assertEqual(
            daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
            [1, 1, 4, 2, 1, 1, 0, 0],
        )
        self.assertEqual(daily_temperatures([]), [])
        self.assertEqual(daily_temperatures([80, 79, 78]), [0, 0, 0])

    def test_largest_rectangle_area(self) -> None:
        self.assertEqual(largest_rectangle_area([2, 1, 5, 6, 2, 3]), 10)
        self.assertEqual(largest_rectangle_area([2, 4]), 4)
        self.assertEqual(largest_rectangle_area([]), 0)
        self.assertEqual(largest_rectangle_area([1, 1, 1, 1]), 4)

    def test_stock_span(self) -> None:
        self.assertEqual(stock_span([100, 80, 60, 70, 60, 75, 85]), [1, 1, 1, 2, 1, 4, 6])
        self.assertEqual(stock_span([]), [])
        self.assertEqual(stock_span([10, 20, 30]), [1, 2, 3])


class TestQueueBasics(unittest.TestCase):
    def test_queue_class(self) -> None:
        q = Queue[int]([1, 2])
        self.assertEqual(len(q), 2)
        self.assertEqual(q.peek(), 1)

        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(list(q), [2, 3])

        q.dequeue()
        q.dequeue()
        self.assertTrue(q.is_empty())

        with self.assertRaises(IndexError):
            q.dequeue()
        with self.assertRaises(IndexError):
            q.peek()

    def test_circular_queue(self) -> None:
        cq: CircularQueue[int] = CircularQueue(3)
        self.assertTrue(cq.is_empty())
        self.assertFalse(cq.is_full())

        cq.enqueue(10)
        cq.enqueue(20)
        cq.enqueue(30)
        self.assertTrue(cq.is_full())
        self.assertEqual(list(cq), [10, 20, 30])

        with self.assertRaises(OverflowError):
            cq.enqueue(40)

        self.assertEqual(cq.dequeue(), 10)
        cq.enqueue(40)  # wrap-around
        self.assertEqual(list(cq), [20, 30, 40])
        self.assertEqual(cq.peek(), 20)

        self.assertEqual(cq.dequeue(), 20)
        self.assertEqual(cq.dequeue(), 30)
        self.assertEqual(cq.dequeue(), 40)
        self.assertTrue(cq.is_empty())

        with self.assertRaises(IndexError):
            cq.dequeue()

    def test_moving_average(self) -> None:
        ma = MovingAverage(3)
        self.assertAlmostEqual(ma.next(1), 1.0)
        self.assertAlmostEqual(ma.next(10), 5.5)
        self.assertAlmostEqual(ma.next(3), 14 / 3)
        self.assertAlmostEqual(ma.next(5), 6.0)

        with self.assertRaises(ValueError):
            MovingAverage(0)

    def test_recent_counter(self) -> None:
        rc = RecentCounter()  # window = 3000, interval [t-2999, t]
        self.assertEqual(rc.ping(1), 1)
        self.assertEqual(rc.ping(100), 2)
        self.assertEqual(rc.ping(3001), 2)  # counts times in [2, 3001] => 100, 3001
        self.assertEqual(rc.ping(3002), 3)  # counts times in [3, 3002] => 100,3001,3002

        with self.assertRaises(ValueError):
            RecentCounter(0)

    def test_bfs_shortest_path_grid(self) -> None:
        grid = [
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(bfs_shortest_path_grid(grid, (0, 0), (2, 3)), 5)
        self.assertEqual(bfs_shortest_path_grid(grid, (0, 0), (0, 0)), 0)

        blocked_goal = [
            [0, 1],
            [0, 1],
        ]
        self.assertEqual(bfs_shortest_path_grid(blocked_goal, (0, 0), (1, 1)), -1)

        unreachable = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]
        self.assertEqual(bfs_shortest_path_grid(unreachable, (0, 0), (2, 2)), -1)

        with self.assertRaises(ValueError):
            bfs_shortest_path_grid([[0, 0], [0]], (0, 0), (0, 1))  # non-rectangular
        with self.assertRaises(ValueError):
            bfs_shortest_path_grid([[0]], (1, 0), (0, 0))  # out of bounds


if __name__ == "__main__":
    unittest.main(verbosity=2)
