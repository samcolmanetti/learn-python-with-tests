# Property-based testing

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/property_based_testing)**

Example-based tests check the cases *you thought of*. Property-based tests check a rule that
must hold for *every* input, and let a library generate hundreds of inputs, including the nasty
edge cases you'd never pick by hand. In Python that library is
[Hypothesis](https://hypothesis.readthedocs.io).

We'll build a Roman-numeral converter and guard it with a property. Make sure the dependencies
are installed with `uv sync` (and `uv add hypothesis` if it isn't in the project yet), then run
the tests with `uv run pytest`.

## Write the test first

Roman numerals go largest-to-smallest with six subtractive pairs (IV, IX, XL, XC, CD, CM). The
neat trick: list every value/symbol pair *including* the subtractive ones in descending order
and greedily consume them.

Before we write any of that, pin down the behaviour with example tests. These are the cases a
human would choose: the subtractive boundaries (4, 9, 40, 90, 400, 900) and a couple of big
composites. We also assert that out-of-range numbers raise. Put this in `v1/test_roman.py`:

```python
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
```

## Try to run the test

We've imported `to_roman` from a module that doesn't define it yet, so the import is the first
thing to break:

```
ImportError: cannot import name 'to_roman' from 'roman'
```

No function, nothing. Listen to the error: it's telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `to_roman` that returns a stub `""`. We're not solving anything yet. We just want the
test to run so we can watch it fail on the value, which proves the test checks what we think it
does. In `v1/roman.py`:

```python
from __future__ import annotations


def to_roman(number: int) -> str:
    return ""
```

Run `uv run pytest`:

```
    def test_to_roman(number, expected):
>       assert to_roman(number) == expected
E       AssertionError: assert '' == 'I'
E         + I
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

List the value/symbol pairs (subtractive forms included) in descending order, then greedily
consume them. Guard the range up front so `0` and `4000` raise.

```python
from __future__ import annotations

# Descending value/symbol pairs, subtractive forms included.
ROMAN_NUMERALS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def to_roman(number: int) -> str:
    if not 1 <= number <= 3999:
        raise ValueError("Roman numerals represent 1..3999")
    result = []
    for value, symbol in ROMAN_NUMERALS:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)
```

Run the tests again and they're green.

Each pass takes the largest pair that still fits and subtracts it, appending the symbol, until
`number` reaches zero. Putting the subtractive pairs (`900` -> `"CM"`, `4` -> `"IV"`, and the
rest) in the same table is what keeps the loop short: there's no special case for them.

## Refactor

There's little to tidy in a dozen lines, but it's worth naming the shape. The table is doing the
work; the loop is a plain greedy consume. We could pull the range check into its own helper, but
inlining it keeps the whole algorithm in one view. Re-run the tests to confirm nothing moved.

Good. But did we pick the *right* examples? What about 3888 (`MMMDCCCLXXXVIII`, the longest
numeral)? Did we test the inverse direction at all? This is where example-based testing runs out
of imagination.

## Add the inverse, then find the property

Our next requirement is the other direction: `from_roman`. Then we'll have a pair of functions
that should undo each other, which is the rule a property test can pin down.

### Write the test first

The natural inverse matches the same pairs greedily from the front of the string. Start with a
few example tests in `v2/test_roman.py` so the function has something concrete to satisfy, and
assert that garbage input raises:

```python
import pytest

from .roman import from_roman, to_roman


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


def test_from_roman_rejects_garbage():
    with pytest.raises(ValueError):
        from_roman("BANANA")
```

### Try to run the test

`from_roman` doesn't exist yet, so the import is what fails first:

```
ImportError: cannot import name 'from_roman' from 'roman'
```

### Write the minimal amount of code for the test to run and check the failing test output

Copy `to_roman` and `ROMAN_NUMERALS` into `v2/roman.py`, then add a stubbed `from_roman` that
returns `0`. The tests can run and fail on the value:

```python
def from_roman(numeral: str) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_from_roman_examples(numeral, expected):
>       assert from_roman(numeral) == expected
E       assert 0 == 1
E        +  where 0 = from_roman('I')
```

Failing on the value, as expected.

### Write enough code to make it pass

Walk the same descending table, consuming each symbol from the front of the string while it
matches. If we don't end up exactly at the end of the string, the input wasn't a valid numeral,
so we raise:

```python
def from_roman(numeral: str) -> int:
    total = 0
    index = 0
    for value, symbol in ROMAN_NUMERALS:
        while numeral[index : index + len(symbol)] == symbol:
            total += value
            index += len(symbol)
    if index != len(numeral):
        raise ValueError(f"not a valid Roman numeral: {numeral!r}")
    return total
```

The tests pass. `"BANANA"` never matches a symbol, so `index` stays at `0`, never reaches the
end, and we get the `ValueError` the test wants.

### Refactor

Now there's a **property** that must hold for every valid number: converting to a numeral and
back returns the original. We don't need to know the right Roman string for 2748 to assert this.
That's the point.

```python
from hypothesis import given
from hypothesis import strategies as st

from .roman import from_roman, to_roman


@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_then_from_roman_round_trips(number):
    assert from_roman(to_roman(number)) == number
```

`@given` tells Hypothesis to *generate* the `number` argument. `st.integers(...)` is a
**strategy**, a description of the inputs to draw from. Hypothesis runs this test on many values,
deliberately biased toward boundaries (1, 3999) and other likely-to-break points. One small test
now covers far more ground than the example table, and we never had to hand-write a single
expected string.

Another useful property: the output only ever uses the seven legal symbols.

```python
@given(st.integers(min_value=1, max_value=3999))
def test_to_roman_only_uses_valid_symbols(number):
    assert set(to_roman(number)) <= set("IVXLCDM")
```

Re-run the tests. The examples and the properties are green together, and the property tests now
guard the round trip for every number in range.

## Shrinking: the killer feature

Suppose `from_roman` had a bug, say it mishandled `IX`. A property test wouldn't just fail; it
would **shrink** the failing input to the simplest value that still breaks, and report it:

```
Falsifying example: test_to_roman_then_from_roman_round_trips(number=9)
```

Not `number=2748` (the first random case that happened to fail), but the minimal `9`. That
shrunk counterexample usually points straight at the bug. Hypothesis also *remembers* failing
examples between runs (in a `.hypothesis/` cache) and replays them first, so once you've seen a
failure it stays caught.

## When to reach for properties

Properties earn their keep when there's a rule independent of specific inputs:

- **Round trips**: `decode(encode(x)) == x` (serialization, compression, this chapter).
- **Invariants**: a sorted list is the same length and a permutation of the input; a result is
  always within bounds.
- **Equivalence**: a fast implementation agrees with an obvious slow one (handy for checking
  interview optimizations against brute force).

Use example tests for the specific cases you care about *and* a property or two for the rules.
Together they cover far more than either alone.

## Wrapping up

- **Property-based tests assert a rule over generated inputs**, catching edge cases you'd never
  hand-pick.
- **`@given` plus strategies** (`st.integers`, `st.text`, `st.lists`, and the rest) drive the
  generation.
- **Shrinking** reduces any failure to a minimal counterexample, often the bug, handed to you.
- **Round trips, invariants, and brute-force equivalence** are the everyday property patterns.
  The last is gold for validating interview optimizations.

Next: [Complexity & Big-O](complexity.md).
</content>
</invoke>
