"""Binary search tree: the node plus the one invariant that makes search fast.

A binary search tree is a binary tree with an ordering rule. For every node:

    every key in its left subtree  < node.val < every key in its right subtree

That rule is the *BST invariant*. It is what lets you skip half the tree at every
step. If the value you want is smaller than the current node it can only live to the
left; if it's larger, only to the right. A balanced BST searches, inserts, and deletes
in O(h) where ``h`` is the height, which is O(log n) when the tree stays balanced.

The invariant is about whole subtrees, not just the immediate children. A node can be
larger than its parent and still break the invariant if it sits in a subtree whose root
demanded everything below be smaller. Validation has to carry a ``(low, high)`` range
down the tree, not just compare neighbours.
"""

from __future__ import annotations


class TreeNode:
    """A binary tree node: a value plus left and right child pointers."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right
