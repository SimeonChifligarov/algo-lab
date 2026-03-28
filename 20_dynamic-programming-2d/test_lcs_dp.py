import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from lcs_dp import build_lcs_table, lcs_length, lcs_string


class TestLCSDP(unittest.TestCase):
    def test_both_empty(self):
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_string("", ""), "")
        self.assertEqual(build_lcs_table("", ""), [[0]])

    def test_one_empty(self):
        self.assertEqual(lcs_length("abc", ""), 0)
        self.assertEqual(lcs_length("", "abc"), 0)
        self.assertEqual(lcs_string("abc", ""), "")
        self.assertEqual(lcs_string("", "abc"), "")

    def test_known_example(self):
        text1 = "abcde"
        text2 = "ace"

        self.assertEqual(lcs_length(text1, text2), 3)
        self.assertEqual(lcs_string(text1, text2), "ace")

    def test_identical_strings(self):
        text = "dynamic"

        self.assertEqual(lcs_length(text, text), len(text))
        self.assertEqual(lcs_string(text, text), text)

    def test_no_common_subsequence(self):
        text1 = "abc"
        text2 = "xyz"

        self.assertEqual(lcs_length(text1, text2), 0)
        self.assertEqual(lcs_string(text1, text2), "")

    def test_repeated_characters(self):
        text1 = "aab"
        text2 = "azab"

        result = lcs_string(text1, text2)

        self.assertEqual(lcs_length(text1, text2), 3)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, "aab")

    def test_multiple_valid_lcs_only_check_length_and_validity(self):
        text1 = "abc"
        text2 = "bac"

        result = lcs_string(text1, text2)

        self.assertEqual(lcs_length(text1, text2), 2)
        self.assertEqual(len(result), 2)
        self.assertIn(result, {"ac", "bc"})

    def test_build_table_dimensions(self):
        text1 = "abcd"
        text2 = "xy"

        dp = build_lcs_table(text1, text2)

        self.assertEqual(len(dp), len(text1) + 1)
        self.assertEqual(len(dp[0]), len(text2) + 1)

    def test_build_table_known_values(self):
        text1 = "abc"
        text2 = "ac"

        dp = build_lcs_table(text1, text2)

        expected = [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 2],
        ]
        self.assertEqual(dp, expected)

    def test_lcs_result_is_subsequence_of_both_inputs(self):
        text1 = "abcbdab"
        text2 = "bdcaba"
        result = lcs_string(text1, text2)

        self.assertEqual(len(result), lcs_length(text1, text2))
        self.assertTrue(_is_subsequence(result, text1))
        self.assertTrue(_is_subsequence(result, text2))


def _is_subsequence(sub: str, full: str) -> bool:
    i = 0
    for ch in full:
        if i < len(sub) and sub[i] == ch:
            i += 1
    return i == len(sub)


if __name__ == "__main__":
    unittest.main()
