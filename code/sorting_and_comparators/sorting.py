"""Sorting in Python: the ``key=`` function, tuple keys, and ``cmp_to_key``.

Python's ``sorted`` (and ``list.sort``) is a stable Timsort. You almost never write a
comparator, you give a ``key`` function that maps each element to something orderable. The one
case where you fall back to a real comparator (via ``functools.cmp_to_key``) is when "which of
two comes first" can't be expressed as an independent key, the ``largest_number`` problem
below is the classic example.
"""

from __future__ import annotations

from functools import cmp_to_key


def by_length(words: list[str]) -> list[str]:
    """Sort strings by length, shortest first (``key=len``)."""
    return sorted(words, key=len)


def by_last_then_first(names: list[str]) -> list[str]:
    """Sort ``"First Last"`` names by last name, then first, a **tuple key**.

    Returning a tuple from the key sorts by the first element, breaking ties on the second, and
    so on. This is how you do multi-level sorts without any comparator.
    """
    return sorted(names, key=lambda full: (full.split()[-1], full.split()[0]))


def by_score_desc_then_name(players: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort ``(name, score)`` by score **descending**, then name ascending.

    Mixed directions: negate the numeric field in the key to reverse just that field while
    keeping the string field ascending.
    """
    return sorted(players, key=lambda p: (-p[1], p[0]))


def largest_number(nums: list[int]) -> str:
    """Arrange the numbers to form the largest possible concatenated number.

    For ``[3, 30, 34, 5, 9]`` the answer is ``"9534330"``. The ordering rule, ``a`` should come
    before ``b`` when ``a+b > b+a`` as strings, is *pairwise* and not a per-element key, so this
    is the textbook ``cmp_to_key`` case.
    """
    if not nums:
        return "0"

    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1  # a should come first
        if a + b < b + a:
            return 1
        return 0

    ordered = sorted((str(n) for n in nums), key=cmp_to_key(compare))
    result = "".join(ordered)
    # Normalise "000" -> "0".
    return "0" if result[0] == "0" else result
