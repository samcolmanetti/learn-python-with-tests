# Hello, pytest

**[You can find all the code for this chapter here](hello_pytest/)**

This is where the whole book starts: the test-driven loop, in Python, with
[`pytest`](https://docs.pytest.org). By the end you will have written a tiny function the way
we will write every function from here on — **test first**.

## Set up

You need Python 3.9+ and `pytest`. If you followed [Install Python & tooling](install-python.md)
you already have them. Quick version:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

Run the whole suite any time with `pytest`. Run one chapter with `pytest hello_pytest/`.

## The TDD loop

Every chapter walks the same cycle:

1. **Write the test first** — describe the behaviour you want as a failing test.
2. **Run it and watch it fail** — prove the test is wired up and fails for the right reason.
3. **Write the minimal code** to make it run, check the failure message.
4. **Make it pass** with the simplest code that works.
5. **Refactor** — improve the code with the test as your safety net.

It feels slow for five minutes and then it makes you fast forever. In an interview it is your
secret weapon: a failing test pins down exactly what "done" means before you write a line.

## Write the test first

We want a function `hello` that returns `"Hello, world"`. Create
`hello_pytest/v1/test_hello_pytest.py`:

```python
from .hello_pytest import hello


def test_says_hello_world():
    assert hello() == "Hello, world"
```

A pytest test is just a function whose name starts with `test_`, containing a plain `assert`.
No assertion library, no boilerplate.

## Try to run the test

```
ImportError: cannot import name 'hello' from 'hello_pytest.v1.hello_pytest'
```

It fails — there is no code yet. Good. A test you have never seen fail is a test you do not
trust.

## Write the minimal amount of code for the test to run and check the failing test output

Create `hello_pytest/v1/hello_pytest.py` with just enough to *run* — let's deliberately return
the wrong thing first:

```python
def hello():
    return ""
```

```
>       assert hello() == "Hello, world"
E       AssertionError: assert '' == 'Hello, world'
```

Now the test runs and fails on the assertion, with a clear diff. That is the failure we want.

## Write enough code to make it pass

```python
def hello():
    return "Hello, world"
```

```
1 passed
```

Green. That is the loop. Commit it to muscle memory.

## Repeat for new requirements — say hello to a person

Now make `hello` greet a specific person, while still defaulting to `"world"`. New tests in
`hello_pytest/v2/test_hello_pytest.py`:

```python
def test_greets_a_person_by_name():
    assert hello("Chris") == "Hello, Chris"


def test_defaults_to_world_when_no_name_given():
    assert hello() == "Hello, world"
```

Make them pass:

```python
def hello(name=""):
    if name == "":
        name = "world"
    return "Hello, " + name
```

A **default argument** (`name=""`) keeps the no-argument call working. Two behaviours, two
tests, both green.

## Refactor — and add a language

With tests guarding us, we can grow the design. `hello_pytest/v3` adds a `language` argument
and pulls the greeting prefixes out as named constants:

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

Extracting `greeting_prefix` keeps `hello` readable and gives each language one obvious place
to live.

### One test, many cases: `parametrize`

Rather than a new test function per language, use `@pytest.mark.parametrize` to run the same
assertion over a table of cases:

```python
import pytest

from .hello_pytest import hello


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

Each row is reported as its own test, so a failure tells you exactly *which* case broke. You
will use `parametrize` constantly — it is the natural way to cover edge cases without copy-paste.

## Wrapping up

- **A pytest test is a `test_*` function with a plain `assert`.** That's the whole framework to
  start.
- **Watch every test fail before you make it pass.** It proves the test is real.
- **Default arguments** keep functions backward-compatible as requirements grow.
- **`@pytest.mark.parametrize`** turns a table of cases into individually-reported tests.

Next: [Numbers](numbers.md).
