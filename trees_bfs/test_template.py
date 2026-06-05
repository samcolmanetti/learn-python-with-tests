from __future__ import annotations

from ._template import level_order
from .node import TreeNode


def test_empty_tree():
    assert level_order(None) == []


def test_single_node():
    assert level_order(TreeNode(1)) == [[1]]


def test_three_levels():
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert level_order(root) == [[3], [9, 20], [15, 7]]


def test_left_skewed():
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert level_order(root) == [[1], [2], [3]]
