"""Insert Interval.

Given a list of non-overlapping intervals already sorted by start, insert a new interval and
merge anything it overlaps. Because the list is already sorted we don't pay to sort again: walk
once in three phases. First copy every interval that ends before the new one starts. Then absorb
every interval that overlaps the new one, widening the new interval as we go. Finally copy the
rest.
"""

from __future__ import annotations


def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    start, end = new_interval
    result: list[list[int]] = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])

    while i < n:
        result.append(intervals[i])
        i += 1

    return result
