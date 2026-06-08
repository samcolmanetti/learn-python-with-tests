# Binary Search Tree

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/bst)**

A binary search tree is a binary tree with one extra rule, and that rule turns search into a
walk down a single path. It's an **interview pattern**: a reusable [`bst/_template.py`](bst/_template.py)
holding the node and the invariant, plus worked problems in `bst/solutions/`, each built test-first.

## When to reach for a BST

The shape on its own buys you nothing. What you're really buying is the ordering rule, so reach for
it when:

- You need a structure that keeps elements **sorted while you insert and delete**, and you want
  search, insert, and delete all in O(h) where `h` is the height (O(log n) when the tree stays
  balanced).
- A problem hands you a tree and tells you it's a BST. That word is a gift: it means you can
  decide left-or-right at every node instead of searching both sides. Use it.
- You're asked for an in-order property (the kth smallest, the floor of a value, a range of keys).
  An in-order walk of a BST visits keys in sorted order, for free.

## The template

The template is small. It's a node and a note about the one rule that makes the node a BST.

```python
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
```

That's just a binary tree node, the same one you'd use for any tree. What makes a tree a *binary
search tree* is the **invariant** every node obeys:

> every key in its left subtree `<` `node.val` `<` every key in its right subtree

Read it carefully, because the trap is in the word *subtree*. The rule is not "the left child is
smaller and the right child is larger". It's that the *entire left subtree* is smaller and the
*entire right subtree* is larger. A node can be a perfectly good child of its parent and still
break the invariant because it sits in a subtree whose root, higher up, demanded everything below
it be smaller. We'll fall into exactly that trap in Problem 1 and climb back out.

The `from __future__ import annotations` import lets us write `TreeNode | None` as a type hint even
though `TreeNode` isn't finished being defined yet, and keeps the file running on Python 3.9. You'll
see that import at the top of every solution file too.

## Problem 1: Validate a BST

> Given the root of a binary tree, return `True` if it's a valid binary search tree.

This is the problem that teaches the invariant, because the obvious solution is wrong in an
interesting way.

### Write the test first

```python
from _template import TreeNode
from validate_bst import is_valid_bst


def test_empty_tree_is_valid():
    assert is_valid_bst(None) is True


def test_single_node_is_valid():
    assert is_valid_bst(TreeNode(1)) is True


def test_simple_valid_tree():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(root) is True


def test_left_child_too_big():
    root = TreeNode(2, TreeNode(3), TreeNode(4))
    assert is_valid_bst(root) is False


def test_deep_violation_passes_neighbour_check():
    # 5 / (1, 6); right child 6 has children 3 and 7.
    # 3 sits in the right subtree of 5, so it breaks the invariant
    # even though it's a valid child of its own parent (6).
    root = TreeNode(5, TreeNode(1), TreeNode(6, TreeNode(3), TreeNode(7)))
    assert is_valid_bst(root) is False


def test_equal_values_are_not_valid():
    root = TreeNode(2, TreeNode(2), TreeNode(3))
    assert is_valid_bst(root) is False
```

`test_deep_violation_passes_neighbour_check` is the one that earns its keep. The `3` is a fine left
child of its parent `6`, but it lives in the right subtree of `5`, so it has to be larger than `5`,
and it isn't. Any solution that only compares a node to its immediate children gets this wrong.
`test_equal_values_are_not_valid` pins down that we want strict inequality: duplicates break it.

### Try to run the test

We've imported `is_valid_bst` from a module that doesn't define it, so the import fails before any
test runs:

```
ImportError: cannot import name 'is_valid_bst' from 'bst.solutions.validate_bst'
```

Listen to the error. It's telling us the function has to exist before anything else can happen.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a function that always says `True`. We know it's wrong, and that's the point: we want to
watch the tests fail on the value so we know they're actually checking something.

```python
from __future__ import annotations

from _template import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    return True
```

Run `uv run pytest`:

```
    def test_left_child_too_big():
        root = TreeNode(2, TreeNode(3), TreeNode(4))
>       assert is_valid_bst(root) is False
E       assert True is False
E        +  where True = is_valid_bst(<bst._template.TreeNode object at 0x1084a5370>)
```

