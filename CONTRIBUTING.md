# Contributing

Thanks for helping grow **Learn Python with Tests**. The whole book follows one rhythm, write
a failing test, make it pass, refactor, and a few simple conventions keep it consistent.

Readers don't need this file or a clone. It's for people working on the book itself.

## Get set up

```bash
git clone https://github.com/samcolmanetti/learn-python-with-tests
cd learn-python-with-tests

uv sync              # install pytest, hypothesis, ruff from the committed pyproject
uv run pytest        # run every chapter's test suite
uv run ruff check    # lint
npm install          # the site toolchain (honkit + plugins)
npm run serve        # preview the book at http://localhost:4000
```

## Ground rules

- **Test-first.** Every behaviour starts as a failing `pytest` test. The chapter prose walks
  the reader through the red → green → refactor loop.
- **Standard library only in solutions.** Interview environments rarely let you `pip install`.
  Solutions import only from the Python standard library. (Dev tooling, `pytest`, `hypothesis`,
  `ruff`, is fine; it just never appears inside a solution.)
- **Python 3.9+.** Keep code runnable on 3.9 and up. If you use modern annotation syntax like
  `list[int]` in annotations, add `from __future__ import annotations` at the top of the file.
- **Everything stays green.** `pytest` and `ruff check` must pass before you commit.

## Where things go

The repo separates three concerns:

```
book/        ← all chapter prose, SUMMARY.md, book.json, styles
code/        ← all chapter code (what pytest runs)
root         ← README, this file, pyproject.toml, deploy config
```

Each chapter is **two things**: a markdown file in `book/`, and a sibling code folder in `code/`.

```
book/iteration.md     ← the chapter prose
code/iteration/       ← the chapter's code
```

Add every chapter to [`book/SUMMARY.md`](book/SUMMARY.md), it is the table of contents and the
single source of truth for navigation. The `code/tests/test_summary_links.py` guard fails the
build if a chapter is linked but missing, or exists but unlinked.

### Layout 1: Fundamentals chapters: one flat pair of files

Single-concept language chapters are the shape readers mirror exactly: two files, side by side,
no `__init__.py`, no `vN/` folders, absolute imports.

```
code/iteration/
├── iteration.py
└── test_iteration.py
```

```python
# test_iteration.py
from iteration import repeat
```

The chapter prose shows the code evolving step by step, but only the final version lives in the
repo. You don't keep `v1/`, `v2/` snapshots, you write the chapter's progression in prose and
commit the end state.

### Layout 2: Interview-pattern chapters: template + solutions

Pattern chapters are genuinely multi-file: a shared, reusable skeleton plus one file per worked
problem. These stay Python packages, because `solutions/` files import the shared `_template.py`
one directory up.

```
code/two_pointers/
├── __init__.py
├── _template.py                  ← the reusable pattern skeleton (real, tested Python)
└── solutions/
    ├── __init__.py
    ├── valid_palindrome.py
    ├── test_valid_palindrome.py
    ├── two_sum_sorted.py
    └── test_two_sum_sorted.py
```

- `_template.py` is the **pattern in the abstract**, a generic, importable, tested function
  you adapt per problem. (These were seeded from common interview templates and rewritten as
  working Python.)
- Each problem in `solutions/` is one `problem_name.py` + `test_problem_name.py` pair, importing
  its solution with a package-relative import (`from .valid_palindrome import is_palindrome`).
- The chapter **prose** still shows flat imports (`from valid_palindrome import is_palindrome`),
  because the reader writes one problem at a time in their flat practice folder. Only the repo's
  reference code uses the package form.

## Naming

- Test files: `test_*.py` (pytest discovery is configured for this in `pyproject.toml`).
- Modules and folders: `snake_case`. Chapter markdown files: `kebab-case.md`.
- Never name a code folder or module after a stdlib module (`math`, `string`, `queue`). Use
  `math_problems`, etc.
- Test functions: `test_<behaviour>`, name the behaviour, not the implementation
  (`test_returns_zero_for_empty_input`, not `test_loop`).

## Running things

```bash
uv run pytest        # or: pytest, inside an activated venv
uv run ruff check    # lint
npm run serve        # preview the book at http://localhost:4000
```

## Writing a chapter

1. Copy [`book/template.md`](book/template.md) to `book/your-chapter.md`.
2. Create the code folder under `code/` using Layout 1 or Layout 2 above.
3. Walk the TDD loop in prose, showing real failing output, then the passing code.
4. Add the chapter to `book/SUMMARY.md`.
5. Run `pytest` and `ruff check`; preview with `npm run serve`.
