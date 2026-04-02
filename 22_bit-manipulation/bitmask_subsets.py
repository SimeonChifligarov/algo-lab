"""
Bit masking and subset generation.

This module focuses on:
- representing subsets with bitmasks
- converting between subsets and masks
- generating all subsets
- generating submasks of a mask
- common bitmask helpers used in combinatorics and optimization

Why this matters:
    Bitmasks are a compact way to represent subsets of small sets.
    They are heavily used in backtracking, DP over subsets, and optimization
    problems such as TSP, set cover variations, and subset sum variants.
"""

from typing import Iterable, List, Sequence, Tuple


def mask_to_binary(mask: int, width: int) -> str:
    """
    Convert a non-negative mask to a zero-padded binary string.

    Args:
        mask: non-negative integer mask
        width: output width

    Returns:
        Binary string of length at least width.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")
    if width < 0:
        raise ValueError("width must be non-negative")

    return bin(mask)[2:].zfill(width)


def is_element_in_mask(mask: int, index: int) -> bool:
    """
    Check whether the bit at 'index' is set in the mask.

    Args:
        mask: non-negative integer mask
        index: bit position

    Returns:
        True if element/index is included in the subset.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")
    if index < 0:
        raise ValueError("index must be non-negative")

    return ((mask >> index) & 1) == 1


def add_element_to_mask(mask: int, index: int) -> int:
    """
    Return a new mask with the given bit set.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")
    if index < 0:
        raise ValueError("index must be non-negative")

    return mask | (1 << index)


def remove_element_from_mask(mask: int, index: int) -> int:
    """
    Return a new mask with the given bit cleared.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")
    if index < 0:
        raise ValueError("index must be non-negative")

    return mask & ~(1 << index)


def toggle_element_in_mask(mask: int, index: int) -> int:
    """
    Return a new mask with the given bit toggled.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")
    if index < 0:
        raise ValueError("index must be non-negative")

    return mask ^ (1 << index)


def subset_to_mask(indices: Iterable[int]) -> int:
    """
    Convert an iterable of non-negative indices into a bitmask.

    Example:
        [0, 2, 3] -> 13  (1101)

    Args:
        indices: iterable of positions to set

    Returns:
        Integer bitmask
    """
    mask = 0

    for index in indices:
        if index < 0:
            raise ValueError("all indices must be non-negative")
        mask |= 1 << index

    return mask


def mask_to_indices(mask: int) -> List[int]:
    """
    Convert a mask into the list of set bit indices.

    Example:
        13 (1101) -> [0, 2, 3]
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")

    indices: List[int] = []
    bit = 0

    while mask > 0:
        if mask & 1:
            indices.append(bit)
        mask >>= 1
        bit += 1

    return indices


def mask_to_subset(items: Sequence[str], mask: int) -> List[str]:
    """
    Convert a mask into the corresponding subset of items.

    Args:
        items: sequence of items
        mask: subset mask

    Returns:
        List of selected items
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")

    subset: List[str] = []

    for i, item in enumerate(items):
        if (mask >> i) & 1:
            subset.append(item)

    return subset


def subset_to_mask_from_items(items: Sequence[str], chosen_items: Iterable[str]) -> int:
    """
    Convert selected items into a mask, based on their positions in 'items'.

    Args:
        items: master sequence of items
        chosen_items: iterable of items to include

    Returns:
        Bitmask

    Raises:
        ValueError: if a chosen item is not in items
    """
    position = {item: i for i, item in enumerate(items)}
    mask = 0

    for item in chosen_items:
        if item not in position:
            raise ValueError(f"item not found in items: {item!r}")
        mask |= 1 << position[item]

    return mask


def generate_all_masks(n: int) -> List[int]:
    """
    Generate all masks for a set of size n.

    Args:
        n: number of elements

    Returns:
        List [0, 1, 2, ..., 2^n - 1]
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    return list(range(1 << n))


def generate_all_subsets(items: Sequence[str]) -> List[List[str]]:
    """
    Generate all subsets of the given items using bitmasks.

    Args:
        items: sequence of items

    Returns:
        List of subsets
    """
    subsets: List[List[str]] = []
    n = len(items)

    for mask in range(1 << n):
        subsets.append(mask_to_subset(items, mask))

    return subsets


def generate_subsets_with_masks(items: Sequence[str]) -> List[Tuple[int, List[str]]]:
    """
    Generate all subsets together with their masks.

    Args:
        items: sequence of items

    Returns:
        List of (mask, subset)
    """
    result: List[Tuple[int, List[str]]] = []
    n = len(items)

    for mask in range(1 << n):
        result.append((mask, mask_to_subset(items, mask)))

    return result


