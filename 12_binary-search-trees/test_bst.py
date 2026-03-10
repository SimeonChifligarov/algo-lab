"""
Tests for Binary Search Trees toolkit (Part 4/4)

Run:
  python test_bst.py

or:
  python -m unittest test_bst.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from bst_core import BSTNode, build_bst, insert, search, inorder_values
from bst_delete import delete
from bst_queries import is_bst, lca_bst, kth_smallest, range_query


class TestBSTCore(unittest.TestCase):
    def test_insert_and_inorder_sorted(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
        self.assertEqual(inorder_values(r), [2, 3, 4, 5, 6, 7, 7, 8])

        # insert into empty
        r2 = insert(None, 10)
        self.assertEqual(inorder_values(r2), [10])

    def test_search(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8])
        self.assertIsNotNone(search(r, 6))
        self.assertIsNone(search(r, 10))

        self.assertIsNone(search(None, 1))


class TestBSTDelete(unittest.TestCase):
    def test_delete_leaf_and_root(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8])
        r = delete(r, 2)
        self.assertEqual(inorder_values(r), [3, 4, 5, 6, 7, 8])

        r = delete(r, 5)  # delete root
        self.assertEqual(inorder_values(r), [3, 4, 6, 7, 8])

    def test_delete_one_child(self) -> None:
        # 5 -> (right 7 -> right 8)
        r = build_bst([5, 7, 8])
        r = delete(r, 7)
        self.assertEqual(inorder_values(r), [5, 8])

    def test_delete_two_children(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8])
        r = delete(r, 7)  # has two children 6 and 8
        self.assertEqual(inorder_values(r), [2, 3, 4, 5, 6, 8])

    def test_delete_duplicates(self) -> None:
        r = build_bst([5, 7, 7, 7, 6])
        self.assertEqual(inorder_values(r), [5, 6, 7, 7, 7])

        r = delete(r, 7)  # delete one 7
        self.assertEqual(inorder_values(r), [5, 6, 7, 7])

        r = delete(r, 7)
        r = delete(r, 7)
        self.assertEqual(inorder_values(r), [5, 6])

        # deleting non-existent is no-op
        r2 = delete(r, 999)
        self.assertEqual(inorder_values(r2), [5, 6])


class TestBSTQueries(unittest.TestCase):
    def test_is_bst(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
        self.assertTrue(is_bst(r))

        # Make an invalid BST by breaking an invariant
        bad = BSTNode(5)
        bad.left = BSTNode(7)  # violates: left must be < 5
        self.assertFalse(is_bst(bad))

        self.assertTrue(is_bst(None))

    def test_lca(self) -> None:
        r = build_bst([6, 2, 8, 0, 4, 7, 9, 3, 5])
        self.assertEqual(lca_bst(r, 2, 8).value, 6)  # type: ignore[union-attr]
        self.assertEqual(lca_bst(r, 2, 4).value, 2)  # type: ignore[union-attr]
        self.assertIsNone(lca_bst(None, 1, 2))

    def test_kth_smallest(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
        self.assertEqual(kth_smallest(r, 1), 2)
        self.assertEqual(kth_smallest(r, 4), 5)
        self.assertEqual(kth_smallest(r, 7), 7)
        self.assertEqual(kth_smallest(r, 8), 8)

        with self.assertRaises(ValueError):
            kth_smallest(r, 0)
        with self.assertRaises(IndexError):
            kth_smallest(r, 9)

    def test_range_query(self) -> None:
        r = build_bst([5, 3, 7, 2, 4, 6, 8, 7])
        self.assertEqual(range_query(r, 4, 7), [4, 5, 6, 7, 7])
        self.assertEqual(range_query(r, 7, 4), [4, 5, 6, 7, 7])  # swapped bounds OK
        self.assertEqual(range_query(r, 100, 200), [])
        self.assertEqual(range_query(None, 1, 2), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
