from .._template import TreeNode
from .search_bst import search_bst


def build_sample():
    # 4 / (2, 7); 2 has children 1 and 3.
    return TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7))


def test_finds_root():
    root = build_sample()
    found = search_bst(root, 4)
    assert found is root


def test_finds_deep_node():
    root = build_sample()
    found = search_bst(root, 3)
    assert found is not None
    assert found.val == 3


def test_missing_returns_none():
    root = build_sample()
    assert search_bst(root, 5) is None


def test_empty_tree_returns_none():
    assert search_bst(None, 1) is None


def test_returns_whole_subtree():
    root = build_sample()
    found = search_bst(root, 2)
    assert found is not None
    assert found.left is not None and found.left.val == 1
    assert found.right is not None and found.right.val == 3
