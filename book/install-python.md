# Install Python & tooling

A five-minute setup. You need two things: **Python** and [`uv`](https://docs.astral.sh/uv/), a
fast Python package and environment manager. `uv` gives you a test runner (`pytest`), a
property-testing library (`hypothesis`), and a linter (`ruff`) without any fuss. You don't need to
clone anything to follow along, you'll write your own code in your own folder.

## Python

You need **Python 3.9 or newer**. Check what you have:

```bash
python3 --version
```

If it's missing or older, install from [python.org](https://www.python.org/downloads/) or with
your package manager (`brew install python` on macOS, `apt install python3` on Debian/Ubuntu).

## uv

Install `uv` with `brew install uv` (macOS) or the [official installer](https://docs.astral.sh/uv/)
for your platform. That's the only tool you'll install by hand.

## Make your practice project

Create a folder to work in and let `uv` set it up. You never write a `pyproject.toml` yourself,
`uv` creates and maintains it for you:

```bash
uv init python-with-tests-practice   # makes the folder and a pyproject.toml
cd python-with-tests-practice
uv add --dev pytest hypothesis ruff  # installs the tools, records them in pyproject.toml
```

That's your workspace. Run the test suite any time with:

```bash
uv run pytest
```

It'll report "no tests ran" until you write one in the next chapter. That's expected, you start
from an empty folder and grow it.

## How each chapter works

Every chapter is **two files that live side by side** in your folder: the code and its test. For
the first chapter you'll make `hello_pytest.py` and `test_hello_pytest.py`, and the test imports
the code with a flat import:

```python
from hello_pytest import hello
```

A few rules that keep this simple:

- **No `__init__.py`, no sub-folders, no `v1`/`v2`.** Just the two files, next to each other.
- **You edit them in place.** When a chapter adds a requirement, you change the same files, you
  don't copy them to a new version.
- **Name the test file `test_<something>.py`.** That's how `pytest` finds it.

One practice folder is all you want.

## Running things

Every command runs through `uv run`, so you never have to activate a virtualenv by hand:

```bash
uv run pytest                       # all your tests
uv run pytest test_hello_pytest.py  # just one file
uv run pytest -k palindrome         # tests matching a name
uv run ruff check                   # lint
```

Need another library later? `uv add <name>` installs it and records it in `pyproject.toml`.

## You're set

Head to [Hello, pytest](hello-pytest.md) and write your first failing test.
