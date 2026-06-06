from __future__ import annotations

from collections import deque

from ..node import TreeNode


def right_side_view(root: TreeNode | None) -> list[int]:
    """Return the values you'd see looking at the tree from the right.

    That is the last node on each level, top to bottom.
    """
    if root is None:
        return []
    view: list[int] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                view.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return view
