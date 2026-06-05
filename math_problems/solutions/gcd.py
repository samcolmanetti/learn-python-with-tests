from __future__ import annotations


def gcd(a: int, b: int) -> int:
    """Greatest common divisor of ``a`` and ``b`` via Euclid's algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)
