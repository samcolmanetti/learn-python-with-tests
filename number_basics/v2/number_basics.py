def add(a, b):
    return a + b


def divide(a, b):
    """Integer division returning ``(quotient, remainder)``.

    Python has two division operators: ``/`` is *true* division and always returns a float
    (``7 / 2 == 3.5``), while ``//`` is *floor* division (``7 // 2 == 3``). The built-in
    ``divmod`` gives you both the quotient and remainder at once — handy in interviews for
    digit problems and grid coordinates.
    """
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return divmod(a, b)


def factorial(n):
    """``n!`` — demonstrates Python's arbitrary-precision integers (no overflow)."""
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
