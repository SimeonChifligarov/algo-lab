import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..basic_bit_operations import (
    bit_length_unsigned,
    clear_bit,
    clear_lowest_set_bit,
    get_bit,
    is_bit_set,
    list_set_bit_positions,
    lowest_set_bit,
    set_bit,
    to_binary,
    toggle_bit,
    update_bit,
)


class TestBasicBitOperations(unittest.TestCase):
    def test_to_binary(self):
        self.assertEqual(to_binary(0), "0")
        self.assertEqual(to_binary(5), "101")
        self.assertEqual(to_binary(5, 5), "00101")

    def test_to_binary_invalid(self):
        with self.assertRaises(ValueError):
            to_binary(-1)
        with self.assertRaises(ValueError):
            to_binary(5, -1)

    def test_bit_length_unsigned(self):
        self.assertEqual(bit_length_unsigned(0), 1)
        self.assertEqual(bit_length_unsigned(1), 1)
        self.assertEqual(bit_length_unsigned(5), 3)
        self.assertEqual(bit_length_unsigned(8), 4)

    def test_bit_length_unsigned_invalid(self):
        with self.assertRaises(ValueError):
            bit_length_unsigned(-1)

    def test_get_and_check_bit(self):
        n = 13  # 1101
        self.assertEqual(get_bit(n, 0), 1)
        self.assertEqual(get_bit(n, 1), 0)
        self.assertEqual(get_bit(n, 2), 1)
        self.assertEqual(get_bit(n, 3), 1)

        self.assertTrue(is_bit_set(n, 0))
        self.assertFalse(is_bit_set(n, 1))
        self.assertTrue(is_bit_set(n, 2))
        self.assertTrue(is_bit_set(n, 3))

    def test_get_and_check_bit_invalid(self):
        with self.assertRaises(ValueError):
            get_bit(5, -1)
        with self.assertRaises(ValueError):
            is_bit_set(5, -1)

    def test_set_bit(self):
        self.assertEqual(set_bit(8, 0), 9)
        self.assertEqual(set_bit(8, 3), 8)

    def test_clear_bit(self):
        self.assertEqual(clear_bit(13, 0), 12)
        self.assertEqual(clear_bit(13, 2), 9)
        self.assertEqual(clear_bit(13, 1), 13)

    def test_toggle_bit(self):
        self.assertEqual(toggle_bit(13, 0), 12)
        self.assertEqual(toggle_bit(13, 1), 15)
        self.assertEqual(toggle_bit(13, 3), 5)

    def test_bit_mutation_invalid(self):
        with self.assertRaises(ValueError):
            set_bit(5, -1)
        with self.assertRaises(ValueError):
            clear_bit(5, -1)
        with self.assertRaises(ValueError):
            toggle_bit(5, -1)

    def test_update_bit(self):
        n = 10  # 1010
        self.assertEqual(update_bit(n, 0, 1), 11)  # 1011
        self.assertEqual(update_bit(n, 1, 0), 8)  # 1000
        self.assertEqual(update_bit(n, 3, 1), 10)  # unchanged

    def test_update_bit_invalid(self):
        with self.assertRaises(ValueError):
            update_bit(5, -1, 1)
        with self.assertRaises(ValueError):
            update_bit(5, 0, 2)

    def test_lowest_set_bit(self):
        self.assertEqual(lowest_set_bit(12), 4)
        self.assertEqual(lowest_set_bit(10), 2)
        self.assertEqual(lowest_set_bit(1), 1)

    def test_lowest_set_bit_invalid(self):
        with self.assertRaises(ValueError):
            lowest_set_bit(0)
        with self.assertRaises(ValueError):
            lowest_set_bit(-4)

    def test_clear_lowest_set_bit(self):
        self.assertEqual(clear_lowest_set_bit(12), 8)
        self.assertEqual(clear_lowest_set_bit(10), 8)
        self.assertEqual(clear_lowest_set_bit(0), 0)

    def test_clear_lowest_set_bit_invalid(self):
        with self.assertRaises(ValueError):
            clear_lowest_set_bit(-1)

    def test_list_set_bit_positions(self):
        self.assertEqual(list_set_bit_positions(0), [])
        self.assertEqual(list_set_bit_positions(13), [0, 2, 3])
        self.assertEqual(list_set_bit_positions(42), [1, 3, 5])

    def test_list_set_bit_positions_invalid(self):
        with self.assertRaises(ValueError):
            list_set_bit_positions(-1)


if __name__ == "__main__":
    unittest.main()
