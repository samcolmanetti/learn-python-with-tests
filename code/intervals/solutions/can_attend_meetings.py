"""Meeting Rooms (can one person attend every meeting?).

Given meeting time intervals, decide whether a single person can attend all of them, which is
true exactly when no two meetings overlap. Sort by start, then sweep adjacent pairs: if any
meeting starts before the previous one ends, they collide and the answer is ``False``. Meetings
that merely touch (one ends as the next begins) are fine.
"""

from __future__ import annotations


def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals, key=lambda interval: interval[0])
    for earlier, later in zip(ordered, ordered[1:]):
        if later[0] < earlier[1]:
            return False
    return True