The three "should be `False`" tests fail on the value, and the valid-tree tests pass only because
our stub happens to agree with them. Good: the tests run, and they fail for the right reason.

### Write enough code to make it pass

Here's the fix for the subtree trap. Instead of comparing a node to its children, we carry a
`(low, high)` range down the tree. Every node has to fall strictly inside its allowed range, and
as we descend we tighten that range: going left, the current value becomes the new upper bound;
going right, it becomes the new lower bound.

```python
from __future__ import annotations

from _template import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    """True if ``root`` satisfies the BST invariant for every subtree."""

    def within(node: TreeNode | None, low: float, high: float) -> bool:
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return within(node.left, low, node.val) and within(node.right, node.val, high)

    return within(root, float("-inf"), float("inf"))
```

The tests pass.

We start the root off with the widest possible range, `(-inf, +inf)`, because the root can be any
value. When we go left into `node.val`'s left subtree, every node there must be less than
`node.val`, so `node.val` becomes the new `high`. When we go right, it becomes the new `low`. That
`3` from the failing test inherits `low = 5` on the way down (it's in `5`'s right subtree), and
`3 < 5` fails the `low < node.val` check. The trap is sprung exactly where it should be.

Using `float("-inf")` and `float("inf")` as the starting bounds saves us a special case for the
root. The strict `<` on both sides is what rejects duplicates, which is why
`test_equal_values_are_not_valid` passes.

### Refactor

The function is already tight, but it's worth naming the shape. `within` is a recursive walk that
threads an *accumulator* (the range) through each call, narrowing it as it descends. That
range-passing idea is the whole trick, and it's the thing to remember from this problem. Re-run the
tests to confirm nothing moved.

## Problem 2: Search a BST

> Given the root of a BST and a target value, return the subtree rooted at the node with that
> value, or `None` if it isn't there.

Now we get to spend the invariant rather than check it. Because we know the tree is a BST, every
comparison eliminates half of what's left.

### Write the test first

```python
from _template import TreeNode
from search_bst import search_bst


def build_sample():
    # 4 / (2, 7); 2 has children 1 and 3.
    return TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7))


def test_finds_root():
    root = build_sample()
    found = search_bst(root, 4)
    assert found is root


def test_finds_deep_node():
    root = build_sample()
    found = search_bst(root, 3)
    assert found is not None
    assert found.val == 3


def test_missing_returns_none():
    root = build_sample()
    assert search_bst(root, 5) is None


def test_empty_tree_returns_none():
    assert search_bst(None, 1) is None


def test_returns_whole_subtree():
    root = build_sample()
    found = search_bst(root, 2)
    assert found is not None
    assert found.left is not None and found.left.val == 1
    assert found.right is not None and found.right.val == 3
```

`test_returns_whole_subtree` is deliberate: search returns the *node*, and the node carries its
children, so we check the subtree comes back intact rather than just the value.

### Try to run the test

```
ImportError: cannot import name 'search_bst' from 'bst.solutions.search_bst'
```

Same story as before. The function has to exist first.

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always return `None`:

```python
from __future__ import annotations

from _template import TreeNode


def search_bst(root: TreeNode | None, target: int) -> TreeNode | None:
    return None
```

Run `uv run pytest`:

```
    def test_finds_root():
        root = build_sample()
        found = search_bst(root, 4)
>       assert found is root
E       assert None is <bst._template.TreeNode object at 0x108812520>
```

The "missing" and "empty" tests pass because `None` is genuinely the right answer for them. The
ones that should find a node fail on `None`. Now let's make them all pass.

### Write enough code to make it pass

Walk down from the root. At each node, if it's the target we're done; if the target is smaller, go
left; otherwise go right. We never look at both sides.

```python
from __future__ import annotations

from _template import TreeNode


def search_bst(root: TreeNode | None, target: int) -> TreeNode | None:
    """Return the subtree rooted at ``target``, or ``None`` if it isn't present."""
    node = root
    while node is not None and node.val != target:
        node = node.left if target < node.val else node.right
    return node
```

Green.

The loop stops in one of two ways: it lands on a node whose value matches (and returns it, children
and all), or it walks off the bottom into `None` (and returns that). Each step moves one level
down, so the whole search costs O(h). On a balanced tree that's O(log n), which is the entire
reason you'd store data in a BST instead of a list.

