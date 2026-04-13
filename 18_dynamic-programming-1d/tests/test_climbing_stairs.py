import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..climbing_stairs import (
    climbing_stairs_bottom_up,
    climbing_stairs_space_optimized,
    climbing_stairs_top_down,
)


class TestClimbingStairs(unittest.TestCase):
    def test_base_case_zero(self):
        self.assertEqual(climbing_stairs_top_down(0), 1)
        self.assertEqual(climbing_stairs_bottom_up(0), 1)
        self.assertEqual(climbing_stairs_space_optimized(0), 1)

    def test_base_case_one(self):
        self.assertEqual(climbing_stairs_top_down(1), 1)
        self.assertEqual(climbing_stairs_bottom_up(1), 1)
        self.assertEqual(climbing_stairs_space_optimized(1), 1)

    def test_small_values(self):
        expected = {
            0: 1,
            1: 1,
            2: 2,
            3: 3,
            4: 5,
            5: 8,
            6: 13,
            7: 21,
        }

        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(climbing_stairs_top_down(n), value)
                self.assertEqual(climbing_stairs_bottom_up(n), value)
                self.assertEqual(climbing_stairs_space_optimized(n), value)

    def test_medium_value(self):
        n = 10
        expected = 89

        self.assertEqual(climbing_stairs_top_down(n), expected)
        self.assertEqual(climbing_stairs_bottom_up(n), expected)
        self.assertEqual(climbing_stairs_space_optimized(n), expected)

    def test_all_implementations_match_for_range(self):
        for n in range(0, 25):
            with self.subTest(n=n):
                top_down = climbing_stairs_top_down(n)
                bottom_up = climbing_stairs_bottom_up(n)
                space_optimized = climbing_stairs_space_optimized(n)

                self.assertEqual(top_down, bottom_up)
                self.assertEqual(bottom_up, space_optimized)

    def test_top_down_uses_provided_memo(self):
        memo = {2: 2, 3: 3}
        result = climbing_stairs_top_down(5, memo)

        self.assertEqual(result, 8)
        self.assertIn(5, memo)
        self.assertEqual(memo[5], 8)

    def test_negative_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            climbing_stairs_top_down(-1)

        with self.assertRaises(ValueError):
            climbing_stairs_bottom_up(-1)

        with self.assertRaises(ValueError):
            climbing_stairs_space_optimized(-1)

    def test_larger_value(self):
        n = 20
        expected = 10946

        self.assertEqual(climbing_stairs_top_down(n), expected)
        self.assertEqual(climbing_stairs_bottom_up(n), expected)
        self.assertEqual(climbing_stairs_space_optimized(n), expected)


if __name__ == "__main__":
    unittest.main()
