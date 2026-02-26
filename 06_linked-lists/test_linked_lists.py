"""
Tests for Linked Lists toolkit (Part 4/4)

Run:
  python test_linked_lists.py

or:
  python -m unittest test_linked_lists.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from linked_list_core import (
    ListNode,
    build_linked_list,
    linked_list_to_list,
    iter_nodes,
    length,
    tail_node,
    node_at,
)
from linked_list_ops import (
    reverse_list,
    merge_sorted_lists,
    remove_first_value,
    remove_all_values,
    remove_nth_from_end,
)
from linked_list_patterns import (
    middle_node,
    has_cycle,
    cycle_entry,
    kth_from_end,
    is_palindrome_list,
)


class TestLinkedListCore(unittest.TestCase):
    def test_build_and_convert(self) -> None:
        head = build_linked_list([1, 2, 3])
        self.assertEqual(linked_list_to_list(head), [1, 2, 3])

        empty = build_linked_list([])
        self.assertIsNone(empty)
        self.assertEqual(linked_list_to_list(empty), [])

    def test_helpers(self) -> None:
        head = build_linked_list([10, 20, 30, 40])
        self.assertEqual(length(head), 4)
        self.assertEqual(tail_node(head).value, 40)  # type: ignore[union-attr]
        self.assertEqual(node_at(head, 0).value, 10)
        self.assertEqual(node_at(head, 2).value, 30)

        self.assertEqual([n.value for n in iter_nodes(head)], [10, 20, 30, 40])

        with self.assertRaises(IndexError):
            node_at(head, -1)
        with self.assertRaises(IndexError):
            node_at(head, 10)

    def test_linked_list_to_list_with_cap(self) -> None:
        head = build_linked_list([1, 2, 3, 4, 5])
        self.assertEqual(linked_list_to_list(head, max_nodes=3), [1, 2, 3])


class TestLinkedListOps(unittest.TestCase):
    def test_reverse_list(self) -> None:
        head = build_linked_list([1, 2, 3, 4])
        rev = reverse_list(head)
        self.assertEqual(linked_list_to_list(rev), [4, 3, 2, 1])

        self.assertIsNone(reverse_list(None))
        one = build_linked_list([99])
        self.assertEqual(linked_list_to_list(reverse_list(one)), [99])

    def test_merge_sorted_lists(self) -> None:
        a = build_linked_list([1, 3, 5])
        b = build_linked_list([2, 4, 6])
        m = merge_sorted_lists(a, b)
        self.assertEqual(linked_list_to_list(m), [1, 2, 3, 4, 5, 6])

        self.assertEqual(linked_list_to_list(merge_sorted_lists(None, None)), [])
        c = build_linked_list([1, 2])
        self.assertEqual(linked_list_to_list(merge_sorted_lists(c, None)), [1, 2])

    def test_remove_first_value(self) -> None:
        head = build_linked_list([1, 2, 3, 2])
        head, removed = remove_first_value(head, 2)
        self.assertTrue(removed)
        self.assertEqual(linked_list_to_list(head), [1, 3, 2])

        head, removed = remove_first_value(head, 9)
        self.assertFalse(removed)
        self.assertEqual(linked_list_to_list(head), [1, 3, 2])

        head2 = build_linked_list([7, 8])
        head2, removed2 = remove_first_value(head2, 7)
        self.assertTrue(removed2)
        self.assertEqual(linked_list_to_list(head2), [8])

    def test_remove_all_values(self) -> None:
        head = build_linked_list([2, 1, 2, 3, 2, 4, 2])
        head = remove_all_values(head, 2)
        self.assertEqual(linked_list_to_list(head), [1, 3, 4])

        self.assertIsNone(remove_all_values(build_linked_list([5, 5]), 5))
        self.assertEqual(linked_list_to_list(remove_all_values(None, 1)), [])

    def test_remove_nth_from_end(self) -> None:
        head = build_linked_list([1, 2, 3, 4, 5])
        head = remove_nth_from_end(head, 2)
        self.assertEqual(linked_list_to_list(head), [1, 2, 3, 5])

        one = build_linked_list([10])
        self.assertIsNone(remove_nth_from_end(one, 1))

        with self.assertRaises(ValueError):
            remove_nth_from_end(build_linked_list([1, 2]), 0)
        with self.assertRaises(IndexError):
            remove_nth_from_end(build_linked_list([1, 2]), 3)


class TestLinkedListPatterns(unittest.TestCase):
    def test_middle_node(self) -> None:
        self.assertIsNone(middle_node(None))
        self.assertEqual(middle_node(build_linked_list([1])).value, 1)  # type: ignore[union-attr]
        self.assertEqual(middle_node(build_linked_list([1, 2, 3])).value, 2)  # type: ignore[union-attr]
        self.assertEqual(middle_node(build_linked_list([1, 2, 3, 4])).value, 3)  # second middle

    def test_kth_from_end(self) -> None:
        head = build_linked_list([10, 20, 30, 40, 50])
        self.assertEqual(kth_from_end(head, 1).value, 50)
        self.assertEqual(kth_from_end(head, 2).value, 40)
        self.assertEqual(kth_from_end(head, 5).value, 10)

        with self.assertRaises(ValueError):
            kth_from_end(head, 0)
        with self.assertRaises(IndexError):
            kth_from_end(head, 6)

    def test_cycle_detection_and_entry(self) -> None:
        head = build_linked_list([10, 20, 30, 40, 50])
        self.assertFalse(has_cycle(head))
        self.assertIsNone(cycle_entry(head))

        # Create cycle: tail -> node with value 30
        entry = node_at(head, 2)
        tail = tail_node(head)
        tail.next = entry  # type: ignore[union-attr]

        self.assertTrue(has_cycle(head))
        self.assertIs(cycle_entry(head), entry)

    def test_is_palindrome_list(self) -> None:
        odd = build_linked_list([1, 2, 3, 2, 1])
        self.assertTrue(is_palindrome_list(odd))
        self.assertEqual(linked_list_to_list(odd), [1, 2, 3, 2, 1])  # restored

        even = build_linked_list([1, 2, 2, 1])
        self.assertTrue(is_palindrome_list(even))
        self.assertEqual(linked_list_to_list(even), [1, 2, 2, 1])  # restored

        not_pal = build_linked_list([1, 2, 3])
        self.assertFalse(is_palindrome_list(not_pal))
        self.assertEqual(linked_list_to_list(not_pal), [1, 2, 3])  # restored

        self.assertTrue(is_palindrome_list(None))
        self.assertTrue(is_palindrome_list(build_linked_list([42])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
