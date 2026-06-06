from __future__ import annotations


def hamming_weight(n: int) -> int:
    """Return the number of set bits in the non-negative integer ``n``."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
