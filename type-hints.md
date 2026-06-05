# Type hints

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/type_hints)**

Type hints are annotations that say what a function takes and returns. Python doesn't enforce them at runtime, so the code runs exactly the same with or without them. What changes is that a type checker and the next human to read your code can see the intent.

That last point is the whole reason we bother. The annotation is a sentence the reader doesn't have to reconstruct from the body.

Our tests in this chapter look a little different from the rest of the book. Because hints change nothing at runtime, there's no clever behaviour to pin down. We assert the functions still do their job, and we lean on the annotations to document what that job is. The interesting part is in the prose, not the asserts.

## Write the test first

Start with the smallest possible function: take a name, return a greeting. We'll put it in `type_hints/annotations.py` and test it from `type_hints/test_annotations.py`.

```python
from .annotations import greet


def test_greet():
    assert greet("Ada") == "Hello, Ada"
```

Nothing here mentions types yet. The test pins the behaviour. The hints are about to go on the function, where they belong.

## Try to run the test

Run `uv run pytest`. We're importing `greet` from a module that doesn't define it, so the import is what breaks first:

```
type_hints/test_annotations.py:1: in <module>
    from .annotations import (
E   ImportError: cannot import name 'greet' from 'type_hints.annotations'
```

No function, no anything. The error is pointing us at the first thing to write.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `greet` that has the right shape, the right annotations, and the wrong body. I know returning `""` feels pointless when the real one-liner is right there, but with TDD we want to watch the test fail on the value first, so we know the test actually checks what we think it does.

```python
from __future__ import annotations


def greet(name: str) -> str:
    return ""
```

The `name: str` says the parameter is a string. The `-> str` says the function hands back a string. That's the core syntax: a colon and a type for each parameter, an arrow and a type for the return.

Run `uv run pytest`:

```
    def test_greet():
>       assert greet("Ada") == "Hello, Ada"
E       AssertionError: assert '' == 'Hello, Ada'
E
E         - Hello, Ada
```

It fails on the value, not on a missing name. That's the failure we wanted.

The `from __future__ import annotations` at the top earns its keep in a minute, when we annotate with `list[int]`. We're on Python 3.9 here, and without that import the subscript would blow up at import time. With it, every annotation is stored as a plain string and never evaluated, so `list[int]` is fine on 3.9. Put the line at the top of every file in this chapter and forget about it.

## Write enough code to make it pass

The smallest real body:

```python
from __future__ import annotations


def greet(name: str) -> str:
    return "Hello, " + name
```

Run the tests and they're green.

Notice that nothing checked the type. If I call `greet(42)`, Python will happily try `"Hello, " + 42`, blow up with a `TypeError`, and the `: str` annotation won't have lifted a finger to stop me. **Hints are documentation, not guard rails.** The thing that reads them is a separate type checker like `mypy` or `pyright`, which you run as a tool. Python itself ignores them at runtime.

## Refactor

There's nothing to tidy in two lines. The point of this first cycle was the syntax, and we have it: `name: str` on the way in, `-> str` on the way out. Re-run the tests to confirm nothing moved, and let's annotate something with more shape to it.

## Repeat for new requirements

`str` is the easy case. The annotations that actually earn their keep describe collections, because "a list" tells you almost nothing and "a list of ints" tells you a lot.

### Write the test first

A function that sums a list of integers. The behaviour is obvious, so we add the empty case straight away to keep ourselves honest.

```python
from .annotations import total


def test_total():
    assert total([1, 2, 3, 4]) == 10


def test_total_empty():
    assert total([]) == 0
```

### Try to run the test

`total` doesn't exist yet, so the import fails again:

```
E   ImportError: cannot import name 'total' from 'type_hints.annotations'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the test runs and fails on the value:

```python
def total(numbers: list[int]) -> int:
    return 0
```

Here's the payoff for that `__future__` import. `list[int]` is a *generic*: the `list` is the container, and the `[int]` inside the brackets is the type of its elements. It reads as "a list of ints" and that's exactly what it means. The return `-> int` says we hand back a single integer.

Run `uv run pytest`:

```
    def test_total():
>       assert total([1, 2, 3, 4]) == 10
E       assert 0 == 10
E        +  where 0 = total([1, 2, 3, 4])
```

`test_total_empty` passes already, because an empty list really does sum to `0`, which is what our stub returns by accident. The non-empty case fails on the value, which is the one we care about.

### Write enough code to make it pass

```python
def total(numbers: list[int]) -> int:
    running = 0
    for number in numbers:
        running += number
    return running
```

Green.

The annotation didn't change the loop one bit. What it bought us is that a reader (and a checker) knows `numbers` holds ints, so `running += number` is adding numbers, not concatenating strings or something stranger. If somebody later passes a list of strings, the checker complains before the code ever runs.

### Refactor

We could write `return sum(numbers)` and call it a day, and in real code I would. The loop is here so the annotation has a body to sit on. Leave it; the test is green either way, and re-running confirms it.

## Repeat for new requirements

So far every function always returns something. Plenty don't. A lookup misses, a parse fails, an empty input has no sensible answer. For those we need a type that says "a value, or nothing".

### Write the test first

Take a full name, return the first word. If the string is empty (or just spaces), there's no first word, so we return `None`.

```python
from .annotations import first_name


