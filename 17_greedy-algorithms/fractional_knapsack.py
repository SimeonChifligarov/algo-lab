"""
Greedy solution for the Fractional Knapsack problem.

Goal:
Given items with value and weight, and a knapsack with limited capacity,
maximize total value. Unlike the 0/1 knapsack problem, here we may take
fractions of items.

Greedy idea:
Always take as much as possible from the item with the highest
value-to-weight ratio.

Why this works:
At every step, the locally best choice (best ratio) is also part of
a globally optimal solution.
"""


def fractional_knapsack(
        capacity: float,
        items: list[tuple[float, float]],
) -> tuple[float, list[tuple[float, float, float]]]:
    """
    Solve the fractional knapsack problem greedily.

    Args:
        capacity:
            Maximum total weight the knapsack can hold.

        items:
            A list of (value, weight) pairs.

    Returns:
        A tuple:
            (max_value, chosen_items)

        max_value:
            Total value obtained.

        chosen_items:
            A list of (value, weight, fraction_taken), where
            fraction_taken is in [0.0, 1.0].

    Raises:
        ValueError:
            If capacity is negative, or if an item has invalid weight.
    """
    _validate_inputs(capacity, items)

    if capacity == 0:
        return 0.0, []

    # Decorate items with value/weight ratio
    items_with_ratio = []
    for value, weight in items:
        ratio = value / weight
        items_with_ratio.append((ratio, value, weight))

    # Sort by descending ratio
    items_with_ratio.sort(reverse=True)

    remaining_capacity = capacity
    total_value = 0.0
    chosen_items: list[tuple[float, float, float]] = []

    for ratio, value, weight in items_with_ratio:
        if remaining_capacity == 0:
            break

        if weight <= remaining_capacity:
            fraction_taken = 1.0
            chosen_weight = weight
            chosen_value = value
        else:
            fraction_taken = remaining_capacity / weight
            chosen_weight = remaining_capacity
            chosen_value = value * fraction_taken

        total_value += chosen_value
        chosen_items.append((value, weight, fraction_taken))
        remaining_capacity -= chosen_weight

    return total_value, chosen_items


def _validate_inputs(capacity: float, items: list[tuple[float, float]]) -> None:
    if capacity < 0:
        raise ValueError("capacity cannot be negative")

    for value, weight in items:
        if weight <= 0:
            raise ValueError(
                f"invalid item (value={value}, weight={weight}): weight must be positive"
            )


def print_solution(
        total_value: float,
        chosen_items: list[tuple[float, float, float]],
) -> None:
    """
    Print the chosen knapsack contents in a readable format.
    """
    print("Chosen items:")
    for value, weight, fraction_taken in chosen_items:
        print(
            f"  value={value}, weight={weight}, fraction_taken={fraction_taken:.4f}"
        )
    print(f"Total value: {total_value:.4f}")


def demo() -> None:
    print("=== Fractional Knapsack Demo ===")

    items = [
        (60, 10),
        (100, 20),
        (120, 30),
    ]
    capacity = 50

    total_value, chosen_items = fractional_knapsack(capacity, items)
    print_solution(total_value, chosen_items)


if __name__ == "__main__":
    demo()
