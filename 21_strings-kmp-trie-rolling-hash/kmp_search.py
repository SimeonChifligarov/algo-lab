"""
KMP (Knuth-Morris-Pratt) Pattern Matching

This module implements KMP string matching using the prefix function / LPS array.

Why KMP?
    A naive pattern search may re-check many characters after a mismatch.
    KMP avoids that by using information about the pattern itself.

Core idea:
    When a mismatch happens after some matched characters, we do not restart
    from scratch. Instead, we use the LPS array to determine how much of the
    previous work can still be reused.

This gives:
    - O(n + m) time complexity
    - O(m) extra space

Where:
    n = len(text)
    m = len(pattern)
"""

from typing import List


def prefix_function(s: str) -> List[int]:
    """
    Compute the prefix function (LPS array) for a string.

    Args:
        s: Input string

    Returns:
        List[int]: pi array where pi[i] is the length of the longest proper
        prefix of s[:i+1] that is also a suffix of s[:i+1].
    """
    n = len(s)
    pi = [0] * n

    for i in range(1, n):
        j = pi[i - 1]

        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1

        pi[i] = j

    return pi


def build_lps(pattern: str) -> List[int]:
    """
    Build the LPS array for a pattern.

    Args:
        pattern: Pattern string

    Returns:
        List[int]: LPS array
    """
    return prefix_function(pattern)


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of pattern in text using KMP.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        List[int]: Starting indices of all matches in text

    Notes:
        - If pattern is empty, returns all valid insertion positions:
          [0, 1, 2, ..., len(text)]
    """
    if pattern == "":
        return list(range(len(text) + 1))

    lps = build_lps(pattern)
    matches: List[int] = []

    j = 0  # index in pattern

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            matches.append(i - len(pattern) + 1)
            j = lps[j - 1]

    return matches


def contains_pattern(text: str, pattern: str) -> bool:
    """
    Check whether pattern appears in text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        bool: True if at least one occurrence exists, False otherwise
    """
    return len(kmp_search(text, pattern)) > 0


def first_occurrence(text: str, pattern: str) -> int:
    """
    Return the first index where pattern appears in text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        int: First match index, or -1 if not found

    Notes:
        - If pattern is empty, returns 0
    """
    matches = kmp_search(text, pattern)
    return matches[0] if matches else -1


def count_occurrences(text: str, pattern: str) -> int:
    """
    Count how many times pattern appears in text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        int: Number of occurrences
    """
    return len(kmp_search(text, pattern))


def explain_kmp_search(text: str, pattern: str) -> None:
    """
    Print a readable summary of the KMP search process.

    This is meant for learning and debugging, not for high-performance use.
    """
    print("\nKMP SEARCH EXPLANATION")
    print("-" * 60)
    print(f"Text   : {text}")
    print(f"Pattern: {pattern}")

    if pattern == "":
        print("\nEmpty pattern matches at every position.")
        print(f"Matches: {list(range(len(text) + 1))}")
        return

    lps = build_lps(pattern)
    print(f"LPS    : {lps}")
    print("-" * 60)

    j = 0
    matches: List[int] = []

    for i in range(len(text)):
        print(f"\nText index i={i}, text[i]='{text[i]}'")

        while j > 0 and text[i] != pattern[j]:
            print(
                f"  mismatch: text[i]='{text[i]}' != pattern[j]='{pattern[j]}'"
            )
            print(f"  fallback: j -> lps[{j - 1}] = {lps[j - 1]}")
            j = lps[j - 1]

        if text[i] == pattern[j]:
            print(f"  match: text[i]='{text[i]}' == pattern[j]='{pattern[j]}'")
            j += 1
            print(f"  advance pattern pointer: j = {j}")
        else:
            print("  no partial match, stay at j = 0")

        if j == len(pattern):
            start_index = i - len(pattern) + 1
            matches.append(start_index)
            print(f"  full match found at index {start_index}")
            j = lps[j - 1]
            print(f"  continue search with fallback j = {j}")

    print("\n" + "-" * 60)
    print(f"All matches: {matches}")


def print_match_context(text: str, pattern: str, window: int = 8) -> None:
    """
    Print each match with some surrounding context.

    Args:
        text: The text to search in
        pattern: The pattern to search for
        window: Number of characters of context before and after the match
    """
    matches = kmp_search(text, pattern)

    print("\nMATCH CONTEXT")
    print("-" * 60)

    if not matches:
        print("No matches found.")
        return

    for idx, start in enumerate(matches, start=1):
        end = start + len(pattern)
        left = max(0, start - window)
        right = min(len(text), end + window)

        prefix = text[left:start]
        middle = text[start:end]
        suffix = text[end:right]

        print(f"{idx}. index={start}")
        print(f"   ...{prefix}[{middle}]{suffix}...")


if __name__ == "__main__":
    text = "ababcabcabababdabababd"
    pattern = "ababd"

    print("KMP Pattern Matching Demo")
    print("=" * 60)
    print(f"Text           : {text}")
    print(f"Pattern        : {pattern}")
    print(f"LPS            : {build_lps(pattern)}")
    print(f"All matches    : {kmp_search(text, pattern)}")
    print(f"First match    : {first_occurrence(text, pattern)}")
    print(f"Contains       : {contains_pattern(text, pattern)}")
    print(f"Count          : {count_occurrences(text, pattern)}")

    print_match_context(text, pattern)
    explain_kmp_search("aaabaaabaaaab", "aaab")
