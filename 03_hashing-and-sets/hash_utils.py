"""
Hashing & Sets — core utilities (Part 1/4)

This first file focuses on the "everyday" hash-table patterns you'll use constantly:
- frequency counting (Counter-style) without relying on collections.Counter
- set operations (union/intersection/difference) with clear APIs
- membership tricks (dedupe, contains-any/all)

Next files will build:
2) a simple open-addressing HashSet implementation
3) classic hash-map algorithm patterns (two-sum, group anagrams, longest consecutive)
4) tests for everything

All functions are standard-library-only and written for clarity + correctness.
"""

from __future__ import annotations

from typing import Dict, Hashable, Iterable, Iterator, List, Sequence, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


# ----------------------------
# Frequency counting
# ----------------------------

def freq_map(items: Iterable[T]) -> Dict[T, int]:
    """
    Return a frequency map: item -> count.

    Example:
        freq_map("banana") -> {'b':1, 'a':3, 'n':2}
    """
    counts: Dict[T, int] = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return counts


def most_common(items: Iterable[T]) -> Tuple[T, int]:
    """
    Return (item, count) with the maximum frequency.
    Raises ValueError on empty input.

    If multiple items tie, returns one of them (deterministic by iteration order
    of the dict in modern Python).
    """
    counts = freq_map(items)
    if not counts:
        raise ValueError("most_common() arg is an empty iterable")

    best_item: T
    best_count = -1
    for k, v in counts.items():
        if v > best_count:
            best_item = k
            best_count = v
    return best_item, best_count  # type: ignore[name-defined]


def first_unique(items: Sequence[T]) -> int:
    """
    Return the index of the first element that appears exactly once, else -1.

    Example:
        first_unique(list("leetcode")) -> 0
        first_unique(list("aabb")) -> -1
    """
    counts = freq_map(items)
    for i, x in enumerate(items):
        if counts.get(x, 0) == 1:
            return i
    return -1


# ----------------------------
# Set operations (functional style)
# ----------------------------

def set_union(a: Iterable[T], b: Iterable[T]) -> Set[T]:
    """Return the union of a and b as a new set."""
    s: Set[T] = set()
    for x in a:
        s.add(x)
    for x in b:
        s.add(x)
    return s


def set_intersection(a: Iterable[T], b: Iterable[T]) -> Set[T]:
    """Return the intersection of a and b as a new set."""
    sb = set(b)
    out: Set[T] = set()
    for x in a:
        if x in sb:
            out.add(x)
    return out


def set_difference(a: Iterable[T], b: Iterable[T]) -> Set[T]:
    """Return a \\ b as a new set."""
    sb = set(b)
    out: Set[T] = set()
    for x in a:
        if x not in sb:
            out.add(x)
    return out


def is_subset(a: Iterable[T], b: Iterable[T]) -> bool:
    """
    Return True if every element of a is contained in b.
    """
    sb = set(b)
    for x in a:
        if x not in sb:
            return False
    return True


# ----------------------------
# Membership tricks / patterns
# ----------------------------

def dedupe_preserve_order(items: Iterable[T]) -> List[T]:
    """
    Deduplicate while preserving first-seen order.

    Example:
        dedupe_preserve_order([3,1,3,2,1]) -> [3,1,2]
    """
    seen: Set[T] = set()
    out: List[T] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def contains_any(haystack: Iterable[T], needles: Iterable[T]) -> bool:
    """
    Return True if haystack contains at least one element from needles.
    """
    hs = set(haystack)
    for n in needles:
        if n in hs:
            return True
    return False


def contains_all(haystack: Iterable[T], needles: Iterable[T]) -> bool:
    """
    Return True if haystack contains every element from needles.
    """
    hs = set(haystack)
    for n in needles:
        if n not in hs:
            return False
    return True


if __name__ == "__main__":
    print(freq_map("banana"))
    print(most_common("banana"))
    print(first_unique(list("loveleetcode")))

    a = [1, 2, 3]
    b = [3, 4]
    print("union:", set_union(a, b))
    print("intersection:", set_intersection(a, b))
    print("difference:", set_difference(a, b))

    print(dedupe_preserve_order([3, 1, 3, 2, 1]))
    print(contains_any([1, 2, 3], [0, 2]))
    print(contains_all([1, 2, 3], [2, 3]))
