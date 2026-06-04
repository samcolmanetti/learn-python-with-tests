"""Remove Duplicates from Sorted Array (same-direction / fast-slow two pointers).

Given a *sorted* list, remove duplicates **in place** so each element appears once, and return
the new logical length ``k``; the first ``k`` entries hold the unique values in order. The slow
pointer is the write head for the next unique value; the fast pointer scans ahead.
"""

from __future__ import annotations


def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0  # nums[:slow + 1] are the uniques found so far
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
