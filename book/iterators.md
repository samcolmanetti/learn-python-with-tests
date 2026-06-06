# Iterators

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/iterators)**

Every time you write `for x in something`, Python is quietly asking that something for an iterator
and pulling values out of it one at a time. In this chapter we'll build an iterator by hand so the
protocol is visible, then write the same idea as a generator and let `yield` do the bookkeeping.

## Write the test first

We want a `Countdown` that, given a number, hands back that number, then each smaller one, down to
`1`, then stops. The natural way to ask "what does it produce?" is to drop it into a `for` loop, or
just call `list` on it.

Put this in `iterators/test_iterators.py`:

```python
from iterators import Countdown


def test_countdown_yields_descending_values():
    assert list(Countdown(3)) == [3, 2, 1]
```

`list(Countdown(3))` iterates the object to exhaustion and collects what comes out. If our object
behaves like an iterator, this is the shortest way to pin down every value it produces.

## Try to run the test

There's no `Countdown` yet, so the import is the first thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'Countdown' from 'iterators.iterators'
```

No class, nothing to import. The error is telling us exactly where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Let's write a `Countdown` that *is* an iterator in shape but produces nothing. An iterator in
Python is any object with two methods: `__iter__`, which returns the iterator itself, and
`__next__`, which returns the next value or raises `StopIteration` when there are no more.

Our stub raises `StopIteration` straight away, so the countdown is empty:

```python
from __future__ import annotations


class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> Countdown:
        return self

    def __next__(self) -> int:
        raise StopIteration
```

I know an iterator that never yields anything feels pointless, but it lets the test run so we can
watch it fail on the values rather than on a missing name. Run `uv run pytest`:

```
    def test_countdown_yields_descending_values():
>       assert list(Countdown(3)) == [3, 2, 1]
E       assert [] == [3, 2, 1]
E         Right contains 3 more items, first extra item: 3
```

The test runs and fails on the value, not on an import. `list` asked our iterator for values, got
`StopIteration` immediately, and ended up with an empty list. That's the right kind of failure.

## Write enough code to make it pass

Now make `__next__` actually count down. Each call returns the current value and steps one lower.
When we hit zero there's nothing left, so we raise `StopIteration`.

```python
from __future__ import annotations


class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> Countdown:
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

Run the tests and they're green.

The shape here is the whole *iterator protocol*. `__iter__` returns something with a `__next__`
(here, `self`), and `__next__` either returns the next item or raises `StopIteration` to say "I'm
done". That `StopIteration` is what a `for` loop catches to know when to stop. **You never write
`for` against `StopIteration` yourself; the loop does it for you.**

## Repeat for new requirements

Let's pin the protocol down with a couple more tests. An empty countdown, and proof that `next`
raises `StopIteration` at the end rather than looping forever.

```python
def test_countdown_of_zero_is_empty():
    assert list(Countdown(0)) == []


def test_countdown_works_in_a_for_loop():
    seen = []
    for value in Countdown(2):
        seen.append(value)
    assert seen == [2, 1]


def test_countdown_next_raises_stopiteration_at_the_end():
    counter = Countdown(1)
    assert next(counter) == 1
    try:
        next(counter)
    except StopIteration:
        pass
    else:
        raise AssertionError("expected StopIteration")
```

These pass as-is, because the implementation already handles them. `Countdown(0)` returns `[]`
since `current` starts at `0` and `__next__` raises right away. The `for` loop test and the manual
`next` test are the same machinery the loop uses, spelled out. Run `uv run pytest` to confirm.

There's a wrinkle worth naming: because `Countdown` returns `self` from `__iter__` and mutates
`current`, it's a *one-shot* iterator. Loop over the same object twice and the second loop sees
nothing, because `current` is already `0`. The built-in `list` and `range` don't have this problem
because they hand back a *fresh* iterator each time you ask. That distinction (an iterable can be
asked for an iterator many times; an iterator is consumed once) is the part people trip on.

## Repeat for new requirements

Writing `__iter__`, `__next__`, and raising `StopIteration` by hand is a lot of ceremony for "count
down". Most of the time you want the lazy, one-value-at-a-time behaviour without the boilerplate,
and that's exactly what a *generator* gives you.

Our next requirement is a `fibonacci(count)` that yields the first `count` Fibonacci numbers,
starting `0, 1, 1, 2, 3, ...`.

### Write the test first

```python
def test_fibonacci_first_values():
    assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]
```

And add `fibonacci` to the import at the top of the test file:

```python
from iterators import Countdown, fibonacci
```

### Try to run the test

`fibonacci` doesn't exist, so the import breaks again:

```
ImportError: cannot import name 'fibonacci' from 'iterators.iterators'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `fibonacci` to produce nothing. `iter([])` is an iterator over an empty list, so calling
`list` on its result gives `[]`:

```python
def fibonacci(count: int) -> Iterator[int]:
    return iter([])
