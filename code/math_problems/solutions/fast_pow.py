from __future__ import annotations


def fast_pow(base: int, exp: int, mod: int) -> int:
    """Return ``(base ** exp) % mod`` using binary exponentiation.

    ``exp`` must be non-negative. Squaring the base while halving the exponent does the work
    in O(log exp) multiplications instead of O(exp).
    """
    if exp < 0:
        raise ValueError("exp must be non-negative")
    result = 1 % mod
    base %= mod
    while exp:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result
