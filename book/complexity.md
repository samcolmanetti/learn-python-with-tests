# Complexity & Big-O

You can't reason about an interview solution without reasoning about its cost. Big-O is the
language for that: how the running time (or memory) grows as the input grows. This is a
reference chapter. No new code, just the model and the Python-specific numbers you need in your
head.

## Big-O in one paragraph

Big-O describes the **growth rate** of an algorithm, ignoring constants and lower-order terms.
O(2n + 5) is just O(n). What matters is the *shape*: doubling the input, what happens to the
work? For O(n) it doubles; for O(n²) it quadruples; for O(log n) it barely moves.

## The hierarchy (fastest to slowest)

| Big-O | Name | Doubling `n` means… | Typical source |
|-------|------|---------------------|----------------|
| O(1) | constant | no change | dict/set lookup, arithmetic, list index |
| O(log n) | logarithmic | +1 step | binary search, balanced-tree op |
| O(n) | linear | doubles | single pass, sliding window |
| O(n log n) | linearithmic | a bit more than doubles | sorting, divide & conquer |
| O(n²) | quadratic | ×4 | nested loop over the same array |
| O(2ⁿ) | exponential | squares | naive subsets/recursion without memo |
| O(n!) | factorial | explodes | generating all permutations |

A useful interview rule of thumb: with `n ≤ ~10⁵`, you want O(n) or O(n log n). If you find
yourself at O(n²) on big input, that's the signal to reach for a pattern (two pointers, sliding
window, a hash map) to drop a factor of `n`.

## Time *and* space

Every solution has both. A hash map that turns an O(n²) scan into O(n) time usually costs O(n)
extra space. Name that trade-off out loud in an interview; it shows you understand the cost.
"Can you do it in O(1) space?" is a common follow-up.

## Amortised analysis: why `append` is O(1)

Python lists are dynamic arrays. Most `append`s are O(1), but occasionally the list is full and
Python allocates a bigger backing array and copies everything (an O(n) step). Averaged over many
appends, the cost per append is still O(1): this is **amortised** O(1). The same logic explains
why a sliding window that adds and removes each element once is O(n) overall, even though any
single step might do a little extra work.

## Cost of common Python operations

Keep these in your head, because the wrong data structure is the most common hidden O(n):

| Operation | Cost | Note |
|-----------|------|------|
| `x in list` | **O(n)** | scans every element, a frequent accidental O(n²) inside a loop |
| `x in set` / `x in dict` | **O(1)** | hashing; prefer these for membership |
| `list[i]` (index) | O(1) | |
| `list.append(x)` | O(1) amortised | |
| `list.pop()` (end) | O(1) | |
| `list.pop(0)` (front) | **O(n)** | shifts everything; use `collections.deque` instead |
| `list.insert(0, x)` | **O(n)** | same reason; `deque.appendleft` is O(1) |
| `del list[i]` | O(n) | shifts the tail |
| `dict[k]` get/set | O(1) | average case |
| `heapq.heappush` / `heappop` | O(log n) | |
| `sorted(xs)` / `xs.sort()` | O(n log n) | stable Timsort |
| `min`/`max`/`sum` | O(n) | one pass |
| `" ".join(parts)` | O(total length) | the right way to build strings |
| string `+=` in a loop | **O(n²)** | strings are immutable; collect in a list and `join` |
| slice `xs[a:b]` | O(length of the slice) | makes a copy |
| `set(a) & set(b)` | O(len a + len b) | intersection |

The two that bite most often in interviews: `x in list` inside a loop (silent O(n²), so switch to
a `set`), and `list.pop(0)` / `insert(0, …)` for a queue (switch to `deque`).

## How to talk about it

When you finish a solution, state its complexity unprompted: *"This is O(n) time and O(n) space,
and the dict is what buys us the single pass."* If asked to do better, the table above is your menu:
can a set replace a scan? can sorting get you two pointers? can a heap avoid a full sort?

## Wrapping up

- Big-O is about **growth shape**; drop constants and lower-order terms.
- Aim for **O(n) or O(n log n)** on inputs up to ~10⁵.
- Always name **time and space**; patterns usually trade space for time.
- Know the **hidden O(n)s**: `in list`, `pop(0)`, `insert(0, …)`, and `+=` on strings.

Next: the [Built-in data structures cheat sheet](builtins-cheatsheet.md), the tools that make
the fast option the easy option.
