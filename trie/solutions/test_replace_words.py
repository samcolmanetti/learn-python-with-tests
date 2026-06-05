from .replace_words import replace_words


def test_basic_replacement():
    roots = ["cat", "bat", "rat"]
    sentence = "the cattle was rattled by the battery"
    assert replace_words(roots, sentence) == "the cat was rat by the bat"


def test_shortest_root_wins():
    roots = ["a", "aa", "aaa", "aaaa"]
    sentence = "a aa a aaaa aaa bbb"
    assert replace_words(roots, sentence) == "a a a a a bbb"


def test_no_root_leaves_word_untouched():
    roots = ["cat"]
    sentence = "the dog ran"
    assert replace_words(roots, sentence) == "the dog ran"


def test_word_equal_to_root():
    roots = ["cat"]
    sentence = "cat"
    assert replace_words(roots, sentence) == "cat"


def test_empty_roots():
    assert replace_words([], "hello world") == "hello world"
