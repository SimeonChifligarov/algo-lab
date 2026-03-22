import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from fractional_knapsack import fractional_knapsack


class TestFractionalKnapsack(unittest.TestCase):
    def test_known_example(self):
        items = [
            (60, 10),
            (100, 20),
            (120, 30),
        ]

        total_value, chosen_items = fractional_knapsack(50, items)

        self.assertAlmostEqual(total_value, 240.0)
        self.assertEqual(
            chosen_items,
            [
                (60, 10, 1.0),
                (100, 20, 1.0),
                (120, 30, 2 / 3),
            ],
        )

    def test_empty_items(self):
        total_value, chosen_items = fractional_knapsack(10, [])

        self.assertEqual(total_value, 0.0)
        self.assertEqual(chosen_items, [])

    def test_zero_capacity(self):
        items = [
            (60, 10),
            (100, 20),
        ]

        total_value, chosen_items = fractional_knapsack(0, items)

        self.assertEqual(total_value, 0.0)
        self.assertEqual(chosen_items, [])

    def test_take_all_items_when_capacity_is_large_enough(self):
        items = [
            (10, 2),
            (15, 3),
            (7, 1),
        ]

        total_value, chosen_items = fractional_knapsack(10, items)

        self.assertEqual(total_value, 32.0)
        self.assertEqual(len(chosen_items), 3)
        self.assertEqual(set(chosen_items), {(10, 2, 1.0), (15, 3, 1.0), (7, 1, 1.0)})

    def test_single_item_taken_fractionally(self):
        items = [
            (100, 20),
        ]

        total_value, chosen_items = fractional_knapsack(5, items)

        self.assertEqual(total_value, 25.0)
        self.assertEqual(chosen_items, [(100, 20, 0.25)])

    def test_items_are_chosen_by_ratio(self):
        items = [
            (100, 50),  # ratio 2
            (60, 10),  # ratio 6
            (120, 30),  # ratio 4
        ]

        total_value, chosen_items = fractional_knapsack(40, items)

        self.assertEqual(
            chosen_items,
            [
                (60, 10, 1.0),
                (120, 30, 1.0),
            ],
        )
        self.assertEqual(total_value, 180.0)

    def test_partial_last_item(self):
        items = [
            (50, 10),  # ratio 5
            (90, 30),  # ratio 3
        ]

        total_value, chosen_items = fractional_knapsack(20, items)

        self.assertEqual(total_value, 80.0)
        self.assertEqual(
            chosen_items,
            [
                (50, 10, 1.0),
                (90, 30, 1 / 3),
            ],
        )

    def test_negative_capacity_raises_value_error(self):
        with self.assertRaises(ValueError):
            fractional_knapsack(-1, [(10, 2)])

    def test_zero_weight_raises_value_error(self):
        with self.assertRaises(ValueError):
            fractional_knapsack(10, [(10, 0)])

    def test_negative_weight_raises_value_error(self):
        with self.assertRaises(ValueError):
            fractional_knapsack(10, [(10, -2)])

    def test_negative_value_is_supported(self):
        items = [
            (10, 2),
            (-5, 1),
        ]

        total_value, chosen_items = fractional_knapsack(2, items)

        self.assertEqual(total_value, 10.0)
        self.assertEqual(chosen_items, [(10, 2, 1.0)])

    def test_equal_ratios(self):
        items = [
            (20, 4),  # ratio 5
            (15, 3),  # ratio 5
            (10, 2),  # ratio 5
        ]

        total_value, chosen_items = fractional_knapsack(5, items)

        self.assertEqual(total_value, 25.0)
        self.assertEqual(sum(weight * fraction for _, weight, fraction in chosen_items), 5.0)


if __name__ == "__main__":
    unittest.main()
