<h1 align="center">Learn Python with Tests</h1>

<p align="center"><em>Learn Python for coding interviews, one failing test at a time.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/tests-740%20passing-brightgreen" alt="tests">
  <img src="https://img.shields.io/badge/chapters-50%2B-1f6feb" alt="chapters">
  <img src="https://img.shields.io/badge/interview%20patterns-25-8957e5" alt="patterns">
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/lint-ruff-261230?logo=ruff&logoColor=white" alt="ruff">
  <img src="https://img.shields.io/badge/license-MIT-3da639" alt="license">
</p>

---

A hands-on course that teaches **Python** and the **algorithmic patterns** behind coding
interviews, entirely through **test-driven development**. It is modelled on Chris James's
[Learn Go with Tests](https://github.com/quii/learn-go-with-tests), re-aimed at Python and
interview prep.

Every concept, from a `for` loop to Dijkstra's algorithm, arrives as a failing test you make
pass. Every line of example code in this repo is real, runnable, and covered by a test that
passes in CI. Nothing here is pseudo-code.

## Why this book

- **Learn by doing.** You write a failing test, watch it fail, make it pass, then refactor.
  The test is the spec, and the discipline is the lesson.
- **Patterns, not problem count.** The core is organised by pattern (Two Pointers, Sliding
  Window, Binary Search, DFS/BFS, Backtracking, Graphs, Heaps, Dynamic Programming, and more).
  Each pattern ships a reusable Python template plus several worked problems.
- **The habit that wins interviews.** Starting from a failing test forces you to define "done",
  enumerate edge cases early, and work in small verified steps. That is exactly what an
  interviewer is scoring.

## What's inside

| | |
|---|---|
| **25** interview-pattern chapters | Two Pointers through Dynamic Programming, Tries, and LRU cache design |
| **~50** chapters total | fundamentals, applied Python, testing, complexity, and the patterns |
| **740** passing tests | every worked example is verified; `ruff` clean; runs in CI |
| **25** reusable templates | one `_template.py` per pattern, the skeleton you adapt |
| **0** third-party deps in solutions | standard library only, like a real interview |
| **Python 3.9+** | runs on the version most interview platforms use |

## Quickstart

Requires Python 3.9+ and [`uv`](https://docs.astral.sh/uv/). Node.js is optional, for the website.

```bash
git clone https://github.com/samcolmanetti/learn-python-with-tests
cd learn-python-with-tests

uv sync            # install pytest, hypothesis, ruff
uv run pytest      # run every chapter's test suite
uv run ruff check  # lint

npx honkit serve   # read it as a website at http://localhost:4000
```

New here? Start with [How to study with this book](how-to-study.md), then
[Hello, pytest](hello-pytest.md).

## The roadmap

### Getting started

1. [Install Python & tooling](install-python.md) · uv, pytest, and a green baseline.
2. [Why TDD for interviews](why-tdd-for-interviews.md) · the case for test-first under pressure.
3. [How to study with this book](how-to-study.md) · the blank-file rule and spaced repetition.

### Python fundamentals

[Hello, pytest](hello-pytest.md) ·
[Numbers](numbers.md) ·
[Control flow](control-flow.md) ·
[Iteration](iteration.md) ·
[Lists & slicing](lists-and-slicing.md) ·
[Strings](strings.md) ·
[Dicts & sets](dicts-and-sets.md) ·
[Comprehensions & generators](comprehensions.md) ·
[Classes & dataclasses](classes-and-dataclasses.md) ·
[Object-oriented Python](object-oriented-python.md) ·
[Exceptions & errors](exceptions.md) ·
[Iterators & iterables](iterators.md) ·
[Type hints](type-hints.md) ·
[Decorators](decorators.md)

### Applied Python

[File handling & context managers](file-handling.md) ·
[Modules & packaging](modules-and-packaging.md) ·
[Concurrency](concurrency.md) ·
[Internet & HTTP calls](internet-and-http.md)

### Testing fundamentals

[pytest deep dive](pytest-deep-dive.md) ·
[Mocking](mocking.md) ·
[Property-based testing](property-based-testing.md) ·
[Test organization](test-organization.md)

### Complexity & Python's toolbox

[Complexity & Big-O](complexity.md) ·
[Built-in data structures cheat sheet](builtins-cheatsheet.md) ·
[Sorting & custom comparators](sorting-and-comparators.md)

### Interview patterns

[Two Pointers](two-pointers.md) ·
[Sliding Window](sliding-window.md) ·
[Binary Search](binary-search.md) ·
[Prefix Sum](prefix-sum.md) ·
[Stack & Monotonic Stack](stack-and-monotonic-stack.md) ·
[Linked Lists](linked-lists.md) ·
[Intervals](intervals.md) ·
[Trees: DFS](trees-dfs.md) ·
[Trees: BFS](trees-bfs.md) ·
[Binary Search Tree](bst.md) ·
[Backtracking](backtracking.md) ·
[Graphs: Traversal](graphs-traversal.md) ·
[Topological Sort](topological-sort.md) ·
[Union Find](union-find.md) ·
[Dijkstra](dijkstra.md) ·
[Heaps](heaps.md) ·
[Greedy](greedy.md) ·
[DP: 1D](dp-1d.md) ·
[DP: Grid](dp-grid.md) ·
[DP: Knapsack](dp-knapsack.md) ·
[DP: Intervals](dp-intervals.md) ·
[Trie](trie.md) ·
[Bit Manipulation](bit-manipulation.md) ·
[Math](math.md) ·
[Design: LRU Cache](design-lru-cache.md)

### Meta

[Anti-patterns](anti-patterns.md) ·
[Speedrun strategy](speedrun-strategy.md) ·
[Contributing](CONTRIBUTING.md) ·
[Chapter template](template.md)

## How it's organised

- Each chapter is a markdown file at the repo root (e.g. `iteration.md`) plus a sibling code
  folder (e.g. `iteration/`).
- **Fundamentals** chapters grow the code in versioned snapshots (`v1/`, `v2/`, ...), one per
  step of the TDD evolution.
- **Pattern** chapters ship a `_template.py` (the reusable skeleton) and a `solutions/` folder
  with one tested problem per file.
- `SUMMARY.md` is the table of contents and the single source of truth for navigation.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the authoring conventions and the house style.

## Built with a little extra

- **A style validator** (`.claude/skills/article-writer/`) keeps every chapter in one voice:
  zero em-dashes, `uv` commands, the full TDD cycle, and working code links. It fails the build
  on a stray em-dash.
- **Rich code blocks** on the website: syntax highlighting, a copy button, and per-line hover
  highlighting, so the reading experience matches a modern docs site.

## License

MIT. Learn freely, and if it helps you land the job, pay it forward by contributing a chapter.
