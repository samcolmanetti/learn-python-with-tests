from __future__ import annotations

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    """Return the kth largest value in `nums` using a min-heap of size k."""
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
