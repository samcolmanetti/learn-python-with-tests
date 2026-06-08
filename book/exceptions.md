# Exceptions

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/exceptions)**

When input is bad, you want your code to stop and say so loudly, not return a `None` that some
caller forgets to check three functions later. In Python that "stop and say so" is an exception.
We'll build a `parse_age` function that raises on garbage input, give it a custom exception type,
and learn how `try`/`except`/`else`/`finally` and `pytest.raises` fit together.

## Write the test first

Start with the happy path so we have something to anchor on. A valid age string parses to an `int`.

```python
import pytest

from exceptions import parse_age


def test_parses_a_valid_age():
    assert parse_age("42") == 42
```

We've also imported `pytest` because we're about to need `pytest.raises`, but let's earn that.

## Try to run the test

Run `uv run pytest`. The module has no `parse_age` yet, so the import is the first thing to break:

```
ImportError: cannot import name 'parse_age' from 'exceptions.exceptions'
```

No function, nothing to call. The error is telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `parse_age` that returns a stub `0`. We want the test to run and fail on the value, which
proves the test checks what we think it does.

```python
from __future__ import annotations


def parse_age(raw):
    return 0
```

Run `uv run pytest`:

```
    def test_parses_a_valid_age():
>       assert parse_age("42") == 42
E       AssertionError: assert 0 == 42
E        +  where 0 = parse_age('42')
```

Failing on the value, not on a missing name. Good.

## Write enough code to make it pass

The simplest real thing is to turn the string into an `int`.

```python
from __future__ import annotations


def parse_age(raw):
    return int(raw)
```

Green. But `int("forty")` would blow up with a `ValueError`, and `int("-3")` would happily give us
a negative age. We haven't said anything about bad input yet, so let's write a test that does.

## Refactor

Nothing to tidy in one line. On to the interesting requirement.

## Repeat for new requirements

We want `parse_age` to *reject* non-numeric input instead of letting `int` raise whatever it
likes. The way you signal "this input is wrong" is the `raise` statement, and the way you assert
that a function raises is `pytest.raises`.

### Write the test first

```python
def test_rejects_non_numeric_age():
    with pytest.raises(Exception):
        parse_age("forty")
```

`pytest.raises(Exception)` is a context manager. The test passes only if the body raises something
that is an `Exception`. If the body runs to the end without raising, the test fails. We'll narrow
`Exception` to a specific type in a moment, but it's enough to drive the next step.

### Try to run the test

Run `uv run pytest`. Our current `parse_age("forty")` calls `int("forty")`, which raises a
`ValueError`, and a `ValueError` *is* an `Exception`, so this test passes by accident. That's not
the failure we want to see, so let me make the stub honest first: the minimal-code step here is a
`parse_age` that does **not** raise, so we can watch `pytest.raises` fail for the right reason.

### Write the minimal amount of code for the test to run and check the failing test output

```python
from __future__ import annotations


def parse_age(raw):
    return 0
```

Run `uv run pytest`:

```
    def test_rejects_non_numeric_age():
        with pytest.raises(Exception):
>           parse_age("forty")
E           Failed: DID NOT RAISE <class 'Exception'>
```

`DID NOT RAISE` is the message you'll see whenever a `pytest.raises` block finishes without an
exception. It's the exception-shaped version of `assert 0 == 42`: the test ran, and the thing we
expected to happen didn't. Now let's make it happen on purpose.

### Write enough code to make it pass

Check the input with `str.isdigit` and `raise` when it's wrong.

```python
from __future__ import annotations


def parse_age(raw):
    if not raw.isdigit():
        raise ValueError(f"age must be digits, got {raw!r}")
    return int(raw)
```

Green. `raise` takes an exception *instance*, here a `ValueError` carrying a message. When Python
hits `raise`, it stops the function on the spot and unwinds until something catches it. Our test
catches it with `pytest.raises`.

### Refactor

Both tests pass, and the function reads cleanly. **The `{raw!r}` in the f-string calls `repr`, so
the message shows `'forty'` with quotes** rather than a bare `forty`, which makes "is this an empty
string or whitespace?" obvious in a log. That's worth keeping. Move on.

## Repeat for new requirements

A `ValueError` is fine, but every caller now has to catch `ValueError` and hope it came from us and
not from some unrelated `int()` deep in the standard library. We want our own type that means
exactly "this failed *our* validation", and we want it to carry which field was bad. This is a
*custom exception class*.

### Write the test first

```python
def test_validation_error_carries_the_field():
    with pytest.raises(ValidationError) as exc_info:
        parse_age("forty")
    assert exc_info.value.field == "age"
```

