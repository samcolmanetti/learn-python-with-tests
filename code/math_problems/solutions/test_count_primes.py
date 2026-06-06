from .count_primes import count_primes


def test_no_primes_below_two():
    assert count_primes(2) == 0


def test_below_zero_and_one():
    assert count_primes(0) == 0
    assert count_primes(1) == 0


def test_classic_example():
    assert count_primes(10) == 4


def test_boundary_is_exclusive():
    assert count_primes(3) == 1
    assert count_primes(4) == 2


def test_larger_range():
    assert count_primes(100) == 25
