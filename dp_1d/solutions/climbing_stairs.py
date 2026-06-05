"""Climbing Stairs.

You can climb 1 or 2 steps at a time. Count the distinct ways to reach step ``n``. The number
of ways to reach step ``i`` is the ways to reach ``i - 1`` (then take a single step) plus the
ways to reach ``i - 2`` (then take a double step), so ``dp[i] = dp[i - 1] + dp[i - 2]``.
"""

from __future__ import annotations


def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