### Refactor

This reads cleanly as an iterative walk, so I'd leave it. You could write it recursively to mirror
Problem 1, but the loop has no stack to grow and says exactly what it does. No change needed.

## Problem 3: Insert into a BST

> Given the root of a BST and a value to insert, add it as a new leaf and return the root.

Inserting is searching that doesn't give up: you walk to where the value *would* be, and when you
fall off the tree, that empty spot is exactly where the new leaf goes.

### Write the test first

```python
from _template import TreeNode
from insert_into_bst import insert_into_bst
from validate_bst import is_valid_bst


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


def test_insert_into_empty_creates_root():
    root = insert_into_bst(None, 5)
    assert root.val == 5
    assert root.left is None and root.right is None


def test_insert_smaller_goes_left():
    root = TreeNode(4)
    insert_into_bst(root, 2)
    assert root.left is not None and root.left.val == 2
    assert root.right is None


def test_insert_larger_goes_right():
    root = TreeNode(4)
    insert_into_bst(root, 7)
    assert root.right is not None and root.right.val == 7
    assert root.left is None


def test_insert_keeps_tree_sorted():
    root = None
    for val in [4, 2, 7, 1, 3, 6]:
        root = insert_into_bst(root, val)
    assert inorder(root) == [1, 2, 3, 4, 6, 7]
    assert is_valid_bst(root) is True


def test_returns_same_root_when_not_empty():
    root = TreeNode(4)
    returned = insert_into_bst(root, 9)
    assert returned is root
```

`test_insert_keeps_tree_sorted` is the real test. It builds a tree one insert at a time, then uses
the `inorder` helper and the `is_valid_bst` we wrote back in Problem 1 to assert the tree comes out
both sorted and valid. Reusing `is_valid_bst` here is a small joy: work from an earlier problem
becomes a test oracle for this one.

### Try to run the test

```
ImportError: cannot import name 'insert_into_bst' from 'bst.solutions.insert_into_bst'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always return a brand-new node and ignore the tree entirely:

```python
from __future__ import annotations

from _template import TreeNode


def insert_into_bst(root: TreeNode | None, val: int) -> TreeNode:
    return TreeNode(val)
```

Run `uv run pytest`:

```
    def test_insert_smaller_goes_left():
        root = TreeNode(4)
        insert_into_bst(root, 2)
>       assert root.left is not None and root.left.val == 2
E       assert (None is not None)
E        +  where None = <bst._template.TreeNode object at 0x10ab1c670>.left
```

The empty-tree test passes (a fresh node is the right answer there), but every test that inserts
*into* an existing tree fails, because our stub throws the tree away. The sorted-tree test in
particular collapses to `[6]`, the last value we made a node for. Now let's wire it into the tree.

### Write enough code to make it pass

Recurse toward the spot where the value belongs. When we reach a `None` (an empty slot), that's
where the new leaf goes, so we return a new node and let the caller reattach it.

```python
from __future__ import annotations

from _template import TreeNode


