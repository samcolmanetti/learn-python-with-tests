"""Integer Square Root (binary search on the answer).

Return ``floor(sqrt(n))`` without using ``math.sqrt``, the canonical "binary search on the
answer space" problem. We're not searching an array; we're searching the range of possible
answers ``[0, n]`` for the largest ``x`` with ``x * x <= n``. ``feasible(x) = x*x <= n`` is
True…True…False, and we want the last True.
"""

from __future__ import annotations


def int_sqrt(n: int) -> int:
    if n < 0:
        raise ValueError("square root is undefined for negative numbers")
    if n < 2:
        return n
    lo, hi = 1, n // 2
    answer = 1  # last x known to satisfy x*x <= n
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            answer = mid
            lo = mid + 1  # try to do better
        else:
            hi = mid - 1
    return answer
