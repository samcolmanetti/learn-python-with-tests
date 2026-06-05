# Dicts & sets

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/dicts_and_sets)**

A dict gives you O(1) lookup by key, and a set gives you O(1) membership and the algebra of
intersection and union. They're the two data structures interview problems lean on hardest, so
we'll build four small functions test-first and meet `Counter` and `defaultdict` along the way.

All four live in one module, [`dicts_and_sets/dicts_and_sets.py`](dicts_and_sets/dicts_and_sets.py),
with their tests next to them. Run everything with `uv run pytest dicts_and_sets/`.

## Write the test first

We'll start with `word_count`: given a string, return how many times each word appears. I'm
using whitespace-separated words to keep the focus on the counting, not the parsing.

```python
from .dicts_and_sets import word_count


def test_word_count_basic():
    assert word_count("the cat the dog the") == {"the": 3, "cat": 1, "dog": 1}
```

Three `the`s, one `cat`, one `dog`. A dict from word to count is the natural shape for the
answer, and it's also what makes the lookup ("how many of this word?") O(1) later.

## Try to run the test

We've imported `word_count` from a module that doesn't define it yet, so the import breaks
before any assertion runs:

```
ImportError: cannot import name 'word_count' from 'dicts_and_sets.dicts_and_sets'
```

Listen to the error. It's telling us the name doesn't exist yet, which is exactly where we start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `word_count` that ignores its input and returns an empty dict. It's wrong on purpose,
and that's the point: we want to watch the test fail on the value, which proves the test checks
what we think it does.

```python
from __future__ import annotations


def word_count(text: str) -> dict[str, int]:
    return {}
```

Run `uv run pytest`:

```
    def test_word_count_basic():
>       assert word_count("the cat the dog the") == {"the": 3, "cat": 1, "dog": 1}
E       AssertionError: assert {} == {'cat': 1, 'dog': 1, 'the': 3}
E
E         Right contains 3 more items:
E         {'cat': 1, 'dog': 1, 'the': 3}
```

The test runs and fails on the value, not on a missing name. Good. Now let's make it count.

## Write enough code to make it pass

The hand-rolled version is a loop with a "have I seen this key?" check on every word:

```python
def word_count(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
```

That `if word in counts` branch is so common that the standard library has a tool that erases it.
`collections.Counter` is a `dict` subclass that tallies any iterable you feed it:

```python
from __future__ import annotations

from collections import Counter


def word_count(text: str) -> dict[str, int]:
    return dict(Counter(text.split()))
```

The test passes. `Counter(text.split())` walks the words once and counts them, O(n) for `n`
words. We wrap it in `dict(...)` so the return type is a plain dict and callers never have to
know a `Counter` was involved.

## Refactor

There's nothing to tidy in one line, but it's worth naming what `Counter` bought us. The
`if word in counts` branch is gone, and so is the chance of getting it wrong. **When you're
tallying occurrences, reach for `Counter` instead of a dict and a branch.** Re-run the tests to
confirm nothing moved.

A couple of edge cases are worth pinning down so a future change can't break them quietly:

```python
def test_word_count_empty():
    assert word_count("") == {}


def test_word_count_single_word():
    assert word_count("solo") == {"solo": 1}
```

Both pass already. `"".split()` is the empty list, so an empty string counts to an empty dict
with no special case from us.

## Repeat for new requirements

Our next requirement is `first_non_repeating_char`: given a string, return the first character
that appears exactly once, or `None` if every character repeats.

### Write the test first

```python
from .dicts_and_sets import first_non_repeating_char


def test_first_non_repeating_char():
    assert first_non_repeating_char("leetcode") == "l"


def test_first_non_repeating_char_skips_repeats():
    assert first_non_repeating_char("aabbc") == "c"
```

In `"leetcode"` the `e` repeats, so the answer is the `l`. In `"aabbc"` the `a`s and `b`s repeat,
so we skip past them to the `c`. The word *first* is doing real work here: order matters.

