from dicts_and_sets import (
    common_elements,
    first_non_repeating_char,
    group_anagrams,
    word_count,
)


def test_word_count_basic():
    assert word_count("the cat the dog the") == {"the": 3, "cat": 1, "dog": 1}


def test_word_count_empty():
    assert word_count("") == {}


def test_word_count_single_word():
    assert word_count("solo") == {"solo": 1}


def test_first_non_repeating_char():
    assert first_non_repeating_char("leetcode") == "l"


def test_first_non_repeating_char_skips_repeats():
    assert first_non_repeating_char("aabbc") == "c"


def test_first_non_repeating_char_none_when_all_repeat():
    assert first_non_repeating_char("aabb") is None


def test_first_non_repeating_char_empty():
    assert first_non_repeating_char("") is None


def test_common_elements():
    assert common_elements([1, 2, 3, 4], [3, 4, 5, 6]) == {3, 4}


def test_common_elements_with_duplicates():
    assert common_elements([1, 1, 2, 2], [2, 2, 3]) == {2}


def test_common_elements_disjoint():
    assert common_elements([1, 2], [3, 4]) == set()


def test_group_anagrams():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = group_anagrams(words)
    as_sets = sorted([sorted(group) for group in groups])
    assert as_sets == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]


def test_group_anagrams_empty():
    assert group_anagrams([]) == []


def test_group_anagrams_no_anagrams():
    groups = group_anagrams(["abc", "def"])
    assert sorted(sorted(g) for g in groups) == [["abc"], ["def"]]
