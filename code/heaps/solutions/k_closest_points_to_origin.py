from __future__ import annotations

import heapq


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """Return the `k` points closest to the origin, in any order.

    We keep a max-heap of size `k` keyed on squared distance. Pushing the
    negated distance turns Python's min-heap into a max-heap, so the heap's
    top is always the worst of the `k` best we've seen so far. Anything
    farther than that top gets dropped.
    """
    heap: list[tuple[int, list[int]]] = []
    for x, y in points:
        distance = x * x + y * y
        heapq.heappush(heap, (-distance, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)
    return [point for _, point in heap]
