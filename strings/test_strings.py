from .strings import (
    is_anagram,
    join_lines,
    normalize_whitespace,
    reverse_words,
)


def test_reverse_words():
    assert reverse_words("the quick brown fox") == "fox brown quick the"


def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_collapses_extra_spaces():
    # split() drops the runs of spaces, so the output is always single-spaced.
    assert reverse_words("  pad   me  out  ") == "out me pad"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_is_anagram_true():
    assert is_anagram("listen", "silent") is True


def test_is_anagram_false():
    assert is_anagram("hello", "world") is False


def test_is_anagram_ignores_case_and_spaces():
    assert is_anagram("Dormitory", "Dirty room") is True


def test_is_anagram_different_lengths():
    assert is_anagram("ab", "abc") is False


def test_normalize_whitespace_collapses_runs():
    assert normalize_whitespace("  hello   world  ") == "hello world"


def test_normalize_whitespace_handles_tabs_and_newlines():
    assert normalize_whitespace("a\tb\n c") == "a b c"


def test_normalize_whitespace_empty():
    assert normalize_whitespace("   ") == ""


def test_join_lines():
    assert join_lines(["a", "b", "c"]) == "a\nb\nc"


def test_join_lines_empty():
    assert join_lines([]) == ""
