# Comprehensions

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/comprehensions)**

A comprehension builds a list, dict, or set from an iterable in a single expression, replacing
the `result = []` then `for` then `.append` ritual with one line. A generator looks almost the
same but hands back its values one at a time, so it never holds the whole sequence in memory.
We'll build both, test-first, starting with the list comprehension.

## Write the test first

Our first job is the simplest one: square every number in a list. We'll put the function in
`comprehensions/comprehensions.py` and the test beside it in `test_comprehensions.py`. The import
uses a package-relative path because both files live in the same package.

```python
from comprehensions import squares


def test_squares():
    assert squares([1, 2, 3, 4]) == [1, 4, 9, 16]


def test_squares_empty():
    assert squares([]) == []
```

The empty-list case is there from the start. An empty input is where off-by-one and `None`
mistakes hide, so I like to pin it down before writing any code.

## Try to run the test

We've imported a name that the module doesn't define yet, so the import is the first thing to
break. Run `uv run pytest`:

```
ImportError: cannot import name 'squares' from 'comprehensions.comprehensions'
```

No function, no import. The error is telling us exactly where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `squares` that takes the argument but returns an empty list. We're not solving anything
yet. We just want the test to run so we can watch it fail on the value, which proves the test
checks what we think it does.

```python
from __future__ import annotations


def squares(numbers):
    return []
```

Run `uv run pytest`:

```
    def test_squares():
>       assert squares([1, 2, 3, 4]) == [1, 4, 9, 16]
E       assert [] == [1, 4, 9, 16]
E
E         Right contains 4 more items, first extra item: 1
```

The test runs and fails on the value, not on a missing name. `test_squares_empty` passes, but
only because our stub returns `[]` by luck. That's a fine reminder that one green test proves
nothing on its own.

## Write enough code to make it pass

The longhand version is a loop that appends:

```python
def squares(numbers):
    result = []
    for n in numbers:
        result.append(n * n)
    return result
```

That works, but it's four lines of bookkeeping around one idea: each output is `n * n`. A *list
comprehension* says exactly that and nothing else.

```python
from __future__ import annotations


def squares(numbers: list[int]) -> list[int]:
    return [n * n for n in numbers]
```

Read it left to right: "the value `n * n`, for each `n` in `numbers`". The square brackets mean
the result is a list. Run the tests and they're green.

## Refactor

There's nothing to tidy in one line, but it's worth naming the shape, because every comprehension
in this chapter is a variation on it: `[expression for item in iterable]`. The expression on the
left is what each element becomes. The `for` clause on the right is what we iterate over. Hold
that template in your head and the rest of the chapter is small twists on it.

## Repeat for new requirements

Our next requirement is a filter: keep only the even numbers and drop the rest.

## Write the test first

```python
from comprehensions import evens, squares


def test_evens():
    assert evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def test_evens_includes_zero():
    assert evens([0, 1, 2]) == [0, 2]
```

`test_evens_includes_zero` earns its place: `0` is even, and `0 % 2 == 0`, so a correct filter
keeps it. A solution that leans on truthiness (`if n`) would silently drop the zero.

## Try to run the test

`evens` doesn't exist yet, so the import fails again:

```
ImportError: cannot import name 'evens' from 'comprehensions.comprehensions'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub `evens` to return an empty list so the tests run:

```python
def evens(numbers):
    return []
```

Run `uv run pytest`:

```
    def test_evens():
>       assert evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
E       assert [] == [2, 4, 6]
E
E         Right contains 3 more items, first extra item: 2
```

Failing on the value, as we wanted.

## Write enough code to make it pass

Same comprehension template, with one new piece bolted on the end: an `if` clause. It decides
which items make it into the result.

```python
def evens(numbers: list[int]) -> list[int]:
    return [n for n in numbers if n % 2 == 0]
