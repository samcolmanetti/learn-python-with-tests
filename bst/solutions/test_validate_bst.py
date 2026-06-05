from .._template import TreeNode
from .validate_bst import is_valid_bst


def test_empty_tree_is_valid():
    assert is_valid_bst(None) is True


def test_single_node_is_valid():
    assert is_valid_bst(TreeNode(1)) is True


def test_simple_valid_tree():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(root) is True


def test_left_child_too_big():
    root = TreeNode(2, TreeNode(3), TreeNode(4))
    assert is_valid_bst(root) is False


def test_deep_violation_passes_neighbour_check():
    # 5 / (1, 6); right child 6 has children 3 and 7.
    # 3 sits in the right subtree of 5, so it breaks the invariant
    # even though it's a valid child of its own parent (6).
    root = TreeNode(5, TreeNode(1), TreeNode(6, TreeNode(3), TreeNode(7)))
    assert is_valid_bst(root) is False


def test_equal_values_are_not_valid():
    root = TreeNode(2, TreeNode(2), TreeNode(3))
    assert is_valid_bst(root) is False
