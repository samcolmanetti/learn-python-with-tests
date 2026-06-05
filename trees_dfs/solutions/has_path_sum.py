from __future__ import annotations

from .._template import TreeNode


def has_path_sum(root: TreeNode | None, target: int) -> bool:
    """True if some root-to-leaf path's values add up to ``target``."""
    if root is None:
        return False
    if root.left is None and root.right is None:
        return root.val == target
    remaining = target - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
