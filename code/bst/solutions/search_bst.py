from __future__ import annotations

from .._template import TreeNode


def search_bst(root: TreeNode | None, target: int) -> TreeNode | None:
    """Return the subtree rooted at ``target``, or ``None`` if it isn't present."""
    node = root
    while node is not None and node.val != target:
        node = node.left if target < node.val else node.right
    return node
