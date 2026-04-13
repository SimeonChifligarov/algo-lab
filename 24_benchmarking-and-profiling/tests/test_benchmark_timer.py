"""
Unit tests for benchmark_timer.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..benchmark_timer import (
    benchmark,
    format_seconds,
    sum_of_squares,
    sum_of_squares_formula,
)


class TestBenchmarkTimer(unittest.TestCase):
    def test_sum_of_squares_matches_formula(self) -> None:
        for n in [1, 5, 10, 100]:
            self.assertEqual(sum_of_squares(n), sum_of_squares_formula(n))

    def test_benchmark_returns_expected_keys(self) -> None:
        result = benchmark(sum_of_squares, 1000, repeats=3)

        self.assertIn("min", result)
        self.assertIn("max", result)
        self.assertIn("mean", result)
        self.assertIn("median", result)

    def test_benchmark_values_are_non_negative(self) -> None:
        result = benchmark(sum_of_squares, 1000, repeats=3)

        for value in result.values():
            self.assertGreaterEqual(value, 0.0)

    def test_benchmark_invalid_repeats_raises(self) -> None:
        with self.assertRaises(ValueError):
            benchmark(sum_of_squares, 100, repeats=0)

    def test_format_seconds_nanoseconds(self) -> None:
        text = format_seconds(1e-9)
        self.assertIn("ns", text)

    def test_format_seconds_microseconds(self) -> None:
        text = format_seconds(1e-5)
        self.assertIn("µs", text)

    def test_format_seconds_milliseconds(self) -> None:
        text = format_seconds(1e-2)
        self.assertIn("ms", text)

    def test_format_seconds_seconds(self) -> None:
        text = format_seconds(2.5)
        self.assertIn("s", text)


if __name__ == "__main__":
    unittest.main()
