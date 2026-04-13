"""
Unit tests for greedy_set_cover.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..greedy_set_cover import greedy_set_cover, coverage_of


class TestGreedySetCover(unittest.TestCase):
    def test_basic_cover(self) -> None:
        universe = {1, 2, 3, 4}
        subsets = {
            "A": {1, 2},
            "B": {2, 3},
            "C": {3, 4},
        }

        solution = greedy_set_cover(universe, subsets)
        covered = coverage_of(solution, subsets)

        self.assertEqual(covered, universe)

    def test_single_subset_covers_all(self) -> None:
        universe = {1, 2, 3}
        subsets = {
            "A": {1, 2, 3},
            "B": {1},
            "C": {2},
        }

        solution = greedy_set_cover(universe, subsets)

        self.assertEqual(solution, ["A"])

    def test_with_overlapping_subsets(self) -> None:
        universe = {1, 2, 3, 4, 5}
        subsets = {
            "A": {1, 2, 3},
            "B": {3, 4},
            "C": {4, 5},
        }

        solution = greedy_set_cover(universe, subsets)
        covered = coverage_of(solution, subsets)

        self.assertEqual(covered, universe)

    def test_uncoverable_universe_raises_error(self) -> None:
        universe = {1, 2, 3}
        subsets = {
            "A": {1},
            "B": {2},
            # missing coverage for element 3
        }

        with self.assertRaises(ValueError):
            greedy_set_cover(universe, subsets)

    def test_empty_universe(self) -> None:
        universe = set()
        subsets = {
            "A": {1, 2},
            "B": {2, 3},
        }

        solution = greedy_set_cover(universe, subsets)
        self.assertEqual(solution, [])

    def test_coverage_of_function(self) -> None:
        subsets = {
            "A": {1, 2},
            "B": {3},
            "C": {4, 5},
        }

        selection = ["A", "C"]
        covered = coverage_of(selection, subsets)

        self.assertEqual(covered, {1, 2, 4, 5})


if __name__ == "__main__":
    unittest.main()
