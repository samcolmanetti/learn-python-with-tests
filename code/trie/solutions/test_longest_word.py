from .longest_word import longest_word


def test_single_chain():
    words = ["a", "ap", "app", "appl", "apple"]
    assert longest_word(words) == "apple"


def test_breaks_in_chain_are_excluded():
    words = ["a", "banana", "app", "appl", "ap", "apply", "apple"]
    assert longest_word(words) == "apple"


def test_lexicographically_smallest_among_longest():
    words = ["w", "wo", "wor", "worl", "world", "t", "ti", "tig", "tige", "tiger"]
    assert longest_word(words) == "tiger"


def test_no_buildable_word():
    words = ["abc", "bcd"]
    assert longest_word(words) == ""


def test_empty_input():
    assert longest_word([]) == ""
