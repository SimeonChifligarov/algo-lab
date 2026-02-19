"""
Hashing & Sets — simple HashSet implementation (Part 2/4)

Goal:
Understand collisions by implementing a *tiny* open-addressing hash set.

Implementation notes:
- Open addressing with linear probing.
- Special sentinels for EMPTY and DELETED slots.
- Resizes when load factor (including tombstones) gets too high.
- Supports: add, remove, contains, len, iteration.

This is for learning, not for production use.
Python's built-in set is vastly more optimized and robust.

Key ideas you’ll see:
- hash(key) gives an integer; we map it to an index with modulo.
- collisions handled by probing: i, i+1, i+2, ...
- deletions leave tombstones to keep probe chains intact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class _Empty:
    __slots__ = ()

    def __repr__(self) -> str:
        return "EMPTY"


class _Deleted:
    __slots__ = ()

    def __repr__(self) -> str:
        return "DELETED"


EMPTY = _Empty()
DELETED = _Deleted()


def _is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0


@dataclass
class _FindResult:
    found: bool
    index: int  # index of existing key (if found) or best insert position (if not)


class OpenAddressingHashSet(Generic[T]):
    """
    Educational open-addressing hash set (linear probing).

    Typical usage:
        s = OpenAddressingHashSet()
        s.add("a")
        s.add("b")
        assert "a" in s
        s.remove("a")
    """

    def __init__(self, initial_capacity: int = 8):
        if initial_capacity < 4:
            initial_capacity = 4
        # power-of-two capacity makes modulo faster in many languages;
        # in Python it's mostly stylistic, but we keep it.
        cap = 1
        while cap < initial_capacity:
            cap <<= 1
        self._table: List[object] = [EMPTY] * cap
        self._size = 0
        self._tombstones = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: T) -> bool:
        return self._find_slot(key).found

    def __iter__(self) -> Iterator[T]:
        for slot in self._table:
            if slot is EMPTY or slot is DELETED:
                continue
            yield slot  # type: ignore[misc]

    def __repr__(self) -> str:
        return f"OpenAddressingHashSet({list(self)!r})"

    # ----------------------------
    # Public API
    # ----------------------------

    def add(self, key: T) -> bool:
        """
        Add key to the set.
        Returns True if inserted, False if it was already present.
        """
        self._maybe_resize_for_insert()
        res = self._find_slot(key)
        if res.found:
            return False

        # Insert into either EMPTY or DELETED slot.
        if self._table[res.index] is DELETED:
            self._tombstones -= 1
        self._table[res.index] = key
        self._size += 1
        return True

    def remove(self, key: T) -> bool:
        """
        Remove key from the set.
        Returns True if removed, False if key not present.
        """
        res = self._find_slot(key)
        if not res.found:
            return False

        # Mark as DELETED to preserve probe chains.
        self._table[res.index] = DELETED
        self._size -= 1
        self._tombstones += 1

        # Optional: if lots of tombstones, rebuild.
        self._maybe_rehash_due_to_tombstones()
        return True

    def clear(self) -> None:
        self._table = [EMPTY] * len(self._table)
        self._size = 0
        self._tombstones = 0

    # ----------------------------
    # Internals
    # ----------------------------

    def _find_slot(self, key: T) -> _FindResult:
        """
        Find key in table using linear probing.

        If found: returns (found=True, index=slot_index)
        If not found: returns (found=False, index=best_insert_index),
          where best_insert_index is the first DELETED encountered, else first EMPTY.
        """
        table = self._table
        n = len(table)
        h = hash(key) & 0x7FFFFFFF  # make non-negative for nicer indexing
        idx = h % n

        first_deleted: Optional[int] = None

        while True:
            slot = table[idx]
            if slot is EMPTY:
                return _FindResult(found=False, index=first_deleted if first_deleted is not None else idx)
            if slot is DELETED:
                if first_deleted is None:
                    first_deleted = idx
            else:
                # real key
                if slot == key:
                    return _FindResult(found=True, index=idx)

            idx = (idx + 1) % n

    def _load_factor(self) -> float:
        # Count both live entries and tombstones as "occupied" for probing cost.
        return (self._size + self._tombstones) / len(self._table)

    def _maybe_resize_for_insert(self) -> None:
        # Keep probing fast by resizing around ~0.7 occupancy (incl tombstones).
        if self._load_factor() >= 0.70:
            self._resize(len(self._table) * 2)

    def _maybe_rehash_due_to_tombstones(self) -> None:
        # If tombstones dominate, rehash to clean them up.
        # Threshold chosen for simplicity.
        if self._tombstones > self._size and len(self._table) > 8:
            self._resize(len(self._table))  # same size, just rebuild

    def _resize(self, new_capacity: int) -> None:
        # Ensure power of two.
        cap = 1
        while cap < new_capacity:
            cap <<= 1

        old_items = list(self)
        self._table = [EMPTY] * cap
        self._size = 0
        self._tombstones = 0

        for x in old_items:
            # Direct insert without repeated resizes
            res = self._find_slot(x)
            self._table[res.index] = x
            self._size += 1

    # Convenience method for teaching/debugging
    def debug_table(self) -> List[object]:
        """Return a shallow copy of the underlying table (shows EMPTY/DELETED)."""
        return list(self._table)


if __name__ == "__main__":
    s = OpenAddressingHashSet[int]()
    for x in [5, 12, 5, 7, 12, 9]:
        print("add", x, "->", s.add(x), s)

    print("contains 7?", 7 in s)
    print("contains 6?", 6 in s)

    print("remove 12 ->", s.remove(12), s)
    print("remove 12 ->", s.remove(12), s)

    print("table:", s.debug_table())
