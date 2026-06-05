# File handling and context managers

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/file_handling)**

Reading and writing files is one of those things that looks trivial until a forgotten `close()`
leaks a file handle in production. Python's answer is the `with` statement, and once you see how it
works you'll want to write your own. We'll build a few small file helpers test-first, then build a
context manager from scratch.

One rule up front, and it shapes every test in this chapter: **our tests never touch real project
files.** They write into a throwaway directory that pytest hands us and cleans up afterwards. That
fixture is called `tmp_path`, and it's a `pathlib.Path` pointing at a fresh temp directory, unique
per test. No mess, no leftover files, no test depending on another test's output.

## Write the test first

The smallest useful thing: write some lines to a file, then read them back and get the same lines.
If that round-trips, our reading and writing agree with each other.

We ask pytest for `tmp_path` by naming it as an argument. pytest sees the name and injects the
fixture.

```python
from pathlib import Path

from .file_handling import write_lines, read_lines


def test_write_then_read_round_trips(tmp_path):
    target = tmp_path / "notes.txt"
    write_lines(target, ["first", "second", "third"])
    assert read_lines(target) == ["first", "second", "third"]
```

Notice `tmp_path / "notes.txt"`. A `Path` overloads the `/` operator to join paths, so that's the
temp directory with `notes.txt` underneath it. No string concatenation, no worrying about which
slash your OS wants.

## Try to run the test

Run `uv run pytest`. The functions don't exist yet, so the import is the first thing to break:

```
ImportError: cannot import name 'write_lines' from 'file_handling.file_handling'
```

Listen to the error. It's telling us exactly which names it wants and where to put them.

## Write the minimal amount of code for the test to run and check the failing test output

We could write the real thing now, but with TDD we want to watch the test fail on the *value*, not
on a missing name. That proves the test actually checks what we think it does. So give it stubs: a
`write_lines` that writes nothing and a `read_lines` that returns an empty list.

```python
from __future__ import annotations

from pathlib import Path


def write_lines(path, lines):
    pass


def read_lines(path):
    return []
```

Run `uv run pytest`:

```
    def test_write_then_read_round_trips(tmp_path):
        target = tmp_path / "notes.txt"
        write_lines(target, ["first", "second", "third"])
>       assert read_lines(target) == ["first", "second", "third"]
E       AssertionError: assert [] == ['first', 'second', 'third']
E         Right contains 3 more items, first extra item: 'first'
```

The test runs and fails on the value, not on a missing import. That's the failure we wanted.

## Write enough code to make it pass

Now open the file and write. The `with` statement is the whole point here, so let's lead with it:

```python
from __future__ import annotations

from pathlib import Path


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]
```

Run the tests and they're green.

That `with open(...) as f:` is a *context manager*. `open` gives back a file object, the `with`
block binds it to `f`, and when the block ends, **Python closes the file for you, even if the body
raises an exception.** That last part is the reason we use `with` instead of a bare `open` followed
by `f.close()`: a `close()` you have to remember is a `close()` you'll eventually forget.

Two small choices worth naming. We pass `encoding="utf-8"` explicitly because the default encoding
depends on the platform, and a test that passes on your machine and fails on someone else's is
worse than no test. And `write_lines` adds the `"\n"` itself, so the caller passes clean strings
without trailing newlines, while `read_lines` strips the newline back off with `rstrip("\n")`. The
two functions are mirror images, which is exactly why the round-trip test holds.

## Refactor

There's not much to tidy in a handful of lines, but iterating a file object directly (`for line in
f`) is worth a comment. A file object is its own iterator: looping over it yields one line at a
time without ever loading the whole file into memory. For a three-line file that doesn't matter; for
a multi-gigabyte log it's the difference between working and an out-of-memory crash. We get the
memory-friendly version for free, so we keep it. Re-run the tests to confirm nothing moved.

## Repeat for new requirements

Our next requirement: count the words in a file. Same hermetic discipline, one new function.

## Write the test first

We'll write a small poem with `write_lines`, then count. Nine words across three lines.

```python
def test_count_words_in_file(tmp_path):
    target = tmp_path / "poem.txt"
    write_lines(target, ["the quick brown fox", "jumps over", "the lazy dog"])
    assert count_words_in_file(target) == 9
