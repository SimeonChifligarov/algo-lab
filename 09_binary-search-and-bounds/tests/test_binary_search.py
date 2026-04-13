"""
Tests for Binary Search & Bounds toolkit (Part 4/4)

Run:
  python test_binary_search.py

or:
  python -m unittest test_binary_search.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from ..binary_search_core import (
    binary_search,
    binary_search_recursive,
    first_occurrence,
    last_occurrence,
    count_occurrences,
)
from ..bounds import (
    lower_bound,
    upper_bound,
    equal_range,
    count_with_bounds,
    insert_position,
)
from ..parametric_search import (
    first_true,
    last_true,
    sqrt_floor,
    min_capacity_to_ship,
    min_eating_speed,
)


class TestBinarySearchCore(unittest.TestCase):
    def test_binary_search(self) -> None:
        a = [1, 2, 3, 4, 5]
        self.assertEqual(binary_search(a, 1), 0)
        self.assertEqual(binary_search(a, 5), 4)
        self.assertEqual(binary_search(a, 3), 2)
        self.assertEqual(binary_search(a, 9), -1)
        self.assertEqual(binary_search([], 1), -1)

    def test_binary_search_recursive(self) -> None:
        a = [1, 3, 5, 7, 9]
        self.assertEqual(binary_search_recursive(a, 7), 3)
        self.assertEqual(binary_search_recursive(a, 2), -1)
        self.assertEqual(binary_search_recursive([], 7), -1)

    def test_first_last_occurrence(self) -> None:
        a = [1, 2, 2, 2, 3, 5, 7]
        self.assertEqual(first_occurrence(a, 2), 1)
        self.assertEqual(last_occurrence(a, 2), 3)
        self.assertEqual(count_occurrences(a, 2), 3)

        self.assertEqual(first_occurrence(a, 4), -1)
        self.assertEqual(last_occurrence(a, 4), -1)
        self.assertEqual(count_occurrences(a, 4), 0)

        b = [2, 2, 2]
        self.assertEqual(first_occurrence(b, 2), 0)
        self.assertEqual(last_occurrence(b, 2), 2)

        self.assertEqual(first_occurrence([], 1), -1)


class TestBounds(unittest.TestCase):
    def test_bounds_basic(self) -> None:
        a = [1, 2, 2, 2, 3, 5, 7]
        self.assertEqual(lower_bound(a, 2), 1)
        self.assertEqual(upper_bound(a, 2), 4)
        self.assertEqual(equal_range(a, 2), (1, 4))
        self.assertEqual(count_with_bounds(a, 2), 3)

        self.assertEqual(lower_bound(a, 0), 0)
        self.assertEqual(upper_bound(a, 0), 0)

        self.assertEqual(lower_bound(a, 10), len(a))
        self.assertEqual(upper_bound(a, 10), len(a))

    def test_insert_position(self) -> None:
        a = [1, 2, 4, 4, 9]
        self.assertEqual(insert_position(a, 0), 0)
        self.assertEqual(insert_position(a, 4), 2)  # first position for 4
        self.assertEqual(insert_position(a, 10), 5)


class TestParametricSearch(unittest.TestCase):
    def test_first_true_last_true(self) -> None:
        # first x >= 7 in [0..10]
        self.assertEqual(first_true(0, 10, lambda x: x >= 7), 7)
        # last x <= 7 in [0..10]
        self.assertEqual(last_true(0, 10, lambda x: x <= 7), 7)

        with self.assertRaises(ValueError):
            first_true(0, 5, lambda x: False)
        with self.assertRaises(ValueError):
            last_true(0, 5, lambda x: False)

        with self.assertRaises(ValueError):
            first_true(5, 0, lambda x: True)

    def test_sqrt_floor(self) -> None:
        self.assertEqual(sqrt_floor(0), 0)
        self.assertEqual(sqrt_floor(1), 1)
        self.assertEqual(sqrt_floor(2), 1)
        self.assertEqual(sqrt_floor(3), 1)
        self.assertEqual(sqrt_floor(4), 2)
        self.assertEqual(sqrt_floor(15), 3)
        self.assertEqual(sqrt_floor(16), 4)
        self.assertEqual(sqrt_floor(17), 4)

        with self.assertRaises(ValueError):
            sqrt_floor(-1)

    def test_min_capacity_to_ship(self) -> None:
        self.assertEqual(min_capacity_to_ship([1, 2, 3, 1, 1], 4), 3)
        self.assertEqual(min_capacity_to_ship([3, 2, 2, 4, 1, 4], 3), 6)
        self.assertEqual(min_capacity_to_ship([], 3), 0)

        with self.assertRaises(ValueError):
            min_capacity_to_ship([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            min_capacity_to_ship([1, 0, 3], 2)

    def test_min_eating_speed(self) -> None:
        self.assertEqual(min_eating_speed([3, 6, 7, 11], 8), 4)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 5), 30)
        self.assertEqual(min_eating_speed([30, 11, 23, 4, 20], 6), 23)
        self.assertEqual(min_eating_speed([], 10), 0)

        with self.assertRaises(ValueError):
            min_eating_speed([1, 2], 0)
        with self.assertRaises(ValueError):
            min_eating_speed([1, -2], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
