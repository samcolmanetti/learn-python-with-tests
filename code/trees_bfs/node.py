"""A tiny binary-tree node for the BFS chapter.

The same minimal shape used across the tree chapters: a value and two child links.
We keep a local copy here so this package's tests import only from within the package,
rather than reaching across into ``trees_dfs``.
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
