def total(numbers):
    return sum(numbers)  # refactor: the loop in v1 is just the built-in `sum`


def reversed_list(items):
    """Return a reversed *copy* using the slice idiom ``[::-1]`` (start:stop:step)."""
    return items[::-1]


def tail(items):
    """Everything after the first element (``items[1:]``).

    Slicing never raises on out-of-range bounds, so ``tail([])`` is just ``[]``.
    """
    return items[1:]
