# Numbers

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/number_basics)**

> The code lives in `number_basics/` rather than `numbers/` on purpose. A top-level package
> named `numbers` would shadow Python's standard-library `numbers` module. That's a small but
> real interview-adjacent lesson: naming collisions with the stdlib bite.

Python's numeric model has a couple of features that come up constantly in interviews: two
different division operators, and integers that never overflow. Let's pin both down with tests.

## Write the test first

Start with the simplest possible thing, adding two numbers, just to get the loop going.

`number_basics/v1/test_number_basics.py`:

```python
from .number_basics import add


def test_adds_two_numbers():
    assert add(2, 2) == 4
```

## Try to run the test

```
ImportError: cannot import name 'add' from 'number_basics.v1.number_basics'
```

We've imported `add` from a module that doesn't define it yet, so the import is the first thing
to break. Listen to the error: it's telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it an `add` that returns a stub `0`. We're not solving anything yet. We just want the test
to run so we can watch it fail on the value, which proves the test checks what we think it does.

`number_basics/v1/number_basics.py`:

```python
def add(a, b):
    return 0
```

Run `uv run pytest`:

```
    def test_adds_two_numbers():
>       assert add(2, 2) == 4
E       assert 0 == 4
E        +  where 0 = add(2, 2)
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

```python
def add(a, b):
    return a + b
```

Run the tests again and they're green.

## Refactor

There's nothing to tidy in a one-line function. The point of the cycle was to get the loop
moving, and we have. From here on each new requirement gets the same treatment.

## Division done right

Our next requirement is division, and division is where Python surprises people. There are
**two** operators:

- `/` is *true division* and always returns a `float`: `7 / 2 == 3.5`.
- `//` is *floor division* and rounds toward negative infinity: `7 // 2 == 3`, but
  `-7 // 2 == -4` (not `-3`).

The built-in `divmod(a, b)` returns `(quotient, remainder)` together, which is exactly what you
want for digit-extraction and grid-coordinate problems.

### Write the test first

We'll specify a `divide` helper that wraps `divmod` and guards against dividing by zero. The
tests move to `number_basics/v2/test_number_basics.py`:

```python
import pytest

from .number_basics import add, divide, factorial


def test_divide_returns_quotient_and_remainder():
    assert divide(7, 2) == (3, 1)
    assert divide(10, 5) == (2, 0)


def test_divide_floors_toward_negative_infinity():
    assert divide(-7, 2) == (-4, 1)


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

Note `pytest.raises`: it's the idiomatic way to assert that something raises. The
`test_divide_floors_toward_negative_infinity` case is the one that earns its keep, since it pins
down the rounding behaviour most people get wrong.

### Try to run the test

```
ImportError: cannot import name 'divide' from 'number_basics.v2.number_basics'
```

Same shape of failure as before. The name doesn't exist yet.

### Write the minimal amount of code for the test to run and check the failing test output

Stub `divide` so it returns a fixed tuple. We want the tests to run and fail on the values.

```python
def divide(a, b):
    return (0, 0)
```

Run `uv run pytest`:

```
    def test_divide_returns_quotient_and_remainder():
>       assert divide(7, 2) == (3, 1)
E       assert (0, 0) == (3, 1)
E         At index 0 diff: 0 != 3
```

Two of the three tests fail on the value, and `test_divide_by_zero_raises` fails because the stub
never raises. Good, now let's make them all pass for the right reason.

### Write enough code to make it pass

Guard zero first, then hand the work to `divmod`:

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return divmod(a, b)
```

The tests pass.

That `-7 // 2 == -4` behaviour is a genuine interview trap. Floor division pairs with a remainder
that always has the **same sign as the divisor**, so `divmod(-7, 2) == (-4, 1)`. Memorise it.

### Refactor

The body is already three lines, so there's nothing to extract. It's worth naming the shape,
though: we let the standard library do the arithmetic and only added the one guard our tests
asked for. Re-run the tests to confirm nothing moved.

## Big integers, no overflow

Our last requirement shows off something Python gives you for free. In many languages `50!`
overflows a 64-bit integer and silently wraps. Python integers have **arbitrary precision**: they
grow as large as memory allows.

### Write the test first

```python
def test_factorial_uses_arbitrary_precision():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert len(str(factorial(50))) == 65  # 50! is a 65-digit number


def test_factorial_rejects_negatives():
    with pytest.raises(ValueError):
        factorial(-1)
```

The `len(str(factorial(50))) == 65` assertion is the interesting one: it would be impossible to
satisfy in a language that caps integers at 64 bits.

### Try to run the test

```
ImportError: cannot import name 'factorial' from 'number_basics.v2.number_basics'
```

No `factorial` yet.

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
def factorial(n):
    return 0
```

Run `uv run pytest`:

```
    def test_factorial_uses_arbitrary_precision():
>       assert factorial(5) == 120
E       assert 0 == 120
E        +  where 0 = factorial(5)
```

Failing on the value, as expected. `test_factorial_rejects_negatives` also fails, because the
stub returns `0` instead of raising.

### Write enough code to make it pass

Reject negatives, then multiply up from `2`:

```python
def factorial(n):
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

Green.

No special "big integer" type, no overflow checks, it just works. The loop starts at `2` because
multiplying by `1` would be a no-op, and `factorial(0)` falls out correctly: the range is empty,
so `result` stays `1`.

### Refactor

There's nothing to tidy in the algorithm. The thing worth noticing is what we *didn't* write: no
overflow guard, no widening, no big-number library. That's a quiet advantage in interviews,
because you never have to worry about integer overflow in Python. Re-run the tests.

## Wrapping up

- **`/` is float division, `//` is floor division**, and `divmod` gives you quotient and
  remainder in one call.
- **Floor division rounds toward negative infinity**, and the remainder takes the divisor's sign:
  `divmod(-7, 2) == (-4, 1)`.
- **Python integers never overflow.** Factorials, big sums, and bit tricks on huge numbers are
  all safe.
- **`pytest.raises`** is how you assert on error paths.

Next: [Iteration](iteration.md).
</content>
</invoke>