```

Run `uv run pytest`:

```
    def test_fibonacci_first_values():
>       assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]
E       assert [] == [0, 1, 1, 2, 3, 5, ...]
E         Right contains 7 more items, first extra item: 0
```

Failing on the values, same as the countdown stub did. Good.

### Write enough code to make it pass

Here's the trick: put a `yield` in the function body and it stops being a normal function. It
becomes a *generator function*, and calling it returns a generator (which is an iterator) instead
of running the body. The body only runs as values are pulled out, pausing at each `yield` and
resuming on the next `next`.

```python
def fibonacci(count: int) -> Iterator[int]:
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b
```

Run the tests and they pass.

Compare this to `Countdown`. There's no class, no `__iter__`, no `__next__`, and no `StopIteration`
to raise. **`yield` keeps the local variables `a` and `b` alive between calls for you, and running
off the end of the function raises `StopIteration` automatically.** The generator is the same lazy
behaviour as the hand-written iterator, with all the protocol plumbing generated for free. This is
why you almost never write `__next__` by hand in real code.

### Refactor

Nothing to tidy in four lines, but it's worth naming what we get for free. `fibonacci(7)` doesn't
compute seven numbers up front; each one is produced only when something asks for it. That laziness
is the point of generators, so let's lean on it.

## Repeat for new requirements

Because a generator is lazy, it doesn't actually need to know `count` at all. It can yield Fibonacci
numbers forever, and the caller decides when to stop. Let's add that, plus a way to take a fixed
number of values from it.

### Write the test first

```python
def test_fibonacci_forever_is_lazy():
    gen = fibonacci_forever()
    assert next(gen) == 0
    assert next(gen) == 1
    assert next(gen) == 1
    assert next(gen) == 2


def test_first_n_fibonacci_matches_the_eager_version():
    assert first_n_fibonacci(7) == [0, 1, 1, 2, 3, 5, 8]
```

The first test pulls four values out by hand to prove the generator is lazy: an infinite loop
inside it never hangs, because we only ask for what we need. Extend the import:

```python
from iterators import Countdown, fibonacci, fibonacci_forever, first_n_fibonacci
```

### Try to run the test

```
ImportError: cannot import name 'fibonacci_forever' from 'iterators.iterators'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub both so the module imports and the tests run:

```python
def fibonacci_forever() -> Iterator[int]:
    return iter([])


def first_n_fibonacci(count: int) -> list[int]:
    return []
```

Run `uv run pytest`. `test_fibonacci_forever_is_lazy` now fails because `next` on an empty iterator
raises `StopIteration`, and `first_n_fibonacci` fails on the empty list:

```
    assert next(gen) == 0
E   StopIteration
```

### Write enough code to make it pass

`fibonacci_forever` is the generator with the `while True` loop. For `first_n_fibonacci`, we don't
want to write a counting loop again. The standard library has `itertools.islice`, which takes the
first `n` values from any iterator, infinite or not, without us managing an index.

```python
from itertools import islice


def fibonacci_forever() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def first_n_fibonacci(count: int) -> list[int]:
    return list(islice(fibonacci_forever(), count))
```

The tests pass.

`islice(fibonacci_forever(), count)` walks the endless generator and stops after `count` items.
The generator never runs past what `islice` pulls, so an infinite producer plus a bounded consumer
is a normal, safe thing to write. **This is the payoff of laziness: a producer that has no end and a
consumer that decides where to stop, wired together with one `itertools` call.**

### Refactor

We could fold `range(count)` back into `fibonacci` and skip the infinite version, but keeping both
makes the point of the chapter: the lazy generator is the general one, and `islice` adapts it to
"give me the first N". `itertools` is full of these adapters (`takewhile`, `chain`, `count`,
`cycle`), and reaching for one beats hand-rolling another loop. Re-run the tests to confirm nothing
moved.

## Wrapping up

- **The iterator protocol is two methods**: `__iter__` returns the iterator, `__next__` returns the
  next value or raises `StopIteration`. A `for` loop is just that protocol with the `StopIteration`
  catch hidden.
- **An iterable can be asked for an iterator many times; an iterator is consumed once.** A class that
  returns `self` from `__iter__` is one-shot, which is why looping over it twice can come up empty.
- **A generator function (any function with `yield`) builds an iterator for you.** It keeps local
  state across pauses and raises `StopIteration` when the body ends, so you skip all the protocol
  boilerplate.
- **Generators are lazy**, so they can be infinite. Pair an endless generator with `itertools.islice`
  (or `takewhile`, `chain`, and friends) to take exactly what you need.

Next: [Comprehensions](comprehensions.md), where the same lazy iteration shows up as generator
expressions and the eager list, set, and dict comprehensions.
