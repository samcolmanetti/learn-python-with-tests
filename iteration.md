# Iteration

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/iteration)**

To do something repeatedly in Python you reach for `for` (usually over a `range` or directly
over a collection) or `while`. We'll build a small function test-first and then refactor it
into idiomatic Python.

## Write the test first

We want a function that repeats a character five times. Start with the test in
`iteration/v1/test_iteration.py`:

```python
from .iteration import repeat


def test_repeats_a_character_five_times():
    assert repeat("a") == "aaaaa"
```

## Try to run the test

We've imported `repeat` from a module that doesn't define it yet, so the import is the first
thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'repeat' from 'iteration.v1.iteration'
```

Listen to the error: there's no function, so that's where we start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `repeat` that takes the argument and returns an empty string. We're not solving
anything yet. We just want the test to run so we can watch it fail on the value, which proves
the test checks what we think it does. In `iteration/v1/iteration.py`:

```python
def repeat(character):
    return ""
```

Run `uv run pytest`:

```
    def test_repeats_a_character_five_times():
>       assert repeat("a") == "aaaaa"
E       assert '' == 'aaaaa'
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

```python
def repeat(character):
    repeated = ""
    for _ in range(5):
        repeated += character
    return repeated
```

`range(5)` yields `0, 1, 2, 3, 4`. We don't use the loop variable, so we name it `_` by
convention. `+=` appends to the string. Run the tests again and they're green.

## Refactor

There's little to tidy in five lines, but it's worth naming the shape. The loop body does one
job, building up `repeated` one character at a time. We'll leave it as is for now: the next
requirement is going to change the function anyway, and we'd rather refactor once we know what
it needs to do. Re-run the tests to confirm nothing moved.

## Repeat for new requirements: a configurable count

Hard-coding `5` is no good. Let's pass the count in.

### Write the test first

In `iteration/v2/test_iteration.py`:

```python
from .iteration import repeat


def test_repeats_a_character_a_given_number_of_times():
    assert repeat("a", 5) == "aaaaa"


def test_repeats_zero_times_is_empty():
    assert repeat("a", 0) == ""
```

The `count == 0` test earns its keep: `range(0)` is empty, so the loop body never runs and we
get `""`. Testing the boundary now means we never wonder about it later.

### Try to run the test

The v1 function takes one argument, so calling it with two is what fails first. Run
`uv run pytest`:

```
E       TypeError: repeat() takes 1 positional argument but 2 were given
```

### Write the minimal amount of code for the test to run and check the failing test output

Add the `count` parameter but ignore it, returning an empty string so the tests run on the
value:

```python
def repeat(character, count):
    return ""
```

Run `uv run pytest`:

```
    def test_repeats_a_character_a_given_number_of_times():
>       assert repeat("a", 5) == "aaaaa"
E       assert '' == 'aaaaa'
```

The signature is right, the value is wrong. `test_repeats_zero_times_is_empty` passes already,
but only because our stub happens to return `""`, which is a fine reminder that one green test
proves nothing on its own.

### Write enough code to make it pass

In `iteration/v2/iteration.py`:

```python
def repeat(character, count):
    repeated = ""
    for _ in range(count):
        repeated += character
    return repeated
```

Both tests pass. The boundary case works for free: `range(0)` is empty, so the loop body never
runs and the zero test returns `""`.

### Refactor

With green tests we can make this idiomatic. In Python, multiplying a string by an integer
repeats it, so the whole function collapses to one line. In `iteration/v3/iteration.py`:

```python
def repeat(character, count):
    return character * count
```

This is the payoff of the safety net: we replaced the implementation entirely and the tests
told us, instantly, that behaviour was preserved. We lock it in with a `parametrize` table
covering the cases we care about, in `iteration/v3/test_iteration.py`:

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

Re-run the tests to confirm the one-liner handles every row.

## A note on building strings in loops

We used `repeated += character`. For a few iterations that's fine. But strings in Python are
**immutable**, so each `+=` builds a brand-new string. In a hot loop over thousands of
elements that's accidentally O(n^2). The interview-safe idiom is to collect parts in a list and
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
- **Test the zero/empty boundary**: `range(0)` runs the body zero times.
- **`str * int` repeats a string**; prefer idiomatic Python once tests have your back.
- **Strings are immutable**: build big strings with a list and `"".join(...)`, not `+=`.

Next: [Lists & slicing](lists-and-slicing.md).
