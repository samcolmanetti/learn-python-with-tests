"""Sliding Window, fixed, longest-flexible, and shortest-flexible templates.

A sliding window maintains a contiguous range ``[left, right]`` and slides it across the
input, adding the entering element and removing the leaving one so each element is touched
O(1) amortised times, an O(n) pass.

Three shapes cover almost everything:

- **Fixed size**: the window is always ``k`` wide. Slide it and track the best.
- **Flexible longest**: grow ``right``; when the window becomes *invalid*, shrink ``left``
  until valid again; record the largest valid window.
- **Flexible shortest**: grow ``right``; while the window is *valid*, record it and shrink
  ``left`` to try to do better.

These are directional skeletons, adapt the per-window bookkeeping per problem.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Callable, TypeVar

T = TypeVar("T")


def fixed_window_max_sum(nums: Sequence[float], k: int) -> float:
    """Maximum sum of any contiguous window of size ``k`` (a concrete fixed-window example).

    Raises ``ValueError`` if ``k`` is not a valid window size for ``nums``.
    """
    if k <= 0 or k > len(nums):
        raise ValueError(f"window size {k} invalid for input of length {len(nums)}")
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]  # add entering, drop leaving
        best = max(best, window)
    return best


def longest_window(
    n: int,
    add: Callable[[int], None],
    remove: Callable[[int], None],
    is_valid: Callable[[], bool],
) -> int:
    """Length of the longest window over ``range(n)`` that stays valid.

    ``add(i)``/``remove(i)`` update external window state for index ``i``; ``is_valid()``
    reports whether the current window is acceptable. The window is shrunk from the left
    until valid again, so the answer is the largest valid width seen.
    """
    left = 0
    best = 0
    for right in range(n):
        add(right)
        while not is_valid():
            remove(left)
            left += 1
        best = max(best, right - left + 1)
    return best


def shortest_window(
    n: int,
    add: Callable[[int], None],
    remove: Callable[[int], None],
    is_valid: Callable[[], bool],
) -> int:
    """Length of the shortest window over ``range(n)`` that is valid, or ``0`` if none.

    Mirror image of :func:`longest_window`: while the window is valid we record it and keep
    shrinking from the left to find a tighter one.
    """
    left = 0
    best = 0
    for right in range(n):
        add(right)
        while is_valid():
            width = right - left + 1
            best = width if best == 0 else min(best, width)
            remove(left)
            left += 1
    return best
