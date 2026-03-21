"""
Greedy solution for Huffman Coding (optimal prefix codes).

Goal:
Given symbol frequencies, build a binary prefix code that minimizes
the total weighted path length (i.e., optimal compression).

Greedy idea:
Repeatedly merge the two least frequent nodes.

Why this works:
Combining the least frequent symbols at the deepest level minimizes
overall cost (can be proven via exchange argument).
"""

import heapq
from typing import Optional


class Node:
    """
    A node in the Huffman tree.
    """

    def __init__(
            self,
            freq: float,
            symbol: Optional[str] = None,
            left: Optional["Node"] = None,
            right: Optional["Node"] = None,
    ):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other: "Node") -> bool:
        # Required for heapq to compare nodes
        return self.freq < other.freq

    def is_leaf(self) -> bool:
        return self.symbol is not None


def build_huffman_tree(frequencies: dict[str, float]) -> Node:
    """
    Build the Huffman tree from symbol frequencies.

    Args:
        frequencies:
            dict mapping symbol -> frequency

    Returns:
        Root of the Huffman tree

    Raises:
        ValueError:
            If input is empty or contains invalid frequencies
    """
    _validate_frequencies(frequencies)

    heap: list[Node] = []

    # Initialize heap with leaf nodes
    for symbol, freq in frequencies.items():
        heapq.heappush(heap, Node(freq, symbol=symbol))

    # Edge case: single symbol
    if len(heap) == 1:
        only = heap[0]
        return Node(only.freq, left=only)

    # Build tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(
            freq=left.freq + right.freq,
            left=left,
            right=right,
        )

        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(root: Node) -> dict[str, str]:
    """
    Generate Huffman codes (symbol -> bitstring).

    Args:
        root:
            Root of the Huffman tree

    Returns:
        Dictionary mapping symbol -> binary code
    """
    codes: dict[str, str] = {}

    def dfs(node: Node, path: str) -> None:
        if node.is_leaf():
            codes[node.symbol] = path or "0"  # handle single-node case
            return

        if node.left:
            dfs(node.left, path + "0")
        if node.right:
            dfs(node.right, path + "1")

    dfs(root, "")
    return codes


def encode(text: str, codes: dict[str, str]) -> str:
    """
    Encode a string using Huffman codes.
    """
    return "".join(codes[ch] for ch in text)


def decode(encoded: str, root: Node) -> str:
    """
    Decode a Huffman-encoded string.
    """
    result = []
    node = root

    for bit in encoded:
        node = node.left if bit == "0" else node.right

        if node.is_leaf():
            result.append(node.symbol)
            node = root

    return "".join(result)


def _validate_frequencies(frequencies: dict[str, float]) -> None:
    if not frequencies:
        raise ValueError("frequencies cannot be empty")

    for symbol, freq in frequencies.items():
        if freq <= 0:
            raise ValueError(f"invalid frequency for symbol '{symbol}': must be positive")


def print_codes(codes: dict[str, str]) -> None:
    """
    Print Huffman codes in a readable format.
    """
    print("Huffman Codes:")
    for symbol, code in sorted(codes.items()):
        print(f"  '{symbol}': {code}")


def demo() -> None:
    print("=== Huffman Coding Demo ===")

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

    print_codes(codes)

    text = "abcdef"
    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    print("\nOriginal:", text)
    print("Encoded: ", encoded)
    print("Decoded: ", decoded)


if __name__ == "__main__":
    demo()