Two new things. We pass our own `ValidationError` to `pytest.raises` so the test only passes if
*that specific type* is raised. And `as exc_info` captures the raised exception so we can inspect
it after the block: `exc_info.value` is the actual exception instance, and we read a `.field`
attribute off it.

### Try to run the test

Run `uv run pytest`. `ValidationError` doesn't exist yet, so the import fails before any test runs:

```
ImportError: cannot import name 'ValidationError' from 'exceptions.exceptions'
```

### Write the minimal amount of code for the test to run and check the failing test output

Define `ValidationError` as a plain subclass of `Exception`, but keep `parse_age` raising the old
`ValueError`. That way the test runs and fails because the *wrong type* came out, which proves
`pytest.raises(ValidationError)` is actually checking the type.

```python
from __future__ import annotations


class ValidationError(Exception):
    pass


def parse_age(raw):
    if not raw.isdigit():
        raise ValueError(f"age must be digits, got {raw!r}")
    return int(raw)
```

Run `uv run pytest`:

```
    def parse_age(raw):
        if not raw.isdigit():
>           raise ValueError("bad age")
E           ValueError: bad age
```

The `ValueError` escaped because `pytest.raises(ValidationError)` only swallows a `ValidationError`.
Anything else propagates and fails the test. That's the type-checking we wanted.

### Write enough code to make it pass

Make `ValidationError` accept a `field` and store it, then raise it from `parse_age`. **A custom
exception is just a class that inherits from `Exception`**, and you can give it any `__init__` you
like, as long as you pass the message up to `super().__init__`.

```python
from __future__ import annotations


class ValidationError(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field


def parse_age(raw):
    if not raw.isdigit():
        raise ValidationError(f"age must be digits, got {raw!r}", field="age")
    return int(raw)
```

Green. `super().__init__(message)` is what makes `str(err)` print the message, so we don't lose the
human-readable part by adding our own attribute.

### Refactor

The earlier `test_rejects_non_numeric_age` still uses `pytest.raises(Exception)`, which now passes
because `ValidationError` is an `Exception`. Tighten it to the real type so the test says what it
means:

```python
def test_rejects_non_numeric_age():
    with pytest.raises(ValidationError):
        parse_age("forty")
```

Re-run the tests. Still green, and now every assertion names the exact type we expect.

## Repeat for new requirements

There's a second kind of bad age: a number that's a perfectly good integer but absurd, like `200`.
We'll reject anything above a maximum, and this time we'll assert on the *message* with the `match`
argument to `pytest.raises`.

### Write the test first

```python
def test_rejects_age_above_maximum():
    with pytest.raises(ValidationError, match="above the maximum"):
        parse_age("200")
```

`match` takes a regular expression and searches the exception's string for it. So this test now
checks two things: that a `ValidationError` is raised, and that its message contains
`above the maximum`. It's a guard against catching the *right type for the wrong reason*.

### Try to run the test

Run `uv run pytest`. `parse_age("200")` passes `isdigit`, so right now it just returns `200` and
never raises:

```
    def test_rejects_age_above_maximum():
        with pytest.raises(ValidationError, match="above the maximum"):
>           parse_age("200")
E           Failed: DID NOT RAISE <class 'exceptions.exceptions.ValidationError'>
```

Same `DID NOT RAISE` as before, now naming our own type.

### Write the minimal amount of code for the test to run and check the failing test output

We've already seen `DID NOT RAISE` is the right failure, so there's no separate wrong-stub to write
here: the function genuinely doesn't raise yet, which is the failing state we want. Straight to the
fix.

### Write enough code to make it pass

Parse the integer, then range-check it.

```python
from __future__ import annotations

MAX_AGE = 150


class ValidationError(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field


def parse_age(raw):
    if not raw.isdigit():
        raise ValidationError(f"age must be digits, got {raw!r}", field="age")
    age = int(raw)
    if age > MAX_AGE:
        raise ValidationError(f"age {age} is above the maximum of {MAX_AGE}", field="age")
    return age
```

Green. The message includes the literal phrase `above the maximum`, so `match` finds it. Note we
only call `int(raw)` after `isdigit` has cleared it, so the conversion can't throw.

### Refactor

`parse_age` now has a single, readable shape: validate, convert, validate again, return. Pull the
type annotations back on for the reader, since the code is settled:

```python
def parse_age(raw: str) -> int:
    if not raw.isdigit():
        raise ValidationError(f"age must be digits, got {raw!r}", field="age")
    age = int(raw)
    if age > MAX_AGE:
        raise ValidationError(f"age {age} is above the maximum of {MAX_AGE}", field="age")
    return age
```

Re-run the tests. Green.

## Repeat for new requirements

