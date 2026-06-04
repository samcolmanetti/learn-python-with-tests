# Contributing

Thanks for helping grow **Learn Python with Tests**. The whole book follows one rhythm — write
a failing test, make it pass, refactor — and a few simple conventions keep it consistent.

## Ground rules

- **Test-first.** Every behaviour starts as a failing `pytest` test. The chapter prose walks
  the reader through the red → green → refactor loop.
- **Standard library only in solutions.** Interview environments rarely let you `pip install`.
  Solutions import only from the Python standard library. (Dev tooling — `pytest`, `hypothesis`,
  `ruff` — is fine; it just never appears inside a solution.)
- **Python 3.9+.** Keep code runnable on 3.9 and up. If you use modern annotation syntax like
  `list[int]` in annotations, add `from __future__ import annotations` at the top of the file.
- **Everything stays green.** `pytest` and `ruff check` must pass before you commit.

## Where things go

Each chapter is **two things**: a markdown file at the repo root, and a sibling code folder.

```
iteration.md          ← the chapter prose
iteration/            ← the chapter's code
```

Add every chapter to [`SUMMARY.md`](SUMMARY.md) — it is the table of contents and the single
source of truth for navigation. The `tests/test_summary_links.py` guard fails the build if a
chapter is linked but missing, or exists but unlinked.

### Layout 1 — Fundamentals chapters: versioned snapshots

Language chapters grow the code one step at a time. Each step is a **complete, runnable
snapshot** in its own `vN/` folder, so the reader can see the code evolve.

```
iteration/
├── __init__.py
├── v1/
│   ├── __init__.py
│   ├── iteration.py
│   └── test_iteration.py
├── v2/
│   ├── __init__.py
│   ├── iteration.py
│   └── test_iteration.py
└── ...
```

Every folder gets an `__init__.py` so the same module name (`iteration.py`) can live in many
`vN/` folders without import collisions.

### Layout 2 — Interview-pattern chapters: template + solutions

Pattern chapters share a reusable skeleton plus one file per worked problem.

```
two_pointers/
├── __init__.py
├── _template.py                  ← the reusable pattern skeleton (real, tested Python)
└── solutions/
    ├── __init__.py
    ├── valid_palindrome.py
    ├── test_valid_palindrome.py
    ├── two_sum_sorted.py
    └── test_two_sum_sorted.py
```

- `_template.py` is the **pattern in the abstract** — a generic, importable, tested function
  you adapt per problem. (These were seeded from common interview templates and rewritten as
  working Python.)
- Each problem in `solutions/` is one `problem_name.py` + `test_problem_name.py` pair.

## Naming

- Test files: `test_*.py` (pytest discovery is configured for this in `pyproject.toml`).
- Modules and folders: `snake_case`. Chapter markdown files: `kebab-case.md`.
- Test functions: `test_<behaviour>` — name the behaviour, not the implementation
  (`test_returns_zero_for_empty_input`, not `test_loop`).

## Running things

```bash
uv run pytest        # or: pytest, inside an activated venv
uv run ruff check    # lint
npx honkit serve     # preview the book at http://localhost:4000
```

## Writing a chapter

1. Copy [`template.md`](template.md) to `your-chapter.md`.
2. Create the code folder using Layout 1 or Layout 2 above.
3. Walk the TDD loop in prose, showing real failing output, then the passing code.
4. Add the chapter to `SUMMARY.md`.
5. Run `pytest` and `ruff check`; preview with `honkit serve`.
