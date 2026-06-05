from .iterators import (
    Countdown,
    fibonacci,
    fibonacci_forever,
    first_n_fibonacci,
)


def test_countdown_yields_descending_values():
    assert list(Countdown(3)) == [3, 2, 1]


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


def test_fibonacci_first_values():
    assert list(fibonacci(7)) == [0, 1, 1, 2, 3, 5, 8]


def test_fibonacci_of_zero_is_empty():
    assert list(fibonacci(0)) == []


def test_fibonacci_of_one():
    assert list(fibonacci(1)) == [0]


def test_fibonacci_forever_is_lazy():
    gen = fibonacci_forever()
    assert next(gen) == 0
    assert next(gen) == 1
    assert next(gen) == 1
    assert next(gen) == 2


def test_first_n_fibonacci_matches_the_eager_version():
    assert first_n_fibonacci(7) == [0, 1, 1, 2, 3, 5, 8]
