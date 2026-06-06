from .._template import build_list, to_list
from .middle_node import middle_node


def test_odd_length_picks_exact_middle():
    assert to_list(middle_node(build_list([1, 2, 3, 4, 5]))) == [3, 4, 5]


def test_even_length_picks_second_middle():
    assert to_list(middle_node(build_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]


def test_single_node_is_its_own_middle():
    assert to_list(middle_node(build_list([1]))) == [1]


def test_two_nodes_returns_second():
    assert to_list(middle_node(build_list([1, 2]))) == [2]
