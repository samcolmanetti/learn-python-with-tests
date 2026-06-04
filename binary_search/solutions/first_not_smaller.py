"""First Element Not Smaller Than Target (binary search on a boundary).

In a sorted array, return the index of the first element ``>= target`` (the lower-bound
insertion point), or ``len(arr)`` if every element is smaller. This is the ``bisect_left``
boundary, written out by hand to show the predicate-search shape: ``feasible(i) = arr[i] >=
target`` is False…False…True…True, and we want the first True.
"""

from __future__ import annotations


def first_not_smaller(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    first_true = len(arr)  # sentinel: nothing is >= target
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            first_true = mid
            hi = mid - 1  # look for an earlier qualifying index
        else:
            lo = mid + 1
    return first_true
