"""Heaps / priority queue, keep the smallest (or largest) thing reachable in O(log n).

`heapq` turns a plain list into a binary *min-heap*: the smallest element is always at
index 0, `heappush` adds in O(log n), and `heappop` removes that smallest in O(log n).
There is no max-heap in the standard library, so to keep the *largest* element on top we
push the negated value and negate again on the way out.

The helpers below are the two moves every problem in this chapter reuses.
"""

from __future__ import annotations

import heapq
from collections.abc import Iterable


def smallest_n(items: Iterable[float], n: int) -> list[float]:
    """Return the `n` smallest items, smallest first, using a min-heap."""
    heap = list(items)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(min(n, len(heap)))]


def largest_n(items: Iterable[float], n: int) -> list[float]:
    """Return the `n` largest items, largest first, by pushing negated values."""
    heap = [-item for item in items]
    heapq.heapify(heap)
    return [-heapq.heappop(heap) for _ in range(min(n, len(heap)))]
