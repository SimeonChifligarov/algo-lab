import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..bit_counting_and_power import (
    count_bits_upto,
    count_set_bits_builtin,
    count_set_bits_kernighan,
    count_set_bits_naive,
    is_power_of_two,
    next_power_of_two,
    parity,
    previous_power_of_two,
)


class TestBitCountingAndPower(unittest.TestCase):
    def test_count_set_bits_methods_agree(self):
        values = [0, 1, 2, 3, 4, 5, 8, 13, 42, 255]
        for value in values:
            expected = count_set_bits_builtin(value)
            self.assertEqual(count_set_bits_naive(value), expected)
            self.assertEqual(count_set_bits_kernighan(value), expected)

    def test_count_set_bits_invalid(self):
        with self.assertRaises(ValueError):
            count_set_bits_naive(-1)
        with self.assertRaises(ValueError):
            count_set_bits_kernighan(-1)
        with self.assertRaises(ValueError):
            count_set_bits_builtin(-1)

    def test_is_power_of_two(self):
        self.assertFalse(is_power_of_two(0))
        self.assertTrue(is_power_of_two(1))
        self.assertTrue(is_power_of_two(2))
        self.assertFalse(is_power_of_two(3))
        self.assertTrue(is_power_of_two(8))
        self.assertFalse(is_power_of_two(10))
        self.assertFalse(is_power_of_two(-8))

    def test_next_power_of_two(self):
        self.assertEqual(next_power_of_two(1), 1)
        self.assertEqual(next_power_of_two(2), 2)
        self.assertEqual(next_power_of_two(5), 8)
        self.assertEqual(next_power_of_two(8), 8)
        self.assertEqual(next_power_of_two(9), 16)

    def test_next_power_of_two_invalid(self):
        with self.assertRaises(ValueError):
            next_power_of_two(0)
        with self.assertRaises(ValueError):
            next_power_of_two(-3)

    def test_previous_power_of_two(self):
        self.assertEqual(previous_power_of_two(1), 1)
        self.assertEqual(previous_power_of_two(2), 2)
        self.assertEqual(previous_power_of_two(5), 4)
        self.assertEqual(previous_power_of_two(8), 8)
        self.assertEqual(previous_power_of_two(15), 8)

    def test_previous_power_of_two_invalid(self):
        with self.assertRaises(ValueError):
            previous_power_of_two(0)
        with self.assertRaises(ValueError):
            previous_power_of_two(-7)

    def test_count_bits_upto(self):
        self.assertEqual(count_bits_upto(0), [0])
        self.assertEqual(count_bits_upto(5), [0, 1, 1, 2, 1, 2])
        self.assertEqual(count_bits_upto(10), [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2])

    def test_count_bits_upto_invalid(self):
        with self.assertRaises(ValueError):
            count_bits_upto(-1)

    def test_parity(self):
        self.assertEqual(parity(0), 0)
        self.assertEqual(parity(1), 1)
        self.assertEqual(parity(3), 0)  # two set bits
        self.assertEqual(parity(7), 1)  # three set bits
        self.assertEqual(parity(10), 0)  # two set bits
        self.assertEqual(parity(13), 1)  # three set bits

    def test_parity_invalid(self):
        with self.assertRaises(ValueError):
            parity(-1)


if __name__ == "__main__":
    unittest.main()
