"""Two Sum II, input array is sorted (opposite-direction two pointers).

Given a 1-indexed-in-the-problem-but-0-indexed-here *sorted* array and a target, return the
indices of the two numbers that add up to the target. Because the array is sorted, two pointers
from the ends find the pair in a single O(n) pass: if the sum is too small move ``left`` right
to increase it; if too big move ``right`` left to decrease it.
"""

from __future__ import annotations


def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(numbers) - 1
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return (left, right)
        if current < target:
            left += 1
        else:
            right -= 1
    return None
