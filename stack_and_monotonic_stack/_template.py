"""Monotonic Stack — find the next/previous greater (or smaller) element in O(n).

A monotonic stack keeps its elements in sorted order (here: strictly decreasing values).
When a new element would break the order, we pop the smaller elements — and *that pop is the
answer* to "what is the next greater element" for each popped item. Each index is pushed and
popped at most once, so the whole scan is O(n).

This concrete template solves "next greater element": for each position, the value of the
next element to its right that is strictly greater, or ``-1`` if none.
"""

from __future__ import annotations

from collections.abc import Sequence


def next_greater(nums: Sequence[int]) -> list[int]:
    """For each index, the next strictly-greater value to its right, else ``-1``.

    Example: ``next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]``.
    """
    result = [-1] * len(nums)
    stack: list[int] = []  # holds indices whose answer is not yet known
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            result[stack.pop()] = value
        stack.append(i)
    return result
