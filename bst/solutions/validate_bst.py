from __future__ import annotations

from .._template import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    """True if ``root`` satisfies the BST invariant for every subtree."""

    def within(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return within(node.left, low, node.val) and within(node.right, node.val, high)

    return within(root, float("-inf"), float("inf"))
