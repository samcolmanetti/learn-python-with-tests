# Install Python & tooling

A five-minute setup. You need Python, a test runner (`pytest`), a property-testing library
(`hypothesis`), and, if you want to render the book as a website, Node.js.

## Python

You need **Python 3.9 or newer**. Check what you have:

```bash
python3 --version
```

If it's missing or older, install from [python.org](https://www.python.org/downloads/) or with
your package manager (`brew install python` on macOS, `apt install python3` on Debian/Ubuntu).

## The tools

This project uses [`uv`](https://docs.astral.sh/uv/), a fast Python package and environment
manager. It's the only tool you need. With `uv` installed (`brew install uv`, or see the docs),
one command sets everything up:

```bash
uv sync          # creates a virtualenv and installs pytest, hypothesis, ruff
uv run pytest    # run the whole test suite
```

You should see all tests pass. That's your green baseline, and the book grows from here.

## Running things

Every command runs through `uv run`, so you never have to activate a virtualenv by hand:

```bash
uv run pytest                       # all tests
uv run pytest hello_pytest/         # just one chapter
uv run pytest -k palindrome         # tests matching a name
uv run pytest -m "not slow"         # skip tests marked slow
uv run ruff check                   # lint
```

Need another library later? `uv add <name>` installs it and records it in `pyproject.toml`.

## Render the book (optional)

The chapters are plain markdown, readable straight on GitHub. To browse them as a website
locally (the same [GitBook](https://www.gitbook.com) look this book is modelled on), install
[Node.js](https://nodejs.org) and run:

```bash
npx honkit serve     # serves at http://localhost:4000
```

[Honkit](https://github.com/honkit/honkit) is the maintained successor to the GitBook CLI and
reads the same `SUMMARY.md` / `book.json` files.

## You're set

Head to [Hello, pytest](hello-pytest.md) and write your first failing test.
