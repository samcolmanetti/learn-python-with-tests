"""Subarray Sum Equals K.

Count the contiguous subarrays whose elements sum to ``k``. A subarray ``nums[i:j]`` sums to
``running[j] - running[i]``, so we want pairs of running prefix sums that differ by ``k``. Walk
the array keeping the running sum and a dict of how many times each prefix sum has been seen.
For each position, the number of earlier prefixes equal to ``running - k`` is the number of
subarrays ending here that sum to ``k``. Seed the dict with ``{0: 1}`` so a prefix that itself
equals ``k`` counts.
"""

from __future__ import annotations

from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    counts: dict[int, int] = defaultdict(int)
    counts[0] = 1
    running = 0
    total = 0
    for value in nums:
        running += value
        total += counts[running - k]
        counts[running] += 1
    return total
