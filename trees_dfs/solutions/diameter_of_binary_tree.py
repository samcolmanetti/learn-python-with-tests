from __future__ import annotations

from .._template import TreeNode


def diameter_of_binary_tree(root: TreeNode | None) -> int:
    """Longest path between any two nodes, measured in edges."""
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
