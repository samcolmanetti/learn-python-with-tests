from __future__ import annotations

from collections import deque

from ..node import TreeNode


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    """Level-order traversal, but alternate direction each level.

    Level 0 reads left to right, level 1 right to left, and so on.
    """
    if root is None:
        return []
    levels: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    left_to_right = True
    while queue:
        level: deque[int] = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(list(level))
        left_to_right = not left_to_right
    return levels
