# Learn Python with Tests

Learn Python **for coding interviews**, the test-driven way.

This is a [GitBook](https://www.gitbook.com)-style course, modelled on the excellent
[Learn Go with Tests](https://github.com/quii/learn-go-with-tests), but re-aimed at Python and
interview preparation. Every concept, from a `for` loop to Dijkstra's algorithm, is learned
by **writing a failing test first**, making it pass with the minimal code, then refactoring.

The book is **patterns-first**: the bulk of it is an interview roadmap grouped by pattern
(Two Pointers, Sliding Window, Binary Search, DFS/BFS, Backtracking, Graphs, Heaps, DP, …),
and each pattern ships with a reusable Python template plus several worked problems.

## Read the book

Open [`SUMMARY.md`](SUMMARY.md) for the full roadmap, or serve it as a website (see below).

## Develop

Requirements: Python 3.9+ and [Node.js](https://nodejs.org) (for the book renderer).

This project is set up to use [`uv`](https://docs.astral.sh/uv/) for Python environment and
dependency management.

```bash
# 1. Set up the Python environment and dev tools (pytest, hypothesis, ruff)
uv sync

# 2. Run every chapter's test suite
uv run pytest

# 3. Lint
uv run ruff check

# 4. Serve the book locally at http://localhost:4000
npx honkit serve
```

No `uv`? A stdlib virtualenv works too:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest hypothesis ruff
pytest
```

## How it's organised

- Each chapter is a markdown file at the repo root (e.g. `iteration.md`) **plus** a sibling
  code folder (e.g. `iteration/`).
- **Fundamentals** chapters use versioned snapshots (`v1/`, `v2/`, …), one per step of the
  TDD evolution, so you can see the code grow.
- **Interview-pattern** chapters use a `_template.py` (the reusable pattern skeleton) and a
  `solutions/` folder with one `problem.py` + `test_problem.py` per worked problem.
- `SUMMARY.md` is the table of contents and the single source of truth for navigation.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the authoring conventions and
[`template.md`](template.md) for the chapter template.

## Reference material

The `references/` directory (gitignored) holds design references only, a clone of
`learn-go-with-tests` and the AlgoMonster roadmap data used to shape this book's structure.
None of it is part of the published book.

## License

MIT.
