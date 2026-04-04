"""
Applications of bit manipulation in optimization and low-level problem solving.

This module brings together the earlier ideas and shows how bit operations
appear in actual algorithmic tasks.

What this file covers:
- swapping values with XOR
- finding the unique element with XOR
- finding two unique elements
- missing number using XOR
- subset sum with bitmask enumeration
- assignment optimization with DP over subsets
- maximum XOR pair
- compact flag storage with a bitset-style class

These examples are practical and commonly appear in interviews,
competitive programming, and systems-style reasoning.
"""

from typing import Iterable, List, Sequence, Tuple


def xor_swap(a: int, b: int) -> Tuple[int, int]:
    """
    Swap two integers using XOR.

    Args:
        a: first integer
        b: second integer

    Returns:
        Tuple[int, int]: swapped values

    Notes:
        In Python this is mostly educational, because normal tuple swap
        is clearer and preferred: a, b = b, a
    """
    a ^= b
    b ^= a
    a ^= b
    return a, b


def find_single_number(nums: Sequence[int]) -> int:
    """
    Find the element that appears exactly once when every other element
    appears exactly twice.

    Args:
        nums: input sequence

    Returns:
        The unique element

    Why this works:
        x ^ x = 0
        x ^ 0 = x
        So all paired elements cancel out.
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def find_two_single_numbers(nums: Sequence[int]) -> Tuple[int, int]:
    """
    Find the two elements that appear exactly once when every other element
    appears exactly twice.

    Args:
        nums: input sequence

    Returns:
        Tuple[int, int]: the two unique values, sorted

    Idea:
        - XOR of all numbers gives x ^ y, where x and y are the unique numbers
        - pick one set bit where x and y differ
        - partition numbers by that bit
        - XOR within each group
    """
    xor_all = 0
    for num in nums:
        xor_all ^= num

    distinguishing_bit = xor_all & -xor_all

    a = 0
    b = 0

    for num in nums:
        if num & distinguishing_bit:
            a ^= num
        else:
            b ^= num

    return tuple(sorted((a, b)))


def find_missing_number(nums: Sequence[int], n: int) -> int:
    """
    Find the missing number from the range [0, n].

    Args:
        nums: numbers from 0 to n with exactly one missing
        n: upper bound of the full range

    Returns:
        Missing number

    Example:
        nums = [0, 1, 3], n = 3 -> 2
    """
    xor_all = 0

    for value in range(n + 1):
        xor_all ^= value

    for num in nums:
        xor_all ^= num

    return xor_all


def subset_sum_exists(numbers: Sequence[int], target: int) -> bool:
    """
    Check whether there exists a subset whose sum equals target.

    Uses full subset enumeration with bitmasks.

    Args:
        numbers: sequence of integers
        target: target sum

    Returns:
        True if such a subset exists, else False

    Time Complexity:
        O(n * 2^n)

    Best for:
        Small n, educational bitmask practice
    """
    n = len(numbers)

    for mask in range(1 << n):
        total = 0
        for i in range(n):
            if (mask >> i) & 1:
                total += numbers[i]
        if total == target:
            return True

    return False


def find_subset_sum(numbers: Sequence[int], target: int) -> List[int]:
    """
    Return one subset whose sum equals target.

    Args:
        numbers: sequence of integers
        target: target sum

    Returns:
        One matching subset as a list, or [] if none exists

    Notes:
        If target is 0, the empty subset may be returned.
    """
    n = len(numbers)

    for mask in range(1 << n):
        subset: List[int] = []
        total = 0

        for i in range(n):
            if (mask >> i) & 1:
                subset.append(numbers[i])
                total += numbers[i]

        if total == target:
            return subset

    return []


def min_assignment_cost(cost: List[List[int]]) -> int:
    """
    Solve the assignment problem using DP over subsets.

    Problem:
        There are n workers and n jobs.
        cost[i][j] = cost of assigning worker i to job j.
        Assign each worker exactly one distinct job with minimum total cost.

    Args:
        cost: square matrix of size n x n

    Returns:
        Minimum assignment cost

    Complexity:
        O(n * 2^n)

    Notes:
        This is a classic subset DP example.
    """
    n = len(cost)

    if n == 0:
        return 0

    for row in cost:
        if len(row) != n:
            raise ValueError("cost matrix must be square")

    dp = [float("inf")] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        worker = mask.bit_count()

        if worker >= n:
            continue

        for job in range(n):
            if ((mask >> job) & 1) == 0:
                new_mask = mask | (1 << job)
                dp[new_mask] = min(dp[new_mask], dp[mask] + cost[worker][job])

    return dp[(1 << n) - 1]


def max_xor_pair(nums: Sequence[int]) -> int:
    """
    Compute the maximum XOR value obtainable from any pair.

    Args:
        nums: sequence of non-negative integers

    Returns:
        Maximum XOR of any pair

    Idea:
        Greedy prefix-building from highest bit to lowest bit.
    """
    if len(nums) < 2:
        return 0

    answer = 0
    mask = 0

    max_bit = max(nums).bit_length()

    for bit in range(max_bit - 1, -1, -1):
        mask |= 1 << bit
        prefixes = {num & mask for num in nums}

        candidate = answer | (1 << bit)

        for prefix in prefixes:
            if (prefix ^ candidate) in prefixes:
                answer = candidate
                break

    return answer


class BitFlags:
    """
    A compact bitset-style utility for storing boolean flags in one integer.

    Example:
        flags = BitFlags()
        flags.enable(2)
        flags.enable(5)
        flags.is_enabled(2) -> True
        flags.is_enabled(3) -> False
    """

    def __init__(self) -> None:
        self._flags = 0

    def enable(self, position: int) -> None:
        """
        Set a flag.
        """
        self._validate_position(position)
        self._flags |= 1 << position

    def disable(self, position: int) -> None:
        """
        Clear a flag.
        """
        self._validate_position(position)
        self._flags &= ~(1 << position)

    def toggle(self, position: int) -> None:
        """
        Toggle a flag.
        """
        self._validate_position(position)
        self._flags ^= 1 << position

    def is_enabled(self, position: int) -> bool:
        """
        Check whether a flag is set.
        """
        self._validate_position(position)
        return ((self._flags >> position) & 1) == 1

    def reset(self) -> None:
        """
        Clear all flags.
        """
        self._flags = 0

    def value(self) -> int:
        """
        Return the raw integer bitmask.
        """
        return self._flags

    def enabled_positions(self) -> List[int]:
        """
        Return all enabled flag positions.
        """
        result: List[int] = []
        value = self._flags
        position = 0

        while value:
            if value & 1:
                result.append(position)
            value >>= 1
            position += 1

        return result

    @staticmethod
    def _validate_position(position: int) -> None:
        if position < 0:
            raise ValueError("position must be non-negative")


def explain_xor_properties(values: Iterable[int]) -> None:
    """
    Print a quick demonstration of XOR accumulation.
    """
    values = list(values)

    print("\nXOR Properties Demo")
    print("=" * 70)
    print(f"values = {values}")

    running = 0
    for value in values:
        previous = running
        running ^= value
        print(f"{previous} ^ {value} = {running}")

    print("-" * 70)
    print(f"final xor = {running}")


def explain_subset_sum(numbers: Sequence[int], target: int) -> None:
    """
    Print all subset sums until a target is found.
    """
    n = len(numbers)

    print("\nSubset Sum via Bitmask Demo")
    print("=" * 70)
    print(f"numbers = {list(numbers)}")
    print(f"target  = {target}")
    print("-" * 70)

    for mask in range(1 << n):
        subset: List[int] = []
        total = 0

        for i in range(n):
            if (mask >> i) & 1:
                subset.append(numbers[i])
                total += numbers[i]

        print(f"mask={mask:>2} subset={subset} sum={total}")

        if total == target:
            print("-" * 70)
            print(f"Found matching subset: {subset}")
            return

    print("-" * 70)
    print("No subset matches the target.")


def explain_assignment_dp(cost: List[List[int]]) -> None:
    """
    Print the subset-DP progression for the assignment problem.
    """
    n = len(cost)

    if n == 0:
        print("Empty cost matrix -> answer is 0")
        return

    for row in cost:
        if len(row) != n:
            raise ValueError("cost matrix must be square")

    dp = [float("inf")] * (1 << n)
    dp[0] = 0

    print("\nAssignment DP Demo")
    print("=" * 70)
    print("Cost matrix:")
    for row in cost:
        print(row)
    print("-" * 70)

    for mask in range(1 << n):
        worker = mask.bit_count()
        print(f"mask={mask:0{n}b} worker={worker} dp={dp[mask]}")

        if worker >= n:
            continue

        for job in range(n):
            if ((mask >> job) & 1) == 0:
                new_mask = mask | (1 << job)
                new_cost = dp[mask] + cost[worker][job]

                if new_cost < dp[new_mask]:
                    print(
                        f"  assign worker {worker} -> job {job}, "
                        f"new_mask={new_mask:0{n}b}, cost={new_cost}"
                    )
                    dp[new_mask] = new_cost

    print("-" * 70)
    print(f"Minimum assignment cost = {dp[(1 << n) - 1]}")


if __name__ == "__main__":
    print("Bit Manipulation Applications Demo")
    print("=" * 70)

    print("\n1) XOR swap")
    print("=" * 70)
    a, b = 5, 9
    print(f"before: a={a}, b={b}")
    a, b = xor_swap(a, b)
    print(f"after : a={a}, b={b}")

    print("\n2) Unique number with XOR")
    print("=" * 70)
    nums1 = [4, 1, 2, 1, 2]
    print(f"nums = {nums1}")
    print(f"single number = {find_single_number(nums1)}")
    explain_xor_properties(nums1)

    print("\n3) Two unique numbers")
    print("=" * 70)
    nums2 = [1, 2, 1, 3, 2, 5]
    print(f"nums = {nums2}")
    print(f"two singles = {find_two_single_numbers(nums2)}")

    print("\n4) Missing number")
    print("=" * 70)
    nums3 = [0, 1, 3, 4]
    print(f"nums = {nums3}, n = 4")
    print(f"missing number = {find_missing_number(nums3, 4)}")

    print("\n5) Subset sum")
    print("=" * 70)
    numbers = [3, 5, 7, 9]
    target = 12
    print(f"subset sum exists? {subset_sum_exists(numbers, target)}")
    print(f"one matching subset: {find_subset_sum(numbers, target)}")
    explain_subset_sum(numbers, target)

    print("\n6) Assignment optimization with subset DP")
    print("=" * 70)
    cost_matrix = [
        [9, 2, 7],
        [6, 4, 3],
        [5, 8, 1],
    ]
    print(f"minimum assignment cost = {min_assignment_cost(cost_matrix)}")
    explain_assignment_dp(cost_matrix)

    print("\n7) Maximum XOR pair")
    print("=" * 70)
    nums4 = [3, 10, 5, 25, 2, 8]
    print(f"nums = {nums4}")
    print(f"max xor pair value = {max_xor_pair(nums4)}")

    print("\n8) Compact flag storage")
    print("=" * 70)
    flags = BitFlags()
    flags.enable(1)
    flags.enable(4)
    flags.toggle(2)
    print(f"raw flags value     = {flags.value()}")
    print(f"enabled positions   = {flags.enabled_positions()}")
    print(f"is 1 enabled?       = {flags.is_enabled(1)}")
    print(f"is 3 enabled?       = {flags.is_enabled(3)}")
    flags.disable(1)
    print(f"after disabling 1   = {flags.value()}")
