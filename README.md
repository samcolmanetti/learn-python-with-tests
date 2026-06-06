<h1 align="center">Learn Python with Tests</h1>

<p align="center"><em>Learn Python for coding interviews, one failing test at a time.</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/tests-716%20passing-brightgreen" alt="tests">
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
| **716** passing tests | every worked example is verified; `ruff` clean; runs in CI |
| **25** reusable templates | one `_template.py` per pattern, the skeleton you adapt |
| **0** third-party deps in solutions | standard library only, like a real interview |
| **Python 3.9+** | runs on the version most interview platforms use |

## Getting started

**Read it online at [learnpython.scol.xyz](https://learnpython.scol.xyz).** You don't clone
anything to follow the book, you write your own code in your own folder as you go.

New here? Start with [Install Python & tooling](book/install-python.md), then
[Hello, pytest](book/hello-pytest.md). All you need is Python 3.9+ and
[`uv`](https://docs.astral.sh/uv/); the install chapter sets up your practice project in two
commands.

Want to contribute a chapter or fix something? That's the one case where you clone the repo, see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## The roadmap

### Getting started

1. [Install Python & tooling](book/install-python.md) · uv, pytest, and a green baseline.
2. [Why TDD for interviews](book/why-tdd-for-interviews.md) · the case for test-first under pressure.
3. [How to study with this book](book/how-to-study.md) · the blank-file rule and spaced repetition.

### Python fundamentals

[Hello, pytest](book/hello-pytest.md) ·
[Numbers](book/numbers.md) ·
[Control flow](book/control-flow.md) ·
[Iteration](book/iteration.md) ·
[Lists & slicing](book/lists-and-slicing.md) ·
[Strings](book/strings.md) ·
[Dicts & sets](book/dicts-and-sets.md) ·
[Comprehensions & generators](book/comprehensions.md) ·
[Classes & dataclasses](book/classes-and-dataclasses.md) ·
[Object-oriented Python](book/object-oriented-python.md) ·
[Exceptions & errors](book/exceptions.md) ·
[Iterators & iterables](book/iterators.md) ·
[Type hints](book/type-hints.md) ·
[Decorators](book/decorators.md)

### Applied Python

[File handling & context managers](book/file-handling.md) ·
[Modules & packaging](book/modules-and-packaging.md) ·
[Concurrency](book/concurrency.md) ·
[Internet & HTTP calls](book/internet-and-http.md)

### Testing fundamentals

[pytest deep dive](book/pytest-deep-dive.md) ·
[Mocking](book/mocking.md) ·
[Property-based testing](book/property-based-testing.md) ·
[Test organization](book/test-organization.md)

### Complexity & Python's toolbox

[Complexity & Big-O](book/complexity.md) ·
[Built-in data structures cheat sheet](book/builtins-cheatsheet.md) ·
[Sorting & custom comparators](book/sorting-and-comparators.md)

### Interview patterns

[Two Pointers](book/two-pointers.md) ·
[Sliding Window](book/sliding-window.md) ·
[Binary Search](book/binary-search.md) ·
[Prefix Sum](book/prefix-sum.md) ·
[Stack & Monotonic Stack](book/stack-and-monotonic-stack.md) ·
[Linked Lists](book/linked-lists.md) ·
[Intervals](book/intervals.md) ·
[Trees: DFS](book/trees-dfs.md) ·
[Trees: BFS](book/trees-bfs.md) ·
[Binary Search Tree](book/bst.md) ·
[Backtracking](book/backtracking.md) ·
[Graphs: Traversal](book/graphs-traversal.md) ·
[Topological Sort](book/topological-sort.md) ·
[Union Find](book/union-find.md) ·
[Dijkstra](book/dijkstra.md) ·
[Heaps](book/heaps.md) ·
[Greedy](book/greedy.md) ·
[DP: 1D](book/dp-1d.md) ·
[DP: Grid](book/dp-grid.md) ·
[DP: Knapsack](book/dp-knapsack.md) ·
[DP: Intervals](book/dp-intervals.md) ·
[Trie](book/trie.md) ·
[Bit Manipulation](book/bit-manipulation.md) ·
[Math](book/math.md) ·
[Design: LRU Cache](book/design-lru-cache.md)

### Meta

[Anti-patterns](book/anti-patterns.md) ·
[Speedrun strategy](book/speedrun-strategy.md) ·
[Contributing](CONTRIBUTING.md) ·
[Chapter template](book/template.md)

## How it's organised

- **`book/`** holds every chapter's prose (e.g. `book/iteration.md`), `SUMMARY.md`, and the site
  config. **`code/`** holds every chapter's code (e.g. `code/iteration/`), which is what `pytest`
  runs.
- **Fundamentals** chapters are one flat pair of files (`code/iteration/iteration.py` +
  `test_iteration.py`), the same shape you write while following along.
- **Pattern** chapters ship a `_template.py` (the reusable skeleton) and a `solutions/` folder
  with one tested problem per file.
- `book/SUMMARY.md` is the table of contents and the single source of truth for navigation.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the authoring conventions and the house style.

## Built with a little extra

- **A style validator** (`.claude/skills/article-writer/`) keeps every chapter in one voice:
  zero em-dashes, `uv` commands, the full TDD cycle, and working code links. It fails the build
  on a stray em-dash.
- **Rich code blocks** on the website: syntax highlighting, a copy button, and per-line hover
  highlighting, so the reading experience matches a modern docs site.

## License

MIT. Learn freely, and if it helps you land the job, pay it forward by contributing a chapter.
