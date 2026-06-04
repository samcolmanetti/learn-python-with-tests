# Numbers

**[You can find all the code for this chapter here](number_basics/)**

> The code lives in `number_basics/` rather than `numbers/` on purpose: a top-level package
> named `numbers` would shadow Python's standard-library `numbers` module. A small but real
> interview-adjacent lesson — naming collisions with the stdlib bite.

Python's numeric model has a couple of features that come up constantly in interviews: two
different division operators, and integers that never overflow. Let's pin both down with tests.

## Write the test first

Start with the simplest possible thing — adding two numbers — just to get the loop going.
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

## Write enough code to make it pass

`number_basics/v1/number_basics.py`:

```python
def add(a, b):
    return a + b


```

```
1 passed
```

## Repeat for new requirements — division done right

Division is where Python surprises people. There are **two** operators:

- `/` is *true division* and always returns a `float`: `7 / 2 == 3.5`.
- `//` is *floor division* and rounds toward negative infinity: `7 // 2 == 3`, but
  `-7 // 2 == -4` (not `-3`!).

The built-in `divmod(a, b)` returns `(quotient, remainder)` together — exactly what you want
for digit-extraction and grid-coordinate problems. Let's specify a `divide` helper with tests
first:

```python
def test_divide_returns_quotient_and_remainder():
    assert divide(7, 2) == (3, 1)
    assert divide(10, 5) == (2, 0)


def test_divide_floors_toward_negative_infinity():
    assert divide(-7, 2) == (-4, 1)


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

Note `pytest.raises` — the idiomatic way to assert that something raises. The implementation:

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return divmod(a, b)
```

That `-7 // 2 == -4` behaviour is a genuine interview trap. Floor division pairs with a
remainder that always has the **same sign as the divisor**, so `divmod(-7, 2) == (-4, 1)`.
Memorise it.

## Big integers, no overflow

In many languages `50!` overflows a 64-bit integer and silently wraps. Python integers have
**arbitrary precision** — they grow as large as memory allows. We can assert that directly:

```python
def test_factorial_uses_arbitrary_precision():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert len(str(factorial(50))) == 65  # 50! is a 65-digit number


def test_factorial_rejects_negatives():
    with pytest.raises(ValueError):
        factorial(-1)
```

```python
def factorial(n):
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

No special "big integer" type, no overflow checks — it just works. This is a quiet superpower
in interviews: you never have to worry about integer overflow in Python.

## Wrapping up

- **`/` is float division, `//` is floor division.** `divmod` gives you quotient and remainder
  in one call.
- **Floor division rounds toward negative infinity**, and the remainder takes the divisor's
  sign — `divmod(-7, 2) == (-4, 1)`.
- **Python integers never overflow.** Factorials, big sums, and bit tricks on huge numbers are
  all safe.
- **`pytest.raises`** is how you assert on error paths.

Next: [Iteration](iteration.md).
