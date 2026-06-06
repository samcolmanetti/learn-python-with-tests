"""Iterators and iterables, built up one behaviour at a time.

We start with a hand-rolled iterator class (``Countdown``) so the ``__iter__`` and ``__next__``
protocol is visible, then write the same idea as a generator (``fibonacci``) where ``yield`` does
the bookkeeping for us, and finish by reaching for ``itertools`` instead of writing the loop.
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import islice


class Countdown:
    """An iterator that yields ``start, start - 1, ..., 1`` and then stops.

    The object is both the iterable (``__iter__`` returns ``self``) and the iterator
    (``__next__`` produces the next value and raises ``StopIteration`` when done).
    """

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> Countdown:
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def fibonacci(count: int) -> Iterator[int]:
    """Yield the first ``count`` Fibonacci numbers starting ``0, 1, 1, 2, 3, ...``.

    This is the same lazy, one-value-at-a-time behaviour as ``Countdown``, but ``yield`` keeps
    the local state for us, so there's no class and no ``StopIteration`` to raise by hand.
    """
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b


def fibonacci_forever() -> Iterator[int]:
    """Yield Fibonacci numbers with no end. Safe because the caller decides when to stop."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def first_n_fibonacci(count: int) -> list[int]:
    """Take ``count`` values from the endless generator using ``itertools.islice``."""
    return list(islice(fibonacci_forever(), count))
