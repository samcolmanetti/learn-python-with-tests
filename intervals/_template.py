"""Intervals: sort by start, then sweep left to right merging or comparing neighbours.

Almost every interval problem reduces to one move: sort the intervals by their start, then
walk them in order keeping a single "current" interval. Because the list is sorted by start,
the only neighbour that can overlap the current interval is the next one, so a single pass
decides everything.

Convention here: an interval is a two-item ``[start, end]`` list (or tuple), inclusive of both
ends, and two intervals overlap when ``a_start <= b_end and b_start <= a_end``. When we sweep a
start-sorted list, the test simplifies: the next interval overlaps the current one when its
start is ``<= current_end``.
"""

from __future__ import annotations

from collections.abc import Sequence


def merge_sorted(intervals: Sequence[Sequence[int]]) -> list[list[int]]:
    """Merge overlapping intervals. Sort by start, then sweep keeping one open interval.

    The skeleton every problem in this chapter adapts: sort, seed ``merged`` with the first
    interval, then for each later interval either extend the open one (overlap) or start a
    new one (gap).
    """
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
