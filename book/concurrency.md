# Concurrency

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/concurrency)**

Python gives you two ways to do many things at once without writing thread-management code by hand: a thread pool for I/O-bound work, and `asyncio` for coroutines on a single thread. We'll reach for both test-first, and along the way meet the GIL, the thing that decides which of them actually helps you.

## Write the test first

Start with the smallest piece of work we can run concurrently: a pure function that squares a number. Pure means same input, same output, no shared state, which is exactly what makes it safe to run on many threads at once.

Put this in `concurrency/test_concurrency.py`:

```python
from concurrency import parallel_map


def test_parallel_map_preserves_order():
    assert parallel_map([1, 2, 3, 4]) == [1, 4, 9, 16]
```

We want `parallel_map` to square every number, possibly on different threads, and hand back the results. The order matters here: even though the threads may finish in any order, we expect the output lined up with the input.

## Try to run the test

There's no `parallel_map` yet, so the import is the first thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'parallel_map' from 'concurrency.concurrency'
```

Nothing to import. The error points at where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Let's write a `parallel_map` that runs but returns the wrong thing. We want to watch it fail on the value, not on a missing name, so we know the test is checking what we think it is.

```python
from __future__ import annotations


def parallel_map(numbers: list[int], workers: int = 4) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_parallel_map_preserves_order():
>       assert parallel_map([1, 2, 3, 4]) == [1, 4, 9, 16]
E       assert [] == [1, 4, 9, 16]
E         
E         Right contains 4 more items, first extra item: 1
```

The test runs and fails on the value. That's the right kind of failure.

## Write enough code to make it pass

Now do the work concurrently. The standard library's `concurrent.futures.ThreadPoolExecutor` is a pool of worker threads with a `map` method that applies a function to every item, spreading the calls across the pool.

```python
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor


def square(n: int) -> int:
    return n * n


def parallel_map(numbers: list[int], workers: int = 4) -> list[int]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(square, numbers))
```

Run the tests and they're green.

The `with` block opens the pool and, on exit, waits for every task to finish and shuts the threads down. **`executor.map` returns results in input order, no matter which thread finishes first**, so we don't have to sort anything to keep the output lined up with the input. That ordering guarantee is what makes the test deterministic instead of a coin flip.

## Refactor

There's little to tidy in a few lines, but it's worth naming the shape. We pulled `square` out as a top-level function rather than a lambda, because the thread pool needs to call it by name, and a named function reads better in the test too. The `with` statement is doing the cleanup we'd otherwise write by hand (`shutdown(wait=True)`), so we lean on it. Re-run the tests to confirm nothing moved.

### But wait, does this actually run in parallel?

Here's the honest answer, and it's the most important idea in the chapter. CPython has a *Global Interpreter Lock*, the GIL, a single lock that lets only one thread execute Python bytecode at a time. So squaring numbers on four threads does **not** run four times faster. For CPU-bound work like arithmetic, the GIL means threads take turns and you get no speedup (sometimes a small slowdown from the overhead).

So why bother with threads at all? Because the GIL is released while a thread waits on I/O: a network request, a disk read, a database call. While one thread is blocked waiting for bytes to arrive, the others can run. **Threads in Python overlap waiting, not computing.** That's why `ThreadPoolExecutor` is the right tool for I/O-bound work (fetching twenty URLs at once) and the wrong tool for crunching numbers (reach for `ProcessPoolExecutor` or `multiprocessing` there, which sidestep the GIL with separate processes).

We square numbers in the tests only because it's pure and instant, which keeps the suite fast and deterministic. In real code, picture each `square` as a slow network call instead.

## Repeat for new requirements

Threads aren't the only game in town. `asyncio` runs many coroutines on a *single* thread using an event loop: a coroutine runs until it hits an `await`, hands control back to the loop, and the loop runs something else while the first one waits. No threads, no GIL contention, one thread cooperating with itself.

Our next requirement is a synchronous `fetch_all` that, given a list of numbers, runs an async pipeline and returns each number squared. Think of each "fetch" as an awaited I/O call that we're standing in for with arithmetic.

### Write the test first

The point of `fetch_all` is that ordinary, non-async code can call it and get a plain list back, without the caller ever touching the event loop.

```python
import asyncio

from concurrency import fetch_all


def test_fetch_all():
    assert fetch_all([2, 3, 4]) == [4, 9, 16]
```

### Try to run the test

`fetch_all` doesn't exist, so the import breaks again:

```
ImportError: cannot import name 'fetch_all' from 'concurrency.concurrency'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the test runs and fails on the value:

```python
def fetch_all(numbers: list[int]) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_fetch_all():
>       assert fetch_all([2, 3, 4]) == [4, 9, 16]
E       assert [] == [4, 9, 16]
E         
E         Right contains 3 more items, first extra item: 4
```

Failing on the values, same as before. Good.

### Write enough code to make it pass

Three pieces. A coroutine `fetch_value` that does the awaited work for one number. A coroutine `gather_values` that runs many of them concurrently with `asyncio.gather`. And the synchronous `fetch_all` that crosses from normal code into async code with `asyncio.run`.

```python
import asyncio


async def fetch_value(n: int) -> int:
    await asyncio.sleep(0)  # yield to the event loop without a real delay
    return n * n


async def gather_values(numbers: list[int]) -> list[int]:
    return await asyncio.gather(*(fetch_value(n) for n in numbers))


def fetch_all(numbers: list[int]) -> list[int]:
    return asyncio.run(gather_values(numbers))
```

The tests pass.

Three things to name here. `async def` makes a *coroutine function*: calling it doesn't run the body, it returns a coroutine you have to `await` or hand to the loop. `await asyncio.sleep(0)` is the cheapest way to yield control back to the loop, no real delay, so a coroutine that has no actual I/O still cooperates (and our tests don't flake on timing). And **`asyncio.run` is the one synchronous call that starts an event loop, runs your top coroutine to completion, and tears the loop down.** It's the door between the ordinary world and the async one.

`asyncio.gather` schedules every coroutine on the loop at once and returns their results **in the order you passed them**, not the order they finished, which is why the list comes back lined up just like `executor.map` did.

### Refactor

The code is already small, but let's tighten the test so it documents the two halves of what we built, the coroutine on its own and the gather step, not just the synchronous wrapper. We can run a coroutine directly from a sync test with `asyncio.run`:

```python
def test_fetch_value_coroutine():
    assert asyncio.run(fetch_value(6)) == 36


def test_gather_values_preserves_order():
    assert asyncio.run(gather_values([1, 2, 3])) == [1, 4, 9]
```

Both pass as-is, because the implementation already handles them. **`asyncio.run` is also how you test a coroutine: call it, await it to completion, assert on the plain result.** No special test framework, no event-loop fixture, just one function that drives the coroutine and gives you back a value. Re-run `uv run pytest` to confirm everything's still green.

## Wrapping up

- **The GIL lets only one thread run Python bytecode at a time**, so threads don't speed up CPU-bound work. They help I/O-bound work because the GIL is released while a thread waits.
- **`ThreadPoolExecutor` maps a function over inputs on a pool of threads**, and `executor.map` returns results in input order, which keeps concurrent code testable without sorting.
- **`asyncio` runs coroutines on one thread with an event loop.** `async def` defines a coroutine, `await` yields to the loop, and `asyncio.gather` runs many at once and returns results in order.
- **`asyncio.run` is the bridge**: it runs a top-level coroutine from synchronous code, and it's also the simplest way to test a coroutine, call it and assert on the result.

Next: [Mocking](mocking.md), where we replace slow or external collaborators (like the network calls these threads and coroutines were standing in for) with fakes we control.
