from __future__ import annotations

from collections.abc import Sequence


def find_target_sum_ways(nums: Sequence[int], target: int) -> int:
    """Count the ways to assign a ``+`` or ``-`` to each number so the expression equals ``target``.

    Let ``P`` be the sum of the numbers we make positive and ``N`` the sum of those we make
    negative. Then ``P - N == target`` and ``P + N == sum(nums)``, so ``P == (target + total) / 2``.
    The problem becomes: how many subsets sum to that value? That's a 0/1 count knapsack.
    """
    total = sum(nums)
    needed = target + total
    if needed < 0 or needed % 2 != 0:
        return 0

    subset_target = needed // 2
    ways = [0] * (subset_target + 1)
    ways[0] = 1

    for num in nums:
        for s in range(subset_target, num - 1, -1):
            ways[s] += ways[s - num]

    return ways[subset_target]
