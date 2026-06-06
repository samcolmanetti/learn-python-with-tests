import pytest

from .valid_palindrome import is_palindrome


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),  # empty string is a palindrome
        (" ", True),  # only non-alphanumeric -> vacuously a palindrome
        ("a", True),  # single character
        ("ab", False),
        ("0P", False),  # digit vs letter, not equal even after lowercasing
        ("Madam", True),
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected
