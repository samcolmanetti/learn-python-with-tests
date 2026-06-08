# Lists & slicing

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/lists_and_slicing)**

Lists are the array of Python and the single most important data structure for interviews.
Slicing (the `[start:stop:step]` syntax) is the feature that makes Python array code so short.
This chapter drills both, plus the copy-vs-alias gotcha that trips up everyone at least once.

## Write the test first

Start small: sum a list of numbers. `test_lists_and_slicing.py`:

```python
from lists_and_slicing import total


def test_sums_a_list_of_numbers():
    assert total([1, 2, 3, 4, 5]) == 15
```

## Try to run the test

We've imported `total` from a module that doesn't define it yet, so the import is the first thing
to break:

```
ImportError: cannot import name 'total' from 'lists_and_slicing'
```

No function, nothing. Listen to the error: it's telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `total` that returns a stub `0`. We're not solving anything yet. We just want the test to
run so we can watch it fail on the value, which proves the test checks what we think it does.

```python
def total(numbers):
    return 0
```

Run `uv run pytest`:

```
    def test_sums_a_list_of_numbers():
>       assert total([1, 2, 3, 4, 5]) == 15
E       assert 0 == 15
E        +  where 0 = total([1, 2, 3, 4, 5])
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

Loop over the numbers and add them up. `lists_and_slicing.py`:

```python
def total(numbers):
    result = 0
    for number in numbers:
        result += number
    return result
```

Run the tests again and they're green.

## Refactor

That loop is just the built-in `sum`. The tests are our safety net, so swap it in and re-run:

```python
def total(numbers):
    return sum(numbers)
```

Still green, and shorter. **Know the built-ins before you reach for a loop.** While we're here,
let's add a couple of slicing idioms in the same file, each driven by a test.

## Write the test first

Our next requirement is reversing a list and dropping its head. The next tests, edited in the same file:

```python
def test_reverses_a_list_via_slicing():
    assert reversed_list([1, 2, 3]) == [3, 2, 1]


def test_tail_drops_the_first_element():
    assert tail([1, 2, 3]) == [2, 3]


def test_tail_of_empty_list_is_empty():
    assert tail([]) == []
```

That last case is deliberate. Slicing never raises on out-of-range bounds, so `tail([])` is `[]`,
not an error, unlike `[][0]` which raises `IndexError`. We pin that boundary down explicitly.

## Try to run the test

Neither function exists yet, so the import fails first:

```
ImportError: cannot import name 'reversed_list' from 'lists_and_slicing'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub both functions to return an empty list so the tests run:

```python
def reversed_list(items):
    return []


def tail(items):
    return []
```

Run `uv run pytest`:

```
    def test_reverses_a_list_via_slicing():
>       assert reversed_list([1, 2, 3]) == [3, 2, 1]
E       assert [] == [3, 2, 1]
```

`test_tail_of_empty_list_is_empty` passes by luck (the stub returns `[]`, which is what it wants),
but the other two fail on the value. That's a fine reminder that one green test proves nothing on
its own.

## Write enough code to make it pass

Both are one-line slices:

```python
def reversed_list(items):
    return items[::-1]


def tail(items):
    return items[1:]
```

Green. Slice notation is `items[start:stop:step]`, every part optional:

- `items[1:]` from index 1 to the end (drop the first element).
- `items[:-1]` everything except the last.
- `items[::-1]` a reversed **copy** (step of `-1`).
- `items[::2]` every other element.

## Refactor

There's nothing to tidy in two one-liners, so the refactor here is about naming the property we
just leaned on. **Slicing tolerates out-of-range bounds; indexing does not.** `tail([])` returns
`[]` because the slice clamps to what's there, whereas `[][0]` would raise. That tolerance is why
slice-based array code stays short: you rarely need a length check first. Re-run the tests to
confirm nothing moved.

## Write the test first

Now for the one that bites in interviews. Assignment does **not** copy a list, it makes another
name for the *same* object. A full slice `items[:]` makes an independent copy. The next tests pin
down both halves:

```python
def test_plain_assignment_is_an_alias():
    original = [1, 2, 3]
    alias = original  # NOT a copy, same underlying list object
    alias.append(4)
    assert original == [1, 2, 3, 4]


def test_slicing_makes_a_copy_not_an_alias():
    original = [1, 2, 3]
    a_copy = copy_of(original)
    a_copy.append(4)
    assert a_copy == [1, 2, 3, 4]
    assert original == [1, 2, 3]
```

The first test mutates through the alias and watches `original` change. The second copies first,
mutates the copy, and asserts `original` is untouched. While we're in here we'll also add
`every_other`:

```python
def test_every_other_takes_a_step_slice():
    assert every_other([0, 1, 2, 3, 4, 5]) == [0, 2, 4]
```

## Try to run the test

`copy_of` and `every_other` don't exist yet, so the import is what fails first:

```
ImportError: cannot import name 'every_other' from 'lists_and_slicing'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub the two new functions. Return the input unchanged from `copy_of` (a wrong answer: that's an
alias, not a copy) and an empty list from `every_other`:

```python
def every_other(items):
    return []


def copy_of(items):
    return items  # deliberately wrong: returns the same object, not a copy
```

Run `uv run pytest`:

```
    def test_slicing_makes_a_copy_not_an_alias():
        original = [1, 2, 3]
        a_copy = copy_of(original)
        a_copy.append(4)
        assert a_copy == [1, 2, 3, 4]
>       assert original == [1, 2, 3]
E       assert [1, 2, 3, 4] == [1, 2, 3]
```

The stub returns the same object, so appending to `a_copy` also changed `original`. The test fails
on exactly the bug it's there to catch. Good.

## Write enough code to make it pass

`every_other` is a step slice, and `copy_of` is a full slice, which makes an independent shallow
copy (`lists_and_slicing.py`):

```python
def every_other(items):
    return items[::2]


def copy_of(items):
    return items[:]
```

The tests pass. `list(items)` and `items.copy()` do the same thing as `items[:]`; pick whichever
reads best.

## Refactor

The functions are already as small as they get, so the refactor is about understanding, not lines.
**Assignment aliases, slicing copies.** `b = a` shares the list; `b = a[:]` copies it. In
backtracking problems especially, forgetting to copy the path before appending it to your results
is the classic bug: you end up with a list full of references to the same, later-empty list. Slice
to copy. Re-run the tests one more time to confirm.

One caveat worth holding onto:

> **Shallow, not deep.** `items[:]` copies the list but not the objects inside it. If your list
> holds other lists, the inner lists are still shared. Reach for `copy.deepcopy` only when you
> truly need it.

## Wrapping up

- **`sum`, `min`, `max`, `len`**: know the built-ins before writing a loop.
- **`items[start:stop:step]`** is the slicing workhorse; `[::-1]` reverses, `[1:]` drops the head,
  `[::2]` steps.
- **Slicing tolerates out-of-range bounds**; indexing does not.
- **Assignment aliases, slicing copies.** `b = a` shares the list; `b = a[:]` copies it.
