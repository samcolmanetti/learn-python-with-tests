# Trees: DFS

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/trees_dfs)**

Depth-first search on a binary tree is just recursion wearing a hat. You do something with the current node, then you recurse into its children, and the call stack remembers where you were. This is an **interview pattern**: a reusable [`trees_dfs/_template.py`](trees_dfs/_template.py) plus worked problems in `trees_dfs/solutions/`, each built test-first.

## When to reach for DFS

You're handed a tree (or anything tree-shaped) and the question is about paths, depth, or some property that depends on a node's descendants. Reach for DFS when:

- You need to **visit every node** and the order is top-down or "children before parent". Recursion gives you that for free, no explicit stack.
- The answer at a node is a **combination of the answers at its children**. Height, sum, "is this balanced", diameter: each one asks every child for a number and folds the children's numbers into its own. This is the "return info up the tree" shape, and it's the half of this chapter worth memorising.
- You can **stop early** once you've found what you want. Searching for a value short-circuits the moment a match shows up.

The whole pattern is one base case (an empty subtree) and one recursive step (combine the children). Get those two right and the rest is bookkeeping.

## The template

Here's the node and the two everyday DFS shapes, straight from `_template.py`:

```python
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
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

Two functions, two shapes. `dfs_search` is the **search** shape: check the current node, and if it's not a match, recurse left then right, returning the first hit. The `or` short-circuits, so once the left subtree finds the target we never touch the right one.

`max_depth` is the **aggregate-up** shape: ask each child for its depth, take the bigger of the two, add one for the current node. Notice the invariant that makes both of these work: *the base case is always `root is None`, and it returns the identity for whatever you're combining*. For a search that's `None`; for a depth that's `0`. Get the empty case right and the recursion writes itself.

`TreeNode | None` appears everywhere because a child can be missing. We add `from __future__ import annotations` so the `list[int]` and `X | None` style hints run on Python 3.9.

Every problem below builds its tree from a level-order list, so before we solve anything, we need that builder.

## Problem 0: Build a tree from a level-order list

> Given a breadth-first list like `[1, 2, 3, None, 4]`, with `None` marking a missing child, return the root of the tree it describes.

This isn't an interview question, it's the helper that makes the other tests readable. LeetCode draws trees as level-order lists, and typing out nested `TreeNode(1, TreeNode(2), ...)` calls by hand gets old fast. So we build a small `build_tree` once and reuse it everywhere.

### Write the test first

```python
from .build import build_tree


def test_empty_list_is_none():
    assert build_tree([]) is None


def test_root_none_is_none():
    assert build_tree([None]) is None


def test_single_node():
    root = build_tree([1])
    assert root is not None
    assert root.val == 1
    assert root.left is None
    assert root.right is None


def test_full_level():
    root = build_tree([1, 2, 3])
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3


def test_skips_missing_children():
    root = build_tree([1, 2, 3, None, 4])
    assert root.left.left is None
    assert root.left.right.val == 4
    assert root.right.left is None
    assert root.right.right is None
```

`test_skips_missing_children` is the one that pins the behaviour down. The `None` at index 3 means "node 2 has no left child", so node 4 has to land as node 2's *right* child. A builder that doesn't track which slot a `None` belongs to gets this wrong.

### Try to run the test

There's no `build.py` with a `build_tree` in it yet, so the import is the first thing to break:

```
ImportError: cannot import name 'build_tree' from 'build'
```

Listen to the error. It's telling us exactly which name to define and where.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `build_tree` that always returns `None`. It's wrong on purpose. We just want the test to run so we can watch it fail on a value instead of an import.

```python
from __future__ import annotations

from .._template import TreeNode


def build_tree(values: list[int | None]) -> TreeNode | None:
    return None
```

Run `uv run pytest`:

```
    def test_single_node():
        root = build_tree([1])
>       assert root is not None
E       assert None is not None

    def test_full_level():
        root = build_tree([1, 2, 3])
