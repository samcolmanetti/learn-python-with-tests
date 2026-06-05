from .redundant_connection import find_redundant_connection


def test_triangle():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]


def test_returns_last_edge_that_closes_the_loop():
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]


def test_self_contained_cycle():
    assert find_redundant_connection([[1, 2], [2, 3], [3, 1]]) == [3, 1]


def test_first_redundant_edge_wins():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3], [3, 4]]) == [2, 3]
