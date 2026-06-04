import pytest

from .hello_pytest import hello


@pytest.mark.parametrize(
    ("name", "language", "expected"),
    [
        ("Chris", "", "Hello, Chris"),
        ("", "", "Hello, world"),
        ("Elodie", "Spanish", "Hola, Elodie"),
        ("Lauren", "French", "Bonjour, Lauren"),
        ("", "Spanish", "Hola, world"),
        ("Chris", "Klingon", "Hello, Chris"),  # unknown language falls back to English
    ],
)
def test_hello(name, language, expected):
    assert hello(name, language) == expected
