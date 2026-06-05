# Decorators

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/decorators)**

A decorator is a function that takes a function and gives you back a new one. That's the whole idea. We'll build one that counts how often a function is called, fix the surprise it leaves behind with `functools.wraps`, then write a `memoize` decorator that caches results so an expensive function runs once per input.

## Write the test first

The smallest useful thing a decorator can do is wrap a function without changing what it returns. So our first test wraps an `add` function and checks the answer still comes out right.

We'll put the decorator in `decorators/decorators.py` and import it with a package-relative import.

```python
from .decorators import log_calls


def test_log_calls_returns_the_same_value():
    @log_calls
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
```

The `@log_calls` line is the decorator syntax. It's sugar for `add = log_calls(add)`: take `add`, pass it through `log_calls`, and bind the result back to the name `add`. Whatever `log_calls` hands back is what we call from now on.

## Try to run the test

We've imported `log_calls` from a module that doesn't define it yet, so the import is the first thing to break. Run `uv run pytest`:

```
E   ImportError: cannot import name 'log_calls' from 'decorators.decorators'
```

No function, nothing to import. The error is telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

The smallest decorator that does nothing is one that hands the function straight back. It satisfies "takes a function, returns a function" and changes none of the behaviour.

```python
def log_calls(func):
    return func
```

That isn't counting anything yet, but the point of this step is to get the test running so we can watch it pass or fail for the right reason.

Run `uv run pytest` and `test_log_calls_returns_the_same_value` passes: `add(2, 3)` is still `5`, because we returned `add` untouched. Good. The wrapping mechanics work even though the wrapper does nothing.

## Write enough code to make it pass

That test already passes, so let's make `log_calls` earn its name with a new test that pins down the counting.

```python
def test_log_calls_counts_invocations():
    @log_calls
    def add(a, b):
        return a + b

    add(1, 1)
    add(2, 2)
    add(3, 3)
    assert add.calls == 3
```

We call the wrapped function three times, then read a `calls` attribute off it. Run `uv run pytest`:

```
    def test_log_calls_counts_invocations():
        @log_calls
        def add(a, b):
            return a + b
        add(1, 1)
        add(2, 2)
        add(3, 3)
>       assert add.calls == 3
E       AttributeError: 'function' object has no attribute 'calls'
```

Our identity decorator hands back the original `add`, which has no `calls` attribute. To track anything, the decorator has to return a *new* function that wraps the original and keeps a count.

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper
```

`wrapper` is the new function we return. It accepts `*args, **kwargs` so it works for any signature, bumps a counter, then calls the original `func` and returns its result. We stash the counter on `wrapper` itself as an attribute (functions are objects, so they can hold attributes) and seed it to `0` before returning.

Run the tests. Both pass. `add` is now `wrapper`, and every call goes through it.

## Refactor

There's nothing to tidy in the logic, but the `wrapper(*args, **kwargs)` shape is the part worth memorising: **a decorator returns an inner function that forwards every argument to the original and adds behaviour around the call.** That forwarding is what lets one decorator wrap functions of any signature.

Re-run the tests to confirm nothing moved.

## Repeat for new requirements

Our counting decorator works, but it quietly broke something. Replacing `add` with `wrapper` means the function now answers to the wrong name, and its docstring is gone. Tooling, tracebacks, and `help()` all see `wrapper` instead of the real function. Let's write the test that exposes it.

### Write the test first

```python
def test_log_calls_preserves_name_and_docstring():
    @log_calls
    def greet(name):
        """Say hello."""
        return "hello " + name

    assert greet.__name__ == "greet"
    assert greet.__doc__ == "Say hello."
```

### Try to run the test

Run `uv run pytest`:

```
    def test_log_calls_preserves_name_and_docstring():
        @log_calls
        def greet(name):
            """Say hello."""
            return "hello " + name
>       assert greet.__name__ == "greet"
E       AssertionError: assert 'wrapper' == 'greet'
E         - greet
E         + wrapper
```

There it is. `greet.__name__` is `'wrapper'`, because `greet` *is* `wrapper` now. The docstring is gone too. This is the classic decorator wart, and it bites you when a traceback names every wrapped function `wrapper`.

### Write the minimal amount of code for the test to run and check the failing test output

The standard library fixes this with `functools.wraps`. It's a decorator you apply to your inner function, and it copies `__name__`, `__doc__`, and friends from the wrapped function onto the wrapper.

```python
import functools


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper
```

### Write enough code to make it pass

That's the whole fix. Run `uv run pytest` and all three `log_calls` tests pass. `greet.__name__` is `'greet'` again, the docstring is back, and the counting still works because `functools.wraps` only copies metadata, it doesn't touch our `calls` attribute.

**Reach for `functools.wraps` on every decorator you write.** It costs one line and saves you from confusing tracebacks later.

### Refactor

Nothing to change. The decorator is three real lines plus the `wraps` line, and the tests cover what we return, that we count, and that we keep the identity of the wrapped function.

## Repeat for new requirements

Now a decorator that pays for itself: `memoize`. It caches results so that calling a function twice with the same arguments computes the answer once and replays it the second time. This is the trick that turns naive recursive Fibonacci from exponential into linear.

### Write the test first

Two things matter here, and we test them separately. First, the cached function still returns the right answers. Second, it doesn't recompute. We prove "doesn't recompute" by recording every real call in a list and asserting the list.

```python
def test_memoize_returns_correct_values():
    @memoize
    def square(n):
        return n * n

    assert square(4) == 16
    assert square(5) == 25
    assert square(4) == 16


