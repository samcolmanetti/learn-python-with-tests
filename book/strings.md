# Strings

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/strings)**

Strings turn up in roughly half of all interview problems, and Python's are pleasant to work with once you internalise one fact: a `str` is *immutable*. You never change a string in place. You build a new one. We'll write three small functions test-first and let that single fact explain `join`, `split`, slicing, and why one innocent-looking loop is a quadratic trap.

Everything lives in `strings.py`, built up behaviour by behaviour, with its tests in `test_strings.py`.

## Write the test first

Our first job is `reverse_words`: take a sentence and reverse the *order of the words*, not the characters. So `"the quick brown fox"` comes back as `"fox brown quick the"`.

```python
from strings import reverse_words


def test_reverse_words():
    assert reverse_words("the quick brown fox") == "fox brown quick the"
```

One assertion, one clear behaviour. We import from a `strings` module that doesn't define `reverse_words` yet, so the import is the first thing that should break.

## Try to run the test

Run `uv run pytest`:

```
ImportError: cannot import name 'reverse_words' from 'strings.strings'
```

No function, no import. The error is telling us exactly where to start: define the name.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `reverse_words` that exists but returns the wrong thing. We want the test to run and fail on the *value*, which proves the test is actually checking what we think it is.

```python
from __future__ import annotations


def reverse_words(sentence: str) -> str:
    return ""
```

Run `uv run pytest`:

```
    def test_reverse_words():
>       assert reverse_words("the quick brown fox") == "fox brown quick the"
E       AssertionError: assert '' == 'fox brown quick the'
E
E         - fox brown quick the
```

Now it fails on the value, not on a missing name. That's the signal to write the real thing.

## Write enough code to make it pass

Three steps: cut the sentence into words, reverse the list, glue it back together.

```python
from __future__ import annotations


def reverse_words(sentence: str) -> str:
    words = sentence.split()
    return " ".join(words[::-1])
```

Green.

Two new tools showed up here. `sentence.split()` with no argument splits on whitespace and gives us a list of words. And `words[::-1]` is a *slice* with a step of `-1`, which reads the list back to front. Slicing is `seq[start:stop:step]`, and leaving `start` and `stop` empty means "the whole thing". A negative step walks it in reverse.

Then `" ".join(...)` stitches the words back together with a single space between each. Notice the join is a method *on the separator string*, not on the list. That trips up everyone once: it's `" ".join(words)`, never `words.join(" ")`.

## Refactor

There's nothing to tidy in three lines, but it's worth pinning down what `split()` did for us, because it's about to matter. Let me add a test that throws messy spacing at it.

```python
def test_reverse_words_collapses_extra_spaces():
    # split() drops the runs of spaces, so the output is always single-spaced.
    assert reverse_words("  pad   me  out  ") == "out me pad"
```

This passes already. `split()` with no argument splits on *runs* of whitespace and throws away the empty pieces, so leading, trailing, and doubled spaces all vanish. That's different from `split(" ")`, which would split on every single space and hand back empty strings for the gaps. **Bare `split()` is the one you almost always want for tidying input.** We'll lean on exactly that behaviour again in a moment.

A single-word sentence and an empty one are worth pinning down too, so the slice and join can't surprise us at the edges:

```python
def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_empty():
    assert reverse_words("") == ""
```

Both green. `"".split()` is `[]`, and joining an empty list is `""`, so the empty case falls out for free.

## Repeat for new requirements

Next up: `is_anagram`. Two strings are anagrams when they're built from the same letters in the same quantities, just rearranged. `"listen"` and `"silent"` are anagrams. We also want it to ignore case and spaces, so `"Dormitory"` and `"Dirty room"` count.

### Write the test first

```python
from strings import is_anagram


def test_is_anagram_true():
    assert is_anagram("listen", "silent") is True
```

I'm asserting `is True` rather than just truthiness, because I want to know the function returns an actual boolean, not some accidental truthy value.

### Try to run the test

```
ImportError: cannot import name 'is_anagram' from 'strings.strings'
```

Same shape as before. The name doesn't exist yet.

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always return `False`:

```python
def is_anagram(first: str, second: str) -> bool:
    return False
```

Run `uv run pytest`:

```
    def test_is_anagram_true():
>       assert is_anagram("listen", "silent") is True
E       AssertionError: assert False is True
E        +  where False = is_anagram('listen', 'silent')
```

Failing on the value, for the right reason. Now make it real.

### Write enough code to make it pass

The question "same letters, same counts" is really "do these two strings have the same *multiset* of characters". Python has a multiset hiding in the standard library: `collections.Counter`. It counts how many times each item appears, and two `Counter`s are equal when their counts match.

```python
from __future__ import annotations

from collections import Counter


def is_anagram(first: str, second: str) -> bool:
    return _letters(first) == _letters(second)


def _letters(text: str) -> Counter:
    cleaned = [char.lower() for char in text if not char.isspace()]
    return Counter(cleaned)
```

The tests pass.

`_letters` does the cleaning: lowercase every character and drop the whitespace with `char.isspace()`. Then `Counter` tallies what's left, and `==` compares the two tallies. There's no sorting and no nested loop. Building each `Counter` is one pass over its string, so the whole thing is O(n).