>       assert root.val == 1
E       AttributeError: 'NoneType' object has no attribute 'val'
```

The two empty-input tests pass (they expect `None`, which is what the stub returns), and the rest fail because there's no tree to inspect. That's the right kind of failure: the test runs, and it's unhappy about the value.

### Write enough code to make it pass

Walk the list breadth-first. Keep a queue of nodes that still need their children attached. The leading value is the root; after that, every node pulls its left and right child values off the list in order, skipping the `None` slots.

```python
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
```

Green.

The key move is that `i` advances **whether or not** the slot held a real value. A `None` still consumes a slot, so node 2's missing left child still "uses up" index 3, and index 4 correctly becomes node 2's right child. We only enqueue real nodes, because only real nodes have children to fill in later.

### Refactor

Nothing to tidy. The function is one pass with a queue, O(n) time and O(n) space for the queue, which is as good as it gets for reading a whole tree. We'll lean on `build_tree` in every problem from here on.

## Problem 1: Invert a binary tree

> Mirror the tree left to right: every node swaps its two children, all the way down.

This is the question a famous tweet claimed got someone rejected from Google, so it has earned its place as the "hello world" of tree recursion. It's a pure DFS: swap the children at the current node, then recurse.

### Write the test first

To check the shape of the result we need to read a whole tree back out, so the test file carries a tiny `level_order` helper that flattens a tree to a list (the inverse of `build_tree`).

```python
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
```

`test_invert_mirrors_children` does the real work. The input has every level filled, so after a correct inversion the whole thing reverses within each level: `2` and `7` swap, and so do all four leaves.

### Try to run the test

No `invert_tree` yet:

```
ImportError: cannot import name 'invert_tree' from 'invert_tree'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to hand the tree straight back, unchanged:

```python
from __future__ import annotations

from .._template import TreeNode


def invert_tree(root):
    return root
```

Run `uv run pytest`:

```
    def test_invert_mirrors_children():
        root = build_tree([4, 2, 7, 1, 3, 6, 9])
>       assert level_order(invert_tree(root)) == [4, 7, 2, 9, 6, 3, 1]
E       assert [4, 2, 7, 1, 3, 6, ...] == [4, 7, 2, 9, 6, 3, ...]
E         
E         At index 1 diff: 2 != 7
```

The empty and single-node tests pass (a tree with nothing to swap is its own mirror), and the real test fails at index 1: we left `2` where `7` should be. The stub returns the tree untouched, which is exactly the bug we expect.

### Write enough code to make it pass

Swap the two children, but swap their *inverted* selves, so the mirroring runs all the way to the leaves. Recurse first, then assign.

```python
from __future__ import annotations

from .._template import TreeNode


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """Mirror the tree: swap every node's left and right child."""
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

Green.

The tuple assignment is doing two jobs at once. The right-hand side runs first: `invert_tree(root.right)` and `invert_tree(root.left)` both finish before either gets assigned, so we don't clobber `root.left` and then read the clobbered value. **Compute the new children, then bind them.** Write it as two separate statements and you'd invert the right subtree, overwrite `root.left` with it, then "invert the right" again and get the same subtree twice.

### Refactor

None needed. Three lines, one base case, one recursive step. This is the template's shape with "swap" as the work.

## Problem 2: Path sum

> Is there a root-to-leaf path whose node values add up to a target number?

The word **leaf** is the trap here. We're not asking whether any path sums to the target, only whether a path that ends at a leaf does. That one constraint is what makes the base case interesting.

### Write the test first

```python
from .build import build_tree
from .has_path_sum import has_path_sum


def test_empty_tree_has_no_path():
    assert has_path_sum(None, 0) is False


def test_single_node_matches():
    assert has_path_sum(build_tree([5]), 5) is True


def test_single_node_misses():
    assert has_path_sum(build_tree([5]), 4) is False


def test_root_to_leaf_path_exists():
    root = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2])
    assert has_path_sum(root, 22) is True


def test_no_matching_path():
    root = build_tree([1, 2, 3])
    assert has_path_sum(root, 5) is False


def test_partial_path_does_not_count():
    # 1 -> 2 sums to 3, but that's not a leaf, so target 1 must reach a leaf.
    root = build_tree([1, 2])
    assert has_path_sum(root, 1) is False
```

`test_partial_path_does_not_count` is the one that earns its keep. The tree is `1` with a single left child `2`. The root alone sums to `1`, which equals the target, but the root *isn't a leaf* (it has a child), so it doesn't count. A solution that checks the sum at every node instead of only at leaves returns `True` here and is wrong.

### Try to run the test

```
ImportError: cannot import name 'has_path_sum' from 'has_path_sum'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always say "no path":

