# Trees: BFS

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/trees_bfs)**

Depth-first search dives down one branch before trying the next. Breadth-first search does the
opposite: it visits a tree level by level, top to bottom, using a queue. That ordering is the
whole point, and it's what makes BFS the right tool for a surprising number of tree problems.

## When to reach for BFS

DFS and BFS both visit every node, so when the question is "do something to all the nodes" either
works. Reach for BFS specifically when the *level* matters, or when *closest* matters:

- The answer is organised **by level**: group values by depth, alternate direction per level, or
  read one node per level (the leftmost, the rightmost).
- You want the **shortest path** or the **nearest** something. BFS reaches nodes in order of
  distance from the root, so the first time it hits a match, that match is the closest one. DFS
  has to explore everything and then take a minimum.

The signal in an interview is the word "level", or any flavour of "shortest" and "minimum
depth". When you hear it, picture a queue.

## The template

Here's the skeleton from [`trees_bfs/_template.py`](trees_bfs/_template.py). It's plain
level-order traversal: return the node values grouped by depth.

```python
from collections import deque


def level_order(root):
    if root is None:
        return []
    levels = []
    queue = deque([root])
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
```

We use a `deque` from `collections`, not a plain list, because we pop from the front every
iteration and `list.pop(0)` is O(n) while `deque.popleft()` is O(1). A queue that's slow to
dequeue is barely a queue.

The line that does the real work is `for _ in range(len(queue))`. **We snapshot the queue's
length at the start of each level, then process exactly that many nodes.** Everything we pop
in that loop belongs to the current level; everything we append belongs to the next one. By the
time the inner loop ends, the queue holds precisely the next level and nothing else.

That snapshot is the invariant worth memorising: *at the top of the outer `while`, the queue
contains all the nodes of one level and only that level.* Every problem in this chapter is a
small variation on what we do inside that inner loop.

The template uses a `Protocol` for the node type so it works with any object that has `.val`,
`.left`, and `.right`. Our solutions use a concrete `TreeNode` from
[`trees_bfs/node.py`](trees_bfs/node.py), the same minimal node the tree chapters share: a value
and two child links.

## Problem 1: Binary Tree Zigzag Level Order Traversal

> Return the values level by level, but alternate the reading direction: the first level left to
> right, the second right to left, and so on.

This is `level_order` with a twist, so it's a good first variation. The traversal doesn't change
at all. Only the order we record values within a level flips every other level.

### Write the test first

```python
from node import TreeNode
from zigzag_level_order import zigzag_level_order


def test_empty_tree():
    assert zigzag_level_order(None) == []


def test_single_node():
    assert zigzag_level_order(TreeNode(1)) == [[1]]


def test_three_levels_alternate():
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert zigzag_level_order(root) == [[3], [20, 9], [15, 7]]


def test_four_levels_flips_twice():
    #          1
    #         / \
    #        2   3
    #       /   / \
    #      4   5   6
    #     /
    #    7
    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4, TreeNode(7))),
        TreeNode(3, TreeNode(5), TreeNode(6)),
    )
    assert zigzag_level_order(root) == [[1], [3, 2], [4, 5, 6], [7]]
```

`test_three_levels_alternate` is the one that pins the behaviour down: level 1 reads `[20, 9]`,
reversed from the order we'd visit them. And `test_four_levels_flips_twice` proves the flag flips
back, so level 2 reads left to right again.

### Try to run the test

The module doesn't exist yet, so the import is the first thing to break:

```
ImportError: cannot import name 'zigzag_level_order' from 'trees_bfs.solutions.zigzag_level_order'
```

Listen to the error: it tells us exactly what to create next.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a function that returns an empty list, no matter the input. We're not solving anything
yet. We just want the tests to run so we can watch them fail on the value, which proves they
check what we think they do.

```python
from __future__ import annotations

from node import TreeNode


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    return []
```

Run `uv run pytest`:

```
    def test_single_node():
>       assert zigzag_level_order(TreeNode(1)) == [[1]]
E       assert [] == [[1]]
E         Right contains one more item: [1]

FAILED test_zigzag_level_order.py::test_single_node
1 passed, 3 failed
```

