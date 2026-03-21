"""
A small driver file that ties together:
- Activity Selection
- Fractional Knapsack
- Huffman Coding

It also includes short notes about greedy design:
- local choice vs global optimum
- why greedy works for some problems
- exchange argument intuition
"""

from activity_selection import activity_selection, print_schedule
from fractional_knapsack import fractional_knapsack, print_solution
from huffman_coding import build_huffman_tree, build_codes, encode, decode, print_codes


def greedy_notes() -> None:
    """
    Print short conceptual notes about greedy algorithms.
    """
    print("=== Greedy Algorithm Notes ===")
    print("1. A greedy algorithm makes the best local choice at each step.")
    print("2. Greedy algorithms do not reconsider previous choices.")
    print("3. They work only when a local optimum leads to a global optimum.")
    print("4. Correctness is often justified with an exchange argument.")
    print("5. Common pattern: sort or prioritize by a key rule, then build a solution.")
    print()


def activity_selection_demo() -> None:
    """
    Run and print a sample Activity Selection example.
    """
    print("=== Activity Selection Demo ===")

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
    print_schedule(selected)
    print()


def fractional_knapsack_demo() -> None:
    """
    Run and print a sample Fractional Knapsack example.
    """
    print("=== Fractional Knapsack Demo ===")

    items = [
        (60, 10),
        (100, 20),
        (120, 30),
    ]
    capacity = 50

    total_value, chosen_items = fractional_knapsack(capacity, items)
    print_solution(total_value, chosen_items)
    print()


def huffman_demo() -> None:
    """
    Run and print a sample Huffman Coding example.
    """
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

    text = "face"
    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    print()
    print("Original:", text)
    print("Encoded: ", encoded)
    print("Decoded: ", decoded)
    print()


def correctness_notes() -> None:
    """
    Print short intuition for why the greedy choices work here.
    """
    print("=== Correctness Intuition ===")
    print("Activity Selection:")
    print("  Choosing the earliest finishing compatible activity leaves")
    print("  as much room as possible for future activities.")
    print()

    print("Fractional Knapsack:")
    print("  Choosing the highest value/weight ratio first is always safe")
    print("  because fractions are allowed.")
    print()

    print("Huffman Coding:")
    print("  Merging the two least frequent symbols first keeps the most")
    print("  expensive code depths away from high-frequency symbols.")
    print()


def main() -> None:
    greedy_notes()
    activity_selection_demo()
    fractional_knapsack_demo()
    huffman_demo()
    correctness_notes()


if __name__ == "__main__":
    main()