```python
from __future__ import annotations

from .._template import TreeNode


def has_path_sum(root, target):
    return False
```

Run `uv run pytest`:

```
    def test_single_node_matches():
>       assert has_path_sum(build_tree([5]), 5) is True
E       assert False is True
E        +  where False = has_path_sum(<TreeNode object>, 5)

2 failed, 4 passed
```

The four `False`-expecting tests pass by luck (the stub returns `False` and they wanted `False`), and the two that need a real `True` fail on the value. This is the moment the template warns you about: a green test proves nothing when the stub happens to agree with it.

### Write enough code to make it pass

Two base cases this time. An empty subtree has no path, so it's `False`. A leaf (no children) is a hit exactly when its value equals what's left of the target. Otherwise, subtract the current value and ask both children whether they can finish the job.

```python
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
```

Green.

We carry the target *down* the tree instead of summing *up*. Each step spends `root.val` from the remaining budget, and the leaf check asks "did we land on exactly zero left over". That's why `test_partial_path_does_not_count` passes: the leaf test only fires at a node with no children, so the non-leaf root never gets to claim a match.

### Refactor

None needed. The `or` short-circuits, so the moment the left subtree finds a valid path we skip the right one. That's the search shape from the template, with a running budget threaded through.

## Problem 3: Is the tree height-balanced?

> A tree is balanced if, at *every* node, the two subtrees' heights differ by at most one. Return whether the whole tree is balanced.

The naive version computes each node's height and checks the difference, but recomputing height at every node walks the tree over and over, O(n^2) on a skewed tree. We can do better by **returning two facts up the tree at once**: the height, and whether everything below is still balanced. We'll smuggle both into a single integer.

### Write the test first

```python
from .build import build_tree
from .is_balanced import is_balanced


def test_empty_is_balanced():
    assert is_balanced(None) is True


def test_single_node_is_balanced():
    assert is_balanced(build_tree([1])) is True


def test_balanced_tree():
    assert is_balanced(build_tree([3, 9, 20, None, None, 15, 7])) is True


def test_unbalanced_tree():
    root = build_tree([1, 2, 2, 3, 3, None, None, 4, 4])
    assert is_balanced(root) is False
```

`test_unbalanced_tree` is the case that matters. The tree is balanced near the root but goes two levels deeper down one branch than the other, so the imbalance is buried, not at the top. A check that only compares the root's two subtree heights misses it.

### Try to run the test

```
ImportError: cannot import name 'is_balanced' from 'is_balanced'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to claim every tree is balanced:

```python
from __future__ import annotations

from .._template import TreeNode


def is_balanced(root):
    return True
```

Run `uv run pytest`:

```
    def test_unbalanced_tree():
        root = build_tree([1, 2, 2, 3, 3, None, None, 4, 4])
>       assert is_balanced(root) is False
E       assert True is False
E        +  where True = is_balanced(<TreeNode object>)

1 failed, 3 passed
```

Three pass because they really are balanced and the stub guesses `True`. The deep-imbalance case is the one that catches the lie. Now let's make the code actually look.

### Write enough code to make it pass

Here's the trick: an inner `height` function returns the real height of a balanced subtree, or `-1` the moment it finds an imbalance anywhere below. The `-1` is a *sentinel*: once it appears it propagates straight up without any more arithmetic, so we never re-walk a subtree.

```python
from __future__ import annotations

from .._template import TreeNode


def is_balanced(root: TreeNode | None) -> bool:
    """True if every node's two subtrees differ in height by at most one."""

    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) != -1