```

Now read it: "the value `n`, for each `n` in `numbers`, but only when `n % 2 == 0`". The tests
pass, and `0` is kept because `0 % 2` really is `0`.

## Refactor

The full template is now visible: `[expression for item in iterable if condition]`. The `if` at
the end is a *filter* and it's optional. **Put the filter on the right end of the comprehension,
not as a separate `if` inside a loop.** Nothing to change here, so re-run the tests to confirm
they're still green and move on.

## Repeat for new requirements

Lists aren't the only thing a comprehension can build. Next we want a *dict*: map each character
of a string to the position it appears at.

## Write the test first

```python
from comprehensions import char_index_map


def test_char_index_map():
    assert char_index_map("abc") == {"a": 0, "b": 1, "c": 2}


def test_char_index_map_keeps_last_index():
    assert char_index_map("aba") == {"a": 2, "b": 1}
```

The second test names a decision we have to make. The string `"aba"` has `"a"` at index `0` and
again at index `2`. A dict can't hold a key twice, so something has to give. We decide the *last*
write wins, so `"a"` maps to `2`. Writing the test first forces us to pick that behaviour on
purpose instead of discovering it by accident later.

## Try to run the test

```
ImportError: cannot import name 'char_index_map' from 'comprehensions.comprehensions'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty dict:

```python
def char_index_map(text):
    return {}
```

Run `uv run pytest`:

```
    def test_char_index_map():
>       assert char_index_map("abc") == {"a": 0, "b": 1, "c": 2}
E       AssertionError: assert {} == {'a': 0, 'b': 1, 'c': 2}
E
E         Right contains 3 more items:
E         {'a': 0, 'b': 1, 'c': 2}
```

Good, it runs and fails on the value.

## Write enough code to make it pass

A *dict comprehension* uses curly braces and a `key: value` pair on the left. We need both the
character and its index, so we iterate with `enumerate`, which hands back `(index, item)` pairs.

```python
def char_index_map(text: str) -> dict[str, int]:
    return {char: index for index, char in enumerate(text)}
```

The tests pass. The "last write wins" behaviour comes for free: as the comprehension walks the
string, a repeated key just overwrites the earlier entry, so `"a"` ends up at `2`. We didn't
write a single `if` to get that. The dict does it for us.

## Refactor

Notice the only real difference from the list version is the braces and the colon. **Curly braces
with a `key: value` pair make a dict comprehension. The same braces with a single value make a
set comprehension**, which is exactly where we're headed next. Re-run the tests; still green.

## Repeat for new requirements

Now the set. We want the distinct word lengths in a list of words, with duplicates collapsed.

## Write the test first

```python
from comprehensions import unique_lengths


def test_unique_lengths():
    assert unique_lengths(["a", "bb", "cc", "ddd"]) == {1, 2, 3}


def test_unique_lengths_dedupes():
    assert unique_lengths(["dog", "cat", "fox"]) == {3}
```

`test_unique_lengths_dedupes` is the whole point of using a set: three words, all length `3`, and
the answer is a single `{3}`. A list would give us `[3, 3, 3]`; a set throws the duplicates away.

## Try to run the test

```
ImportError: cannot import name 'unique_lengths' from 'comprehensions.comprehensions'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub it with an empty set. Note `set()`, not `{}`, because `{}` is an empty dict:

```python
def unique_lengths(words):
    return set()
```

Run `uv run pytest`:

```
    def test_unique_lengths():
>       assert unique_lengths(["a", "bb", "cc", "ddd"]) == {1, 2, 3}
E       assert set() == {1, 2, 3}
E
E         Extra items in the right set:
E         1
E         2
E         3
```

Fails on the value, as expected.

## Write enough code to make it pass

A *set comprehension* is curly braces with a single value (no colon). It de-duplicates as it goes.

```python
def unique_lengths(words: list[str]) -> set[int]:
    return {len(word) for word in words}
