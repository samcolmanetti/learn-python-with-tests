# Property-based testing

**[You can find all the code for this chapter here](property_based_testing/)**

Example-based tests check the cases *you thought of*. Property-based tests check a rule that
must hold for *every* input, and let a library generate hundreds of inputs — including the
nasty edge cases you'd never pick by hand. In Python that library is
[Hypothesis](https://hypothesis.readthedocs.io).

We'll build a Roman-numeral converter and guard it with a property.

## Start example-first

Roman numerals go largest-to-smallest with six subtractive pairs (IV, IX, XL, XC, CD, CM). The
neat trick: list every value/symbol pair *including* the subtractive ones in descending order
and greedily consume them. `property_based_testing/v1/roman.py`:

```python
ROMAN_NUMERALS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(number):
    if not 1 <= number <= 3999:
        raise ValueError("Roman numerals represent 1..3999")
    result = []
    for value, symbol in ROMAN_NUMERALS:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)
```

We pin it down with example tests (`v1/test_roman.py`), the cases a human would choose —
the subtractive boundaries (4, 9, 40, 90, 400, 900) and a couple of big composites:

```python
@pytest.mark.parametrize(
    ("number", "expected"),
    [(1, "I"), (4, "IV"), (9, "IX"), (1984, "MCMLXXXIV"), (3999, "MMMCMXCIX")],
)
def test_to_roman(number, expected):
    assert to_roman(number) == expected
```

Good — but did we pick the *right* examples? What about 3888 (`MMMDCCCLXXXVIII`, the longest
numeral)? Did we test the inverse direction at all? This is where example-based testing runs
out of imagination.

## Add the inverse, then find the property

`v2` adds `from_roman`, the natural inverse — match the same pairs greedily from the front of
the string:

```python
def from_roman(numeral):
    total = 0
    index = 0
    for value, symbol in ROMAN_NUMERALS:
        while numeral[index:index + len(symbol)] == symbol:
            total += value
            index += len(symbol)
    if index != len(numeral):
        raise ValueError(f"not a valid Roman numeral: {numeral!r}")
    return total
```

Now there's a **property** that must hold for every valid number: converting to a numeral and
back returns the original. We don't need to know the right Roman string for 2748 to assert
this — that's the power of it.

```python
from hypothesis import given
from hypothesis import strategies as st

from .roman import from_roman, to_roman


@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_then_from_roman_round_trips(number):
    assert from_roman(to_roman(number)) == number
```

`@given` tells Hypothesis to *generate* the `number` argument. `st.integers(...)` is a
**strategy** — a description of the inputs to draw from. Hypothesis runs this test on many
values, deliberately biased toward boundaries (1, 3999) and other likely-to-break points.

Another useful property — the output only ever uses the seven legal symbols:

```python
@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_only_uses_valid_symbols(number):
    assert set(to_roman(number)) <= set("IVXLCDM")
```

## Shrinking: the killer feature

Suppose `from_roman` had a bug — say it mishandled `IX`. A property test wouldn't just fail; it
would **shrink** the failing input to the simplest value that still breaks, and report it:

```
Falsifying example: test_to_roman_then_from_roman_round_trips(number=9)
```

Not `number=2748` (the first random case that happened to fail), but the minimal `9`. That
shrunk counterexample usually points straight at the bug. Hypothesis also *remembers* failing
examples between runs (in a `.hypothesis/` cache) and replays them first, so once you've seen a
failure it stays caught.

## When to reach for properties

Properties shine when there's a rule independent of specific inputs:

- **Round trips**: `decode(encode(x)) == x` (serialization, compression, this chapter).
- **Invariants**: a sorted list is the same length and a permutation of the input; a result is
  always within bounds.
- **Equivalence**: a fast implementation agrees with an obvious slow one (great for checking
  interview optimizations against brute force).

Use example tests for the specific cases you care about *and* a property or two for the rules.
Together they cover far more than either alone.

## Wrapping up

- **Property-based tests assert a rule over generated inputs**, catching edge cases you'd never
  hand-pick.
- **`@given` + strategies** (`st.integers`, `st.text`, `st.lists`, …) drive the generation.
- **Shrinking** reduces any failure to a minimal counterexample — often the bug, handed to you.
- **Round trips, invariants, and brute-force equivalence** are the everyday property patterns —
  the last is gold for validating interview optimizations.

Next: [Complexity & Big-O](complexity.md).