```

While we're here, let's pin down the two cases that break a naive counter: an empty file, and a file
full of irregular whitespace. We write the messy one directly with `tmp_path.write_text`, which is
`pathlib`'s one-shot "dump this string into this file" method, handy when we don't want our own
helper in the mix.

```python
def test_count_words_in_empty_file(tmp_path):
    target = tmp_path / "blank.txt"
    target.write_text("", encoding="utf-8")
    assert count_words_in_file(target) == 0


def test_count_words_ignores_extra_whitespace(tmp_path):
    target = tmp_path / "spaced.txt"
    target.write_text("  one   two  \n\n   three   \n", encoding="utf-8")
    assert count_words_in_file(target) == 3
```

The whitespace test is the one that earns its keep. Three words buried in runs of spaces and blank
lines: a counter that splits on a single space character would miscount this badly.

## Try to run the test

```
ImportError: cannot import name 'count_words_in_file' from 'file_handling.file_handling'
```

No such function yet. Same start as before: the import points us at the work.

## Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
def count_words_in_file(path):
    return 0
```

Run `uv run pytest`:

```
    def test_count_words_in_file(tmp_path):
        target = tmp_path / "poem.txt"
        write_lines(target, ["the quick brown fox", "jumps over", "the lazy dog"])
>       assert count_words_in_file(target) == 9
E       AssertionError: assert 0 == 9
E        +  where 0 = count_words_in_file(...poem.txt)
```

The poem test fails on the value, which is right. Note that `test_count_words_in_empty_file` passes
already, but only because the empty file genuinely has zero words and our stub returns zero by luck.
**One green test on a stub proves nothing.** That's why we wrote three.

## Write enough code to make it pass

Read line by line and let `str.split()` do the work. Called with no argument, `split` treats any run
of whitespace as a single separator and ignores leading and trailing whitespace, which handles both
the messy-spaces case and empty lines without a single `if`.

```python
def count_words_in_file(path):
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
    return total
```

All three tests pass.

`line.split()` with no argument is doing the heavy lifting. `"  one   two  ".split()` is
`["one", "two"]`, not a pile of empty strings, and `"".split()` is `[]`. Reach for the
no-argument form whenever you're splitting human-typed text.

## Refactor

Nothing to change, but worth a note: we stream the file line by line again rather than reading it
all at once and splitting the whole blob. The result is identical for small files and far kinder to
memory for huge ones. Re-run the tests.

## Repeat for new requirements

Now the interesting part. `with open(...)` uses a context manager, but nothing stops us writing our
own. The cleanest case is a resource you set up, hand to a block of code, and tear down afterwards no
matter what happens. Changing the working directory is a perfect example: step into a directory, do
some work, and always step back out, even if the work blows up.

We'll build a `working_directory` context manager that you use like `with working_directory(path):`,
and that restores the original directory on the way out.

## Write the test first

Two behaviours matter. Inside the block, the current directory is the one we asked for. After the
block, we're back where we started.

```python
def test_working_directory_changes_then_restores(tmp_path):
    start = Path.cwd()
    with working_directory(tmp_path):
        # Inside the block we're in tmp_path. resolve() handles symlinked temp dirs.
        assert Path.cwd().resolve() == tmp_path.resolve()
    assert Path.cwd() == start
```

`Path.cwd()` is the current working directory as a `Path`. We call `.resolve()` on both sides of the
inside-check because on a Mac the temp directory is reached through a symlink, so the raw path and
the real path differ. Resolving both collapses that difference.

