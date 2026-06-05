from .number_of_connected_components import count_components


def test_two_components():
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2


def test_one_component():
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1


def test_no_edges():
    assert count_components(4, []) == 4


def test_redundant_edges_dont_double_count():
    assert count_components(3, [[0, 1], [1, 2], [0, 2]]) == 1


def test_single_node():
    assert count_components(1, []) == 1