### Try to run the test

The function doesn't exist yet, so the import fails first:

```
ImportError: cannot import name 'first_non_repeating_char' from 'dicts_and_sets.dicts_and_sets'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `None` so the test runs:

```python
def first_non_repeating_char(text: str) -> str | None:
    return None
```

Run `uv run pytest`:

```
    def test_first_non_repeating_char():
>       assert first_non_repeating_char("leetcode") == "l"
E       AssertionError: assert None == 'l'
E        +  where None = first_non_repeating_char('leetcode')
```

Failing on the value, as we want.

### Write enough code to make it pass

The trap is to count and check in the same pass. You can't: when you reach the first `l`, you
don't yet know whether a second `l` is coming. So we do it in two passes. First count every
character, then walk the string again in order and return the first one whose count is `1`.

```python
from collections import Counter


def first_non_repeating_char(text: str) -> str | None:
    counts = Counter(text)
    for char in text:
        if counts[char] == 1:
            return char
    return None
```

The test passes. The second loop walks `text` in its original left-to-right order, which is what
makes the answer the *first* such character rather than just any of them.

This leans on a property worth stating out loud: **iterating a string (or a dict) visits items in
insertion order.** Dicts have guaranteed insertion order since Python 3.7, so the same two-pass
shape works when you're scanning the keys of a dict instead of a string.

### Refactor

The two-pass version is already the clean one, so there's nothing to cut. Let's add the cases
that earn their keep instead:

```python
def test_first_non_repeating_char_none_when_all_repeat():
    assert first_non_repeating_char("aabb") is None


def test_first_non_repeating_char_empty():
    assert first_non_repeating_char("") is None
```

Both pass. The `return None` at the end of the loop covers both: a string where everything
repeats, and the empty string where the loop never runs at all. Re-run the tests.

## Repeat for new requirements

Now for sets. `common_elements` takes two lists and returns the values that appear in both.

### Write the test first

```python
from .dicts_and_sets import common_elements


def test_common_elements():
    assert common_elements([1, 2, 3, 4], [3, 4, 5, 6]) == {3, 4}


def test_common_elements_with_duplicates():
    assert common_elements([1, 1, 2, 2], [2, 2, 3]) == {2}
```

Only `3` and `4` are in both of the first pair. The second test makes the contract explicit: the
result is a *set*, so duplicates collapse. `2` appears in both lists, repeatedly, and comes back
exactly once.

### Try to run the test

```
ImportError: cannot import name 'common_elements' from 'dicts_and_sets.dicts_and_sets'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty set:

```python
def common_elements(a: list[int], b: list[int]) -> set[int]:
    return set()
```

Run `uv run pytest`:

```
    def test_common_elements():
>       assert common_elements([1, 2, 3, 4], [3, 4, 5, 6]) == {3, 4}
E       assert set() == {3, 4}
E
E         Extra items in the right set:
E         3
E         4
```

The empty set fails against `{3, 4}`. Now let's fill it in.

### Write enough code to make it pass

The naive answer is a nested loop: for every value in `a`, scan `b` to see if it's there. That's
O(n * m), and it does nothing to dedupe. Convert both lists to sets and take the intersection
with `&` instead:

```python
def common_elements(a: list[int], b: list[int]) -> set[int]:
    return set(a) & set(b)
```

The test passes. Building each set is O(n) and O(m), and the intersection is O(min(n, m)) because
set membership is O(1). **The set version turns an O(n * m) double loop into a linear pass, and
the deduping is free.** That last part is why `test_common_elements_with_duplicates` passes
without any extra code from us: a set can't hold `2` twice.

### Refactor

One line, nothing to refactor. One more case to lock down the empty-intersection path:

```python
def test_common_elements_disjoint():
    assert common_elements([1, 2], [3, 4]) == set()
```