def generate_submasks(mask: int) -> List[int]:
    """
    Generate all submasks of a mask in descending order.

    Classic trick:
        sub = mask
        while sub:
            ...
            sub = (sub - 1) & mask

    Includes 0 at the end.

    Args:
        mask: non-negative integer mask

    Returns:
        List of all submasks in descending order
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")

    submasks: List[int] = []
    sub = mask

    while True:
        submasks.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask

    return submasks


def generate_subsets_of_size(items: Sequence[str], k: int) -> List[List[str]]:
    """
    Generate all subsets of exactly size k.

    Args:
        items: sequence of items
        k: desired subset size

    Returns:
        List of subsets whose size is exactly k
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    subsets: List[List[str]] = []
    n = len(items)

    for mask in range(1 << n):
        if mask.bit_count() == k:
            subsets.append(mask_to_subset(items, mask))

    return subsets


def is_subset(submask: int, mask: int) -> bool:
    """
    Check whether 'submask' is a subset of 'mask'.

    In bit terms:
        every 1 bit in submask must also be 1 in mask
    """
    if submask < 0 or mask < 0:
        raise ValueError("masks must be non-negative")

    return (submask & mask) == submask


def union_masks(mask1: int, mask2: int) -> int:
    """
    Return the union of two masks.
    """
    if mask1 < 0 or mask2 < 0:
        raise ValueError("masks must be non-negative")

    return mask1 | mask2


def intersection_masks(mask1: int, mask2: int) -> int:
    """
    Return the intersection of two masks.
    """
    if mask1 < 0 or mask2 < 0:
        raise ValueError("masks must be non-negative")

    return mask1 & mask2


def difference_masks(mask1: int, mask2: int) -> int:
    """
    Return elements in mask1 but not in mask2.
    """
    if mask1 < 0 or mask2 < 0:
        raise ValueError("masks must be non-negative")

    return mask1 & ~mask2


def explain_subset_generation(items: Sequence[str]) -> None:
    """
    Print all subsets of the given items together with masks.
    """
    n = len(items)

    print("\nSubset Generation Demo")
    print("=" * 70)
    print(f"items = {list(items)}")
    print("-" * 70)

    for mask in range(1 << n):
        binary = mask_to_binary(mask, n)
        subset = mask_to_subset(items, mask)
        print(f"mask={mask:>2}  bits={binary}  subset={subset}")


def explain_submasks(mask: int, width: int = 0) -> None:
    """
    Print all submasks of a given mask.
    """
    if mask < 0:
        raise ValueError("mask must be non-negative")

    if width == 0:
        width = max(1, mask.bit_length())

    print("\nSubmask Generation Demo")
    print("=" * 70)
    print(f"mask = {mask} ({mask_to_binary(mask, width)})")
    print("-" * 70)

    for sub in generate_submasks(mask):
        print(f"submask={sub:>2}  bits={mask_to_binary(sub, width)}")


if __name__ == "__main__":
    items = ["A", "B", "C"]

    explain_subset_generation(items)

    print("\nBasic mask helpers")
    print("=" * 70)
    mask = subset_to_mask([0, 2])
    print(f"subset_to_mask([0, 2]) -> {mask}")
    print(f"mask_to_indices({mask}) -> {mask_to_indices(mask)}")
    print(f"mask_to_subset({items}, {mask}) -> {mask_to_subset(items, mask)}")

    print("\nMask updates")
    print("=" * 70)
    print(f"start mask                -> {mask} ({mask_to_binary(mask, len(items))})")
    print(f"add index 1               -> {add_element_to_mask(mask, 1)}")
    print(f"remove index 2            -> {remove_element_from_mask(mask, 2)}")
    print(f"toggle index 0            -> {toggle_element_in_mask(mask, 0)}")
    print(f"is element 2 in mask?     -> {is_element_in_mask(mask, 2)}")
    print(f"is element 1 in mask?     -> {is_element_in_mask(mask, 1)}")

    print("\nSet relations")
    print("=" * 70)
    mask1 = subset_to_mask([0, 1])
    mask2 = subset_to_mask([1, 2])
    print(f"mask1                     -> {mask1} ({mask_to_binary(mask1, 3)})")
    print(f"mask2                     -> {mask2} ({mask_to_binary(mask2, 3)})")
    print(f"union                     -> {union_masks(mask1, mask2)}")
    print(f"intersection              -> {intersection_masks(mask1, mask2)}")
    print(f"difference mask1 - mask2  -> {difference_masks(mask1, mask2)}")
    print(f"is_subset(mask1, union)?  -> {is_subset(mask1, union_masks(mask1, mask2))}")

    print("\nSubsets of fixed size")
    print("=" * 70)
    print(f"subsets of size 2 -> {generate_subsets_of_size(items, 2)}")

    explain_submasks(subset_to_mask([0, 2, 3]), width=4)
