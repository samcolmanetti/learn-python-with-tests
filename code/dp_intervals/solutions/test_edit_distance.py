from .edit_distance import edit_distance


def test_classic_horse_to_ros():
    assert edit_distance("horse", "ros") == 3


def test_substitution_chain():
    assert edit_distance("intention", "execution") == 5


def test_identical_strings():
    assert edit_distance("abc", "abc") == 0


def test_pure_insertions():
    assert edit_distance("", "abc") == 3


def test_pure_deletions():
    assert edit_distance("abc", "") == 3


def test_single_substitution():
    assert edit_distance("cat", "cut") == 1


def test_both_empty():
    assert edit_distance("", "") == 0
