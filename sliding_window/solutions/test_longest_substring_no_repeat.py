import pytest

from .longest_substring_no_repeat import length_of_longest_substring


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcabcbb", 3),  # "abc"
        ("bbbbb", 1),  # "b"
        ("pwwkew", 3),  # "wke"
        ("", 0),  # empty
        ("au", 2),
        ("dvdf", 3),  # "vdf" — left must jump correctly
        ("abba", 2),  # tests that left never moves backwards
    ],
)
def test_length_of_longest_substring(text, expected):
    assert length_of_longest_substring(text) == expected
