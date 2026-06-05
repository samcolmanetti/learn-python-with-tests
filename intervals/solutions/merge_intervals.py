"""Merge Intervals.

Given a list of ``[start, end]`` intervals, merge every set that overlaps and return the
non-overlapping result. Sort by start so the only interval that can overlap the current open
one is the next in line, then sweep once: extend the open interval when the next one starts at
or before the open one's end, otherwise close it and open a new one.
"""

from __future__ import annotations


def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged
