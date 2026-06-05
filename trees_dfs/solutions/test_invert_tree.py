from .build import build_tree
from .invert_tree import invert_tree


def level_order(root):
    """Flatten a tree to a level-order list including None gaps, then trim trailing Nones."""
    from collections import deque

    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def test_invert_empty():
    assert invert_tree(None) is None


def test_invert_single_node():
    root = build_tree([1])
    assert level_order(invert_tree(root)) == [1]


def test_invert_mirrors_children():
    root = build_tree([4, 2, 7, 1, 3, 6, 9])
    assert level_order(invert_tree(root)) == [4, 7, 2, 9, 6, 3, 1]
