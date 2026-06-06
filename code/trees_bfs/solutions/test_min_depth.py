from ..node import TreeNode
from .min_depth import min_depth


def test_empty_tree_is_zero():
    assert min_depth(None) == 0


def test_single_node_is_one():
    assert min_depth(TreeNode(1)) == 1


def test_shortest_branch_wins():
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    # The shortest root-to-leaf path ends at 9, depth 2.
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert min_depth(root) == 2


def test_single_child_is_not_a_leaf():
    #    1
    #     \
    #      2
    #       \
    #        3
    # Node 1 has only a right child, so it is not a leaf. The only leaf is 3, depth 3.
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert min_depth(root) == 3
