from .._template import TreeNode
from .lowest_common_ancestor_bst import lowest_common_ancestor


def build_sample():
    # 6
    #    / (2, 8)
    # 2 has children 0 and 4; 4 has children 3 and 5.
    # 8 has children 7 and 9.
    return TreeNode(
        6,
        TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
        TreeNode(8, TreeNode(7), TreeNode(9)),
    )


def test_split_across_root():
    root = build_sample()
    assert lowest_common_ancestor(root, 2, 8).val == 6


def test_both_in_left_subtree():
    root = build_sample()
    assert lowest_common_ancestor(root, 0, 5).val == 2


def test_ancestor_is_one_of_the_nodes():
    root = build_sample()
    assert lowest_common_ancestor(root, 2, 4).val == 2


def test_deep_pair():
    root = build_sample()
    assert lowest_common_ancestor(root, 3, 5).val == 4
