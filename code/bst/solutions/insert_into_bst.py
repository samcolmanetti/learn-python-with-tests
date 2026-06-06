from __future__ import annotations

from .._template import TreeNode


def insert_into_bst(root: TreeNode | None, val: int) -> TreeNode:
    """Insert ``val`` as a new leaf and return the (possibly new) root."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
