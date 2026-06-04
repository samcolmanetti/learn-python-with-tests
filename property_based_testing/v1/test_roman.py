import pytest

from .roman import to_roman


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "I"),
        (4, "IV"),
        (9, "IX"),
        (14, "XIV"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (1984, "MCMLXXXIV"),
        (3999, "MMMCMXCIX"),
    ],
)
def test_to_roman(number, expected):
    assert to_roman(number) == expected


def test_out_of_range_raises():
    with pytest.raises(ValueError):
        to_roman(0)
    with pytest.raises(ValueError):
        to_roman(4000)
