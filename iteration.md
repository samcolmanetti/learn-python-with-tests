# Iteration

**[You can find all the code for this chapter here](iteration/)**

To do something repeatedly in Python you reach for `for` (usually over a `range` or directly
over a collection) or `while`. We'll build a small function test-first and then refactor it
into idiomatic Python.

## Write the test first

A function that repeats a character five times. `iteration/v1/test_iteration.py`:

```python
from .iteration import repeat


def test_repeats_a_character_five_times():
    assert repeat("a") == "aaaaa"
```

## Try to run the test

```
ImportError: cannot import name 'repeat' from 'iteration.v1.iteration'
```

## Write enough code to make it pass

`iteration/v1/iteration.py`:

```python
def repeat(character):
    repeated = ""
    for _ in range(5):
        repeated += character
    return repeated
```

`range(5)` yields `0, 1, 2, 3, 4`. We don't use the loop variable, so we name it `_` by
convention. `+=` appends to the string.

```
1 passed
```

## Repeat for new requirements — a configurable count

Hard-coding `5` is no good. Let's pass the count in. `iteration/v2`:

```python
def test_repeats_a_character_a_given_number_of_times():
    assert repeat("a", 5) == "aaaaa"


def test_repeats_zero_times_is_empty():
    assert repeat("a", 0) == ""
```

```python
def repeat(character, count):
    repeated = ""
    for _ in range(count):
        repeated += character
    return repeated
```

The `count == 0` test matters: `range(0)` is empty, so the loop body never runs and we get
`""`. Testing the boundary now means we never wonder about it later.

## Refactor

With green tests we can make this idiomatic. In Python, multiplying a string by an integer
repeats it, so the whole function collapses to one line (`iteration/v3`):

```python
def repeat(character, count):
    return character * count
```

This is the payoff of the safety net: we replaced the implementation entirely and the tests
told us, instantly, that behaviour was preserved. We lock it in with a `parametrize` table
covering the cases we care about:

```python
@pytest.mark.parametrize(
    ("character", "count", "expected"),
    [
        ("a", 5, "aaaaa"),
        ("a", 0, ""),
        ("a", 1, "a"),
        ("ab", 3, "ababab"),
        ("", 4, ""),
    ],
)
def test_repeat(character, count, expected):
    assert repeat(character, count) == expected
```

## A note on building strings in loops

We used `repeated += character`. For a few iterations that's fine. But strings in Python are
**immutable**, so each `+=` builds a brand-new string — in a hot loop over thousands of
elements that's accidentally O(n²). The interview-safe idiom is to collect parts in a list and
`"".join(...)` them at the end, which is O(n):

```python
parts = []
for chunk in chunks:
    parts.append(chunk)
result = "".join(parts)
```

We'll lean on `join` throughout the string and pattern chapters.

## Wrapping up

- **`for ... in range(n)`** is the workhorse loop; name the unused variable `_`.
- **Test the zero/empty boundary** — `range(0)` runs the body zero times.
- **`str * int` repeats a string**; prefer idiomatic Python once tests have your back.
- **Strings are immutable** — build big strings with a list and `"".join(...)`, not `+=`.

Next: [Lists & slicing](lists-and-slicing.md).
