"""1D Dynamic Programming, fill a table from base cases up to the answer.

A 1D DP problem has a state you can describe with a single index ``i`` and an answer
``dp[i]`` that depends only on a few earlier entries. You write down the base cases, then a
*transition* that builds ``dp[i]`` from ``dp[i - 1]``, ``dp[i - 2]``, and so on. Fill the table
from the bottom up and the answer is the last cell.

This module shows the bottom-up shape in the abstract: a ``dp`` array, base cases at the front,
and one transition applied in a loop. Each problem in ``solutions/`` is this same shape with a
different transition.

Convention here: ``dp[i]`` is the answer for the subproblem of size ``i``. We size the table to
``n + 1`` so ``dp[0]`` can hold the empty-input base case without a special branch.
"""

from __future__ import annotations

from collections.abc import Callable


def bottom_up(n: int, base: list[int], transition: Callable[[list[int], int], int]) -> int:
    """Fill ``dp[0..n]`` from ``base`` then ``transition``, and return ``dp[n]``.

    ``base`` seeds ``dp[0], dp[1], ...``. ``transition(dp, i)`` returns ``dp[i]`` from the
    entries already filled. This is the skeleton every solution below adapts.
    """
    if n < len(base):
        return base[n]
    dp = base + [0] * (n + 1 - len(base))
    for i in range(len(base), n + 1):
        dp[i] = transition(dp, i)
    return dp[n]
