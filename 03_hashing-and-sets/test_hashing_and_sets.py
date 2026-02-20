"""
Tests for hashing-and-sets toolkit (Part 4/4)

Run:
  python test_hashing_and_sets.py

or:
  python -m unittest test_hashing_and_sets.py

This uses only the standard library (unittest).
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Ensure this directory (03_hashing-and-sets) is importable
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from hash_utils import (
    freq_map,
    most_common,
    first_unique,
    set_union,
    set_intersection,
    set_difference,
    is_subset,
    dedupe_preserve_order,
    contains_any,
    contains_all,
)

from open_addressing_set import OpenAddressingHashSet
from hash_patterns import (
    two_sum_indices,
    group_anagrams,
    longest_consecutive,
    intersection_unique,
    has_duplicate,
)


class TestHashUtils(unittest.TestCase):
    def test_freq_map(self) -> None:
        self.assertEqual(freq_map("banana"), {"b": 1, "a": 3, "n": 2})
        self.assertEqual(freq_map([]), {})

    def test_most_common(self) -> None:
        item, count = most_common("banana")
        self.assertEqual(count, 3)
        self.assertIn(item, {"a"})  # deterministic here

        with self.assertRaises(ValueError):
            most_common([])

    def test_first_unique(self) -> None:
        self.assertEqual(first_unique(list("leetcode")), 0)
        self.assertEqual(first_unique(list("aabb")), -1)

    def test_set_ops(self) -> None:
        a = [1, 2, 3]
        b = [3, 4]
        self.assertEqual(set_union(a, b), {1, 2, 3, 4})
        self.assertEqual(set_intersection(a, b), {3})
        self.assertEqual(set_difference(a, b), {1, 2})
        self.assertTrue(is_subset([1, 2], a))
        self.assertFalse(is_subset([1, 4], a))

    def test_membership_tricks(self) -> None:
        self.assertEqual(dedupe_preserve_order([3, 1, 3, 2, 1]), [3, 1, 2])
        self.assertTrue(contains_any([1, 2, 3], [0, 2]))
        self.assertFalse(contains_any([1, 2, 3], [0, 4]))
        self.assertTrue(contains_all([1, 2, 3], [2, 3]))
        self.assertFalse(contains_all([1, 2, 3], [2, 4]))


class TestOpenAddressingHashSet(unittest.TestCase):
    def test_add_contains_len(self) -> None:
        s = OpenAddressingHashSet[int]()
        self.assertEqual(len(s), 0)
        self.assertTrue(s.add(10))
        self.assertTrue(10 in s)
        self.assertEqual(len(s), 1)
        self.assertFalse(s.add(10))  # already present
        self.assertEqual(len(s), 1)

    def test_remove(self) -> None:
        s = OpenAddressingHashSet[int]()
        for x in [1, 2, 3]:
            s.add(x)
        self.assertTrue(s.remove(2))
        self.assertFalse(2 in s)
        self.assertEqual(len(s), 2)
        self.assertFalse(s.remove(2))  # not present

    def test_resize_and_iteration(self) -> None:
        s = OpenAddressingHashSet[int](initial_capacity=4)
        items = list(range(100))
        for x in items:
            s.add(x)
        self.assertEqual(len(s), 100)
        self.assertEqual(set(iter(s)), set(items))

    def test_tombstones_behavior(self) -> None:
        s = OpenAddressingHashSet[int]()
        for x in range(50):
            s.add(x)
        for x in range(0, 50, 2):
            s.remove(x)
        # Remaining odds
        self.assertEqual(set(s), set(range(1, 50, 2)))


class TestHashPatterns(unittest.TestCase):
    def test_two_sum_indices(self) -> None:
        i, j = two_sum_indices([2, 7, 11, 15], 9)
        self.assertEqual({i, j}, {0, 1})

        with self.assertRaises(ValueError):
            two_sum_indices([1, 2, 3], 100)

    def test_group_anagrams(self) -> None:
        groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Compare as sets of frozensets to ignore ordering
        got = {frozenset(g) for g in groups}
        expect = {frozenset(["eat", "tea", "ate"]), frozenset(["tan", "nat"]), frozenset(["bat"])}
        self.assertEqual(got, expect)

    def test_longest_consecutive(self) -> None:
        self.assertEqual(longest_consecutive([100, 4, 200, 1, 3, 2]), 4)  # 1,2,3,4
        self.assertEqual(longest_consecutive([]), 0)
        self.assertEqual(longest_consecutive([1, 2, 0, 1]), 3)  # 0,1,2

    def test_intersection_unique(self) -> None:
        inter = intersection_unique([1, 2, 2, 3], [2, 2, 4])
        self.assertEqual(set(inter), {2})

    def test_has_duplicate(self) -> None:
        self.assertTrue(has_duplicate([1, 2, 3, 2]))
        self.assertFalse(has_duplicate([1, 2, 3]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
