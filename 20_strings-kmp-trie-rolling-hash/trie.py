"""
Trie (Prefix Tree)

This module implements a Trie data structure for efficient string storage,
exact lookup, prefix lookup, and related dictionary-style operations.

Why use a Trie?
    A Trie is useful when working with many strings that share prefixes.

Typical applications:
    - dictionary word lookup
    - autocomplete
    - prefix counting
    - spell-check style tasks
    - word game backtracking
    - storing many patterns

Main operations:
    - insert(word)
    - search(word)
    - starts_with(prefix)
    - delete(word)
    - words_with_prefix(prefix)

Time complexity:
    Most operations are O(k), where k is the length of the word/prefix.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TrieNode:
    """
    A single node in the Trie.

    Attributes:
        children: outgoing edges keyed by character
        is_end_of_word: True if a full word ends at this node
        word_count: number of times this exact word was inserted
        prefix_count: number of inserted words passing through this node
    """
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    is_end_of_word: bool = False
    word_count: int = 0
    prefix_count: int = 0


class Trie:
    """
    Trie / Prefix Tree implementation.

    Supports insertion, exact search, prefix checks, deletion,
    prefix enumeration, and basic counting helpers.
    """

    def __init__(self) -> None:
        self.root = TrieNode()
        self._size = 0

    def __len__(self) -> int:
        """
        Number of distinct words currently stored.
        """
        return self._size

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Args:
            word: word to insert

        Notes:
            - Empty string is allowed.
            - Re-inserting the same word increases its word_count but does not
              increase the number of distinct stored words.
        """
        node = self.root
        node.prefix_count += 1

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.prefix_count += 1

        if node.word_count == 0:
            self._size += 1

        node.is_end_of_word = True
        node.word_count += 1

    def search(self, word: str) -> bool:
        """
        Check whether a full word exists in the trie.

        Args:
            word: word to search

        Returns:
            True if the exact word exists, otherwise False.
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check whether any stored word starts with the given prefix.

        Args:
            prefix: prefix to check

        Returns:
            True if at least one word has this prefix, otherwise False.
        """
        return self._find_node(prefix) is not None

    def count_word(self, word: str) -> int:
        """
        Return how many times a word was inserted.

        Args:
            word: exact word

        Returns:
            insertion count for this exact word
        """
        node = self._find_node(word)
        if node is None:
            return 0
        return node.word_count

    def count_prefix(self, prefix: str) -> int:
        """
        Return how many inserted words share the given prefix.

        Args:
            prefix: prefix to count

        Returns:
            Number of words passing through the node for this prefix.
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        return node.prefix_count

    def delete(self, word: str) -> bool:
        """
        Delete one occurrence of a word from the trie.

        Args:
            word: word to remove

        Returns:
            True if a word occurrence was removed, False if the word
            was not present.

        Notes:
            - If a word was inserted multiple times, this removes only one copy.
            - Unused nodes are pruned.
        """
        if not self.search(word):
            return False

        self._delete(self.root, word, 0)
        return True

    def words_with_prefix(self, prefix: str) -> List[str]:
        """
        Return all stored words that start with the given prefix.

        Args:
            prefix: prefix to expand

        Returns:
            List of matching words in lexicographic traversal order.
        """
        start_node = self._find_node(prefix)
        if start_node is None:
            return []

        results: List[str] = []
        self._collect_words(start_node, prefix, results)
        return results

    def all_words(self) -> List[str]:
        """
        Return all stored distinct words in the trie.
        """
        return self.words_with_prefix("")

    def longest_prefix_of(self, text: str) -> str:
        """
        Return the longest stored word that is a prefix of the given text.

        Args:
            text: input text

        Returns:
            Longest matching stored prefix word, or empty string if none exists.
        """
        node = self.root
        longest_end = -1

        if node.is_end_of_word:
            longest_end = 0

        for i, ch in enumerate(text):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_end_of_word:
                longest_end = i + 1

        return text[:longest_end] if longest_end != -1 else ""

    def _find_node(self, s: str) -> Optional[TrieNode]:
        """
        Traverse the trie following string s.

        Args:
            s: string to follow

        Returns:
            Final node if path exists, otherwise None.
        """
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect_words(self, node: TrieNode, prefix: str, results: List[str]) -> None:
        """
        DFS helper to collect all words below a node.
        """
        if node.is_end_of_word:
            results.append(prefix)

        for ch in sorted(node.children):
            self._collect_words(node.children[ch], prefix + ch, results)

    def _delete(self, node: TrieNode, word: str, depth: int) -> bool:
        """
        Recursive delete helper.

        Returns:
            True if this node should be pruned from its parent,
            otherwise False.
        """
        node.prefix_count -= 1

        if depth == len(word):
            node.word_count -= 1

            if node.word_count == 0:
                node.is_end_of_word = False
                self._size -= 1

            return (
                    node.prefix_count == 0
                    and not node.is_end_of_word
                    and len(node.children) == 0
            )

        ch = word[depth]
        child = node.children[ch]
        should_prune_child = self._delete(child, word, depth + 1)

        if should_prune_child:
            del node.children[ch]

        return (
                node.prefix_count == 0
                and not node.is_end_of_word
                and len(node.children) == 0
        )

    def pretty_print(self) -> None:
        """
        Print the trie contents in a tree-like form.
        """
        print("\nTrie structure")
        print("=" * 50)
        self._pretty_print(self.root, prefix="", edge_label="ROOT", depth=0)

    def _pretty_print(
            self,
            node: TrieNode,
            prefix: str,
            edge_label: str,
            depth: int,
    ) -> None:
        """
        Recursive helper for pretty_print.
        """
        marker = " *" if node.is_end_of_word else ""
        print(
            f"{'  ' * depth}{edge_label}"
            f"  (prefix_count={node.prefix_count}, word_count={node.word_count}){marker}"
        )

        for ch in sorted(node.children):
            self._pretty_print(node.children[ch], prefix + ch, ch, depth + 1)

    def explain_search(self, word: str) -> None:
        """
        Show step-by-step traversal for an exact search.
        """
        node = self.root

        print(f"\nSearching for: '{word}'")
        print("-" * 50)

        for i, ch in enumerate(word):
            print(f"Step {i}: need character '{ch}'")

            if ch not in node.children:
                print(f"  character '{ch}' not found")
                print("  search failed")
                return

            node = node.children[ch]
            print(
                f"  moved to node: prefix_count={node.prefix_count}, "
                f"word_count={node.word_count}, end={node.is_end_of_word}"
            )

        print("-" * 50)
        if node.is_end_of_word:
            print("Exact word found.")
        else:
            print("Prefix exists, but exact word does not end here.")


if __name__ == "__main__":
    trie = Trie()

    words = [
        "app",
        "apple",
        "apply",
        "apt",
        "bat",
        "batch",
        "bath",
        "banana",
    ]

    print("Building trie")
    print("=" * 50)
    for word in words:
        print(f"Inserting: {word}")
        trie.insert(word)

    print("\nBasic queries")
    print("=" * 50)
    print("search('apple')      ->", trie.search("apple"))
    print("search('apples')     ->", trie.search("apples"))
    print("starts_with('app')   ->", trie.starts_with("app"))
    print("starts_with('cat')   ->", trie.starts_with("cat"))
    print("count_word('apple')  ->", trie.count_word("apple"))
    print("count_prefix('ba')   ->", trie.count_prefix("ba"))
    print("all_words()          ->", trie.all_words())
    print("words_with_prefix('ap') ->", trie.words_with_prefix("ap"))
    print("longest_prefix_of('applicationform') ->", trie.longest_prefix_of("applicationform"))

    trie.pretty_print()
    trie.explain_search("batch")

    print("\nDeleting 'bat'")
    print("=" * 50)
    trie.delete("bat")
    print("search('bat')        ->", trie.search("bat"))
    print("words_with_prefix('ba') ->", trie.words_with_prefix("ba"))
    trie.pretty_print()
