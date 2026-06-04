import pytest

from .iteration import repeat


@pytest.mark.parametrize(
    ("character", "count", "expected"),
    [
        ("a", 5, "aaaaa"),
        ("a", 0, ""),
        ("a", 1, "a"),
        ("ab", 3, "ababab"),
        ("", 4, ""),
    ],
)
def test_repeat(character, count, expected):
    assert repeat(character, count) == expected
