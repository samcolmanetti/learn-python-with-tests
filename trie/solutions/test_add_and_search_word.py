from .add_and_search_word import WordDictionary


def test_exact_match():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("bad") is True


def test_missing_word():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("dad") is False


def test_single_dot_matches_one_char():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search(".ad") is True
    assert d.search("b.d") is True


def test_all_dots():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("...") is True


def test_dot_does_not_match_wrong_length():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("..") is False
    assert d.search("....") is False


def test_dot_picks_among_several_branches():
    d = WordDictionary()
    d.add_word("bad")
    d.add_word("mad")
    assert d.search(".ad") is True
    assert d.search("pad") is False


def test_prefix_is_not_a_word():
    d = WordDictionary()
    d.add_word("bads")
    assert d.search("bad") is False
