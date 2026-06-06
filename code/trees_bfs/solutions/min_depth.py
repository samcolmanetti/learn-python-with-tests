from __future__ import annotations

from collections import deque

from ..node import TreeNode


def min_depth(root: TreeNode | None) -> int:
    """Number of nodes on the shortest path from the root to a leaf.

    A leaf is a node with no children. BFS returns the moment it meets the first
    leaf, so it never explores deeper than it has to.
    """
    if root is None:
        return 0
    queue: deque[tuple[TreeNode, int]] = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth
        if node.left is not None:
            queue.append((node.left, depth + 1))
        if node.right is not None:
            queue.append((node.right, depth + 1))
    return 0  # unreachable: a non-empty tree always has a leaf