```

The tests pass. The three length-`3` words all produce `3`, and the set keeps just one copy.

## Refactor

We've now seen all three brackets: `[]` for a list, `{key: value}` for a dict, `{value}` for a
set. Same template, three containers. Nothing to refactor, so re-run the tests and let's get to
the part where comprehensions stop being enough.

## Repeat for new requirements

Every comprehension so far builds the whole result in memory before returning it. That's fine for
four words. It's a problem when the input is huge, or infinite. Our last requirement is a running
total: given numbers, yield the cumulative sum after each one. And it has to work even when the
input never ends.

## Write the test first

```python
from itertools import count, islice

from comprehensions import running_total


def test_running_total():
    assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]


def test_running_total_empty():
    assert list(running_total([])) == []


def test_running_total_is_lazy():
    assert list(islice(running_total(count(1)), 3)) == [1, 3, 6]
```

`test_running_total_is_lazy` is the one that matters. `count(1)` from `itertools` is an *infinite*
counter: `1, 2, 3, 4, ...` forever. `islice(..., 3)` pulls only the first three values. If
`running_total` tried to build a full list first, this test would hang and never finish. It only
returns if `running_total` produces values on demand and stops the moment we stop asking.

## Try to run the test

```
ImportError: cannot import name 'running_total' from 'comprehensions.comprehensions'
```

## Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list:

```python
def running_total(numbers):
    return []
```

Run `uv run pytest`:

```
    def test_running_total():
>       assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]
E       assert [] == [1, 3, 6, 10]
E
E         Right contains 4 more items, first extra item: 1
```

It runs and fails on the value. `test_running_total_is_lazy` also fails here rather than hanging,
because an empty list is trivially finite. The hang only becomes a risk once we feed the infinite
counter into real iterating code, which is the next step.

## Write enough code to make it pass

A comprehension is the wrong tool here, because `[total for ...]` would compute every total up
front, and over `count(1)` that loop never ends. Instead we write a *generator*: a function that
uses `yield` instead of `return`. Each `yield` hands back one value and pauses the function, so
the next value is only computed when the caller asks for it.

```python
def running_total(numbers):
    total = 0
    for number in numbers:
        total += number
        yield total
```

The presence of `yield` is what makes this a generator. Calling `running_total([1, 2, 3, 4])`
doesn't run the loop; it returns a generator object that runs the loop one step at a time as you
pull values out of it. That's why `list(...)` is in the tests: it does the pulling, draining the
generator into a real list so we can compare.

Run the tests. All three pass, including the lazy one: `islice` pulls exactly three values from
the infinite counter and then stops, and because the generator only runs as far as it's asked, it
stops too.

## Refactor

The body reads cleanly, so the refactor is about types, not logic. We're using `list[int]`-style
hints elsewhere, and a generator that accepts any iterable and yields ints is best spelled with
`Iterable` and `Iterator` from `collections.abc`. Adding `from __future__ import annotations` at
the top keeps it running on Python 3.9.

```python
from __future__ import annotations

from collections.abc import Iterable, Iterator


def running_total(numbers: Iterable[int]) -> Iterator[int]:
    total = 0
    for number in numbers:
        total += number
        yield total
```

The hints say it out loud: in goes an iterable of ints, out comes an iterator of ints. Re-run the
tests one last time to confirm the safety net held while we annotated.

**A comprehension builds the whole result now; a generator produces it lazily, one value at a
time.** Reach for the generator when the input is large or unbounded, or when the caller might
not want every value.

## Wrapping up

* List comprehensions: `[expression for item in iterable if condition]`, with the filter
  optional.
* Dict comprehensions (`{key: value for ...}`) and set comprehensions (`{value for ...}`) use the
  same shape with different brackets. A set de-duplicates; a dict keeps the last value written for
  a repeated key.
* `enumerate` pairs each item with its index, which is how you build an index map in one line.
* Generators swap `return` for `yield` and produce values lazily, so they work on huge or infinite
  inputs without building the whole sequence. `itertools.count` and `itertools.islice` are the
  handy way to test that laziness.

Next: [Iterators](iterators.md), where we go one level down and see the protocol that makes both
comprehensions and generators work.
