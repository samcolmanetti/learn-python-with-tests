import pytest

from .number_basics import add, divide, factorial


def test_adds_two_numbers():
    assert add(2, 2) == 4


def test_divide_returns_quotient_and_remainder():
    assert divide(7, 2) == (3, 1)
    assert divide(10, 5) == (2, 0)


def test_divide_floors_toward_negative_infinity():
    # Python's floor division rounds toward negative infinity, a classic interview gotcha.
    assert divide(-7, 2) == (-4, 1)


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_factorial_uses_arbitrary_precision():
    # No overflow: Python ints grow without bound. 50! is a 65-digit number.
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert len(str(factorial(50))) == 65


def test_factorial_rejects_negatives():
    with pytest.raises(ValueError):
        factorial(-1)
