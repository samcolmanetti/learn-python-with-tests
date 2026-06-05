# Sorting & custom comparators

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/sorting_and_comparators)**

Sorting shows up in a huge fraction of interview solutions. Sometimes it's the whole answer, and
sometimes it's the setup that lets two pointers or a greedy sweep work. Python's sort is good; the
skill is knowing how to sort by *the right thing*. That's the `key` function. Let's build the
techniques test-first.

## `sorted` vs `.sort`, and stability

- `sorted(xs)` returns a **new** list; `xs.sort()` sorts **in place** and returns `None`.
- Both are **stable**: elements that compare equal keep their original relative order. That's a
  property you can rely on (and test).

```python
def test_by_length_is_stable():
    # equal-length items keep their input order
    assert by_length(["bb", "aa", "cc"]) == ["bb", "aa", "cc"]
```

## Sort by a key

The `key` is a function mapping each element to something orderable. Sort strings by length:

```python
def test_by_length():
    assert by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]
```

```python
def by_length(words):
    return sorted(words, key=len)
```

`key=len` calls `len` once per element (not per comparison), so it's efficient as well as
readable. This "decorate, then sort" approach is why you almost never need a raw comparator.

## Multi-level sort with a tuple key

Return a **tuple** from the key to sort by several fields. Sort `"First Last"` names by last
name, then first:

```python
def test_by_last_then_first():
    names = ["John Smith", "Jane Adams", "Bob Smith"]
    assert by_last_then_first(names) == ["Jane Adams", "Bob Smith", "John Smith"]
```

```python
def by_last_then_first(names):
    return sorted(names, key=lambda full: (full.split()[-1], full.split()[0]))
```

Tuples compare element by element: sort on the first, break ties on the second, and so on.

## Mixed directions: descending one field, ascending another

There's no per-field `reverse`, but for numbers you can **negate** the key. Sort players by score
descending, then name ascending:

```python
def test_by_score_desc_then_name():
    players = [("alice", 50), ("bob", 90), ("carol", 50)]
    assert by_score_desc_then_name(players) == [("bob", 90), ("alice", 50), ("carol", 50)]
```

```python
def by_score_desc_then_name(players):
    return sorted(players, key=lambda p: (-p[1], p[0]))
```

(For non-numeric descending fields, sort in two stable passes, or reverse afterwards. But `-x`
covers most interview cases.)

## When a key isn't enough: `cmp_to_key`

Sometimes "does `a` come before `b`?" depends on the **pair**, not on any independent property of
each element. The classic is **Largest Number**: arrange integers to form the biggest possible
concatenation.

```python
def test_largest_number():
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"


def test_largest_number_all_zeros():
    assert largest_number([0, 0]) == "0"
```

Why no key works: should `3` come before `30`? Compare `"3"+"30" = "330"` against `"30"+"3" = "303"`.
`330` wins, so `3` goes first. That decision is inherently pairwise. `functools.cmp_to_key` adapts an
old-style comparator (returns negative / 0 / positive) into a key:

```python
from functools import cmp_to_key


def largest_number(nums):
    if not nums:
        return "0"

    def compare(a, b):
        if a + b > b + a:
            return -1   # a should come first
        if a + b < b + a:
            return 1
        return 0

    ordered = sorted((str(n) for n in nums), key=cmp_to_key(compare))
    result = "".join(ordered)
    return "0" if result[0] == "0" else result   # normalise "00" -> "0"
```

The `"0"` normalisation is the edge case the `test_largest_number_all_zeros` test pins down: if
the largest arrangement starts with `0`, every digit is `0`, so the answer is just `"0"`.

## Wrapping up

- **Prefer `key=`**: it's called once per element and expresses intent directly.
- **Tuple keys** do multi-level sorting; **negate** a numeric field to reverse just that field.
- Python's sort is **stable**, so rely on it for "preserve original order among equals".
- **`cmp_to_key`** is the escape hatch for genuinely *pairwise* ordering (Largest Number,
  custom orderings). Reach for it only when no per-element key exists.

Next, the main event: the [Interview patterns](two-pointers.md), starting with Two Pointers.
