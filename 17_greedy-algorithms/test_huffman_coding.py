import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from huffman_coding import (
    Node,
    build_codes,
    build_huffman_tree,
    decode,
    encode,
)


class TestHuffmanCoding(unittest.TestCase):
    def test_build_huffman_tree_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_huffman_tree({})

    def test_build_huffman_tree_non_positive_frequency_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_huffman_tree({"a": 0})

        with self.assertRaises(ValueError):
            build_huffman_tree({"a": -3})

    def test_single_symbol_gets_code_zero(self):
        frequencies = {"a": 5}

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        self.assertEqual(codes, {"a": "0"})

    def test_encode_single_symbol_text(self):
        frequencies = {"x": 10}

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        encoded = encode("xxxx", codes)

        self.assertEqual(encoded, "0000")

    def test_encode_and_decode_round_trip_known_example(self):
        frequencies = {
            "a": 5,
            "b": 9,
            "c": 12,
            "d": 13,
            "e": 16,
            "f": 45,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        text = "abcdef"
        encoded = encode(text, codes)
        decoded = decode(encoded, root)

        self.assertEqual(decoded, text)

    def test_encode_and_decode_round_trip_repeated_symbols(self):
        frequencies = {
            "a": 5,
            "b": 9,
            "c": 12,
            "d": 13,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        text = "abacabad"
        encoded = encode(text, codes)
        decoded = decode(encoded, root)

        self.assertEqual(decoded, text)

    def test_codes_contain_all_symbols(self):
        frequencies = {
            "a": 5,
            "b": 9,
            "c": 12,
            "d": 13,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        self.assertEqual(set(codes.keys()), set(frequencies.keys()))

    def test_codes_are_prefix_free(self):
        frequencies = {
            "a": 5,
            "b": 9,
            "c": 12,
            "d": 13,
            "e": 16,
            "f": 45,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)
        codewords = list(codes.values())

        for i, code1 in enumerate(codewords):
            for j, code2 in enumerate(codewords):
                if i == j:
                    continue
                self.assertFalse(code2.startswith(code1))

    def test_more_frequent_symbol_does_not_have_longer_code_than_rare_symbol_in_simple_case(self):
        frequencies = {
            "a": 100,
            "b": 1,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        self.assertLessEqual(len(codes["a"]), len(codes["b"]))

    def test_encode_empty_string_returns_empty_string(self):
        frequencies = {
            "a": 5,
            "b": 7,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        self.assertEqual(encode("", codes), "")

    def test_encode_unknown_symbol_raises_key_error(self):
        frequencies = {
            "a": 5,
            "b": 7,
        }

        root = build_huffman_tree(frequencies)
        codes = build_codes(root)

        with self.assertRaises(KeyError):
            encode("abc", codes)

    def test_decode_empty_string_returns_empty_string_for_multi_symbol_tree(self):
        frequencies = {
            "a": 5,
            "b": 7,
        }

        root = build_huffman_tree(frequencies)

        self.assertEqual(decode("", root), "")

    def test_manual_node_is_leaf(self):
        leaf = Node(3, symbol="z")
        self.assertTrue(leaf.is_leaf())

    def test_manual_node_is_not_leaf(self):
        internal = Node(5, left=Node(2, symbol="a"), right=Node(3, symbol="b"))
        self.assertFalse(internal.is_leaf())


if __name__ == "__main__":
    unittest.main()
