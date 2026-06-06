import pytest
from hypothesis import given
from hypothesis import strategies as st
from roman import from_roman, to_roman


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "I"),
        (4, "IV"),
        (1984, "MCMLXXXIV"),
        (3999, "MMMCMXCIX"),
    ],
)
def test_to_roman_examples(number, expected):
    assert to_roman(number) == expected


@pytest.mark.parametrize(
    ("numeral", "expected"),
    [
        ("I", 1),
        ("IV", 4),
        ("MCMLXXXIV", 1984),
        ("MMMCMXCIX", 3999),
    ],
)
def test_from_roman_examples(numeral, expected):
    assert from_roman(numeral) == expected


# ----- The property: round-trip identity ----------------------------------------------
# Instead of hand-picking examples, assert a *property* that must hold for EVERY input in
# range, and let Hypothesis generate hundreds of cases (and shrink any failure to a minimal
# counterexample).


@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_then_from_roman_round_trips(number):
    assert from_roman(to_roman(number)) == number


@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_only_uses_valid_symbols(number):
    assert set(to_roman(number)) <= set("IVXLCDM")


def test_from_roman_rejects_garbage():
    with pytest.raises(ValueError):
        from_roman("BANANA")
