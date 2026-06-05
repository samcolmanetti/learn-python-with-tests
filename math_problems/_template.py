"""Number theory, the small kit of tricks that turns "loop and check" into "do the math".

Three ideas carry most interview number-theory questions, and the first one is a sieve.

A *sieve* precomputes a fact about every number up to ``n`` in one shared pass instead of
re-deriving it per number. The Sieve of Eratosthenes is the classic: to find every prime
below ``n``, start by assuming all are prime, then walk the primes in order and cross off
their multiples. Each composite gets struck by its smallest prime factor, so the whole thing
runs in about O(n log log n), much better than testing each number for primality on its own.

The skeleton below is that sieve in the abstract: a boolean array where ``is_prime[i]`` answers
"is ``i`` prime?" after one build. The chapter adapts it to count primes, and the same
"precompute once, then read off answers" shape underlies the gcd and fast-power solutions too.
"""

from __future__ import annotations


def sieve(n: int) -> list[bool]:
    """Return ``is_prime`` where ``is_prime[i]`` is ``True`` iff ``i`` is prime, for ``i < n``.

    One shared pass marks every composite below ``n`` by crossing off multiples of each prime.
    """
    if n < 2:
        return [False] * n
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n, i):
                is_prime[multiple] = False
    return is_prime
