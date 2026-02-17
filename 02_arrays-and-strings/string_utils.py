"""
String utilities + interview-style primitives.

Includes:
- is_palindrome (ignores non-alnum, case-insensitive by default)
- are_anagrams (optionally ignores non-alnum and case)
- longest_common_prefix
- reverse_words (reverse word order, normalize whitespace by default)
- run_length_encode (simple compression like "aaabb" -> "a3b2")
- first_unique_char_index (index of first non-repeating char)

All functions are pure (no mutation), easy to test, and have clear edge-case rules.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Optional


def _normalize_chars(
        s: str,
        *,
        case_insensitive: bool,
        alnum_only: bool,
) -> str:
    if case_insensitive:
        s = s.lower()
    if alnum_only:
        s = "".join(ch for ch in s if ch.isalnum())
    return s


def is_palindrome(
        s: str,
        *,
        case_insensitive: bool = True,
        alnum_only: bool = True,
) -> bool:
    """
    Return True if s is a palindrome under the chosen normalization.

    Default behavior matches common interview interpretation:
    - ignore case
    - ignore non-alphanumeric characters

    Examples:
      "Racecar" -> True
      "A man, a plan, a canal: Panama" -> True
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    t = _normalize_chars(s, case_insensitive=case_insensitive, alnum_only=alnum_only)
    # Two-pointer without allocating reverse copy (still O(n), but shows the pattern)
    i, j = 0, len(t) - 1
    while i < j:
        if t[i] != t[j]:
            return False
        i += 1
        j -= 1
    return True


def are_anagrams(
        a: str,
        b: str,
        *,
        case_insensitive: bool = True,
        alnum_only: bool = True,
) -> bool:
    """
    Return True if a and b are anagrams under the chosen normalization.

    Default:
    - ignore case
    - ignore non-alphanumeric characters

    Examples:
      "listen", "silent" -> True
      "Dormitory", "Dirty room!!" -> True
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be str")

    na = _normalize_chars(a, case_insensitive=case_insensitive, alnum_only=alnum_only)
    nb = _normalize_chars(b, case_insensitive=case_insensitive, alnum_only=alnum_only)
    return Counter(na) == Counter(nb)


def longest_common_prefix(strings: Iterable[str]) -> str:
    """
    Return the longest common prefix among the given strings.

    Rules:
    - If iterable is empty -> ""
    - If any element is "" -> ""
    - Works in O(total length) by scanning char-by-char on the shortest string.
    """
    strs = list(strings)
    if not strs:
        return ""
    for s in strs:
        if not isinstance(s, str):
            raise TypeError("All items must be str")

    shortest = min(strs, key=len)
    if shortest == "":
        return ""

    end = 0
    for i in range(len(shortest)):
        ch = shortest[i]
        if all(s[i] == ch for s in strs):
            end = i + 1
        else:
            break
    return shortest[:end]


def reverse_words(s: str, *, normalize_whitespace: bool = True) -> str:
    """
    Reverse the order of words in a string.

    Default:
    - normalize whitespace (like many interview problems): collapse runs of whitespace
      and strip ends.

    Examples:
      "  the   sky  is blue " -> "blue is sky the"
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    if normalize_whitespace:
        words = s.split()  # splits on any whitespace and discards empties
        return " ".join(reversed(words))
    else:
        # Keep exact whitespace? That requires more complex tokenization.
        # Here we interpret "words" as split on spaces only, preserving empties.
        parts = s.split(" ")
        parts.reverse()
        return " ".join(parts)


def run_length_encode(s: str) -> str:
    """
    Simple run-length encoding.
    - Encodes consecutive runs as <char><count> when count > 1
    - Single chars are left as just <char>

    Examples:
      "" -> ""
      "aaabbc" -> "a3b2c"
      "abcd" -> "abcd"
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    if not s:
        return ""

    out: list[str] = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append(prev if count == 1 else f"{prev}{count}")
            prev = ch
            count = 1
    out.append(prev if count == 1 else f"{prev}{count}")
    return "".join(out)


def first_unique_char_index(s: str) -> int:
    """
    Return index of the first non-repeating character in s, or -1 if none.

    Example:
      "leetcode" -> 0 (l)
      "loveleetcode" -> 2 (v)
      "aabb" -> -1
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))
    print(are_anagrams("Dormitory", "Dirty room!!"))
    print(longest_common_prefix(["flower", "flow", "flight"]))
    print(reverse_words("  the   sky  is blue "))
    print(run_length_encode("aaabbc"))
    print(first_unique_char_index("loveleetcode"))
