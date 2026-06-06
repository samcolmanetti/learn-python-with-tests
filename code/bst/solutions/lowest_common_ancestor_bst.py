from __future__ import annotations

from .._template import TreeNode


def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> TreeNode:
    """Return the lowest node that has both ``p`` and ``q`` in its subtree.

    Both values are assumed present in the tree.
    """
    node = root
    while node is not None:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node
    raise ValueError("p and q must both be present in the tree")
