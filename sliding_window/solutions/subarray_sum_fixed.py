"""Maximum Sum Subarray of Size K (fixed-size sliding window).

Maintain a window of exactly ``k`` elements. Slide it one step at a time, adding the entering
element and subtracting the leaving one, so each step is O(1) and the whole scan is O(n), far
better than recomputing each window's sum.
"""

from __future__ import annotations


def max_subarray_sum(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        raise ValueError(f"window size {k} invalid for input of length {len(nums)}")
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best