def test_first_name_returns_first_word():
    assert first_name("Grace Hopper") == "Grace"


def test_first_name_returns_none_for_empty():
    assert first_name("   ") is None
```

The second test is the one that forces the issue. A function that can return `None` needs to say so in its signature, or every caller is one missed check away from an `AttributeError`.

### Try to run the test

```
E   ImportError: cannot import name 'first_name' from 'type_hints.annotations'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it returning `""`, which is wrong for both tests:

```python
from typing import Optional


def first_name(full_name: str) -> Optional[str]:
    return ""
```

`Optional[str]` is the new piece. It means "a `str`, or `None`". It comes from the `typing` module, which is the standard library's home for hint helpers. Under the hood `Optional[str]` is shorthand for `Union[str, None]`, "either a `str` or `None`", and `Optional` is just the common case of that written shorter.

Run `uv run pytest`:

```
    def test_first_name_returns_first_word():
>       assert first_name("Grace Hopper") == "Grace"
E       AssertionError: assert '' == 'Grace'
E
E         - Grace
```

Both tests fail on the value. `""` is neither `"Grace"` nor `None`, exactly as a stub should be.

### Write enough code to make it pass

```python
from typing import Optional


def first_name(full_name: str) -> Optional[str]:
    parts = full_name.split()
    if not parts:
        return None
    return parts[0]
```

Green. `split()` with no argument splits on runs of whitespace and drops empties, so `"   ".split()` is `[]`, and we return `None`.

The signature now tells the truth: this function gives you a `str` or it gives you `None`, and a caller who reads it knows to check before using the result. **`Optional[X]` is the honest annotation for anything that can come back empty.** A type checker will even flag a caller who forgets the check and treats the result as always a string.

### Refactor

Nothing to refactor in the body. One note on style: if you're on Python 3.10 or newer you can write `str | None` instead of `Optional[str]`, and many linters nudge you toward it. We're targeting 3.9, and `Optional` reads clearly, so we'll keep it. (`str | None` as a real runtime expression doesn't work on 3.9, which is one more reason `Optional` is the safe choice across versions.) Re-run the tests.

## Repeat for new requirements

One more shape worth naming: a dictionary. `dict` alone is as vague as `list` alone. The generic version takes two types in the brackets, one for the keys and one for the values.

### Write the test first

Count how many times each word appears.

```python
from .annotations import word_counts


def test_word_counts():
    assert word_counts(["a", "b", "a"]) == {"a": 2, "b": 1}


def test_word_counts_empty():
    assert word_counts([]) == {}
```

### Try to run the test

```
E   ImportError: cannot import name 'word_counts' from 'type_hints.annotations'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it returning an empty dict:

```python
def word_counts(words: list[str]) -> dict[str, int]:
    return {}
```

`dict[str, int]` is "a dict whose keys are strings and whose values are ints". The first type in the brackets is the key, the second is the value. So this signature reads as "give me a list of strings, get back a mapping from word to count", which is the whole function in one line.

Run `uv run pytest`:

```
    def test_word_counts():
>       assert word_counts(["a", "b", "a"]) == {"a": 2, "b": 1}
E       AssertionError: assert {} == {'a': 2, 'b': 1}
E
E         Right contains 2 more items:
E         {'a': 2, 'b': 1}
```

`test_word_counts_empty` passes (an empty input gives an empty dict, which our stub returns by luck), and the real case fails on the value.

### Write enough code to make it pass

```python
def word_counts(words: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
```

Green.

Look at the line `counts: dict[str, int] = {}`. That's a *variable annotation*, the same colon-and-type syntax we put on parameters, used on a local name instead. A bare `{}` could be a dict of anything, so we tell the reader and the checker that this one maps strings to ints from the moment it's created.

### Refactor

`collections.Counter` would do this whole function in a line, and it's what I'd reach for in real code. We wrote the loop out so the annotations had something to sit on, and the variable annotation had a place to demonstrate itself. The tests are green, so re-run them and leave the body as is.

## Wrapping up

- **Type hints are annotations Python ignores at runtime.** The code runs identically with or without them. A separate type checker (`mypy`, `pyright`) is what reads them and complains.
- **The syntax is a colon for parameters and variables, an arrow for the return**: `name: str`, `-> int`, `counts: dict[str, int] = {}`.
- **Built-in generics describe what's inside a container**: `list[int]`, `dict[str, int]`. On Python 3.9 they need `from __future__ import annotations` at the top of the file.
- **`Optional[X]` is the honest signature for anything that can return `None`.** It's `Union[X, None]` written shorter, and it forces callers to face the empty case.

Next: [Classes and dataclasses](classes-and-dataclasses.md), where these same annotations describe the fields of a type you define yourself.
