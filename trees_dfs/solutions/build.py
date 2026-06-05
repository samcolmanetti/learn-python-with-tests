"""Build a binary tree from a level-order list, the way LeetCode draws them.

The list is breadth-first with ``None`` marking a missing child, so
``[1, 2, 3, None, 4]`` is::

        1
       / \
      2   3
       \
        4

We only enqueue real nodes, and we pull child values from the list as we go.
"""

from __future__ import annotations

from collections import deque

from .._template import TreeNode


def build_tree(values: list[int | None]) -> TreeNode | None:
    """Return the root of the tree described by ``values`` in level order."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root
