import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from .sqrt import int_sqrt


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (4, 2),
        (8, 2),  # floor(2.82...)
        (9, 3),
        (15, 3),
        (16, 4),
        (2, 1),
    ],
)
def test_int_sqrt(n, expected):
    assert int_sqrt(n) == expected


def test_negative_raises():
    with pytest.raises(ValueError):
        int_sqrt(-1)


@given(st.integers(min_value=0, max_value=10**12))
def test_matches_math_isqrt(n):
    # Property: agree with the standard library's integer sqrt for all non-negative n.
    assert int_sqrt(n) == math.isqrt(n)
