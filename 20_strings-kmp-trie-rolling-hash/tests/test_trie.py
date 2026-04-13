import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        for word in ["app", "apple", "apply", "apt", "bat", "batch", "bath"]:
            self.trie.insert(word)

    def test_search_existing_word(self):
        self.assertTrue(self.trie.search("apple"))
        self.assertTrue(self.trie.search("bat"))

    def test_search_missing_word(self):
        self.assertFalse(self.trie.search("apples"))
        self.assertFalse(self.trie.search("bad"))

    def test_starts_with_existing_prefix(self):
        self.assertTrue(self.trie.starts_with("app"))
        self.assertTrue(self.trie.starts_with("ba"))

    def test_starts_with_missing_prefix(self):
        self.assertFalse(self.trie.starts_with("cat"))

    def test_len_counts_distinct_words(self):
        self.assertEqual(len(self.trie), 7)

    def test_reinsert_same_word(self):
        self.trie.insert("apple")
        self.assertEqual(self.trie.count_word("apple"), 2)
        self.assertEqual(len(self.trie), 7)

    def test_count_word_missing(self):
        self.assertEqual(self.trie.count_word("banana"), 0)

    def test_count_prefix(self):
        self.assertEqual(self.trie.count_prefix("app"), 3)
        self.assertEqual(self.trie.count_prefix("ba"), 3)
        self.assertEqual(self.trie.count_prefix("zzz"), 0)

    def test_words_with_prefix(self):
        self.assertEqual(
            self.trie.words_with_prefix("app"),
            ["app", "apple", "apply"],
        )

    def test_all_words(self):
        self.assertEqual(
            self.trie.all_words(),
            ["app", "apple", "apply", "apt", "bat", "batch", "bath"],
        )

    def test_longest_prefix_of(self):
        self.assertEqual(self.trie.longest_prefix_of("application"), "app")
        self.assertEqual(self.trie.longest_prefix_of("bathtub"), "bath")
        self.assertEqual(self.trie.longest_prefix_of("cat"), "")

    def test_delete_existing_word(self):
        self.assertTrue(self.trie.delete("bat"))
        self.assertFalse(self.trie.search("bat"))
        self.assertTrue(self.trie.search("batch"))
        self.assertTrue(self.trie.search("bath"))

    def test_delete_missing_word(self):
        self.assertFalse(self.trie.delete("banana"))

    def test_delete_one_occurrence_of_duplicate(self):
        self.trie.insert("apple")
        self.assertEqual(self.trie.count_word("apple"), 2)

        self.assertTrue(self.trie.delete("apple"))
        self.assertTrue(self.trie.search("apple"))
        self.assertEqual(self.trie.count_word("apple"), 1)

    def test_empty_string_insert_and_search(self):
        trie = Trie()
        trie.insert("")
        self.assertTrue(trie.search(""))
        self.assertTrue(trie.starts_with(""))
        self.assertEqual(trie.count_word(""), 1)
        self.assertEqual(len(trie), 1)


if __name__ == "__main__":
    unittest.main()
