"""
Basic bit manipulation utilities.

This file covers the core operations you usually learn first:
- get/check a bit
- set a bit
- clear a bit
- toggle a bit
- update a bit to 0 or 1
- count total bits needed to represent a number
- view binary strings nicely

Bit positions are 0-indexed from the right.

Example:
    number = 13
    binary = 1101

    position: 3 2 1 0
              1 1 0 1
"""

from typing import List


def to_binary(n: int, width: int = 0) -> str:
    """
    Convert an integer to its binary representation without the '0b' prefix.

    Args:
        n: Non-negative integer.
        width: Minimum width of the result. Pads with leading zeros if needed.

    Returns:
        Binary string.

    Raises:
        ValueError: If n is negative or width is negative.
    """
    if n < 0:
        raise ValueError("to_binary only supports non-negative integers")
    if width < 0:
        raise ValueError("width must be non-negative")

    binary = bin(n)[2:]
    if width > 0:
        binary = binary.zfill(width)
    return binary


def bit_length_unsigned(n: int) -> int:
    """
    Return the number of bits needed to represent a non-negative integer.

    Args:
        n: Non-negative integer.

    Returns:
        Number of bits needed to represent n in binary.
        Returns 1 for n = 0.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("bit_length_unsigned only supports non-negative integers")

    if n == 0:
        return 1

    length = 0
    while n > 0:
        length += 1
        n >>= 1
    return length


def is_bit_set(n: int, position: int) -> bool:
    """
    Check whether the bit at 'position' is set to 1.

    Args:
        n: Integer.
        position: Bit position, 0-indexed from the right.

    Returns:
        True if the bit is 1, otherwise False.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    return ((n >> position) & 1) == 1


def get_bit(n: int, position: int) -> int:
    """
    Return the bit value (0 or 1) at a given position.

    Args:
        n: Integer.
        position: Bit position, 0-indexed from the right.

    Returns:
        0 or 1.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    return (n >> position) & 1


def set_bit(n: int, position: int) -> int:
    """
    Set the bit at 'position' to 1.

    Args:
        n: Integer.
        position: Bit position.

    Returns:
        New integer with that bit set.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    return n | (1 << position)


def clear_bit(n: int, position: int) -> int:
    """
    Clear the bit at 'position' to 0.

    Args:
        n: Integer.
        position: Bit position.

    Returns:
        New integer with that bit cleared.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    return n & ~(1 << position)


def toggle_bit(n: int, position: int) -> int:
    """
    Flip the bit at 'position'.

    0 becomes 1, and 1 becomes 0.

    Args:
        n: Integer.
        position: Bit position.

    Returns:
        New integer with that bit toggled.

    Raises:
        ValueError: If position is negative.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    return n ^ (1 << position)


def update_bit(n: int, position: int, value: int) -> int:
    """
    Update the bit at 'position' to a specific value: 0 or 1.

    Args:
        n: Integer.
        position: Bit position.
        value: Must be 0 or 1.

    Returns:
        New integer with the requested bit value.

    Raises:
        ValueError: If position is negative or value is not 0 or 1.
    """
    if position < 0:
        raise ValueError("position must be non-negative")
    if value not in (0, 1):
        raise ValueError("value must be 0 or 1")

    mask = 1 << position
    n &= ~mask
    if value == 1:
        n |= mask
    return n


def lowest_set_bit(n: int) -> int:
    """
    Return the value of the lowest set bit.

    Example:
        n = 12 (1100)
        result = 4 (0100)

    Args:
        n: Positive integer.

    Returns:
        Integer value of the lowest set bit.

    Raises:
        ValueError: If n <= 0.
    """
    if n <= 0:
        raise ValueError("lowest_set_bit requires a positive integer")

    return n & -n


def clear_lowest_set_bit(n: int) -> int:
    """
    Clear the lowest set bit in n.

    Example:
        n = 12 (1100)
        result = 8 (1000)

    Args:
        n: Non-negative integer.

    Returns:
        Integer after removing the lowest set bit.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("clear_lowest_set_bit requires a non-negative integer")

    return n & (n - 1)


def list_set_bit_positions(n: int) -> List[int]:
    """
    Return a list of positions where n has a 1 bit.

    Args:
        n: Non-negative integer.

    Returns:
        List of bit positions in increasing order.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("list_set_bit_positions only supports non-negative integers")

    positions: List[int] = []
    position = 0

    while n > 0:
        if n & 1:
            positions.append(position)
        n >>= 1
        position += 1

    return positions


def explain_bit_operations(n: int, position: int) -> None:
    """
    Print a compact explanation of the main operations for a given number and bit position.
    """
    if position < 0:
        raise ValueError("position must be non-negative")

    width = max(bit_length_unsigned(abs(n)) if n >= 0 else 1, position + 1, 4)

    print("\nBit operation demo")
    print("=" * 60)
    print(f"number              = {n}")
    if n >= 0:
        print(f"binary              = {to_binary(n, width)}")
    print(f"position            = {position}")
    print("-" * 60)

    print(f"get_bit             -> {get_bit(n, position)}")
    print(f"is_bit_set          -> {is_bit_set(n, position)}")

    set_result = set_bit(n, position)
    clear_result = clear_bit(n, position)
    toggle_result = toggle_bit(n, position)

    print(f"set_bit             -> {set_result}")
    if set_result >= 0:
        print(f"                      {to_binary(set_result, width)}")

    print(f"clear_bit           -> {clear_result}")
    if clear_result >= 0:
        print(f"                      {to_binary(clear_result, width)}")

    print(f"toggle_bit          -> {toggle_result}")
    if toggle_result >= 0:
        print(f"                      {to_binary(toggle_result, width)}")

    if n > 0:
        lsb = lowest_set_bit(n)
        cleared = clear_lowest_set_bit(n)
        print(f"lowest_set_bit      -> {lsb} ({to_binary(lsb, width)})")
        print(f"clear_lowest_set_bit-> {cleared} ({to_binary(cleared, width)})")

    if n >= 0:
        print(f"set bit positions   -> {list_set_bit_positions(n)}")


if __name__ == "__main__":
    number = 13
    position = 1

    explain_bit_operations(number, position)

    print("\nManual examples")
    print("=" * 60)

    examples = [0, 1, 5, 13, 42]

    for value in examples:
        width = bit_length_unsigned(value)
        print(f"value={value:>2}  binary={to_binary(value, width)}  set_bits={list_set_bit_positions(value)}")

    print("\nUpdate bit examples")
    print("=" * 60)
    value = 10  # 1010
    print(f"original: {value} -> {to_binary(value, 4)}")
    updated_1 = update_bit(value, 0, 1)
    updated_2 = update_bit(value, 3, 0)
    print(f"set bit 0 to 1: {updated_1} -> {to_binary(updated_1, 4)}")
    print(f"set bit 3 to 0: {updated_2} -> {to_binary(updated_2, 4)}")
