"""Knapsack DP, fill a 1D table over a budget, one item at a time.

Every knapsack problem has the same two parts: a set of items, and a budget (a weight cap, a
target sum, an amount of money). You walk the items once. For each item you update a table
indexed by the budget, asking at every budget cell: am I better off skipping this item or
taking it?

The only thing that changes between the two flavours is the *direction* you sweep the budget,
and that single detail is the whole chapter:

- **0/1 knapsack**: each item can be used at most once. Sweep the budget *downward* (high to
  low). Sweeping down means that when you read ``dp[b - cost]`` you read the value from
  *before* this item was considered, so the item can't be picked twice in one pass.
- **Unbounded knapsack**: each item can be used any number of times. Sweep the budget *upward*
  (low to high). Sweeping up means ``dp[b - cost]`` may already include this item, so taking it
  again is allowed.

Same table, same "skip or take" question, opposite sweep. The two skeletons below are identical
except for the ``range`` direction. ``take`` decides how a chosen item folds into the cell
(``dp[b] = take(dp[b], dp[b - cost])``): use ``max`` for "best value", ``lambda a, b: a + b``
for "count the ways", and so on.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def knapsack_01(
    costs: Sequence[int],
    budget: int,
    base: Sequence[T],
    take: Callable[[T, T], T],
) -> list[T]:
    """Fill a ``dp`` table of length ``budget + 1`` using each item at most once.

    ``base`` is the starting table (the answer when no item has been considered yet).
    ``take(current, candidate)`` folds the "take this item" option (``candidate``, derived from
    ``dp[b - cost]``) into the current cell. The downward sweep is what makes it 0/1: when we
    read ``dp[b - cost]`` it still holds the previous item's value.
    """
    dp = list(base)
    for cost in costs:
        for b in range(budget, cost - 1, -1):
            dp[b] = take(dp[b], dp[b - cost])
    return dp


def knapsack_unbounded(
    costs: Sequence[int],
    budget: int,
    base: Sequence[T],
    take: Callable[[T, T], T],
) -> list[T]:
    """Fill a ``dp`` table of length ``budget + 1`` reusing each item any number of times.

    Identical to :func:`knapsack_01` except the budget sweeps *upward*, so ``dp[b - cost]`` can
    already include the current item and taking it again is allowed.
    """
    dp = list(base)
    for cost in costs:
        for b in range(cost, budget + 1):
            dp[b] = take(dp[b], dp[b - cost])
    return dp
