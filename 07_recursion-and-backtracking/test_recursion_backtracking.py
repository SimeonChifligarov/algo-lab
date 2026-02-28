"""
Tests for Recursion & Backtracking toolkit (Part 4/4)

Run:
  python test_recursion_backtracking.py

or:
  python -m unittest test_recursion_backtracking.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from recursion_core import (
    recursive_sum,
    recursive_max,
    recursive_binary_search,
    merge_sort,
    TreeNode,
    tree_depth,
    inorder_traversal,
    preorder_traversal,
    postorder_traversal,
)
from backtracking_subsets_perms import (
    subsets,
    subsets_with_dup,
    permutations,
    permutations_unique,
    combinations_n_choose_k,
    combination_sum,
)
from backtracking_constraints import (
    solve_n_queens,
    generate_parentheses,
    word_exists,
)


class TestRecursionCore(unittest.TestCase):
    def test_recursive_sum(self) -> None:
        self.assertEqual(recursive_sum([]), 0)
        self.assertEqual(recursive_sum([1, 2, 3, 4]), 10)

    def test_recursive_max(self) -> None:
        self.assertEqual(recursive_max([1, 9, 3, 7]), 9)
        with self.assertRaises(ValueError):
            recursive_max([])

    def test_recursive_binary_search(self) -> None:
        nums = [1, 3, 5, 7, 9]
        self.assertEqual(recursive_binary_search(nums, 1), 0)
        self.assertEqual(recursive_binary_search(nums, 9), 4)
        self.assertEqual(recursive_binary_search(nums, 7), 3)
        self.assertEqual(recursive_binary_search(nums, 2), -1)
        self.assertEqual(recursive_binary_search([], 1), -1)

    def test_merge_sort(self) -> None:
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([1]), [1])
        self.assertEqual(merge_sort([5, 2, 4, 6, 1, 3]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(merge_sort([3, 3, 2, 1]), [1, 2, 3, 3])


class TestTreeRecursion(unittest.TestCase):
    def test_tree_depth_and_traversals(self) -> None:
        #      2
        #     / \
        #    1   3
        root = TreeNode(2, left=TreeNode(1), right=TreeNode(3))

        self.assertEqual(tree_depth(root), 2)
        self.assertEqual(inorder_traversal(root), [1, 2, 3])
        self.assertEqual(preorder_traversal(root), [2, 1, 3])
        self.assertEqual(postorder_traversal(root), [1, 3, 2])

        self.assertEqual(tree_depth(None), 0)
        self.assertEqual(inorder_traversal(None), [])


class TestBacktrackingGenerators(unittest.TestCase):
    def test_subsets(self) -> None:
        got = subsets([1, 2])
        self.assertEqual({tuple(x) for x in got}, {(), (1,), (2,), (1, 2)})

    def test_subsets_with_dup(self) -> None:
        got = subsets_with_dup([1, 2, 2])
        self.assertEqual({tuple(x) for x in got}, {(), (1,), (2,), (1, 2), (2, 2), (1, 2, 2)})

    def test_permutations(self) -> None:
        got = permutations([1, 2, 3])
        self.assertEqual(len(got), 6)
        self.assertEqual({tuple(x) for x in got}, {
            (1, 2, 3), (1, 3, 2),
            (2, 1, 3), (2, 3, 1),
            (3, 1, 2), (3, 2, 1),
        })

    def test_permutations_unique(self) -> None:
        got = permutations_unique([1, 1, 2])
        self.assertEqual({tuple(x) for x in got}, {(1, 1, 2), (1, 2, 1), (2, 1, 1)})

    def test_combinations_n_choose_k(self) -> None:
        got = combinations_n_choose_k(4, 2)
        self.assertEqual({tuple(x) for x in got}, {(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)})

        self.assertEqual(combinations_n_choose_k(3, 0), [[]])
        self.assertEqual(combinations_n_choose_k(3, 5), [])
        with self.assertRaises(ValueError):
            combinations_n_choose_k(-1, 2)

    def test_combination_sum(self) -> None:
        got = combination_sum([2, 3, 6, 7], 7)
        self.assertEqual({tuple(x) for x in got}, {(7,), (2, 2, 3)})

        self.assertEqual(combination_sum([2], 1), [])
        self.assertEqual(combination_sum([1], 0), [[]])


class TestConstraints(unittest.TestCase):
    def test_solve_n_queens(self) -> None:
        self.assertEqual(solve_n_queens(0), [[]])
        self.assertEqual(solve_n_queens(1), [["Q"]])
        self.assertEqual(len(solve_n_queens(4)), 2)

        with self.assertRaises(ValueError):
            solve_n_queens(-1)

    def test_generate_parentheses(self) -> None:
        self.assertEqual(generate_parentheses(0), [""])
        self.assertEqual(set(generate_parentheses(1)), {"()"})
        self.assertEqual(set(generate_parentheses(3)), {"((()))", "(()())", "(())()", "()(())", "()()()"})

        with self.assertRaises(ValueError):
            generate_parentheses(-1)

    def test_word_exists(self) -> None:
        board = [
            ["A", "B", "C", "E"],
            ["S", "F", "C", "S"],
            ["A", "D", "E", "E"],
        ]
        self.assertTrue(word_exists(board, "ABCCED"))
        self.assertTrue(word_exists(board, "SEE"))
        self.assertFalse(word_exists(board, "ABCB"))
        self.assertTrue(word_exists(board, ""))

        self.assertFalse(word_exists([], "A"))
        with self.assertRaises(ValueError):
            word_exists([["A"], ["B", "C"]], "AB")  # non-rectangular


if __name__ == "__main__":
    unittest.main(verbosity=2)
