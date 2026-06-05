from .longest_common_subsequence import longest_common_subsequence


def test_shared_run():
    assert longest_common_subsequence("abcde", "ace") == 3


def test_identical_strings():
    assert longest_common_subsequence("abc", "abc") == 3


def test_no_common_characters():
    assert longest_common_subsequence("abc", "def") == 0


def test_interleaved_match():
    assert longest_common_subsequence("abcba", "abcbcba") == 5


def test_empty_first():
    assert longest_common_subsequence("", "abc") == 0


def test_empty_second():
    assert longest_common_subsequence("abc", "") == 0


def test_both_empty():
    assert longest_common_subsequence("", "") == 0
