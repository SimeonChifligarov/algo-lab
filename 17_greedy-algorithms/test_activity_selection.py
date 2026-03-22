import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from activity_selection import activity_selection, max_activity_count


class TestActivitySelection(unittest.TestCase):
    def test_known_example(self):
        activities = [
            (1, 4),
            (3, 5),
            (0, 6),
            (5, 7),
            (3, 9),
            (5, 9),
            (6, 10),
            (8, 11),
            (8, 12),
            (2, 14),
            (12, 16),
        ]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 4), (5, 7), (8, 11), (12, 16)])
        self.assertEqual(max_activity_count(activities), 4)

    def test_empty_input(self):
        self.assertEqual(activity_selection([]), [])
        self.assertEqual(max_activity_count([]), 0)

    def test_single_activity(self):
        activities = [(2, 5)]
        self.assertEqual(activity_selection(activities), [(2, 5)])
        self.assertEqual(max_activity_count(activities), 1)

    def test_already_non_overlapping(self):
        activities = [(1, 2), (2, 3), (3, 4), (4, 5)]

        selected = activity_selection(activities)

        self.assertEqual(selected, activities)
        self.assertEqual(max_activity_count(activities), 4)

    def test_all_overlapping_keeps_earliest_finishing(self):
        activities = [(1, 10), (2, 9), (3, 8), (4, 7)]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(4, 7)])
        self.assertEqual(max_activity_count(activities), 1)

    def test_unsorted_input_is_handled(self):
        activities = [(5, 7), (1, 4), (8, 11), (12, 16)]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 4), (5, 7), (8, 11), (12, 16)])

    def test_back_to_back_activities_are_allowed(self):
        activities = [(1, 3), (3, 5), (5, 8)]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 3), (3, 5), (5, 8)])
        self.assertEqual(max_activity_count(activities), 3)

    def test_zero_length_activities_are_allowed(self):
        activities = [(1, 1), (1, 2), (2, 2), (2, 3)]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 1), (1, 2), (2, 2), (2, 3)])

    def test_invalid_activity_raises_value_error(self):
        activities = [(3, 1)]

        with self.assertRaises(ValueError):
            activity_selection(activities)

        with self.assertRaises(ValueError):
            max_activity_count(activities)

    def test_tie_on_end_time_breaks_by_start_time(self):
        activities = [(2, 5), (1, 5), (5, 6)]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 5), (5, 6)])

    def test_mixed_case(self):
        activities = [
            (0, 3),
            (1, 2),
            (3, 4),
            (2, 5),
            (4, 6),
            (6, 7),
        ]

        selected = activity_selection(activities)

        self.assertEqual(selected, [(1, 2), (3, 4), (4, 6), (6, 7)])
        self.assertEqual(max_activity_count(activities), 4)


if __name__ == "__main__":
    unittest.main()
