"""
Learn 1D dynamic programming through two classic problems:
- House Robber
- Kadane's Algorithm (Maximum Subarray)

Main DP ideas:
- define a state clearly
- write the transition from smaller states
- optimize space when only a few previous states are needed
"""


def house_robber(nums: list[int]) -> int:
    """
    Return the maximum amount of money you can rob without
    robbing two adjacent houses.

    State:
        dp[i] = maximum money that can be robbed from the first
                i + 1 houses (houses 0..i)

    Transition:
        dp[i] = max(
            dp[i - 1],            # skip current house
            dp[i - 2] + nums[i]   # rob current house
        )

    Space optimization:
        We only need the previous two states, so we use O(1) space.
    """
    if not nums:
        return 0

    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current

    return prev1


def house_robber_with_table(nums: list[int]) -> int:
    """
    Same House Robber problem, but with an explicit DP table
    to make the transition easier to see.
    """
    if not nums:
        return 0

    if len(nums) == 1:
        return nums[0]

    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

    return dp[-1]


def kadane_max_subarray(nums: list[int]) -> int:
    """
    Return the maximum possible sum of a non-empty contiguous subarray.

    State:
        best_ending_here = maximum subarray sum ending at current index

    Transition:
        best_ending_here = max(nums[i], best_ending_here + nums[i])

    Global answer:
        best_so_far = max(best_so_far, best_ending_here)

    Space optimization:
        Only O(1) extra space is needed.
    """
    if not nums:
        raise ValueError("nums must not be empty")

    best_ending_here = nums[0]
    best_so_far = nums[0]

    for i in range(1, len(nums)):
        best_ending_here = max(nums[i], best_ending_here + nums[i])
        best_so_far = max(best_so_far, best_ending_here)

    return best_so_far


def kadane_with_indices(nums: list[int]) -> tuple[int, int, int]:
    """
    Return:
        (max_sum, start_index, end_index)

    where nums[start_index:end_index + 1] is a maximum-sum subarray.
    """
    if not nums:
        raise ValueError("nums must not be empty")

    best_ending_here = nums[0]
    best_so_far = nums[0]

    current_start = 0
    best_start = 0
    best_end = 0

    for i in range(1, len(nums)):
        if nums[i] > best_ending_here + nums[i]:
            best_ending_here = nums[i]
            current_start = i
        else:
            best_ending_here = best_ending_here + nums[i]

        if best_ending_here > best_so_far:
            best_so_far = best_ending_here
            best_start = current_start
            best_end = i

    return best_so_far, best_start, best_end


def demo() -> None:
    print("=== House Robber Demo ===")
    houses = [2, 7, 9, 3, 1]
    print("houses =", houses)
    print("house_robber =", house_robber(houses))
    print("house_robber_with_table =", house_robber_with_table(houses))
    print()

    print("=== Kadane's Algorithm Demo ===")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("nums =", nums)
    print("kadane_max_subarray =", kadane_max_subarray(nums))
    max_sum, start, end = kadane_with_indices(nums)
    print("kadane_with_indices =", (max_sum, start, end))
    print("best subarray =", nums[start:end + 1])


if __name__ == "__main__":
    demo()