The one that passes is `test_empty_tree`, which happens to expect `[]`, exactly what our stub
returns. The other three fail on the value. That's the failure we wanted: the tests run and
disagree with the stub for the right reason.

### Write enough code to make it pass

Start from the template's traversal and add a `left_to_right` flag that flips each level. When
we're going right to left, we still visit nodes in the same queue order, but we record each value
at the *front* of the level instead of the back. A `deque` with `appendleft` makes that O(1).

```python
from __future__ import annotations

from collections import deque

from node import TreeNode


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
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
```

The tests pass.

Notice the traversal is byte-for-byte the template: same queue, same `popleft`, same children
appended left then right. **We never reverse the queue itself, only the order we collect values
into a level.** Reversing the traversal would scramble which nodes land on the next level;
reversing the output keeps the structure correct and just changes the reading direction.

### Refactor

We could build each level as a plain `list` and call `level.reverse()` on the odd levels
instead of using a `deque` with `appendleft`. Both are fine. I prefer the `deque` here because it
collects values in their final order as it goes, so there's no second pass and no off-by-one to
get wrong about which levels to reverse. It reads as "append at this end or that end", which is
exactly the idea. Re-run the tests to confirm nothing moved.

## Problem 2: Binary Tree Right Side View

> Imagine standing to the right of the tree. Return the values you can see, top to bottom: the
> last node of each level.

This is where the level snapshot earns its keep. Once you know exactly which nodes form a level,
the rightmost one is just the last node you pop in the inner loop.

### Write the test first

```python
from node import TreeNode
from right_side_view import right_side_view


def test_empty_tree():
    assert right_side_view(None) == []


def test_single_node():
    assert right_side_view(TreeNode(1)) == [1]


def test_rightmost_per_level():
    #        1
    #       / \
    #      2   3
    #       \   \
    #        5   4
    root = TreeNode(1, TreeNode(2, None, TreeNode(5)), TreeNode(3, None, TreeNode(4)))
    assert right_side_view(root) == [1, 3, 4]


def test_left_node_visible_when_no_right():
    #        1
    #       /
    #      2
    #     /
    #    3
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert right_side_view(root) == [1, 2, 3]


def test_deeper_left_subtree_shows_through():
    #          1
    #         / \
    #        2   3
    #       /
    #      4
    # Level 2 has only node 4 (a left child), so it is the rightmost on its level.
    root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
    assert right_side_view(root) == [1, 3, 4]
```

`test_left_node_visible_when_no_right` and `test_deeper_left_subtree_shows_through` are the cases
that stop you from cheating. **"Right side view" does not mean "always go right".** It means the
last node on each level, and that node can be a left child when the right side of the tree is
shorter. A solution that just walks right children gets both of these wrong.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'right_side_view' from 'trees_bfs.solutions.right_side_view'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations

from node import TreeNode


def right_side_view(root: TreeNode | None) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_single_node():
>       assert right_side_view(TreeNode(1)) == [1]
E       assert [] == [1]
E         Right contains one more item: 1

FAILED test_right_side_view.py::test_single_node
1 passed, 4 failed
```

`test_empty_tree` passes by luck (it expects `[]`); the rest fail on the value. Good, the tests
are wired up and watching.

### Write enough code to make it pass

Walk the tree level by level. Keep the snapshot length in a variable so we can spot the last node
of the level: when the loop index `i` reaches `level_size - 1`, that node is the rightmost on its
level, so we record it.

```python
from __future__ import annotations

from collections import deque

from node import TreeNode


