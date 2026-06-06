from annotations import (
    first_name,
    greet,
    total,
    word_counts,
)


def test_greet():
    assert greet("Ada") == "Hello, Ada"


def test_total():
    assert total([1, 2, 3, 4]) == 10


def test_total_empty():
    assert total([]) == 0


def test_first_name_returns_first_word():
    assert first_name("Grace Hopper") == "Grace"


def test_first_name_returns_none_for_empty():
    assert first_name("   ") is None


def test_word_counts():
    assert word_counts(["a", "b", "a"]) == {"a": 2, "b": 1}


def test_word_counts_empty():
    assert word_counts([]) == {}
