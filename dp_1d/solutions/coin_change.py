"""Coin Change (minimum coins).

Given coin denominations and a target ``amount``, return the fewest coins that sum to it, or
``-1`` if no combination works. ``dp[a]`` is the fewest coins for amount ``a``. For each coin
``c <= a`` we could use it as the last coin, giving ``1 + dp[a - c]``; we take the best over all
coins, so ``dp[a] = min(1 + dp[a - c] for c in coins if c <= a)``.
"""

from __future__ import annotations


def coin_change(coins: list[int], amount: int) -> int:
    unreachable = amount + 1
    dp = [0] + [unreachable] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], 1 + dp[a - coin])
    return dp[amount] if dp[amount] != unreachable else -1
