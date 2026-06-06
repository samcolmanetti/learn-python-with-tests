from __future__ import annotations

from collections.abc import Sequence


def change(amount: int, coins: Sequence[int]) -> int:
    """Count the number of distinct combinations of ``coins`` that sum to ``amount``.

    Each coin may be used any number of times. Combinations are unordered: using a 1 then a 2 is
    the same combination as a 2 then a 1.
    """
    ways = [0] * (amount + 1)
    ways[0] = 1

    for coin in coins:
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]

    return ways[amount]
