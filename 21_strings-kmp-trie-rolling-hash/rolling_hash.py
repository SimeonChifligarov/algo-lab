"""
Rolling Hash / Rabin-Karp

This module implements polynomial rolling hash techniques for string matching.

What this file covers:
    - prefix hash construction
    - O(1) substring hash queries after preprocessing
    - Rabin-Karp pattern search
    - duplicate substring utilities
    - longest common prefix by hashing

Why rolling hash?
    It lets us compare substrings efficiently by converting them into numbers.
    With prefix hashes and powers precomputed, substring hashes can be extracted
    in constant time.

Important note:
    Hashes can collide. In practice, good parameters make collisions rare.
    For stronger safety, this file uses double hashing.
"""

from typing import List, Tuple


class RollingHash:
    """
    Double rolling hash for a string.

    Uses two moduli to reduce collision risk.
    Supports O(1) substring hash extraction after O(n) preprocessing.
    """

    _BASE = 911382323
    _MOD1 = 1_000_000_007
    _MOD2 = 1_000_000_009

    def __init__(self, s: str) -> None:
        self.s = s
        self.n = len(s)

        self.pow1 = [1] * (self.n + 1)
        self.pow2 = [1] * (self.n + 1)

        self.pref1 = [0] * (self.n + 1)
        self.pref2 = [0] * (self.n + 1)

        for i, ch in enumerate(s):
            value = ord(ch)

            self.pow1[i + 1] = (self.pow1[i] * self._BASE) % self._MOD1
            self.pow2[i + 1] = (self.pow2[i] * self._BASE) % self._MOD2

            self.pref1[i + 1] = (self.pref1[i] * self._BASE + value) % self._MOD1
            self.pref2[i + 1] = (self.pref2[i] * self._BASE + value) % self._MOD2

    def __len__(self) -> int:
        return self.n

    def hash_substring(self, left: int, right: int) -> Tuple[int, int]:
        """
        Return the double hash of s[left:right].

        Args:
            left: inclusive start index
            right: exclusive end index

        Returns:
            Tuple[int, int]: pair of hash values

        Raises:
            ValueError: if indices are invalid
        """
        if not (0 <= left <= right <= self.n):
            raise ValueError(f"Invalid substring range [{left}, {right})")

        hash1 = (
                        self.pref1[right]
                        - self.pref1[left] * self.pow1[right - left]
                ) % self._MOD1

        hash2 = (
                        self.pref2[right]
                        - self.pref2[left] * self.pow2[right - left]
                ) % self._MOD2

        return hash1, hash2

    def full_hash(self) -> Tuple[int, int]:
        """
        Return the hash of the entire string.
        """
        return self.hash_substring(0, self.n)

    def compare_substrings(
            self,
            left1: int,
            right1: int,
            left2: int,
            right2: int,
    ) -> bool:
        """
        Compare s[left1:right1] and s[left2:right2] using hashes.
        """
        if right1 - left1 != right2 - left2:
            return False
        return self.hash_substring(left1, right1) == self.hash_substring(left2, right2)

    def longest_common_prefix(self, i: int, j: int) -> int:
        """
        Return the length of the longest common prefix of s[i:] and s[j:].

        Uses binary search on substring hashes.

        Args:
            i: start index of first suffix
            j: start index of second suffix

        Returns:
            Length of common prefix
        """
        if not (0 <= i <= self.n and 0 <= j <= self.n):
            raise ValueError("Indices out of range")

        low = 0
        high = min(self.n - i, self.n - j)

        while low < high:
            mid = (low + high + 1) // 2
            if self.hash_substring(i, i + mid) == self.hash_substring(j, j + mid):
                low = mid
            else:
                high = mid - 1

        return low


