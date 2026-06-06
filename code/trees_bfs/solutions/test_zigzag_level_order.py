from ..node import TreeNode
from .zigzag_level_order import zigzag_level_order


def test_empty_tree():
    assert zigzag_level_order(None) == []


def test_single_node():
    assert zigzag_level_order(TreeNode(1)) == [[1]]


def test_three_levels_alternate():
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert zigzag_level_order(root) == [[3], [20, 9], [15, 7]]


def test_four_levels_flips_twice():
    #          1
    #         / \
    #        2   3
    #       /   / \
    #      4   5   6
    #     /
    #    7
    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4, TreeNode(7))),
        TreeNode(3, TreeNode(5), TreeNode(6)),
    )
    assert zigzag_level_order(root) == [[1], [3, 2], [4, 5, 6], [7]]
