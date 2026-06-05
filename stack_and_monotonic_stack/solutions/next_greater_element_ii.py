from __future__ import annotations

from collections.abc import Sequence


def next_greater_circular(nums: Sequence[int]) -> list[int]:
    """For each index, the next strictly-greater value going around the ring, else ``-1``."""
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []  # indices whose answer is not yet known
    for step in range(2 * n):
        value = nums[step % n]
        while stack and nums[stack[-1]] < value:
            result[stack.pop()] = value
        if step < n:
            stack.append(step)
    return result
