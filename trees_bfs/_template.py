"""Breadth-First Search on a binary tree, level-order traversal.

BFS visits the tree level by level using a queue (``collections.deque``). The key trick for
"per level" problems: snapshot ``len(queue)`` at the start of each level so you process
exactly the nodes on that level before moving deeper.

Reuses :class:`trees_dfs._template.TreeNode`-shaped nodes (any object with ``.val``,
``.left``, ``.right`` works).
"""

from __future__ import annotations

from collections import deque
from typing import Protocol


class _Node(Protocol):
    val: int
    left: _Node | None
    right: _Node | None


def level_order(root: _Node | None) -> list[list[int]]:
    """Return node values grouped by depth: ``[[level0], [level1], ...]``."""
    if root is None:
        return []
    levels: list[list[int]] = []
    queue: deque = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):  # exactly this level's nodes
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)
    return levels
