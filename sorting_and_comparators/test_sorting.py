from .sorting import (
    by_last_then_first,
    by_length,
    by_score_desc_then_name,
    largest_number,
)


def test_by_length():
    assert by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]


def test_by_length_is_stable():
    # Stable sort: equal-length items keep their original relative order.
    assert by_length(["bb", "aa", "cc"]) == ["bb", "aa", "cc"]


def test_by_last_then_first():
    names = ["John Smith", "Jane Adams", "Bob Smith"]
    assert by_last_then_first(names) == ["Jane Adams", "Bob Smith", "John Smith"]


def test_by_score_desc_then_name():
    players = [("alice", 50), ("bob", 90), ("carol", 50)]
    # 90 first; the two 50s tie-break by name ascending.
    assert by_score_desc_then_name(players) == [("bob", 90), ("alice", 50), ("carol", 50)]


def test_largest_number():
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"


def test_largest_number_all_zeros():
    assert largest_number([0, 0]) == "0"


def test_largest_number_empty():
    assert largest_number([]) == "0"


def test_largest_number_single():
    assert largest_number([10]) == "10"