It passes. `set(a) & set(b)` with nothing in common is the empty set, no branch required. While
we're here: `&` is intersection, `|` is union, `-` is difference, and `^` is symmetric
difference (in one or the other but not both). The same four operators are your set toolbox for
the rest of the book.

## Repeat for new requirements

Last one, and it's the showcase for `defaultdict`. `group_anagrams` takes a list of words and
groups the ones that are anagrams of each other.

### Write the test first

```python
from .dicts_and_sets import group_anagrams


def test_group_anagrams():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = group_anagrams(words)
    as_sets = sorted([sorted(group) for group in groups])
    assert as_sets == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
```

`eat`, `tea`, and `ate` are one group; `tan` and `nat` are another; `bat` is alone. The function
returns a list of groups, and we don't want to promise an order for those groups or for the words
inside them. So the test normalises: it sorts the words inside each group and sorts the groups,
then compares. That way any correct grouping passes, however it's ordered.

### Try to run the test

```
ImportError: cannot import name 'group_anagrams' from 'dicts_and_sets.dicts_and_sets'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list:

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    return []
```

Run `uv run pytest`:

```
    def test_group_anagrams():
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        groups = group_anagrams(words)
        as_sets = sorted([sorted(group) for group in groups])
>       assert as_sets == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
E       AssertionError: assert [] == [['ate', 'eat...'nat', 'tan']]
E
E         Right contains 3 more items, first extra item: ['ate', 'eat', 'tea']
```

Empty list against the three expected groups. Now let's group for real.

### Write enough code to make it pass

The insight is that anagrams share the same letters, so their *sorted* letters are identical.
`"eat"`, `"tea"`, and `"ate"` all sort to `"aet"`. That sorted string is a perfect bucket key:
group every word under the sorted version of itself.

With a plain dict, appending to a bucket means first checking whether the bucket exists:

```python
groups: dict[str, list[str]] = {}
for word in words:
    key = "".join(sorted(word))
    if key not in groups:
        groups[key] = []
    groups[key].append(word)
```

That `if key not in groups` is the same branch `Counter` saved us from earlier, in a different
costume. `collections.defaultdict` erases it: you give it a factory, and the first time you touch
a missing key it calls the factory to create the value. Pass `list` and a missing key springs
into being as an empty list, ready to `.append` to:

```python
from collections import defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
```

The test passes. We sort each word once (O(k log k) for a word of length `k`), look the key up in
O(1), and append. `groups.values()` hands back the buckets, which is the list of groups we want.

### Refactor

The body is already tight. The refactor here is naming the pattern: **`defaultdict(list)` is for
grouping, `defaultdict(int)` is for counting**, and both replace a "create the value if it's
missing" branch with a factory. Reach for it whenever you're bucketing things into lists keyed by
some computed value.

A couple of boundary cases to finish:

```python
def test_group_anagrams_empty():
    assert group_anagrams([]) == []


def test_group_anagrams_no_anagrams():
    groups = group_anagrams(["abc", "def"])
    assert sorted(sorted(g) for g in groups) == [["abc"], ["def"]]
```

Both pass. An empty input never enters the loop, so `groups.values()` is empty. Words with no
anagram each get a bucket of one. Run `uv run pytest dicts_and_sets/` one last time and the whole
chapter is green.

## Wrapping up

- **A dict gives O(1) lookup by key and a set gives O(1) membership.** That's what turns a nested
  scan into a single pass over and over in these problems.
- **`Counter` tallies any iterable** and is a `dict` subclass, so it replaces the hand-rolled
  count-with-a-branch loop.
- **Dicts and strings iterate in insertion order**, which is what lets a second pass find the
  *first* element matching a condition.
- **Set algebra is `&` `|` `-` `^`** (intersection, union, difference, symmetric difference), and
  it dedupes for free.
- **`defaultdict(list)` groups and `defaultdict(int)` counts**, both by replacing a
  "create-if-missing" branch with a factory.

Next: [Comprehensions & generators](comprehensions.md), where we build these same dicts and sets
in a single expression instead of a loop.
