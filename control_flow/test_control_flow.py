import pytest

from .control_flow import first_passing, fizzbuzz, grade_classifier


def test_fizzbuzz_plain_numbers():
    assert fizzbuzz(2) == ["1", "2"]


def test_fizzbuzz_fizz_on_three():
    assert fizzbuzz(3) == ["1", "2", "Fizz"]


def test_fizzbuzz_buzz_on_five():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizzbuzz_fizzbuzz_on_fifteen():
    assert fizzbuzz(15)[-1] == "FizzBuzz"


def test_fizzbuzz_zero_is_empty():
    assert fizzbuzz(0) == []


def test_grade_a():
    assert grade_classifier(95) == "A"


def test_grade_boundaries():
    assert grade_classifier(90) == "A"
    assert grade_classifier(89) == "B"
    assert grade_classifier(60) == "D"
    assert grade_classifier(59) == "F"


def test_grade_zero():
    assert grade_classifier(0) == "F"


def test_grade_rejects_too_high():
    with pytest.raises(ValueError):
        grade_classifier(101)


def test_grade_rejects_negative():
    with pytest.raises(ValueError):
        grade_classifier(-1)


def test_first_passing_finds_first():
    assert first_passing([40, 55, 72, 95]) == "C"


def test_first_passing_skips_invalid():
    assert first_passing([200, -3, 88]) == "B"


def test_first_passing_none_when_all_fail():
    assert first_passing([10, 20, 30]) == "none"


def test_first_passing_empty():
    assert first_passing([]) == "none"
