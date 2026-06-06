from .build import build_tree
from .diameter_of_binary_tree import diameter_of_binary_tree


def test_empty_tree_has_zero_diameter():
    assert diameter_of_binary_tree(None) == 0


def test_single_node_has_zero_diameter():
    assert diameter_of_binary_tree(build_tree([1])) == 0


def test_diameter_through_root():
    assert diameter_of_binary_tree(build_tree([1, 2, 3, 4, 5])) == 3


def test_diameter_not_through_root():
    # Longest path lives entirely in the left subtree, never touching the root.
    root = build_tree([1, 2, None, 3, None, 4, 5, 6, None, None, 7])
    assert diameter_of_binary_tree(root) == 4
