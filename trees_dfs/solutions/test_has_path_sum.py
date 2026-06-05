from .build import build_tree
from .has_path_sum import has_path_sum


def test_empty_tree_has_no_path():
    assert has_path_sum(None, 0) is False


def test_single_node_matches():
    assert has_path_sum(build_tree([5]), 5) is True


def test_single_node_misses():
    assert has_path_sum(build_tree([5]), 4) is False


def test_root_to_leaf_path_exists():
    root = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2])
    assert has_path_sum(root, 22) is True


def test_no_matching_path():
    root = build_tree([1, 2, 3])
    assert has_path_sum(root, 5) is False


def test_partial_path_does_not_count():
    # 1 -> 2 sums to 3, but that's not a leaf, so target 1 must reach a leaf.
    root = build_tree([1, 2])
    assert has_path_sum(root, 1) is False
