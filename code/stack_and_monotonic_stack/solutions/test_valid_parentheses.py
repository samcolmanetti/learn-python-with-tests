from .valid_parentheses import is_valid


def test_single_pair():
    assert is_valid("()") is True


def test_mixed_pairs():
    assert is_valid("()[]{}") is True


def test_nested():
    assert is_valid("([{}])") is True


def test_wrong_order():
    assert is_valid("(]") is False


def test_interleaved_is_invalid():
    assert is_valid("([)]") is False


def test_unclosed_opener():
    assert is_valid("(") is False


def test_stray_closer():
    assert is_valid(")") is False


def test_empty_is_valid():
    assert is_valid("") is True
