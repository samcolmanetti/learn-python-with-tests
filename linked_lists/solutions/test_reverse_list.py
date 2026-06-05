from .._template import build_list, to_list
from .reverse_list import reverse_list


def test_reverses_several_nodes():
    assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]


def test_single_node_is_unchanged():
    assert to_list(reverse_list(build_list([1]))) == [1]


def test_empty_list_returns_none():
    assert reverse_list(build_list([])) is None


def test_two_nodes_swap():
    assert to_list(reverse_list(build_list([1, 2]))) == [2, 1]
