from .._template import TreeNode
from .insert_into_bst import insert_into_bst
from .validate_bst import is_valid_bst


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


def test_insert_into_empty_creates_root():
    root = insert_into_bst(None, 5)
    assert root.val == 5
    assert root.left is None and root.right is None


def test_insert_smaller_goes_left():
    root = TreeNode(4)
    insert_into_bst(root, 2)
    assert root.left is not None and root.left.val == 2
    assert root.right is None


def test_insert_larger_goes_right():
    root = TreeNode(4)
    insert_into_bst(root, 7)
    assert root.right is not None and root.right.val == 7
    assert root.left is None


def test_insert_keeps_tree_sorted():
    root = None
    for val in [4, 2, 7, 1, 3, 6]:
        root = insert_into_bst(root, val)
    assert inorder(root) == [1, 2, 3, 4, 6, 7]
    assert is_valid_bst(root) is True


def test_returns_same_root_when_not_empty():
    root = TreeNode(4)
    returned = insert_into_bst(root, 9)
    assert returned is root
