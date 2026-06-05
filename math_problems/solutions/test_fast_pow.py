import pytest

from .fast_pow import fast_pow


def test_small_power():
    assert fast_pow(2, 10, 1000) == 24


def test_exponent_zero():
    assert fast_pow(7, 0, 13) == 1


def test_mod_one_is_always_zero():
    assert fast_pow(7, 5, 1) == 0


def test_matches_builtin_pow():
    assert fast_pow(3, 200, 1_000_000_007) == pow(3, 200, 1_000_000_007)


def test_base_larger_than_mod():
    assert fast_pow(123, 4, 7) == pow(123, 4, 7)


def test_negative_exponent_rejected():
    with pytest.raises(ValueError):
        fast_pow(2, -1, 5)