The second behaviour is the one people forget: cleanup has to happen even when the body raises. So
we test it directly.

```python
def test_working_directory_restores_on_exception(tmp_path):
    start = Path.cwd()
    try:
        with working_directory(tmp_path):
            raise ValueError("boom")
    except ValueError:
        pass
    assert Path.cwd() == start
```

We deliberately throw inside the block, catch it outside, and then assert we're back home. If
restoration only happened on the happy path, this test would fail.

## Try to run the test

```
ImportError: cannot import name 'working_directory' from 'file_handling.file_handling'
```

No `working_directory` yet.

## Write the minimal amount of code for the test to run and check the failing test output

Here's the deliberately-wrong stub. We use `contextlib.contextmanager`, which turns a generator into
a context manager: everything before the `yield` is the setup, the yielded value is what `as` binds,
and everything after the `yield` is the teardown. Our stub yields but never actually changes the
directory, so inside the block we're still in the original directory.

```python
from contextlib import contextmanager


@contextmanager
def working_directory(path):
    yield Path(path)
```

Run `uv run pytest`:

```
    def test_working_directory_changes_then_restores(tmp_path):
        start = Path.cwd()
        with working_directory(tmp_path):
>           assert Path.cwd().resolve() == tmp_path.resolve()
E           AssertionError: assert PosixPath('.../file_handling') == PosixPath('.../test_working_directory_changes0')
```

The block runs, but we never moved, so the current directory is still the project folder instead of
`tmp_path`. The stub fails for exactly the right reason.

## Write enough code to make it pass

Record where we are, change directory, `yield`, and change back in a `finally` so the restore runs
whether or not the body raised.

```python
import os
from contextlib import contextmanager


@contextmanager
def working_directory(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)
```

Both tests pass, including the one that throws inside the block.

The `try`/`finally` around the `yield` is the whole game. When the body of the `with` raises, the
exception propagates back up through the `yield`, the `finally` runs on its way out, and only then
does the exception continue. That's how `working_directory` guarantees `os.chdir(previous)` happens
even on `ValueError`. **The setup, the yield, and a `finally` for teardown: that's the shape of every
`@contextmanager` generator you'll write.**

## Refactor

The code is already tight. The one cleanup is the import block: gather `os`, `contextmanager`, and
`Path` at the top of the module, and add `from __future__ import annotations` so we can use
`list[str]` style hints and stay runnable on Python 3.9. Here's the finished module.

```python
from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def write_lines(path: Path, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def count_words_in_file(path: Path) -> int:
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
    return total


@contextmanager
def working_directory(path: Path) -> Iterator[Path]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)
```

The return type on `working_directory` is `Iterator[Path]`, because under the hood
`@contextmanager` wraps a generator and a generator that yields a `Path` is an `Iterator[Path]`.
Re-run `uv run pytest` one last time and watch all eight stay green.

If you'd rather not use a generator, the other way to write a context manager is a class with
`__enter__` (the setup, returning what `as` binds) and `__exit__` (the teardown, which gets any
exception that occurred). The `@contextmanager` generator is the same idea with less ceremony, and
it's what I reach for first.

## Wrapping up

- **The `with` statement closes your resources for you, even on an exception.** Use it for every
  `open`. A `close()` you have to remember is one you'll forget.
- **`pathlib.Path` joins with `/`** and gives you `cwd`, `read_text`, and `write_text` without
  string fiddling.
- **`str.split()` with no argument** splits on any run of whitespace and drops the empties, which is
  what you want for word counting.
- **Write your own context manager with `@contextmanager`**: setup, `yield`, teardown in a
  `finally`. The class form is `__enter__` and `__exit__`.
- **Keep file tests hermetic with `tmp_path`.** They write into a throwaway directory pytest cleans
  up, so a test never touches real files or depends on another test.

Next: [Exceptions](exceptions.md), where the `try`/`finally` we leaned on here becomes the main
event.
