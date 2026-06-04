"""Longest Substring Without Repeating Characters (flexible-longest sliding window).

Grow the window to the right; when the entering character is already inside the window, jump
``left`` to just past its previous position so the window is valid (all-unique) again. Track
the largest width seen. O(n) with a dict of last-seen indices.
"""

from __future__ import annotations


def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
