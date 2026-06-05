"""Type hints in Python: annotate functions, Optional, and built-in generics.

Annotations are documentation that tooling can read. At runtime Python does not check them,
so every function here behaves exactly as it would without a single hint. The point is that a
type checker (and a human) can read the intent.

``from __future__ import annotations`` lets us write ``list[int]`` and ``dict[str, int]`` on
Python 3.9, where those subscripts would otherwise need ``typing.List`` and ``typing.Dict``.
With the import every annotation is stored as a string and never evaluated at runtime.
"""

from __future__ import annotations

from typing import Optional


def greet(name: str) -> str:
    """Return a greeting. The annotations say: takes a ``str``, returns a ``str``."""
    return "Hello, " + name


def total(numbers: list[int]) -> int:
    """Sum a list of ints. ``list[int]`` documents the element type, not just 'a list'."""
    running = 0
    for number in numbers:
        running += number
    return running


def first_name(full_name: str) -> Optional[str]:  # noqa: UP045
    """Return the first word of a name, or ``None`` if the string is empty.

    ``Optional[str]`` means 'a ``str`` or ``None``'. It is exactly ``Union[str, None]`` with a
    shorter name, and it is the honest signature for any function that can return nothing.
    """
    parts = full_name.split()
    if not parts:
        return None
    return parts[0]


def word_counts(words: list[str]) -> dict[str, int]:
    """Count how often each word appears. The return is a ``dict`` from ``str`` to ``int``."""
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
