from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from operator import xor


def single_number(nums: Iterable[int]) -> int:
    """Return the one element that appears once; every other appears exactly twice."""
    return reduce(xor, nums, 0)
