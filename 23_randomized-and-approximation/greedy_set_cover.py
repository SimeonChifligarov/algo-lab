"""
Goal:
Implement a greedy approximation algorithm for the Set Cover problem.

Problem:
- Given a universe U of elements
- Given a collection of subsets whose union equals U
- Find as few subsets as possible that cover all elements in U

Key idea (Greedy):
- At each step, pick the subset that covers the largest number of uncovered elements

Properties:
- This is NOT optimal in general (Set Cover is NP-hard)
- Greedy achieves an approximation ratio of O(log n)

This file includes:
- A greedy set cover implementation
- A simple approximation ratio illustration
- A demo
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple


def greedy_set_cover(
        universe: Set[int],
        subsets: Dict[str, Set[int]],
) -> List[str]:
    """
    Greedy approximation for Set Cover.

    Args:
        universe: set of elements to cover
        subsets: mapping from subset name -> set of elements

    Returns:
        A list of subset names forming a cover

    Raises:
        ValueError: if the universe cannot be fully covered
    """
    uncovered = set(universe)
    chosen_subsets: List[str] = []

    while uncovered:
        best_subset_name = None
        best_covered: Set[int] = set()

        # Find subset covering the most uncovered elements
        for name, subset in subsets.items():
            covered = uncovered & subset
            if len(covered) > len(best_covered):
                best_subset_name = name
                best_covered = covered

        if not best_subset_name:
            raise ValueError("Universe cannot be covered with given subsets")

        chosen_subsets.append(best_subset_name)
        uncovered -= best_covered

    return chosen_subsets


def coverage_of(selection: List[str], subsets: Dict[str, Set[int]]) -> Set[int]:
    """
    Compute the union of selected subsets.
    """
    result: Set[int] = set()
    for name in selection:
        result |= subsets[name]
    return result


def demo() -> None:
    """
    Demonstration of greedy set cover.
    """
    # Universe of elements
    universe = set(range(1, 11))

    # Subsets (intentionally overlapping)
    subsets: Dict[str, Set[int]] = {
        "A": {1, 2, 3, 4},
        "B": {3, 4, 5, 6},
        "C": {5, 6, 7},
        "D": {7, 8, 9},
        "E": {9, 10},
        "F": {1, 10},
    }

    print("Universe:", universe)
    print("Subsets:")
    for name, subset in subsets.items():
        print(f"  {name}: {sorted(subset)}")

    solution = greedy_set_cover(universe, subsets)

    print("\nGreedy solution (subset names):", solution)

    covered = coverage_of(solution, subsets)
    print("Covered elements:", sorted(covered))

    print("\nNumber of subsets used:", len(solution))
    print("Total subsets available:", len(subsets))

    print("\nNote:")
    print("- Greedy does not always produce the optimal solution")
    print("- But it is efficient and has a logarithmic approximation guarantee")


if __name__ == "__main__":
    demo()
