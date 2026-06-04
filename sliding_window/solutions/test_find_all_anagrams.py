from .find_all_anagrams import find_anagrams


def test_finds_two_anagrams():
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]


def test_overlapping_anagrams():
    assert find_anagrams("abab", "ab") == [0, 1, 2]


def test_no_anagrams():
    assert find_anagrams("hello", "xyz") == []


def test_pattern_longer_than_string():
    assert find_anagrams("a", "aa") == []


def test_whole_string_is_the_anagram():
    assert find_anagrams("bca", "abc") == [0]