Now the part of exceptions people get wrong: handling them. We want a `parse_record` that wraps a
parse, writes an audit line whether it succeeds or fails, and still lets the failure propagate to
the caller. That's the job of `try`/`except`/`else`/`finally`, and it's the cleanest demonstration
of what each clause is for.

### Write the test first

```python
def test_record_logs_acceptance_then_done():
    audit: list[str] = []
    assert parse_record("30", audit) == 30
    assert audit == ["accepted 30", "done"]


def test_record_logs_rejection_then_done_and_reraises():
    audit: list[str] = []
    with pytest.raises(ValidationError):
        parse_record("nope", audit)
    assert audit == ["rejected 'nope': age", "done"]
```

The two tests pin down the whole behaviour. On success the log reads `accepted 30` then `done`. On
failure it reads `rejected 'nope': age` then `done`, **and** the `ValidationError` still escapes
(that's why the second test wraps the call in `pytest.raises`). The `done` line shows up in both,
because `finally` runs no matter what.

### Try to run the test

Run `uv run pytest`. No `parse_record` yet:

```
ImportError: cannot import name 'parse_record' from 'exceptions.exceptions'
```

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `parse_record` that just forwards to `parse_age` and logs nothing. It'll return the right
number and re-raise correctly, so the *value* and *raising* are fine, but the audit list stays
empty, which is the failure we want to see.

```python
def parse_record(raw, audit):
    return parse_age(raw)
```

Run `uv run pytest`:

```
    def test_record_logs_acceptance_then_done():
        audit = []
        assert parse_record("30", audit) == 30
>       assert audit == ["accepted 30", "done"]
E       AssertionError: assert [] == ['accepted 30', 'done']
E         Right contains 2 more items, first extra item: 'accepted 30'
```

The empty list versus the expected two lines tells us exactly what's missing: the logging.

### Write enough code to make it pass

Wrap the parse. `except` catches the failure, logs it, and `raise` with no argument re-raises *the
same exception* so the caller still sees it. `else` runs only when the `try` block didn't raise.
`finally` runs in both cases.

```python
def parse_record(raw, audit):
    try:
        age = parse_age(raw)
    except ValidationError as err:
        audit.append(f"rejected {raw!r}: {err.field}")
        raise
    else:
        audit.append(f"accepted {age}")
        return age
    finally:
        audit.append("done")
```

Green. Walk the two paths. On `"30"`: `parse_age` succeeds, the `except` is skipped, `else` logs
`accepted 30`, then `finally` logs `done`. On `"nope"`: `parse_age` raises, `except` logs
`rejected 'nope': age` and re-raises, then `finally` still runs and logs `done` on the way out.

### Why `else` and not just more code in `try`?

A fair objection: why put `audit.append(f"accepted {age}")` in an `else` instead of right after the
`parse_age` call inside `try`? Because anything inside `try` is also guarded by the `except`. If the
append itself somehow raised a `ValidationError`, the `except` would catch it and mislabel a *logging*
failure as a *validation* failure. **`else` holds the code that should run only on success and
should not be guarded by the `except`.** It keeps the `try` block down to exactly the line that can
fail.

### Refactor

The bare `raise` is the detail worth naming. Writing `raise` with no argument re-raises the
exception currently being handled, preserving its original traceback. If you wrote
`raise err` instead it would still work, but a plain `raise` is the idiom for "log it and let it
keep going". Add the annotations now that the shape is settled:

```python
def parse_record(raw: str, audit: list[str]) -> int:
    try:
        age = parse_age(raw)
    except ValidationError as err:
        audit.append(f"rejected {raw!r}: {err.field}")
        raise
    else:
        audit.append(f"accepted {age}")
        return age
    finally:
        audit.append("done")
```

One thing that surprises people: the `finally` block runs even though `else` already hit `return`.
Python holds the return value, runs `finally`, and *then* returns. (If `finally` itself returned a
value it would override that, which is a good reason to never `return` from a `finally`.) Re-run the
tests one last time. Green.

## Wrapping up

- **`raise` signals "this is wrong" and stops the function**, unwinding until something catches it.
  You raise an instance, usually with a message.
- **A custom exception is a class that inherits from `Exception`.** Give it the `__init__` you want,
  pass the message to `super().__init__`, and callers can catch your type specifically instead of a
  generic `ValueError`.
- **`pytest.raises(SomeError)` asserts a block raises that type**, `match="..."` checks the message
  with a regex, and `as exc_info` captures the instance so you can read its attributes.
- **`except` catches, `else` runs only on success, `finally` runs always.** A bare `raise` inside
  `except` re-raises the current exception with its traceback intact.
- **`DID NOT RAISE`** is the failing output you'll see whenever a `pytest.raises` block finishes
  without throwing. Treat it like any other red test: the thing you expected didn't happen.
