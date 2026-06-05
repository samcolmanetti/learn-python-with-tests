from ..node import TreeNode
from .right_side_view import right_side_view


def test_empty_tree():
    assert right_side_view(None) == []


def test_single_node():
    assert right_side_view(TreeNode(1)) == [1]


def test_rightmost_per_level():
    #        1
    #       / \
    #      2   3
    #       \   \
    #        5   4
    root = TreeNode(1, TreeNode(2, None, TreeNode(5)), TreeNode(3, None, TreeNode(4)))
    assert right_side_view(root) == [1, 3, 4]


def test_left_node_visible_when_no_right():
    #        1
    #       /
    #      2
    #     /
    #    3
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert right_side_view(root) == [1, 2, 3]


def test_deeper_left_subtree_shows_through():
    #          1
    #         / \
    #        2   3
    #       /
    #      4
    # Level 2 has only node 4 (a left child), so it is the rightmost on its level.
    root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
    assert right_side_view(root) == [1, 3, 4]
