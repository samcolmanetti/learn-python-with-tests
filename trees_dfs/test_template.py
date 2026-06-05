from ._template import TreeNode, dfs_search, max_depth


def test_dfs_search_finds_node():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    found = dfs_search(root, 3)
    assert found is not None
    assert found.val == 3


def test_dfs_search_missing_returns_none():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    assert dfs_search(root, 99) is None


def test_dfs_search_empty_tree():
    assert dfs_search(None, 1) is None


def test_max_depth_empty_is_zero():
    assert max_depth(None) == 0


def test_max_depth_counts_longest_path():
    root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
    assert max_depth(root) == 3
