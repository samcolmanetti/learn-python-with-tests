from .build import build_tree


def test_empty_list_is_none():
    assert build_tree([]) is None


def test_root_none_is_none():
    assert build_tree([None]) is None


def test_single_node():
    root = build_tree([1])
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None


def test_full_level():
    root = build_tree([1, 2, 3])
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3


def test_skips_missing_children():
    root = build_tree([1, 2, 3, None, 4])
    assert root.left.left is None
    assert root.left.right.val == 4
    assert root.right.left is None
    assert root.right.right is None
