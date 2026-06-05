from __future__ import annotations

from .._template import TreeNode


def is_balanced(root: TreeNode | None) -> bool:
    """True if every node's two subtrees differ in height by at most one."""

    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) != -1