def test_memoize_caches_repeated_calls():
    calls = []

    @memoize
    def square(n):
        calls.append(n)
        return n * n

    square(4)
    square(4)
    square(4)
    assert calls == [4]
```

`test_memoize_caches_repeated_calls` is the one that earns its keep. Three calls with the same argument, but `square`'s body should run only once, so `calls` should be `[4]`, not `[4, 4, 4]`. A decorator that returns correct values but recomputes every time would pass the first test and fail this one.

### Try to run the test

`memoize` doesn't exist yet, so the import fails first. Run `uv run pytest`:

```
E   ImportError: cannot import name 'memoize' from 'decorators.decorators'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `memoize` as an identity decorator, the same wrong-but-running shape we started `log_calls` with. It returns correct values (it just calls the function) but caches nothing.

```python
def memoize(func):
    return func
```

Run `uv run pytest`:

```
    def test_memoize_caches_repeated_calls():
        calls = []
        @memoize
        def square(n):
            calls.append(n)
            return n * n
        square(4)
        square(4)
        square(4)
>       assert calls == [4]
E       assert [4, 4, 4] == [4]
E         Left contains 2 more items, first extra item: 4
```

`test_memoize_returns_correct_values` passes (an identity decorator returns the right answers), but the caching test fails: the body ran all three times, so `calls` is `[4, 4, 4]`. That's the test doing its job, failing for exactly the reason we built it.

### Write enough code to make it pass

Give the wrapper a dictionary keyed by the call's arguments. On each call, check the cache. If we've seen these arguments, return the stored result without calling `func`. Otherwise call `func`, store the result, and return it.

```python
import functools


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache
    return wrapper
```

Run the tests. Both pass. The `cache[args] = func(*args)` line only runs when `args` is new, so `square`'s body fires once per distinct argument and the count comes out right.

A couple of details. We key the cache on `args`, the tuple of positional arguments, because tuples are hashable and so make valid dict keys. That's also the catch: **memoize only works for functions whose arguments are hashable** (numbers, strings, tuples), not lists or dicts. We take `*args` only, no `**kwargs`, to keep the key simple. And we expose the dict as `wrapper.cache` so a caller can inspect it, the same way `log_calls` exposed `calls`.

### Refactor

The code is already tight. What's worth seeing is the payoff on recursion, so let's add one more test that uses `memoize` on Fibonacci.

```python
def test_memoize_speeds_up_recursive_fibonacci():
    calls = []

    @memoize
    def fib(n):
        calls.append(n)
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(10) == 55
    # Without memoization fib(10) makes 177 calls. Memoized, each n runs once.
    assert len(calls) == 11
```

Because `fib` calls itself through the memoized wrapper, each `fib(n)` for `n` from `0` to `10` runs its body exactly once. That's 11 real calls instead of 177. The cache turns the exponential blow-up of repeated subproblems into one linear pass. Run `uv run pytest` and it's green.

### You don't have to write memoize yourself

The standard library ships this decorator as `functools.lru_cache`. In real code you reach for it instead of hand-rolling a cache:

```python
import functools


@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

`lru_cache` does what our `memoize` does and more: it caps the cache size (LRU stands for *least recently used*, the entries it evicts first), handles keyword arguments, and gives you `fib.cache_info()` to see hits and misses. Writing our own first is how we understand what it's doing for us. In an interview, `@functools.lru_cache(maxsize=None)` on a recursive function is often the whole optimisation. On Python 3.9+ you can also write `@functools.cache`, which is just `lru_cache(maxsize=None)` spelled shorter.

## Wrapping up

- **A decorator is a function that takes a function and returns a replacement**, usually an inner `wrapper(*args, **kwargs)` that forwards arguments and adds behaviour around the call. `@deco` is sugar for `f = deco(f)`.
- **Always apply `functools.wraps` to your wrapper** so the wrapped function keeps its `__name__` and `__doc__`. Skipping it gives every function the name `wrapper` in tracebacks.
- **Memoize by caching results in a dict keyed on the arguments**, returning the stored value on a repeat call. It only works when the arguments are hashable.
- **Prefer `functools.lru_cache` (or `functools.cache`) in real code.** It's the same idea, written and tested for you, and it's a one-line speed-up for recursive functions.

Next: [Design an LRU Cache](design-lru-cache.md), where we build the eviction policy that `lru_cache` hides behind that one decorator line.
