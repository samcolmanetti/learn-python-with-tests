from .decorators import log_calls, memoize


def test_log_calls_returns_the_same_value():
    @log_calls
    def add(a, b):
        return a + b

    assert add(2, 3) == 5


def test_log_calls_counts_invocations():
    @log_calls
    def add(a, b):
        return a + b

    add(1, 1)
    add(2, 2)
    add(3, 3)
    assert add.calls == 3


def test_log_calls_preserves_name_and_docstring():
    @log_calls
    def greet(name):
        """Say hello."""
        return "hello " + name

    assert greet.__name__ == "greet"
    assert greet.__doc__ == "Say hello."


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


def test_memoize_recomputes_for_new_arguments():
    calls = []

    @memoize
    def square(n):
        calls.append(n)
        return n * n

    square(4)
    square(5)
    square(4)
    assert calls == [4, 5]


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
