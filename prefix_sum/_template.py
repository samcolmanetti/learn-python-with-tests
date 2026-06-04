"""Prefix Sum — precompute cumulative sums for O(1) range queries.

Build a `prefix` array once in O(n); then the sum of any range ``[left, right]`` (inclusive)
is a single subtraction. The same idea generalises to "count" and "XOR" prefixes and to 2D.

Convention here: ``prefix`` has length ``n + 1`` with ``prefix[0] == 0`` and
``prefix[i] == sum(arr[:i])``. The extra leading zero removes the ``left == 0`` special case.
"""

from __future__ import annotations

from collections.abc import Sequence


def build_prefix(arr: Sequence[float]) -> list[float]:
    """Return cumulative sums with a leading zero: ``prefix[i] == sum(arr[:i])``."""
    prefix = [0.0] * (len(arr) + 1)
    for i, value in enumerate(arr):
        prefix[i + 1] = prefix[i] + value
    return prefix


def range_sum(prefix: Sequence[float], left: int, right: int) -> float:
    """Sum of ``arr[left:right + 1]`` (inclusive) given a prefix array from :func:`build_prefix`."""
    return prefix[right + 1] - prefix[left]