def insert_into_bst(root: TreeNode | None, val: int) -> TreeNode:
    """Insert ``val`` as a new leaf and return the (possibly new) root."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
```

The tests pass.

The trick is the reassignment `root.left = insert_into_bst(root.left, val)`. When the recursion hits
an empty child, it returns a fresh node, and that line hangs the new node onto its parent. When the
child already exists, the recursive call returns the *same* child (unchanged except deeper down), so
the assignment is a harmless no-op that keeps the link intact. Either way the function returns the
root it was given, which is why `test_returns_same_root_when_not_empty` holds: we only mint a new
root when the tree was empty to begin with.

### Refactor

The reassign-the-child idiom is worth keeping in your pocket: it's the same shape you use to delete
a node or to build any recursive tree mutation. There's nothing to tidy here, so we'll re-run the
tests and move on.

## Problem 4: Lowest common ancestor in a BST

> Given a BST and two values `p` and `q` that are both present, return the value at their lowest
> common ancestor: the deepest node that has both in its subtree.

In a general tree this needs real work. In a BST it's almost embarrassingly easy, because the
ordering tells you which way each value went.

### Write the test first

```python
from _template import TreeNode
from lowest_common_ancestor_bst import lowest_common_ancestor


def build_sample():
    # 6
    #    / (2, 8)
    # 2 has children 0 and 4; 4 has children 3 and 5.
    # 8 has children 7 and 9.
    return TreeNode(
        6,
        TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
        TreeNode(8, TreeNode(7), TreeNode(9)),
    )


def test_split_across_root():
    root = build_sample()
    assert lowest_common_ancestor(root, 2, 8).val == 6


def test_both_in_left_subtree():
    root = build_sample()
    assert lowest_common_ancestor(root, 0, 5).val == 2


def test_ancestor_is_one_of_the_nodes():
    root = build_sample()
    assert lowest_common_ancestor(root, 2, 4).val == 2


def test_deep_pair():
    root = build_sample()
    assert lowest_common_ancestor(root, 3, 5).val == 4
```

`test_ancestor_is_one_of_the_nodes` covers the case people forget: a node can be its own ancestor.
`2` is the LCA of `2` and `4`, because `4` lives in `2`'s subtree.

### Try to run the test

```
ImportError: cannot import name 'lowest_common_ancestor' from 'bst.solutions.lowest_common_ancestor_bst'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return the root no matter what:

```python
from __future__ import annotations

from _template import TreeNode


def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> TreeNode:
    return root
```

Run `uv run pytest`:

```
    def test_both_in_left_subtree():
        root = build_sample()
>       assert lowest_common_ancestor(root, 0, 5).val == 2
E       assert 6 == 2
E        +  where 6 = <bst._template.TreeNode object at 0x106142310>.val
```

`test_split_across_root` passes by luck, because the root really is the answer when the two values
straddle it. The rest fail: returning the root is too shallow whenever both values live on the same
side. Now let's descend properly.

### Write enough code to make it pass

Walk down from the root. If both values are smaller than the current node, the answer is somewhere
left, so go left. If both are larger, go right. The moment they *split* (one goes left and one goes
right, or one of them equals the current node), the current node is the lowest node that contains
both, and we return it.

```python
from __future__ import annotations

from _template import TreeNode


def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> TreeNode:
    """Return the lowest node that has both ``p`` and ``q`` in its subtree.

    Both values are assumed present in the tree.
    """
    node = root
    while node is not None:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node
    raise ValueError("p and q must both be present in the tree")
```

Green.

The split is the whole insight. As long as both values are on the same side, the ancestor has to be
deeper, so we keep descending. The first node where they part ways, or where one of them *is* the
node, is by definition the lowest one whose subtree holds both. That's why
`test_ancestor_is_one_of_the_nodes` works: when we reach `2`, the value `2` is not less than `2` and
not greater than `2`, so we fall into the `else` and return `2`.

The final `raise` can't actually fire given the problem's promise that both values are present, but
it keeps the function honest about its assumption rather than silently walking off the tree and
returning `None`.

### Refactor

Nothing to refactor: the loop is already the algorithm. It's O(h) time and O(1) space, no recursion
stack, because the BST ordering hands us the direction for free at every step. **That free
direction is the thing every BST problem is really about.**

## Wrapping up

- **The BST invariant is about subtrees, not neighbours**: every key on the left is smaller, every
  key on the right is larger. Validate it by threading a `(low, high)` range down the tree, not by
  comparing a node to its children.
- **Search, insert, and LCA all spend the same coin**: at each node the ordering tells you to go
  left or right, so you visit one path instead of the whole tree. That's O(h), which is O(log n)
  when the tree is balanced.
- **Insert with the reassign-the-child idiom** (`root.left = insert(root.left, val)`), the same
  shape you'll reuse for deletion and other recursive tree edits.
- **An in-order walk of a BST yields sorted keys**, which makes earlier solutions (like
  `is_valid_bst`) handy as test oracles and opens up the kth-smallest and range-query variants.

The catch worth remembering: all of these are O(h), and `h` is only O(log n) if the tree stays
balanced. Insert sorted data into a plain BST and it degrades into a linked list with O(n)
everything. Self-balancing trees fix that, but for interviews the four walks above carry you a long
way.
