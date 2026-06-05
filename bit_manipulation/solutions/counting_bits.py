from __future__ import annotations


def count_bits(n: int) -> list[int]:
    """Return a list where entry ``i`` is the number of set bits in ``i``, for ``0..n``."""
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result
