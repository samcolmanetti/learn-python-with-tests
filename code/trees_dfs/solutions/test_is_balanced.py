from .build import build_tree
from .is_balanced import is_balanced


def test_empty_is_balanced():
    assert is_balanced(None) is True


def test_single_node_is_balanced():
    assert is_balanced(build_tree([1])) is True


def test_balanced_tree():
    assert is_balanced(build_tree([3, 9, 20, None, None, 15, 7])) is True


def test_unbalanced_tree():
    root = build_tree([1, 2, 2, 3, 3, None, None, 4, 4])
    assert is_balanced(root) is False
