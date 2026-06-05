from .partition_labels import partition_labels


def test_classic_example():
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]


def test_single_char():
    assert partition_labels("a") == [1]


def test_all_same():
    assert partition_labels("aaaa") == [4]


def test_all_distinct():
    assert partition_labels("abcde") == [1, 1, 1, 1, 1]


def test_empty():
    assert partition_labels("") == []


def test_one_big_partition():
    assert partition_labels("abccba") == [6]
