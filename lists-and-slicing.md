# Lists & slicing

**[You can find all the code for this chapter here](lists_and_slicing/)**

Lists are the array of Python and the single most important data structure for interviews.
Slicing — the `[start:stop:step]` syntax — is the feature that makes Python array code so
short. This chapter drills both, plus the copy-vs-alias gotcha that trips up everyone at least
once.

## Write the test first

Sum a list of numbers. `lists_and_slicing/v1/test_lists_and_slicing.py`:

```python
from .lists_and_slicing import total


def test_sums_a_list_of_numbers():
    assert total([1, 2, 3, 4, 5]) == 15
```

## Write enough code to make it pass

`lists_and_slicing/v1/lists_and_slicing.py`:

```python
def total(numbers):
    result = 0
    for number in numbers:
        result += number
    return result
```

```
1 passed
```

## Refactor — and meet slicing

The loop is just the built-in `sum`. While we refactor, let's add the slicing idioms
(`lists_and_slicing/v2`):

```python
def total(numbers):
    return sum(numbers)


def reversed_list(items):
    return items[::-1]


def tail(items):
    return items[1:]
```

Slice notation is `items[start:stop:step]`, every part optional:

- `items[1:]` — from index 1 to the end (drop the first element).
- `items[:-1]` — everything except the last.
- `items[::-1]` — a reversed **copy** (step of `-1`).
- `items[::2]` — every other element.

A crucial property: **slicing never raises on out-of-range bounds.** `tail([])` is `[]`, not an
error — unlike `[][0]`, which raises `IndexError`. We test that boundary explicitly:

```python
def test_tail_of_empty_list_is_empty():
    assert tail([]) == []
```

## The copy-vs-alias gotcha

This is the one that bites in interviews. Assignment does **not** copy a list — it makes
another name for the *same* object:

```python
def test_plain_assignment_is_an_alias():
    original = [1, 2, 3]
    alias = original          # same list object!
    alias.append(4)
    assert original == [1, 2, 3, 4]   # mutating `alias` changed `original`
```

A full slice `items[:]` (or `list(items)`, or `items.copy()`) makes an independent shallow
copy:

```python
def test_slicing_makes_a_copy_not_an_alias():
    original = [1, 2, 3]
    a_copy = copy_of(original)   # copy_of returns items[:]
    a_copy.append(4)
    assert a_copy == [1, 2, 3, 4]
    assert original == [1, 2, 3]  # untouched
```

```python
def every_other(items):
    return items[::2]


def copy_of(items):
    return items[:]
```

In backtracking problems especially, forgetting to copy the path before appending it to your
results is the classic bug — you end up with a list full of references to the same, later-empty,
list. Slice to copy.

> **Shallow, not deep.** `items[:]` copies the list but not the objects inside it. If your list
> holds other lists, the inner lists are still shared. Reach for `copy.deepcopy` only when you
> truly need it.

## Wrapping up

- **`sum`, `min`, `max`, `len`** — know the built-ins before writing a loop.
- **`items[start:stop:step]`** is the slicing Swiss-army knife; `[::-1]` reverses, `[1:]` drops
  the head, `[::2]` steps.
- **Slicing tolerates out-of-range bounds**; indexing does not.
- **Assignment aliases, slicing copies.** `b = a` shares the list; `b = a[:]` copies it.

Next up, the testing toolbox: [pytest deep dive](pytest-deep-dive.md).
