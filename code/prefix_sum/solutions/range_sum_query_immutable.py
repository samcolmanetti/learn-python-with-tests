"""Range Sum Query - Immutable.

Given an integer array that never changes, answer many ``sum_range(i, j)`` queries (inclusive)
in O(1) each. Build a prefix array once in the constructor; every query is then a single
subtraction.
"""

from __future__ import annotations


class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0] * (len(nums) + 1)
        for i, value in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + value

    def sum_range(self, i: int, j: int) -> int:
        return self.prefix[j + 1] - self.prefix[i]
