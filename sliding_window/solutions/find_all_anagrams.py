"""Find All Anagrams in a String (fixed-size sliding window of character counts).

Return the start indices of every substring of ``s`` that is an anagram of ``p``. Keep a
fixed-width window of size ``len(p)`` and compare its character-count ``Counter`` against
``p``'s. Maintaining the counts incrementally keeps each slide O(1) (over the fixed alphabet).
"""

from __future__ import annotations

from collections import Counter


def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    need = Counter(p)
    window = Counter(s[: len(p)])
    result = []

    if window == need:
        result.append(0)

    for right in range(len(p), len(s)):
        window[s[right]] += 1  # element entering on the right
        left_char = s[right - len(p)]  # element leaving on the left
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]  # keep Counters comparable (no zero entries)
        if window == need:
            result.append(right - len(p) + 1)

    return result
