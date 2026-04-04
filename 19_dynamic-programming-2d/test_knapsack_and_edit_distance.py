import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from knapsack_and_edit_distance import (
    build_edit_distance_table,
    build_knapsack_table,
    edit_distance,
    knapsack_01,
)


class TestKnapsack01(unittest.TestCase):
    def test_empty_items(self):
        self.assertEqual(knapsack_01([], [], 10), 0)
        self.assertEqual(build_knapsack_table([], [], 10), [[0] * 11])

    def test_zero_capacity(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]

        self.assertEqual(knapsack_01(values, weights, 0), 0)
        self.assertEqual(
            build_knapsack_table(values, weights, 0),
            [[0], [0], [0], [0]],
        )

    def test_known_example(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50

        self.assertEqual(knapsack_01(values, weights, capacity), 220)

    def test_single_item_fits(self):
        self.assertEqual(knapsack_01([10], [5], 5), 10)

    def test_single_item_does_not_fit(self):
        self.assertEqual(knapsack_01([10], [6], 5), 0)

    def test_choose_best_combination_not_greedy_by_value(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]

        self.assertEqual(knapsack_01(values, weights, 30), 160)

    def test_zero_weight_item_is_supported(self):
        values = [5, 10]
        weights = [0, 5]

        self.assertEqual(knapsack_01(values, weights, 5), 15)

    def test_zero_value_item(self):
        values = [0, 10]
        weights = [3, 5]

        self.assertEqual(knapsack_01(values, weights, 5), 10)

    def test_invalid_length_mismatch_raises_value_error(self):
        with self.assertRaises(ValueError):
            knapsack_01([10, 20], [5], 10)

        with self.assertRaises(ValueError):
            build_knapsack_table([10], [5, 6], 10)

    def test_negative_capacity_raises_value_error(self):
        with self.assertRaises(ValueError):
            knapsack_01([10], [5], -1)

        with self.assertRaises(ValueError):
            build_knapsack_table([10], [5], -1)

    def test_negative_weight_raises_value_error(self):
        with self.assertRaises(ValueError):
            knapsack_01([10], [-5], 10)

        with self.assertRaises(ValueError):
            build_knapsack_table([10], [-5], 10)

    def test_knapsack_table_known_values(self):
        values = [15, 20, 30]
        weights = [1, 3, 4]
        capacity = 4

        expected = [
            [0, 0, 0, 0, 0],
            [0, 15, 15, 15, 15],
            [0, 15, 15, 20, 35],
            [0, 15, 15, 20, 35],
        ]

        self.assertEqual(build_knapsack_table(values, weights, capacity), expected)
        self.assertEqual(knapsack_01(values, weights, capacity), 35)


class TestEditDistance(unittest.TestCase):
    def test_both_empty(self):
        self.assertEqual(edit_distance("", ""), 0)
        self.assertEqual(build_edit_distance_table("", ""), [[0]])

    def test_one_empty(self):
        self.assertEqual(edit_distance("abc", ""), 3)
        self.assertEqual(edit_distance("", "abc"), 3)

        self.assertEqual(
            build_edit_distance_table("abc", ""),
            [[0], [1], [2], [3]],
        )
        self.assertEqual(
            build_edit_distance_table("", "abc"),
            [[0, 1, 2, 3]],
        )

    def test_identical_strings(self):
        self.assertEqual(edit_distance("dynamic", "dynamic"), 0)

    def test_known_example_kitten_sitting(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)

    def test_known_example_flaw_lawn(self):
        self.assertEqual(edit_distance("flaw", "lawn"), 2)

    def test_case_sensitive(self):
        self.assertEqual(edit_distance("A", "a"), 1)

    def test_single_character_cases(self):
        self.assertEqual(edit_distance("a", "b"), 1)
        self.assertEqual(edit_distance("a", ""), 1)
        self.assertEqual(edit_distance("", "b"), 1)

    def test_build_edit_distance_table_dimensions(self):
        word1 = "abc"
        word2 = "xy"

        dp = build_edit_distance_table(word1, word2)

        self.assertEqual(len(dp), len(word1) + 1)
        self.assertEqual(len(dp[0]), len(word2) + 1)

    def test_build_edit_distance_table_known_values(self):
        word1 = "ab"
        word2 = "ac"

        expected = [
            [0, 1, 2],
            [1, 0, 1],
            [2, 1, 1],
        ]

        self.assertEqual(build_edit_distance_table(word1, word2), expected)

    def test_symmetry(self):
        pairs = [
            ("kitten", "sitting"),
            ("abc", "yabd"),
            ("", "hello"),
            ("same", "same"),
        ]

        for a, b in pairs:
            with self.subTest(a=a, b=b):
                self.assertEqual(edit_distance(a, b), edit_distance(b, a))


if __name__ == "__main__":
    unittest.main()