You'll see the sorted-string trick a lot for this problem: `sorted("listen") == sorted("silent")`. It works and it's a fine answer. It's O(n log n) because of the sort, where `Counter` is O(n), but at interview lengths either is fine. I reach for `Counter` because it reads as what we mean: count the letters, compare the counts.

### Refactor

Let me lock in the case-and-spaces requirement and the rejections with more tests, since one passing assertion proves very little:

```python
def test_is_anagram_false():
    assert is_anagram("hello", "world") is False


def test_is_anagram_ignores_case_and_spaces():
    assert is_anagram("Dormitory", "Dirty room") is True


def test_is_anagram_different_lengths():
    assert is_anagram("ab", "abc") is False
```

All green. `test_is_anagram_ignores_case_and_spaces` is the one that earns its keep: it only passes because `_letters` lowercases and strips whitespace before counting. Take either step out and that test goes red, which is exactly the safety net you want around a requirement that's easy to forget.

## Repeat for new requirements

Last function: `normalize_whitespace`. Collapse every run of whitespace down to a single space and trim the ends, so `"  hello   world  "` becomes `"hello world"`. This is the kind of cleanup you do constantly with scraped or user-typed text.

### Write the test first

```python
from strings import normalize_whitespace


def test_normalize_whitespace_collapses_runs():
    assert normalize_whitespace("  hello   world  ") == "hello world"
```

### Try to run the test

```
ImportError: cannot import name 'normalize_whitespace' from 'strings.strings'
```

You know this dance by now. Define the name.

### Write the minimal amount of code for the test to run and check the failing test output

```python
def normalize_whitespace(text: str) -> str:
    return ""
```

Run `uv run pytest`:

```
    def test_normalize_whitespace_collapses_runs():
>       assert normalize_whitespace("  hello   world  ") == "hello world"
E       AssertionError: assert '' == 'hello world'
E
E         - hello world
```

Fails on the value. Good.

### Write enough code to make it pass

Here's where the `split()` behaviour we noticed earlier does all the work. Bare `split()` already collapses runs of whitespace and drops the empties, so we split and rejoin with single spaces:

```python
def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())
```

Green, and it's a one-liner.

The whole function is `split` then `join`. `text.split()` turns `"  hello   world  "` into `["hello", "world"]`, throwing away the runs of spaces, and `" ".join(...)` puts exactly one space back between the words. Tabs and newlines count as whitespace too, so they get collapsed the same way.

### Refactor

Nothing to refactor in one line, but let me prove the claims about tabs, newlines, and the all-whitespace case:

```python
def test_normalize_whitespace_handles_tabs_and_newlines():
    assert normalize_whitespace("a\tb\n c") == "a b c"


def test_normalize_whitespace_empty():
    assert normalize_whitespace("   ") == ""
```

Both pass. `"   ".split()` is `[]`, and joining an empty list is `""`, so a string of nothing but spaces normalises to the empty string without a single special case.

## Why `+=` in a loop is a trap

We've used `join` three times now without dwelling on it. It's worth a detour, because the alternative is the single most common performance mistake people make with strings.

Say you want to glue a list of lines together with newlines. The "obvious" way reaches for a loop and `+=`:

```python
result = ""
for line in parts:
    result += line + "\n"   # do not do this
```

This looks fine and it's **bad and wrong** for anything but tiny inputs. Remember that strings are immutable: `result += line` can't extend `result` in place, because a `str` cannot be changed. Python has to allocate a *brand new* string and copy the whole of `result` into it, every time through the loop. Glue together `n` lines and you copy a growing string `n` times, which is O(n^2) total work. On a few lines you'll never notice. On a few hundred thousand, it's the difference between instant and a coffee break.

`join` is the fix, and it's the function we built:

```python
def join_lines(parts: list[str]) -> str:
    return "\n".join(parts)
```

```python
def test_join_lines():
    assert join_lines(["a", "b", "c"]) == "a\nb\nc"


def test_join_lines_empty():
    assert join_lines([]) == ""
```

Both green. `join` walks the list once, works out the total size up front, allocates the result string a single time, and fills it in one pass. That's O(n), not O(n^2). **When you're assembling a string from pieces, collect the pieces in a list and `join` them at the end.** Never grow a string with `+=` inside a loop.

(The same logic is why f-strings, `f"{name} scored {score}"`, are the right tool for *formatting* a handful of values, but a loop concatenating thousands of them still wants `join`.)

## Wrapping up

* **Strings are immutable.** Every "change" builds a new string, which is the fact under everything else in this chapter.
* **Slicing** with `seq[start:stop:step]`, and `[::-1]` to reverse.
* **`split()` and `join`**: bare `split()` collapses runs of whitespace and drops empties; `join` is a method on the separator, `" ".join(words)`.
* **`Counter` is a multiset**, which makes anagram and frequency checks a one-pass `==`.
* **`+=` in a loop is O(n^2)** because each step copies the whole string. Collect pieces in a list and `join` once for O(n).