def rabin_karp_search(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of pattern in text using rolling hash.

    Args:
        text: text to search in
        pattern: pattern to search for

    Returns:
        List[int]: starting indices of all matches

    Notes:
        - Uses hash comparison first, then verifies by direct string comparison
          to eliminate any collision risk.
        - If pattern is empty, returns all insertion positions.
    """
    n = len(text)
    m = len(pattern)

    if pattern == "":
        return list(range(n + 1))

    if m > n:
        return []

    text_hash = RollingHash(text)
    pattern_hash = RollingHash(pattern).full_hash()

    matches: List[int] = []

    for i in range(n - m + 1):
        if text_hash.hash_substring(i, i + m) == pattern_hash:
            if text[i:i + m] == pattern:
                matches.append(i)

    return matches


def contains_pattern_hash(text: str, pattern: str) -> bool:
    """
    Return True if pattern appears in text.
    """
    return len(rabin_karp_search(text, pattern)) > 0


def count_occurrences_hash(text: str, pattern: str) -> int:
    """
    Count occurrences of pattern in text.
    """
    return len(rabin_karp_search(text, pattern))


def find_duplicate_substrings(s: str, length: int) -> List[str]:
    """
    Find distinct duplicate substrings of a given fixed length.

    Args:
        s: input string
        length: substring length

    Returns:
        Sorted list of distinct substrings that appear at least twice.

    Notes:
        - Uses hashes to group candidates.
        - Confirms duplicates with actual substring values.
    """
    n = len(s)

    if length <= 0 or length > n:
        return []

    rh = RollingHash(s)
    seen = {}
    duplicates = set()

    for i in range(n - length + 1):
        h = rh.hash_substring(i, i + length)
        substring = s[i:i + length]

        if h in seen:
            if substring in seen[h]:
                duplicates.add(substring)
            else:
                seen[h].add(substring)
        else:
            seen[h] = {substring}

    return sorted(duplicates)


def longest_repeated_substring(s: str) -> str:
    """
    Return one longest repeated substring in s.

    Uses binary search on substring length and rolling hashes.

    Args:
        s: input string

    Returns:
        One longest repeated substring, or "" if none exists.
    """
    n = len(s)
    if n == 0:
        return ""

    rh = RollingHash(s)

    def has_duplicate_of_length(length: int) -> str:
        seen = {}

        for i in range(n - length + 1):
            h = rh.hash_substring(i, i + length)
            substring = s[i:i + length]

            if h in seen:
                if substring in seen[h]:
                    return substring
                seen[h].add(substring)
            else:
                seen[h] = {substring}

        return ""

    low = 0
    high = n
    answer = ""

    while low <= high:
        mid = (low + high) // 2
        candidate = has_duplicate_of_length(mid)

        if candidate:
            answer = candidate
            low = mid + 1
        else:
            high = mid - 1

    return answer


def group_identical_substrings(s: str, length: int) -> List[List[Tuple[int, str]]]:
    """
    Group equal substrings of fixed length.

    Args:
        s: input string
        length: substring length

    Returns:
        A list of groups. Each group is a list of (start_index, substring).
        Only groups with at least two equal substrings are returned.
    """
    n = len(s)
    if length <= 0 or length > n:
        return []

    rh = RollingHash(s)
    buckets = {}

    for i in range(n - length + 1):
        substring = s[i:i + length]
        h = rh.hash_substring(i, i + length)
        buckets.setdefault(h, {}).setdefault(substring, []).append((i, substring))

    groups: List[List[Tuple[int, str]]] = []

    for variants in buckets.values():
        for positions in variants.values():
            if len(positions) >= 2:
                groups.append(positions)

    groups.sort(key=lambda group: (group[0][1], group[0][0]))
    return groups


def explain_rabin_karp(text: str, pattern: str) -> None:
    """
    Print a learning-oriented explanation of Rabin-Karp matching.
    """
    print("\nRabin-Karp Explanation")
    print("=" * 70)
    print(f"Text   : {text}")
    print(f"Pattern: {pattern}")

    if pattern == "":
        print("Empty pattern matches at every position.")
        print(list(range(len(text) + 1)))
        return

    n = len(text)
    m = len(pattern)

    if m > n:
        print("Pattern is longer than text, so there are no matches.")
        return

    text_hash = RollingHash(text)
    pattern_hash = RollingHash(pattern).full_hash()

    print(f"Pattern hash: {pattern_hash}")
    print("-" * 70)

    matches = []

    for i in range(n - m + 1):
        window = text[i:i + m]
        window_hash = text_hash.hash_substring(i, i + m)
        same_hash = window_hash == pattern_hash

        print(
            f"Window [{i}:{i + m}] -> '{window}' | "
            f"hash={window_hash} | hash_match={same_hash}"
        )

        if same_hash:
            if window == pattern:
                print("  verified exact match")
                matches.append(i)
            else:
                print("  hash collision avoided by direct verification")

    print("-" * 70)
    print(f"Matches: {matches}")


def demo_substring_hash_queries(s: str, queries: List[Tuple[int, int]]) -> None:
    """
    Demonstrate substring hash extraction for several ranges.
    """
    rh = RollingHash(s)

    print("\nSubstring Hash Demo")
    print("=" * 70)
    print(f"String: {s}")

    for left, right in queries:
        substring = s[left:right]
        h = rh.hash_substring(left, right)
        print(f"s[{left}:{right}] = '{substring}' -> hash = {h}")


if __name__ == "__main__":
    text = "abracadabra abracadabra"
    pattern = "abra"

    print("Rolling Hash / Rabin-Karp Demo")
    print("=" * 70)
    print(f"Text   : {text}")
    print(f"Pattern: {pattern}")
    print(f"Matches: {rabin_karp_search(text, pattern)}")
    print(f"Contains pattern: {contains_pattern_hash(text, pattern)}")
    print(f"Count occurrences: {count_occurrences_hash(text, pattern)}")

    explain_rabin_karp(text, pattern)

    sample = "banana"
    rh = RollingHash(sample)

    print("\nSingle-string rolling hash demo")
    print("=" * 70)
    print(f"String: {sample}")
    print(f"Full hash: {rh.full_hash()}")
    print(f"Hash of 'ana' at [1:4]: {rh.hash_substring(1, 4)}")
    print(f"Hash of 'ana' at [3:6]: {rh.hash_substring(3, 6)}")
    print(f"Equal substrings? {rh.compare_substrings(1, 4, 3, 6)}")
    print(f"LCP of suffixes at 1 and 3: {rh.longest_common_prefix(1, 3)}")

    demo_substring_hash_queries(
        "mississippi",
        [(0, 4), (1, 5), (4, 7), (7, 11)],
    )

    print("\nDuplicate substring utilities")
    print("=" * 70)
    print(f"Duplicate substrings of length 2 in 'banana': {find_duplicate_substrings('banana', 2)}")
    print(f"Duplicate substrings of length 3 in 'banana': {find_duplicate_substrings('banana', 3)}")
    print(f"Longest repeated substring in 'banana': {longest_repeated_substring('banana')}")
    print(f"Grouped identical substrings of length 3 in 'banana': {group_identical_substrings('banana', 3)}")
