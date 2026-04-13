import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..bitmask_subsets import (
    add_element_to_mask,
    difference_masks,
    generate_all_masks,
    generate_all_subsets,
    generate_submasks,
    generate_subsets_of_size,
    generate_subsets_with_masks,
    intersection_masks,
    is_element_in_mask,
    is_subset,
    mask_to_binary,
    mask_to_indices,
    mask_to_subset,
    remove_element_from_mask,
    subset_to_mask,
    subset_to_mask_from_items,
    toggle_element_in_mask,
    union_masks,
)


class TestBitmaskSubsets(unittest.TestCase):
    def test_mask_to_binary(self):
        self.assertEqual(mask_to_binary(5, 4), "0101")
        self.assertEqual(mask_to_binary(0, 3), "000")

    def test_mask_to_binary_invalid(self):
        with self.assertRaises(ValueError):
            mask_to_binary(-1, 3)
        with self.assertRaises(ValueError):
            mask_to_binary(3, -1)

    def test_is_element_in_mask(self):
        mask = 0b1010
        self.assertFalse(is_element_in_mask(mask, 0))
        self.assertTrue(is_element_in_mask(mask, 1))
        self.assertFalse(is_element_in_mask(mask, 2))
        self.assertTrue(is_element_in_mask(mask, 3))

    def test_is_element_in_mask_invalid(self):
        with self.assertRaises(ValueError):
            is_element_in_mask(-1, 0)
        with self.assertRaises(ValueError):
            is_element_in_mask(1, -1)

    def test_add_remove_toggle_element(self):
        mask = 0b0101
        self.assertEqual(add_element_to_mask(mask, 1), 0b0111)
        self.assertEqual(remove_element_from_mask(mask, 2), 0b0001)
        self.assertEqual(toggle_element_in_mask(mask, 0), 0b0100)

    def test_subset_to_mask_and_back(self):
        indices = [0, 2, 3]
        mask = subset_to_mask(indices)
        self.assertEqual(mask, 13)
        self.assertEqual(mask_to_indices(mask), indices)

    def test_subset_to_mask_invalid(self):
        with self.assertRaises(ValueError):
            subset_to_mask([0, -1])

    def test_mask_to_indices_invalid(self):
        with self.assertRaises(ValueError):
            mask_to_indices(-1)

    def test_mask_to_subset(self):
        items = ["A", "B", "C", "D"]
        self.assertEqual(mask_to_subset(items, 0b1010), ["B", "D"])
        self.assertEqual(mask_to_subset(items, 0), [])

    def test_mask_to_subset_invalid(self):
        with self.assertRaises(ValueError):
            mask_to_subset(["A"], -1)

    def test_subset_to_mask_from_items(self):
        items = ["A", "B", "C", "D"]
        self.assertEqual(subset_to_mask_from_items(items, ["A", "C"]), 0b0101)
        self.assertEqual(subset_to_mask_from_items(items, []), 0)

    def test_subset_to_mask_from_items_invalid(self):
        with self.assertRaises(ValueError):
            subset_to_mask_from_items(["A", "B"], ["C"])

    def test_generate_all_masks(self):
        self.assertEqual(generate_all_masks(0), [0])
        self.assertEqual(generate_all_masks(3), list(range(8)))

    def test_generate_all_masks_invalid(self):
        with self.assertRaises(ValueError):
            generate_all_masks(-1)

    def test_generate_all_subsets(self):
        items = ["A", "B"]
        self.assertEqual(
            generate_all_subsets(items),
            [[], ["A"], ["B"], ["A", "B"]],
        )

    def test_generate_subsets_with_masks(self):
        items = ["A", "B"]
        self.assertEqual(
            generate_subsets_with_masks(items),
            [
                (0, []),
                (1, ["A"]),
                (2, ["B"]),
                (3, ["A", "B"]),
            ],
        )

    def test_generate_submasks(self):
        self.assertEqual(generate_submasks(0), [0])
        self.assertEqual(generate_submasks(0b101), [0b101, 0b100, 0b001, 0b000])

    def test_generate_submasks_invalid(self):
        with self.assertRaises(ValueError):
            generate_submasks(-1)

    def test_generate_subsets_of_size(self):
        items = ["A", "B", "C"]
        self.assertEqual(
            generate_subsets_of_size(items, 2),
            [["A", "B"], ["A", "C"], ["B", "C"]],
        )
        self.assertEqual(generate_subsets_of_size(items, 0), [[]])

    def test_generate_subsets_of_size_invalid(self):
        with self.assertRaises(ValueError):
            generate_subsets_of_size(["A"], -1)

    def test_is_subset(self):
        self.assertTrue(is_subset(0b0011, 0b0111))
        self.assertFalse(is_subset(0b1000, 0b0111))

    def test_is_subset_invalid(self):
        with self.assertRaises(ValueError):
            is_subset(-1, 3)
        with self.assertRaises(ValueError):
            is_subset(1, -3)

    def test_set_operations(self):
        mask1 = 0b0011
        mask2 = 0b0110
        self.assertEqual(union_masks(mask1, mask2), 0b0111)
        self.assertEqual(intersection_masks(mask1, mask2), 0b0010)
        self.assertEqual(difference_masks(mask1, mask2), 0b0001)

    def test_set_operations_invalid(self):
        with self.assertRaises(ValueError):
            union_masks(-1, 1)
        with self.assertRaises(ValueError):
            intersection_masks(1, -1)
        with self.assertRaises(ValueError):
            difference_masks(-1, -1)


if __name__ == "__main__":
    unittest.main()
