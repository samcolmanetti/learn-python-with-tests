"""Binary search — the *predicate* template.

The most reusable form of binary search is not "find a value in a sorted array". It is:

    given a boolean predicate that is False, False, ..., False, True, True, ..., True
    over a range, find the index of the FIRST True.

Almost every binary search problem (find target, find insertion point, "minimum capacity
such that ...", sqrt, rotated array) can be expressed as "find the first index where some
feasibility test flips to True". Get comfortable writing `feasible(mid)` and the rest is
boilerplate.

This is a directional template — adapt `feasible` per problem.
"""

from __future__ import annotations

from typing import Callable


def find_first_true(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Return the smallest ``x`` in ``[lo, hi]`` with ``feasible(x)`` True.

    Assumes ``feasible`` is monotonic: once it becomes True it stays True. Returns ``hi + 1``
    if it is never True (the conventional "not found / past the end" sentinel).
    """
    first_true = hi + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            first_true = mid
            hi = mid - 1  # look for an even earlier True
        else:
            lo = mid + 1  # True (if any) is to the right
    return first_true


def binary_search(arr: list[int], target: int) -> int:
    """Classic "find the index of ``target``" expressed via the predicate template.

    Returns the index of ``target`` or ``-1`` if absent.
    """
    idx = find_first_true(0, len(arr) - 1, lambda i: arr[i] >= target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1
