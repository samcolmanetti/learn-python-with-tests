"""Bit manipulation, the three operations every bit problem leans on.

Integers are just bit strings, and three moves cover most interview questions:

XOR (``^``): ``a ^ a == 0`` and ``a ^ 0 == a``. XOR is its own inverse, so XORing a value in
twice cancels it out. That cancellation is what finds the one unpaired element in a list.

Mask and test (``x & (1 << i)``): isolate bit ``i``. If the result is non-zero, bit ``i`` is
set. Shift a mask across every position to inspect a number bit by bit.

Lowest set bit (``x & -x``): two's complement makes ``-x`` the bitwise-not of ``x`` plus one, so
``x & -x`` keeps only the rightmost ``1`` and zeroes everything else. Subtracting it,
``x & (x - 1)``, clears that rightmost ``1``. Looping on ``x & (x - 1)`` walks one set bit per
step instead of all 32 (or 64) positions.
"""

from __future__ import annotations


def lowest_set_bit(x: int) -> int:
    """Return the value of the lowest set bit of ``x`` (0 when ``x`` is 0)."""
    return x & -x


def clear_lowest_set_bit(x: int) -> int:
    """Return ``x`` with its lowest set bit cleared."""
    return x & (x - 1)


def is_bit_set(x: int, i: int) -> bool:
    """Return True when bit ``i`` of ``x`` is set."""
    return (x & (1 << i)) != 0
