"""House Robber.

Houses sit in a row, each holding some money. You can't rob two adjacent houses. Return the
most you can take. At house ``i`` you either skip it (keeping ``dp[i - 1]``) or rob it (taking
``nums[i] + dp[i - 2]``), so ``dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])``.
"""

from __future__ import annotations


def rob(nums: list[int]) -> int:
    skip, take = 0, 0
    for value in nums:
        skip, take = take, max(take, skip + value)
    return take
