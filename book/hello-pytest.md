# Hello, pytest

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/hello_pytest)**

This is where the whole book starts: the test-driven loop, in Python, with
[`pytest`](https://docs.pytest.org). We'll write a tiny function the way we write every function
from here on, test first.

## Set up

You need Python 3.9+ and `pytest`. If you followed [Install Python & tooling](install-python.md)
you've got a practice folder with `pytest` installed. Each chapter is two files that live side by
side in that folder: the code and its test. For this one, make `hello_pytest.py` and
`test_hello_pytest.py`. You won't make a sub-folder or a `v1`, you'll write one version and keep
editing it. Run the tests from your folder with `uv run pytest`.

## The TDD loop

Every chapter walks the same cycle:

1. **Write the test first.** Describe the behaviour you want as a failing test.
2. **Try to run the test.** Prove it's wired up and fails for the right reason.
3. **Write the minimal code** so it runs, then read the failure message.
4. **Make it pass** with the simplest code that works.
5. **Refactor** with the test as your safety net.

It feels slow for five minutes and then it makes you fast forever. In an interview it's your
secret weapon: a failing test pins down exactly what "done" means before you write a line.

## Write the test first

Start with the smallest thing that could work: a function `hello` that returns `"hello"`. Put this
in `test_hello_pytest.py`:

```python
from hello_pytest import hello


def test_hello_pytest():
    assert hello() == "hello"
```

A pytest test is just a function whose name starts with `test_`, containing a plain `assert`. No
assertion library, no boilerplate. The import is flat: `from hello_pytest import hello` reaches the
`hello_pytest.py` sitting right next to this test.

## Try to run the test

Run `uv run pytest`:

```
ImportError: cannot import name 'hello' from 'hello_pytest'
```

It fails because there's no code yet. Good. A test you've never seen fail is a test you don't
trust.

## Write the minimal amount of code for the test to run and check the failing test output

Create `hello_pytest.py` with just enough to *run*. Let's deliberately return the wrong thing
first, so we can watch the test fail on the value rather than on a missing name:

```python
def hello():
    return ""
```

Run `uv run pytest`:

```
    def test_hello_pytest():
>       assert hello() == "hello"
E       AssertionError: assert '' == 'hello'
E
E         - hello
```

Now the test runs and fails on the assertion, with a clear diff. The `>` marks the line that blew
up, and the `-` shows what was expected but missing. That's the failure we want.

## Write enough code to make it pass

```python
def hello():
    return "hello"
```

```
1 passed
```

Green. That's the loop.

## Refactor

There's nothing to tidy in a one-line function. Even so, the refactor step always happens: you
look at the code with green tests behind you and decide whether it can read better. Here it can't,
so we move on. Re-run the tests to confirm nothing moved.

## Greet the world

A bare `"hello"` is a weak greeting. The real requirement is `"Hello, world"`. Change the test in
place, you don't make a new file:

```python
from hello_pytest import hello


def test_says_hello_world():
    assert hello() == "Hello, world"
```

Run `uv run pytest` and watch it fail on the new expectation:

```
>       assert hello() == "Hello, world"
E       AssertionError: assert 'hello' == 'Hello, world'
```

Then update `hello_pytest.py` to match:

```python
def hello():
    return "Hello, world"
```

Back to green.

## Say hello to a person

Our next requirement is to greet a specific person, while still defaulting to `"world"`.

### Write the test first

Edit `test_hello_pytest.py` to pin down both behaviours:

```python
from hello_pytest import hello


def test_greets_a_person_by_name():
    assert hello("Chris") == "Hello, Chris"


def test_defaults_to_world_when_no_name_given():
    assert hello() == "Hello, world"
```

### Try to run the test

Run `uv run pytest`. The current `hello` still ignores its argument, so the named case fails on the
value:

```
>       assert hello("Chris") == "Hello, Chris"
E       AssertionError: assert 'Hello, world' == 'Hello, Chris'
```

### Write enough code to make it pass

```python
def hello(name=""):
    if name == "":
        name = "world"
    return "Hello, " + name
```

A **default argument** (`name=""`) keeps the no-argument call working. Two behaviours, two tests,
both green.

### Refactor

The two cases each have a test guarding them, so we're free to tidy. The function already reads
cleanly: one branch for the default, one string to build. We leave it and re-run the tests.

## Add a language

Our next requirement is to greet in a chosen language, falling back to English for anything we
don't know.

### Write the test first

Rather than a new test function per language, use `@pytest.mark.parametrize` to run the same
assertion over a table of cases. Each row is reported as its own test, so a failure tells you
exactly *which* case broke. Replace the body of `test_hello_pytest.py`:

```python
import pytest

from hello_pytest import hello


@pytest.mark.parametrize(
    ("name", "language", "expected"),
    [
        ("Chris", "", "Hello, Chris"),
        ("", "", "Hello, world"),
        ("Elodie", "Spanish", "Hola, Elodie"),
        ("Lauren", "French", "Bonjour, Lauren"),
        ("", "Spanish", "Hola, world"),
        ("Chris", "Klingon", "Hello, Chris"),  # unknown language falls back to English
    ],
)
def test_hello(name, language, expected):
    assert hello(name, language) == expected
```

### Try to run the test

Run `uv run pytest`. The `hello` from before takes no `language` argument, so each row blows up on the
call:

```
TypeError: hello() takes from 0 to 1 positional arguments but 2 were given
```

### Write enough code to make it pass

Add a `language` argument and branch on it in `hello_pytest.py`:

```python
def hello(name="", language=""):
    if name == "":
        name = "world"
    if language == "Spanish":
        return "Hola, " + name
    if language == "French":
        return "Bonjour, " + name
    return "Hello, " + name
```

All six rows pass, including the Klingon case, which falls through to the English greeting.

### Refactor

That works, but the greeting logic is now tangled into `hello`, and the prefixes are bare strings
scattered through the branches. With the tests guarding us, we can grow the design: pull the
prefixes out as named constants and move the language choice into its own function.

```python
ENGLISH_HELLO_PREFIX = "Hello, "
SPANISH = "Spanish"
SPANISH_HELLO_PREFIX = "Hola, "
FRENCH = "French"
FRENCH_HELLO_PREFIX = "Bonjour, "

DEFAULT_NAME = "world"


def hello(name="", language=""):
    if name == "":
        name = DEFAULT_NAME
    return greeting_prefix(language) + name


def greeting_prefix(language):
    if language == SPANISH:
        return SPANISH_HELLO_PREFIX
    if language == FRENCH:
        return FRENCH_HELLO_PREFIX
    return ENGLISH_HELLO_PREFIX
```

Extracting `greeting_prefix` keeps `hello` readable and gives each language one obvious place to
live. Re-run the tests: still green, and now the design is cleaner than the code that passed.

## Wrapping up

- **A pytest test is a `test_*` function with a plain `assert`.** That's the whole framework to
  start.
- **Watch every test fail before you make it pass.** It proves the test is real.
- **You edit one file in place.** No version folders, you just keep changing your two files.
- **Default arguments** keep functions backward-compatible as requirements grow.
- **`@pytest.mark.parametrize`** turns a table of cases into individually-reported tests.

Next: [Numbers](numbers.md).
