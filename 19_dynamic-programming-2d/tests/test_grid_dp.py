import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..grid_dp import (
    build_min_path_sum_table,
    build_unique_paths_table,
    min_path_sum,
    unique_paths,
)


class TestUniquePaths(unittest.TestCase):
    def test_single_cell(self):
        self.assertEqual(unique_paths(1, 1), 1)
        self.assertEqual(build_unique_paths_table(1, 1), [[1]])

    def test_single_row(self):
        self.assertEqual(unique_paths(1, 5), 1)
        self.assertEqual(build_unique_paths_table(1, 5), [[1, 1, 1, 1, 1]])

    def test_single_column(self):
        self.assertEqual(unique_paths(4, 1), 1)
        self.assertEqual(build_unique_paths_table(4, 1), [[1], [1], [1], [1]])

    def test_small_grid(self):
        self.assertEqual(unique_paths(3, 2), 3)
        self.assertEqual(unique_paths(3, 3), 6)

    def test_known_example(self):
        self.assertEqual(unique_paths(3, 4), 10)

        expected = [
            [1, 1, 1, 1],
            [1, 2, 3, 4],
            [1, 3, 6, 10],
        ]
        self.assertEqual(build_unique_paths_table(3, 4), expected)

    def test_invalid_dimensions_raise_value_error(self):
        with self.assertRaises(ValueError):
            unique_paths(0, 3)

        with self.assertRaises(ValueError):
            unique_paths(3, 0)

        with self.assertRaises(ValueError):
            build_unique_paths_table(-1, 2)

        with self.assertRaises(ValueError):
            build_unique_paths_table(2, -1)


class TestMinPathSum(unittest.TestCase):
    def test_single_cell(self):
        grid = [[7]]
        self.assertEqual(min_path_sum(grid), 7)
        self.assertEqual(build_min_path_sum_table(grid), [[7]])

    def test_single_row(self):
        grid = [[1, 2, 3, 4]]

        self.assertEqual(min_path_sum(grid), 10)
        self.assertEqual(build_min_path_sum_table(grid), [[1, 3, 6, 10]])

    def test_single_column(self):
        grid = [
            [1],
            [2],
            [3],
        ]

        self.assertEqual(min_path_sum(grid), 6)
        self.assertEqual(build_min_path_sum_table(grid), [[1], [3], [6]])

    def test_known_example(self):
        grid = [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1],
        ]

        self.assertEqual(min_path_sum(grid), 7)

        expected = [
            [1, 4, 5],
            [2, 7, 6],
            [6, 8, 7],
        ]
        self.assertEqual(build_min_path_sum_table(grid), expected)

    def test_another_example(self):
        grid = [
            [1, 2, 3],
            [4, 5, 6],
        ]

        self.assertEqual(min_path_sum(grid), 12)

        expected = [
            [1, 3, 6],
            [5, 8, 12],
        ]
        self.assertEqual(build_min_path_sum_table(grid), expected)

    def test_empty_grid_raises_value_error(self):
        with self.assertRaises(ValueError):
            min_path_sum([])

        with self.assertRaises(ValueError):
            build_min_path_sum_table([])

    def test_empty_first_row_raises_value_error(self):
        with self.assertRaises(ValueError):
            min_path_sum([[]])

        with self.assertRaises(ValueError):
            build_min_path_sum_table([[]])

    def test_non_rectangular_grid_raises_value_error(self):
        grid = [
            [1, 2],
            [3],
        ]

        with self.assertRaises(ValueError):
            min_path_sum(grid)

        with self.assertRaises(ValueError):
            build_min_path_sum_table(grid)

    def test_negative_value_raises_value_error(self):
        grid = [
            [1, -2],
            [3, 4],
        ]

        with self.assertRaises(ValueError):
            min_path_sum(grid)

        with self.assertRaises(ValueError):
            build_min_path_sum_table(grid)


if __name__ == "__main__":
    unittest.main()
