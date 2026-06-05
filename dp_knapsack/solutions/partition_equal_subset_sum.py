from __future__ import annotations

from collections.abc import Sequence


def can_partition(nums: Sequence[int]) -> bool:
    """Return True if ``nums`` can be split into two subsets with equal sum."""
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    reachable = [False] * (target + 1)
    reachable[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            if reachable[s - num]:
                reachable[s] = True

    return reachable[target]
