# Iteration

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/iteration)**

To do something repeatedly in Python you reach for `for` (usually over a `range` or directly
over a collection) or `while`. We'll build a small function test-first and then refactor it
into idiomatic Python.

## Write the test first

We want a function that repeats a character five times. Start with the test in
`test_iteration.py`:

```python
from iteration import repeat


def test_repeats_a_character_five_times():
    assert repeat("a") == "aaaaa"
```

## Try to run the test

We've imported `repeat` from a module that doesn't define it yet, so the import is the first
thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'repeat' from 'iteration'
```

Listen to the error: there's no function, so that's where we start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `repeat` that takes the argument and returns an empty string. We're not solving
anything yet. We just want the test to run so we can watch it fail on the value, which proves
the test checks what we think it does. In `iteration.py`:

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

`range(5)` yields `0, 1, 2, 3, 4`, so the body runs five times. We don't use the loop variable,
so we name it `_` by convention. `+=` appends to the string. Run the tests again and they're
green.

## How a for loop works

If you've come from a C-style language, you might expect to manage an index by hand: set a
counter to zero, check it against a length, bump it each pass. Python's `for` loop doesn't work
like that. It walks an *iterable* one element at a time, binding each element to the loop
variable for you. There's no index and no counter to get wrong.

An iterable is anything you can step through. A list is iterable, and the loop variable takes
each element in turn:

```python
for item in [10, 20, 30]:
    print(item)
# prints 10, then 20, then 30
```

A string is iterable too, and stepping through it yields its characters one at a time:

```python
for letter in "hi":
    print(letter)
# prints "h", then "i"
```

So `for x in something` is the same shape every time: `something` hands over its elements one by
one, and `x` is bound to each.

`range` is just one more iterable. It doesn't build a list in memory; it produces numbers on
demand, which is why it's handy for counting. It comes in three forms:

- `range(stop)` counts from `0` up to but *not* including `stop`. `range(5)` gives
  `0, 1, 2, 3, 4`.
- `range(start, stop)` lets you pick where to begin. `range(2, 6)` gives `2, 3, 4, 5`. The stop
  is always excluded, so to count `2` through `6` *inclusive* you push the stop one past it:
  `range(2, 7)`. (That `+ 1` on the stop is the trick behind `range(1, count + 1)` and friends.)
- `range(start, stop, step)` takes a stride. `range(0, 10, 2)` gives the evens `0, 2, 4, 6, 8`.

That's the whole loop in our `repeat`: `range(count)` produces the right number of values, and we
ignore each one because we only care about how *many* times the body runs.

When you do need the position as well as the element, `enumerate` pairs an index with each value:
`for index, item in enumerate(["a", "b"]):` binds two names at once and gives you `(0, "a")` then
`(1, "b")`. And when you're looping until a condition rather than over a collection, that's the job
of `while`: `while n > 0:` runs its body again and again until `n` stops being positive. You'll
reach for `while` far less often than `for`.

## Refactor

There's little to tidy in five lines, but it's worth naming the shape. The loop body does one
job, building up `repeated` one character at a time. We'll leave it as is for now: the next
requirement is going to change the function anyway, and we'd rather refactor once we know what
it needs to do. Re-run the tests to confirm nothing moved.

## Repeat for new requirements: a configurable count

Hard-coding `5` is no good. Let's pass the count in.

### Write the test first

In `test_iteration.py`:

```python
from iteration import repeat


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

In `iteration.py`:

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
repeats it, so the whole function collapses to one line. In `iteration.py`:

```python
def repeat(character, count):
    return character * count
```

This is the payoff of the safety net: we replaced the implementation entirely and the tests
told us, instantly, that behaviour was preserved. We lock it in with a `parametrize` table
covering the cases we care about, in `test_iteration.py`:

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

- **`for x in iterable`** walks any iterable (list, string, `range`) one element at a time,
  binding each to the loop variable; name the unused variable `_`.
- **`range` is just one iterable**: `range(stop)`, `range(start, stop)`, and
  `range(start, stop, step)`, with the stop always excluded.
- **Test the zero/empty boundary**: `range(0)` runs the body zero times.
- **`str * int` repeats a string**; prefer idiomatic Python once tests have your back.
- **Strings are immutable**: build big strings with a list and `"".join(...)`, not `+=`.
