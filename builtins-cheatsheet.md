# Built-in data structures cheat sheet

Python's standard library does a lot of interview work for you: `collections`, `heapq`, and
`bisect` give you the right data structure with O(1) or O(log n) operations, so you write less
code and it runs faster. This is a reference chapter, so keep it open while you drill the pattern
chapters.

## `list`: the dynamic array

```python
xs = [3, 1, 2]
xs.append(4)        # O(1) amortised, add to the end
xs.pop()            # O(1), remove from the end
xs.sort()           # O(n log n) in place, stable
xs[::-1]            # O(n) reversed copy
xs[1:3]             # O(k) slice (copy)
```

**Trap:** `xs.pop(0)` and `xs.insert(0, x)` are **O(n)**, since they shift every element. For a
queue, use `deque`.

## `dict` and `set`: hashing for O(1) lookup

```python
seen = set()
seen.add(x); x in seen          # O(1)

counts = {}
counts[k] = counts.get(k, 0) + 1
```

Use a `set` for membership/dedup and a `dict` for key to value. Both are O(1) average. `dict`
preserves insertion order (guaranteed since Python 3.7).

## `collections.Counter`: counting, done

```python
from collections import Counter

c = Counter("mississippi")     # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
c.most_common(2)               # [('i', 4), ('s', 4)]
c["z"]                         # 0  (missing keys are 0, no KeyError)
Counter("listen") == Counter("silent")   # True, an anagram check!
```

Counters add and subtract like multisets (`c1 + c2`, `c1 - c2`) and compare by counts. That gives
you the anagram pattern in one line.

## `collections.defaultdict`: no more "if key not in dict"

```python
from collections import defaultdict

graph = defaultdict(list)
graph[u].append(v)             # no KeyError; missing keys default to []

groups = defaultdict(int)
groups[k] += 1                 # missing keys default to 0
```

The factory (`list`, `int`, `set`) supplies a default the first time a key is touched. Perfect
for adjacency lists and grouping.

## `collections.deque`: the O(1) double-ended queue

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)        # O(1) right
q.appendleft(0)    # O(1) left
q.popleft()        # O(1) left  (this is why BFS uses deque)
q.pop()            # O(1) right
```

**Always** use `deque` for BFS and any FIFO queue. A plain list as a queue (`list.pop(0)`) is
O(n) per dequeue, which makes the whole thing O(n²).

## `heapq`: the binary heap (priority queue)

```python
import heapq

h = []
heapq.heappush(h, 3)           # O(log n)
heapq.heappush(h, 1)
smallest = heapq.heappop(h)    # O(log n), returns 1   (MIN-heap)
heapq.heapify(xs)              # O(n) build in place

heapq.nsmallest(3, xs)         # O(n log k)
heapq.nlargest(3, xs)
```

`heapq` is a **min-heap**. For a max-heap, push negated values (`heapq.heappush(h, -x)`) or
push tuples `(-priority, item)`. The top-K and merge-K patterns are built on this.

## `bisect`: binary search on a sorted list

```python
import bisect

i = bisect.bisect_left(xs, target)   # first index >= target  (O(log n))
j = bisect.bisect_right(xs, target)  # first index > target
bisect.insort(xs, x)                 # insert keeping sorted order (O(n) shift)
```

Reach for `bisect` instead of hand-writing boundary searches. See the
[Binary Search](binary-search.md) chapter for when each boundary applies.

## `itertools`: lazy combinatorics

```python
from itertools import accumulate, combinations, permutations, product

list(accumulate([1, 2, 3, 4]))        # [1, 3, 6, 10]  (prefix sums for free)
list(combinations([1, 2, 3], 2))      # [(1,2), (1,3), (2,3)]
list(permutations([1, 2], 2))         # [(1,2), (2,1)]
list(product([0, 1], repeat=2))       # [(0,0),(0,1),(1,0),(1,1)]
```

Handy for brute-forcing small inputs and as a correctness oracle to property-test your clever
solution against.

## Quick reference

| Need | Reach for | Key ops (cost) |
|------|-----------|----------------|
| Membership / dedup | `set` | `add`, `in` (O(1)) |
| Key to value | `dict` | `[]`, `get` (O(1)) |
| Counting | `Counter` | `most_common`, `+`/`-` |
| Grouping / adjacency | `defaultdict` | auto-default value |
| FIFO queue / BFS | `deque` | `append`, `popleft` (O(1)) |
| Priority queue / top-K | `heapq` | `heappush`, `heappop` (O(log n)) |
| Sorted-list search | `bisect` | `bisect_left/right` (O(log n)) |
| Combinatorics | `itertools` | `combinations`, `product` |

## Wrapping up

- The standard library is fair game and expected, so reach for it.
- **`deque` for queues, `heapq` for priority, `Counter`/`defaultdict` for tallies and groups,
  `bisect` for sorted search.**
- Picking the right structure is often the difference between O(n²) and O(n), and far less code.

Next: [Sorting & custom comparators](sorting-and-comparators.md).
