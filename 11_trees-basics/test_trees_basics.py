"""
Tests for Trees Basics toolkit (Part 4/4)

Run:
  python test_trees_basics.py

or:
  python -m unittest test_trees_basics.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from tree_core import build_tree_level_order, tree_to_level_order, TreeNode
from tree_traversals import (
    preorder_recursive,
    inorder_recursive,
    postorder_recursive,
    preorder_iterative,
    inorder_iterative,
    postorder_iterative,
    level_order,
    level_order_levels,
)
from tree_utils import (
    size,
    height,
    invert,
    are_equal,
    is_same_values_multiset,
    max_path_sum_root_to_leaf,
    has_path_sum,
    is_valid_bst,
)


class TestTreeCore(unittest.TestCase):
    def test_build_and_to_level_order(self) -> None:
        self.assertIsNone(build_tree_level_order([]))
        self.assertIsNone(build_tree_level_order([None]))
        t = build_tree_level_order([1, 2, 3, None, 4])
        self.assertEqual(tree_to_level_order(t), [1, 2, 3, None, 4])

        # trimming trailing Nones
        t2 = build_tree_level_order([1, None, 2, None, None, None, 3])
        self.assertEqual(tree_to_level_order(t2), [1, None, 2, None, 3])


class TestTraversals(unittest.TestCase):
    def test_traversals_match(self) -> None:
        t = build_tree_level_order([1, 2, 3, None, 4, 5])
        self.assertEqual(preorder_recursive(t), preorder_iterative(t))
        self.assertEqual(inorder_recursive(t), inorder_iterative(t))
        self.assertEqual(postorder_recursive(t), postorder_iterative(t))

    def test_known_traversal_orders(self) -> None:
        #      1
        #     / \
        #    2   3
        #     \  /
        #     4 5
        t = build_tree_level_order([1, 2, 3, None, 4, 5])
        self.assertEqual(preorder_recursive(t), [1, 2, 4, 3, 5])
        self.assertEqual(inorder_recursive(t), [2, 4, 1, 5, 3])
        self.assertEqual(postorder_recursive(t), [4, 2, 5, 3, 1])
        self.assertEqual(level_order(t), [1, 2, 3, 4, 5])
        self.assertEqual(level_order_levels(t), [[1], [2, 3], [4, 5]])

    def test_empty(self) -> None:
        self.assertEqual(preorder_recursive(None), [])
        self.assertEqual(inorder_iterative(None), [])
        self.assertEqual(level_order_levels(None), [])


class TestTreeUtils(unittest.TestCase):
    def test_size_height(self) -> None:
        self.assertEqual(size(None), 0)
        self.assertEqual(height(None), 0)

        t = build_tree_level_order([1, 2, 3, None, 4])
        self.assertEqual(size(t), 4)
        self.assertEqual(height(t), 3)

    def test_invert_and_equality(self) -> None:
        t = build_tree_level_order([4, 2, 7, 1, 3, 6, 9])
        inv = build_tree_level_order([4, 7, 2, 9, 6, 3, 1])

        invert(t)
        self.assertTrue(are_equal(t, inv))

    def test_value_multiset(self) -> None:
        a = build_tree_level_order([1, 2, 3])
        b = build_tree_level_order([2, 1, 3])
        self.assertTrue(is_same_values_multiset(a, b))

        c = build_tree_level_order([1, 2])
        self.assertFalse(is_same_values_multiset(a, c))

    def test_path_sum(self) -> None:
        #      5
        #     / \
        #    4   8
        #   /   / \
        #  11  13  4
        # / \       \
        # 7   2       1
        t = build_tree_level_order([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
        self.assertTrue(has_path_sum(t, 22))  # 5-4-11-2
        self.assertFalse(has_path_sum(t, 26))  # no root-to-leaf sum 26 here
        self.assertEqual(max_path_sum_root_to_leaf(t), 27)  # 5-4-11-7

    def test_is_valid_bst(self) -> None:
        bst = build_tree_level_order([4, 2, 6, 1, 3, 5, 7])
        self.assertTrue(is_valid_bst(bst))

        not_bst = build_tree_level_order([5, 1, 4, None, None, 3, 6])
        self.assertFalse(is_valid_bst(not_bst))


if __name__ == "__main__":
    unittest.main(verbosity=2)
