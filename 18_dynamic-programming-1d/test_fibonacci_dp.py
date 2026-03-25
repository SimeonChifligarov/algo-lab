import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from fibonacci_dp import (
    fibonacci_bottom_up,
    fibonacci_space_optimized,
    fibonacci_top_down,
)


class TestFibonacciDP(unittest.TestCase):
    def test_base_case_zero(self):
        self.assertEqual(fibonacci_top_down(0), 0)
        self.assertEqual(fibonacci_bottom_up(0), 0)
        self.assertEqual(fibonacci_space_optimized(0), 0)

    def test_base_case_one(self):
        self.assertEqual(fibonacci_top_down(1), 1)
        self.assertEqual(fibonacci_bottom_up(1), 1)
        self.assertEqual(fibonacci_space_optimized(1), 1)

    def test_small_values(self):
        expected = {
            0: 0,
            1: 1,
            2: 1,
            3: 2,
            4: 3,
            5: 5,
            6: 8,
            7: 13,
            8: 21,
            9: 34,
            10: 55,
        }

        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(fibonacci_top_down(n), value)
                self.assertEqual(fibonacci_bottom_up(n), value)
                self.assertEqual(fibonacci_space_optimized(n), value)

    def test_medium_value(self):
        n = 20
        expected = 6765

        self.assertEqual(fibonacci_top_down(n), expected)
        self.assertEqual(fibonacci_bottom_up(n), expected)
        self.assertEqual(fibonacci_space_optimized(n), expected)

    def test_all_implementations_match_for_range(self):
        for n in range(0, 25):
            with self.subTest(n=n):
                top_down = fibonacci_top_down(n)
                bottom_up = fibonacci_bottom_up(n)
                space_optimized = fibonacci_space_optimized(n)

                self.assertEqual(top_down, bottom_up)
                self.assertEqual(bottom_up, space_optimized)

    def test_top_down_uses_provided_memo(self):
        memo = {2: 1, 3: 2}
        result = fibonacci_top_down(5, memo)

        self.assertEqual(result, 5)
        self.assertIn(5, memo)
        self.assertEqual(memo[5], 5)

    def test_negative_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            fibonacci_top_down(-1)

        with self.assertRaises(ValueError):
            fibonacci_bottom_up(-1)

        with self.assertRaises(ValueError):
            fibonacci_space_optimized(-1)

    def test_larger_value(self):
        n = 30
        expected = 832040

        self.assertEqual(fibonacci_bottom_up(n), expected)
        self.assertEqual(fibonacci_space_optimized(n), expected)
        self.assertEqual(fibonacci_top_down(n), expected)


if __name__ == "__main__":
    unittest.main()
