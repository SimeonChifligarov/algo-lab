"""
Greedy solution for the Activity Selection problem
(also called Interval Scheduling).

Goal:
Given a set of activities with start and end times,
select the maximum number of non-overlapping activities.

Greedy idea:
Always pick the activity that finishes earliest among
the remaining compatible activities.

Why this works:
Choosing the earliest finishing activity leaves as much room
as possible for future activities.
"""


def activity_selection(
        activities: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """
    Select the maximum number of non-overlapping activities.

    Args:
        activities:
            A list of (start, end) pairs.

    Returns:
        A list of selected activities in the order they are chosen.

    Raises:
        ValueError:
            If an activity has start > end.
    """
    _validate_activities(activities)

    # Sort by finishing time, then by start time for stable behavior
    sorted_activities = sorted(activities, key=lambda activity: (activity[1], activity[0]))

    selected: list[tuple[int, int]] = []
    current_end = float("-inf")

    for start, end in sorted_activities:
        if start >= current_end:
            selected.append((start, end))
            current_end = end

    return selected


def max_activity_count(activities: list[tuple[int, int]]) -> int:
    """
    Return the maximum number of non-overlapping activities.
    """
    return len(activity_selection(activities))


def _validate_activities(activities: list[tuple[int, int]]) -> None:
    for start, end in activities:
        if start > end:
            raise ValueError(f"invalid activity ({start}, {end}): start cannot be greater than end")


def print_schedule(selected: list[tuple[int, int]]) -> None:
    """
    Print the selected schedule in a readable format.
    """
    print("Selected activities:")
    for start, end in selected:
        print(f"  start={start}, end={end}")
    print(f"Total selected: {len(selected)}")


def demo() -> None:
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


if __name__ == "__main__":
    demo()
