from .longest_palindromic_subsequence import longest_palindromic_subsequence


def test_classic_bbbab():
    assert longest_palindromic_subsequence("bbbab") == 4


def test_two_char_palindrome():
    assert longest_palindromic_subsequence("cbbd") == 2


def test_single_character():
    assert longest_palindromic_subsequence("a") == 1


def test_already_a_palindrome():
    assert longest_palindromic_subsequence("racecar") == 7


def test_no_repeats():
    assert longest_palindromic_subsequence("abcd") == 1


def test_empty():
    assert longest_palindromic_subsequence("") == 0
