def total(numbers):
    return sum(numbers)


def reversed_list(items):
    return items[::-1]


def tail(items):
    return items[1:]


def every_other(items):
    """Return every other element using a step slice (``items[::2]``)."""
    return items[::2]


def copy_of(items):
    """A shallow copy via full slice ``items[:]``.

    Crucial interview gotcha: ``b = a`` makes ``b`` an *alias* (same list object), so mutating
    one mutates the other. ``b = a[:]`` makes an independent copy. This function exists to make
    that distinction testable and explicit.
    """
    return items[:]
