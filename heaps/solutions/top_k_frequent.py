from __future__ import annotations

import heapq
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return the `k` most frequent values, most frequent first."""
    counts = Counter(nums)
    heap: list[tuple[int, int]] = []
    for value, freq in counts.items():
        heapq.heappush(heap, (freq, value))
        if len(heap) > k:
            heapq.heappop(heap)
    result = [heapq.heappop(heap)[1] for _ in range(len(heap))]
    result.reverse()
    return result
