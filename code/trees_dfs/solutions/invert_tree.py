from __future__ import annotations

from .._template import TreeNode


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """Mirror the tree: swap every node's left and right child."""
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