def right_side_view(root: TreeNode | None) -> list[int]:
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
```

Green.

We still append children left then right, so the last node we pop on each level really is the
rightmost one. **Because the snapshot tells us the level's exact size, "last on this level" is
just `i == level_size - 1`, no lookahead and no second list.** The left-child cases pass for free:
if a level has only a left child, then that child is the last node we pop, so it's the one we see.

### Refactor

Nothing to tidy in the algorithm. One thing worth naming: a left-side view is the same code with
`i == 0` instead of `i == level_size - 1`. The level snapshot makes "first on this level" and
"last on this level" equally cheap, which is why both views are one BFS with a one-line change.
Re-run the tests.

## Problem 3: Minimum Depth of Binary Tree

> Return the number of nodes on the shortest path from the root down to a leaf. A leaf is a node
> with no children.

This is the problem that shows why BFS, not DFS, belongs in your toolkit. The DFS version has to
visit every node, compute every root-to-leaf path, and take the minimum. BFS reaches nodes in
order of depth, so **the first leaf it meets is the shallowest one, and we can return on the
spot.**

### Write the test first

```python
from node import TreeNode
from min_depth import min_depth


def test_empty_tree_is_zero():
    assert min_depth(None) == 0


def test_single_node_is_one():
    assert min_depth(TreeNode(1)) == 1


def test_shortest_branch_wins():
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    # The shortest root-to-leaf path ends at 9, depth 2.
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert min_depth(root) == 2


def test_single_child_is_not_a_leaf():
    #    1
    #     \
    #      2
    #       \
    #        3
    # Node 1 has only a right child, so it is not a leaf. The only leaf is 3, depth 3.
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert min_depth(root) == 3
```

`test_single_child_is_not_a_leaf` is the trap. A node with one child is *not* a leaf, so its
depth doesn't count as a candidate. The shortest path has to end at a real leaf, node `3` at depth
`3`. A naive `1 + min(left, right)` returns `1` here, because the missing left subtree has depth
`0`. That's wrong, and this test catches it.

### Try to run the test

No module yet:

```
ImportError: cannot import name 'min_depth' from 'trees_bfs.solutions.min_depth'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations

from node import TreeNode


def min_depth(root: TreeNode | None) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_single_node_is_one():
>       assert min_depth(TreeNode(1)) == 1
E       assert 0 == 1
E        +  where 0 = min_depth(TreeNode(1))

FAILED test_min_depth.py::test_single_node_is_one
1 passed, 3 failed
```

`test_empty_tree_is_zero` passes because it wants `0`; the rest fail on the value. Now let's make
them all pass for the right reason.

### Write enough code to make it pass

Carry each node's depth alongside it in the queue, as a `(node, depth)` pair. The first time we
pop a leaf, return its depth. Because BFS visits shallower nodes before deeper ones, that first
leaf is guaranteed to be the shallowest, so we never look at the rest of the tree.

```python
from __future__ import annotations

from collections import deque

from node import TreeNode


def min_depth(root: TreeNode | None) -> int:
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
```

The tests pass, including the single-child trap. We only call something a leaf when *both*
children are `None`, so node `1` in that tree is skipped and we walk on to the real leaf at depth
`3`.

Notice this version doesn't use the level-snapshot loop. It doesn't need to: we track depth per
node in the tuple, so we never have to know where one level ends and the next begins. Both styles
are BFS. The snapshot groups nodes by level; the depth-tagged queue just needs to know how far
down each node sits.

### Refactor

The early `return depth` is the entire optimisation, so there's nothing to factor out. It's worth
saying plainly why this beats DFS: DFS would compute the depth of every leaf and take the minimum,
visiting all `n` nodes. BFS stops at the first leaf, so on a tree with a shallow branch it can
return after touching a tiny fraction of the nodes. **When the question is "shortest" or
"minimum depth", BFS's visit order is the algorithm.** Re-run the tests one last time.

## Wrapping up

- **BFS visits a tree level by level with a `deque`**, popping from the front in O(1). It's the
  tool when the level matters or the nearest thing matters.
- **The level snapshot is the core trick**: `for _ in range(len(queue))` processes exactly one
  level, because everything you pop belongs to this level and everything you append belongs to the
  next. Right side view falls straight out of it.
- **Zigzag is the same traversal with the output reversed**, never the queue. Reverse the queue
  and you scramble the next level.
- **For minimum depth, BFS returns at the first leaf it meets**, which is the shallowest, so it
  beats DFS by not exploring the whole tree. Carry depth in the queue as a `(node, depth)` pair,
  and remember a one-child node is not a leaf.
