"""Search in Rotated Sorted Array (binary search with a twist).

A sorted array rotated at some unknown pivot (e.g. ``[4, 5, 6, 7, 0, 1, 2]``) is still
"half sorted" at every step: for any ``mid``, at least one of ``[lo..mid]`` or ``[mid..hi]`` is
fully sorted. Figure out which half is sorted, check whether the target lies inside it, and
discard the other half. Still O(log n). Returns the index of ``target`` or ``-1``.
"""

from __future__ import annotations


def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
