"""Valid Palindrome (opposite-direction two pointers).

Given a string, return True if it reads the same forwards and backwards considering only
alphanumeric characters and ignoring case. Classic opposite-direction two pointers: compare the
ends, skip anything that isn't alphanumeric, walk inward.
"""

from __future__ import annotations


def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