```

Green.

Each node asks its children for their heights *once*. If either child already reported `-1`, or if this node's own two children differ by more than one, we return `-1` and stop. Otherwise we return the genuine height, `1 + max(left, right)`, exactly like `max_depth` in the template. **One DFS pass carries two answers home: the height, and balance encoded as "is it `-1`".** That's the whole reason this is O(n) instead of O(n^2).

### Refactor

None needed, but it's worth naming the move. Folding two return values into one integer (a real height, or `-1` for "abandon ship") is the trick that keeps this to a single pass. The next problem uses the same idea, except it carries its second answer in a `nonlocal` variable instead.

## Problem 4: Diameter of a binary tree

> The diameter is the number of edges on the longest path between any two nodes. That path doesn't have to pass through the root.

The longest path through a given node is its left subtree's height plus its right subtree's height. So if we already compute height everywhere (we do), we can check "longest path bending at this node" at every node and keep the best. The catch in the problem statement, "doesn't have to pass through the root", is the whole point: the answer can live entirely inside one subtree.

### Write the test first

```python
from .build import build_tree
from .diameter_of_binary_tree import diameter_of_binary_tree


def test_empty_tree_has_zero_diameter():
    assert diameter_of_binary_tree(None) == 0


def test_single_node_has_zero_diameter():
    assert diameter_of_binary_tree(build_tree([1])) == 0


def test_diameter_through_root():
    assert diameter_of_binary_tree(build_tree([1, 2, 3, 4, 5])) == 3


def test_diameter_not_through_root():
    # Longest path lives entirely in the left subtree, never touching the root.
    root = build_tree([1, 2, None, 3, None, 4, 5, 6, None, None, 7])
    assert diameter_of_binary_tree(root) == 4
```

`test_diameter_not_through_root` is the test that distinguishes a correct solution from a tempting wrong one. If you only measured the path that bends at the root (left height plus right height *at the top*), you'd miss a longer path coiled up inside the left subtree. The answer here is `4`, and it never touches the root.

### Try to run the test

```
ImportError: cannot import name 'diameter_of_binary_tree' from 'diameter_of_binary_tree'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
from __future__ import annotations

from .._template import TreeNode


def diameter_of_binary_tree(root):
    return 0
```

Run `uv run pytest`:

```
    def test_diameter_through_root():
>       assert diameter_of_binary_tree(build_tree([1, 2, 3, 4, 5])) == 3
E       assert 0 == 3
E        +  where 0 = diameter_of_binary_tree(<TreeNode object>)

2 failed, 2 passed
```

The two zero-diameter cases pass (a single node or no node has no path, so `0` is right), and the two real cases fail on the value. Exactly the failure we want before writing the real thing.

### Write enough code to make it pass

Compute height with the aggregate-up DFS, and along the way, at every node, update a running `best` with `left + right`, the length of the path that bends here. We keep `best` in a `nonlocal` so the inner `height` can both return the height *and* record the widest path it saw.

```python
from __future__ import annotations

from .._template import TreeNode


def diameter_of_binary_tree(root: TreeNode | None) -> int:
    """Longest path between any two nodes, measured in edges."""
    best = 0

    def height(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
```

Green.

`height` returns `1 + max(left, right)` just like the template, so the recursion is unchanged. The new line is `best = max(best, left + right)`, which runs at *every* node and asks "is the path bending here the longest one yet". Because it fires everywhere, the best can come from deep inside a subtree, which is what `test_diameter_not_through_root` checks. **We compute height once per node and piggyback the diameter on the same pass**, so it's O(n).

### Refactor

None needed. This is the balanced-tree trick again with a different second answer: there we encoded the extra fact as a sentinel return value, here we carry it in a `nonlocal`. Both keep us to one pass. Pick whichever reads cleaner for the problem in front of you.

## Wrapping up

- **DFS on a tree is recursion with one base case (`root is None`) and one recursive step (combine the children).** Get the empty case returning the right identity and the rest follows.
- **The search shape** (`dfs_search`, `has_path_sum`) checks the node, then recurses left `or` right, short-circuiting on the first hit.
- **The aggregate-up shape** (`max_depth`, `is_balanced`, `diameter`) asks each child for a number and folds the children's numbers into its own. This is the "return info up the tree" pattern.
- **When you need a second answer on the same pass**, encode it in the return value (a `-1` sentinel for balance) or carry it in a `nonlocal` (the running `best` for diameter). Either way you stay at O(n) instead of recomputing height at every node.
- **Watch the problem's exact words.** "Root-to-leaf" means the leaf check matters; "doesn't have to pass through the root" means the answer can hide in a subtree.

Next: [BST](bst.md), where the tree's ordering lets DFS prune half the work at every step.
