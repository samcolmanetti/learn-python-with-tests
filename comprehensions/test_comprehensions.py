from itertools import count, islice

from .comprehensions import (
    char_index_map,
    evens,
    running_total,
    squares,
    unique_lengths,
)


def test_squares():
    assert squares([1, 2, 3, 4]) == [1, 4, 9, 16]


def test_squares_empty():
    assert squares([]) == []


def test_evens():
    assert evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def test_evens_includes_zero():
    assert evens([0, 1, 2]) == [0, 2]


def test_char_index_map():
    assert char_index_map("abc") == {"a": 0, "b": 1, "c": 2}


def test_char_index_map_keeps_last_index():
    # A repeated key keeps the last value written.
    assert char_index_map("aba") == {"a": 2, "b": 1}


def test_unique_lengths():
    assert unique_lengths(["a", "bb", "cc", "ddd"]) == {1, 2, 3}


def test_unique_lengths_dedupes():
    assert unique_lengths(["dog", "cat", "fox"]) == {3}


def test_running_total():
    assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]


def test_running_total_empty():
    assert list(running_total([])) == []


def test_running_total_is_lazy():
    # count() is infinite; islice pulls only the first three totals and we never hang.
    assert list(islice(running_total(count(1)), 3)) == [1, 3, 6]
