"""Depth-First Search on a binary tree.

DFS on a tree is just recursion: do something with the current node, then recurse into the
children. The two everyday shapes are:

- **Search**: walk until you find a target, short-circuiting as soon as it is found.
- **Aggregate up**: compute each child's answer, then combine them into this node's answer
  (the "return info up the tree" pattern — e.g. height, sum, "is balanced").

``TreeNode`` is the minimal node used throughout the tree chapters.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self,
        val: int,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def dfs_search(root: TreeNode | None, target: int) -> TreeNode | None:
    """Return the first node whose ``val == target`` (pre-order), or ``None``."""
    if root is None:
        return None
    if root.val == target:
        return root
    return dfs_search(root.left, target) or dfs_search(root.right, target)


def max_depth(root: TreeNode | None) -> int:
    """Height of the tree (number of nodes on the longest root-to-leaf path).

    The canonical "aggregate up" DFS: a node's depth is ``1 + max(child depths)``.
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
