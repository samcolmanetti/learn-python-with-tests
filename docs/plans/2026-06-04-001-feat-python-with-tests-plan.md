---
title: "feat: Learn Python with Tests — TDD-driven interview prep book"
type: feat
status: active
date: 2026-06-04
---

# feat: Learn Python with Tests — TDD-driven interview prep book

## Overview

Build **Learn Python with Tests** — a GitBook-style learning resource modeled on
[`quii/learn-go-with-tests`](https://github.com/quii/learn-go-with-tests), but re-aimed at
**learning Python for coding interviews through test-driven development (TDD)**.

The book has two intertwined goals:

1. **Teach Python the TDD way** — every language concept is introduced by writing a failing
   `pytest` test first, then the minimal code to pass, then refactoring (the canonical
   red → green → refactor loop the Go book uses).
2. **Drill interview patterns** — the bulk of the book is a **patterns-first** DSA roadmap
   (Two Pointers, Sliding Window, Binary Search, DFS/BFS, Backtracking, Graphs, Heaps, DP,
   …) where each pattern gets a reusable Python template plus several worked problems, each
   solved test-first.

This plan establishes the **project framework + full roadmap + exemplar chapters** that lock
in the conventions. It deliberately does *not* author all ~150 problem solutions — it builds
the skeleton and enough fully-worked exemplars per part that the remaining chapters can be
filled in mechanically by following the established template.

## Problem Frame

The user is preparing for coding interviews and learns best via TDD. They like the
`learn-go-with-tests` format (incremental, test-first, GitBook-rendered) but need Python and
an interview-pattern focus. Forking the Go repo is the wrong strategy — its content, code
samples, build tooling, and `go.mod` are Go-specific and would all be discarded. The right
move is a **fresh Python project that reuses the Go book's *structure and design*** (GitBook
`SUMMARY.md` TOC, `book.json`, `.gitbook/assets/`, per-chapter code folders, chapter
template) while replacing all content.

The Go repo has been cloned into `references/learn-go-with-tests/` (gitignored) as a design
reference. AlgoMonster's roadmap (`references/algomonster/sidebar.json`) and its 18 pattern
code-templates (`references/algomonster/templates.json`) drive the DSA roadmap structure.

## Requirements Trace

- **R1.** Reuse the GitBook website design of `learn-go-with-tests` (same `SUMMARY.md` +
  `book.json` + `.gitbook/assets/` format, same per-chapter markdown + code-folder layout, so
  it renders identically on GitBook.com and via a local CLI).
- **R2.** Content is Python, not Go — Python fundamentals taught test-first with `pytest`.
- **R3.** Every concept and problem is introduced via the TDD cycle (write the failing test
  first → minimal pass → refactor), mirroring the Go book's chapter template.
- **R4.** The roadmap is **patterns-first**: DSA content is grouped by pattern (e.g. Sliding
  Window), and each pattern has multiple worked example problems.
- **R5.** Roadmap topics are derived from the AlgoMonster sidebar and reusable templates, plus
  the Go book's pedagogical arc, adapted to Python.
- **R6.** Do **not** fork the Go repo. Start a fresh `python-with-tests` project; keep the Go
  clone in a gitignored `references/` folder for design reference only.
- **R7.** The project must be runnable and verifiable: `pytest` runs all chapter test suites
  green, and the book builds/serves locally as a static site.

## Scope Boundaries

- **Not** authoring every problem in the AlgoMonster roadmap. We build the framework + full
  TOC + exemplar chapters per part. The full SUMMARY lists all planned chapters; non-exemplar
  chapters ship as consistent **stubs** following the template.
- **Not** building a custom static-site generator. Reuse the GitBook/Honkit format the Go book
  already uses.
- **Not** covering System Design / Company-OA sections in depth — they appear in the roadmap
  as a clearly-marked "later" section but are out of scope for exemplar authoring.
- **Not** porting any Go code. The Go clone is reference-only and stays gitignored.

### Deferred to Separate Tasks

- Authoring the remaining (non-exemplar) pattern chapters and problem solutions: ongoing,
  incremental — one chapter/problem at a time following the established conventions.
- GitBook.com hosting/publishing setup (account, sync): future iteration once content matures.
- Translations, cover art, and "support me" pages (Go book has these; not needed initially).

## Context & Research

### Reference: how `learn-go-with-tests` is structured

Confirmed by inspecting the clone at `references/learn-go-with-tests/`:

- **TOC / design:** `SUMMARY.md` is the GitBook table of contents, grouped under `##` section
  headings (`Go fundamentals`, `Testing fundamentals`, `Build an application`, `Questions and
  answers`, `Meta`). `book.json` sets `{ "structure": { "readme": "gb-readme.md" } }`. Images
  live in `.gitbook/assets/`. This is the **legacy GitBook format**, which renders on
  GitBook.com and via the maintained `honkit` CLI locally — reusing it verbatim satisfies R1.
- **Per-chapter layout:** each chapter is a markdown file at repo root (e.g. `iteration.md`)
  **plus** a sibling code folder (e.g. `for/`). Fundamentals chapters use **versioned**
  subfolders `v1/ v2/ … v8/`, each a complete, compilable snapshot showing the TDD evolution.
- **Chapter template** (`template.md`): `intro → Write the test first → Try to run the test →
  Write the minimal amount of code… (check failing output) → Write enough code to make it pass
  → Refactor → Repeat for new requirements → Wrapping up`.
- **Prose convention:** each chapter opens with "**[You can find all the code for this chapter
  here](…)**" linking to its code folder, then narrates the red/green/refactor loop with code
  blocks and the exact failing-test output.
- `.gitignore` already ignores build output (`_book/`, `*.epub`, `*.pdf`).

### Reference: AlgoMonster roadmap (drives the DSA TOC)

From `references/algomonster/sidebar.json` (full title list extracted) and
`references/algomonster/templates.json` (18 pattern templates with Python skeletons):

- **Pattern families:** Binary Search, Two Pointers (same/opposite direction), Sliding Window
  (fixed/longest/shortest), Prefix Sum, Fast & Slow / Cycle, DFS (tree), BFS (tree),
  Backtracking (basic/pruning/aggregation/memo), BFS/DFS on Graph, Matrix-as-Graph,
  Topological Sort, Union Find (DSU), Dijkstra/weighted, Heap/Priority Queue (top-K,
  two-heaps), DP (1D/grid/dual-sequence/knapsack/interval/tree/bitmask), Trie, Monotonic
  Stack, Intervals, Greedy, Math (sieve), Divide & Conquer, Line Sweep, Segment Tree, OOP
  Design (LRU cache, etc.), System Design + Company OAs (out of exemplar scope).
- **18 reusable templates** (`templates.json` → each has a `python` code skeleton): these map
  almost 1:1 to the pattern chapters and become the book's per-pattern `_template.py`
  reference, rewritten as real, importable, *tested* Python (the AlgoMonster versions are
  pseudo-code, e.g. `remove input[left] from window`).

### External References

- `learn-go-with-tests` GitBook format → local rendering via **Honkit** (maintained GitBook
  fork; `npx honkit serve` / `npx honkit build`). Same `SUMMARY.md`/`book.json` contract.
- `pytest` (test runner), `hypothesis` (property-based testing — the Python analog to the Go
  book's property-based "Roman Numerals" chapter), `ruff` (lint/format), `uv` (fast,
  reproducible env + dependency management).

## Key Technical Decisions

- **Fresh project, not a fork.** Reuse design/structure only; the Go clone stays in gitignored
  `references/`. (R6)
- **Keep the exact GitBook file contract** (`SUMMARY.md`, `book.json` with `gb-readme.md`
  readme, `.gitbook/assets/`) so the site renders the same way and can later sync to
  GitBook.com. Build locally with **Honkit** via `npx` (no global install; pinned in
  `package.json`). (R1)
- **Tooling:** Python 3.12+, **uv** for env/deps, **pytest** for tests, **hypothesis** for
  property tests, **ruff** for lint/format. A single `uv run pytest` runs every chapter's
  suite. (R7)
- **Code-folder conventions** (mirrors Go book, adapted to Python + interview patterns):
  - *Fundamentals chapters* → versioned snapshots: `iteration/v1/`, `iteration/v2/`, … each a
    runnable package with `__init__.py`, the solution module, and `test_*.py`.
  - *Interview-pattern chapters* → a pattern folder containing `_template.py` (the reusable
    pattern skeleton) plus a `solutions/` dir with one `problem_name.py` +
    `test_problem_name.py` per worked problem.
  - pytest discovery via `test_*.py` naming; package dirs carry `__init__.py` so imports are
    unambiguous and chapters don't collide.
- **Patterns-first roadmap** (R4): the interview section is organized by pattern; within each
  pattern, an intro + template + several worked problems (each test-first).
- **Full TOC up front, exemplars deep.** `SUMMARY.md` enumerates the *entire* roadmap so the
  learning path is visible; this plan fully authors a few exemplar chapters per part and ships
  the rest as template-following stubs to be filled in incrementally.

## Open Questions

### Resolved During Planning

- **Fork vs. clone-to-references?** → Clone-to-references (gitignored). Forking a Go repo for a
  Python book provides no reusable content. (R6)
- **Which static-site tool matches the Go book's design?** → The legacy GitBook format it
  already uses; build locally with Honkit. No redesign needed. (R1)
- **What seeds the DSA roadmap?** → AlgoMonster `sidebar.json` (taxonomy) + `templates.json`
  (18 Python pattern skeletons), reconciled with the Go book's pedagogical ordering. (R5)
- **Property-based testing analog?** → `hypothesis`, introduced in the Testing-fundamentals
  part as the counterpart to the Go book's property-based Roman Numerals chapter. (R3)

### Deferred to Implementation

- Exact problem selection per exemplar pattern (which 2–4 LeetCode-style problems best teach
  each pattern) — decided while authoring, drawing from the AlgoMonster article list.
- Whether `_template.py` files are kept import-only (skeleton with `NotImplementedError`) or
  fully runnable — decide per pattern once the first real solution exists to generalize from.
- Final pinned versions of `honkit`, `pytest`, `hypothesis`, `ruff` — resolved at install time
  against current releases.

## Output Structure

    python-with-tests/
    ├── .gitignore                      # ignores references/, _book/, .venv/, __pycache__, *.pdf/epub
    ├── README.md                       # GitHub landing (dev/run instructions)
    ├── gb-readme.md                    # GitBook readme (book landing page, per book.json)
    ├── SUMMARY.md                      # FULL roadmap = GitBook table of contents
    ├── book.json                       # { structure: { readme: gb-readme.md } }
    ├── template.md                     # Python TDD chapter template
    ├── CONTRIBUTING.md                 # chapter/solution authoring conventions
    ├── pyproject.toml                  # uv project: pytest, hypothesis, ruff config
    ├── package.json                    # pins honkit for `npx honkit serve|build`
    ├── .github/workflows/ci.yml        # run pytest + ruff + honkit build on push
    ├── .gitbook/assets/                # images (placeholder cover to start)
    ├── references/                     # GITIGNORED — design reference only
    │   ├── learn-go-with-tests/        # (already cloned)
    │   └── algomonster/                # sidebar.json, templates.json (already present)
    │
    ├── install-python.md               # Part 0 — setup & tooling
    ├── why-tdd-for-interviews.md
    ├── how-to-study.md
    │
    ├── hello-pytest.md   + hello_pytest/{v1,v2,...}/        # Part 1 — Python fundamentals
    ├── numbers.md        + numbers/{v1,...}/
    ├── iteration.md      + iteration/{v1,...}/
    ├── lists-and-slicing.md + lists_and_slicing/{v1,...}/
    ├── strings.md, dicts-and-sets.md, comprehensions.md, classes-and-dataclasses.md,
    │   exceptions.md, iterators.md, type-hints.md, decorators.md   (stubs follow template)
    │
    ├── pytest-deep-dive.md + pytest_deep_dive/             # Part 2 — Testing fundamentals
    ├── property-based-testing.md + property_based_testing/{v1,...}/
    ├── mocking.md, test-organization.md                    (stubs)
    │
    ├── complexity.md, builtins-cheatsheet.md,              # Part 3 — Complexity & toolbox
    │   sorting-and-comparators.md + sorting_and_comparators/
    │
    ├── two-pointers.md   + two_pointers/{_template.py, solutions/}      # Part 4 — Patterns
    ├── sliding-window.md + sliding_window/{_template.py, solutions/}
    ├── binary-search.md  + binary_search/{_template.py, solutions/}
    ├── prefix-sum.md, stack-and-monotonic-stack.md, linked-lists.md, intervals.md,
    │   trees-dfs.md, trees-bfs.md, bst.md, backtracking.md, graphs-traversal.md,
    │   topological-sort.md, union-find.md, dijkstra.md, heaps.md, greedy.md,
    │   dp-1d.md, dp-grid.md, dp-knapsack.md, dp-intervals.md, trie.md,
    │   bit-manipulation.md, math.md, design-lru-cache.md      (stubs + _template.py each)
    │
    └── anti-patterns.md, speedrun-strategy.md               # Part 5 — Meta

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not
> implementation specification. The implementing agent should treat it as context, not code to
> reproduce.*

**Content architecture — three building blocks, reused everywhere:**

    SUMMARY.md  ──(GitBook TOC, grouped by ## section)──▶  renders the whole roadmap
        │
        ├─ Fundamentals chapter            ├─ Interview-pattern chapter
        │   foo.md  (narrates TDD loop)    │   pattern.md  (intro + when-to-use + template walk)
        │   foo/                           │   pattern/
        │     v1/  __init__.py             │     _template.py        ← real, tested Python skeleton
        │         foo.py                   │                            (adapted from templates.json)
        │         test_foo.py              │     solutions/
        │     v2/  … (next TDD step)       │       problem_a.py
        │     …                            │       test_problem_a.py  ← test-first per problem
        │                                  │       problem_b.py / test_problem_b.py

**Roadmap sections (SUMMARY.md `##` groups):**

    Part 0  Getting started      → install-python, why-tdd-for-interviews, how-to-study
    Part 1  Python fundamentals  → hello-pytest, numbers, iteration, lists/slicing, strings,
                                    dicts/sets, comprehensions, classes/dataclasses, exceptions,
                                    iterators, type-hints, decorators
    Part 2  Testing fundamentals → pytest-deep-dive, mocking, property-based-testing (hypothesis),
                                    test-organization
    Part 3  Complexity & toolbox → complexity (Big-O), builtins-cheatsheet (deque/heapq/Counter…),
                                    sorting-and-comparators
    Part 4  Interview patterns   → Two Pointers, Sliding Window, Binary Search, Prefix Sum,
                                    Stack/Monotonic Stack, Linked Lists, Intervals, Trees-DFS,
                                    Trees-BFS, BST, Backtracking, Graphs, Topo Sort, Union Find,
                                    Dijkstra, Heaps, Greedy, DP (1D/grid/knapsack/intervals),
                                    Trie, Bit Manipulation, Math, Design (LRU)
    Part 5  Meta                 → anti-patterns, speedrun-strategy
    (Later, out of scope)        → System Design, Company OAs  (listed, not authored)

**Verification loop (every chapter):** `uv run pytest` green ⇄ `npx honkit build` succeeds ⇄
every `SUMMARY.md` link resolves to an existing file.

## Implementation Units

- [ ] **Unit 1: Project scaffolding & tooling**

**Goal:** A runnable Python project with reproducible tooling and the GitBook build contract in
place, with the reference clone gitignored.

**Requirements:** R1, R6, R7

**Dependencies:** None

**Files:**
- Create: `.gitignore`, `pyproject.toml`, `package.json`, `book.json`, `README.md`,
  `.github/workflows/ci.yml`
- Create: `.gitbook/assets/.gitkeep` (placeholder for images)

**Approach:**
- `.gitignore` ignores `references/`, `_book/`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`,
  `*.epub`, `*.pdf`, `.DS_Store` (mirror the Go book's ignore set + `references/`).
- `pyproject.toml`: project metadata, dev deps `pytest`, `hypothesis`, `ruff`; configure
  pytest (`testpaths`, `python_files = test_*.py`) and ruff. Managed via `uv`.
- `package.json`: pin `honkit` as a devDependency so `npx honkit serve|build` reproduces the
  Go book's rendering. `book.json` mirrors the Go book: `{ "structure": { "readme": "gb-readme.md" } }`.
- `README.md`: GitHub-facing — how to set up (`uv sync`), run tests (`uv run pytest`), serve the
  book (`npx honkit serve`), and note `references/` is reference-only.
- `ci.yml`: on push/PR run `uv run ruff check`, `uv run pytest`, and `npx honkit build`.

**Patterns to follow:** `references/learn-go-with-tests/.gitignore`,
`references/learn-go-with-tests/book.json`.

**Test scenarios:**
- Integration: `uv run pytest` exits 0 on a freshly scaffolded project (no tests yet =
  "no tests ran" is acceptable, or a trivial smoke test passes).
- Integration: `npx honkit build` produces `_book/` without error once `SUMMARY.md` exists
  (validated end-to-end after Unit 2).
- Edge case: `git status` does not list anything under `references/` (gitignore works).

**Verification:** `uv sync` succeeds; `uv run pytest` runs; `references/` is untracked; CI file
is valid YAML.

- [ ] **Unit 2: GitBook structure & full roadmap (SUMMARY.md + section landings + stubs)**

**Goal:** The complete learning roadmap exists as a navigable GitBook TOC, with every chapter
file present (exemplars filled later; the rest as template-following stubs).

**Requirements:** R1, R4, R5

**Dependencies:** Unit 1

**Files:**
- Create: `SUMMARY.md` (full TOC grouped by `##` part headings — see High-Level Design),
  `gb-readme.md` (book landing page)
- Create: stub markdown for every roadmap chapter (Parts 0–5) not authored as an exemplar in
  later units — each stub follows `template.md` headings with a one-line "coming soon" intro
  and the canonical TDD section skeleton.

**Approach:**
- `SUMMARY.md` uses the exact Go-book format: `# Table of contents`, a readme bullet, then
  `## <Part>` headings with `* [Title](file.md)` links. Every link must resolve to a real file.
- `gb-readme.md` introduces the book: what it is (Python + TDD + interview patterns), who it's
  for, how to read it. No "support me"/translations boilerplate.
- Stubs are intentionally thin but structurally complete so the TOC is fully navigable and the
  build is green from day one.

**Patterns to follow:** `references/learn-go-with-tests/SUMMARY.md`,
`references/learn-go-with-tests/gb-readme.md`, `references/learn-go-with-tests/template.md`.

**Test scenarios:**
- Integration: every `(file.md)` referenced in `SUMMARY.md` exists on disk (link-integrity
  check — can be a small `pytest` test that parses `SUMMARY.md` and asserts each path exists).
- Integration: `npx honkit build` succeeds with the full SUMMARY and produces a page per entry.
- Edge case: no orphan markdown files (every chapter `.md` at root is referenced by SUMMARY),
  asserted by the same test.

**Verification:** `npx honkit serve` renders the full roadmap; SUMMARY link-integrity test is
green; section groupings match the Part 0–5 design.

- [ ] **Unit 3: Chapter & solution conventions (template, contributing, pattern templates)**

**Goal:** Lock in *how* chapters and solutions are written so every future chapter is
consistent — including the 18 reusable pattern templates converted to real, tested Python.

**Requirements:** R3, R4, R5

**Dependencies:** Unit 2

**Files:**
- Create: `template.md` (Python TDD chapter template), `CONTRIBUTING.md` (conventions:
  versioned folders for fundamentals, `_template.py` + `solutions/` for patterns, `test_*.py`
  naming, `__init__.py` packaging)
- Create: `_template.py` skeleton for each Part-4 pattern folder (e.g. `two_pointers/_template.py`,
  `sliding_window/_template.py`, `binary_search/_template.py`, …) adapted from
  `references/algomonster/templates.json` (18 templates), rewritten as valid Python.
- Test: `tests/test_templates_importable.py` (or per-folder) asserting each `_template.py`
  imports cleanly.

**Approach:**
- `template.md` mirrors the Go template but Python/pytest-flavored: intro → Write the test
  first → Run it (show the failing output, e.g. `NameError` / `AssertionError`) → Minimal code →
  Make it pass → Refactor → Repeat → Wrapping up.
- Convert each AlgoMonster pseudo-code template (`templates.json[*].code.python`) into real
  Python — replacing pseudo lines like `remove input[left] from window` with working code.
  Each `_template.py` is a documented, importable reference skeleton.
- `CONTRIBUTING.md` documents folder/file naming so stubs can be filled in uniformly.

**Patterns to follow:** `references/learn-go-with-tests/template.md`,
`references/learn-go-with-tests/contributing.md`; `references/algomonster/templates.json`.

**Test scenarios:**
- Happy path: importing each `_template.py` succeeds (no syntax errors, no top-level side
  effects).
- Edge case: a template that is intentionally a skeleton raises `NotImplementedError` (not a
  silent wrong answer) when its placeholder is called — assert that contract if used.
- Integration: `ruff check` passes on all `_template.py` files.

**Verification:** all templates import and lint clean; `CONTRIBUTING.md` + `template.md`
describe both fundamentals and pattern layouts.

- [ ] **Unit 4: Exemplar Python-fundamentals chapters (fully TDD)**

**Goal:** Three to four fully-authored fundamentals chapters that prove the test-first teaching
format end-to-end with versioned code snapshots.

**Requirements:** R2, R3

**Dependencies:** Unit 3

**Files:**
- Author: `hello-pytest.md` + `hello_pytest/v1..vN/` (`__init__.py`, module, `test_*.py`)
- Author: `numbers.md` + `numbers/v1..vN/`
- Author: `iteration.md` + `iteration/v1..vN/`
- Author: `lists-and-slicing.md` + `lists_and_slicing/v1..vN/`
- Test: `test_*.py` inside each versioned folder.

**Execution note:** Author test-first — each chapter section introduces the failing test before
the implementation, and each `vN` folder is a green snapshot of that step.

**Approach:**
- `hello-pytest`: install/run pytest, the red→green→refactor loop, assertions, `pytest -k`,
  first refactor — the Python analog of the Go book's "Hello, World".
- `numbers`: int/float, integer vs true division, `divmod`, overflow-free ints; test-driven.
- `iteration`: `for`/`while`, `range`, `enumerate`, building strings, a benchmark aside.
- `lists-and-slicing`: list ops, slicing (incl. negative/step), copy vs alias, comprehensions
  teaser — the gateway to interview array work.
- Each chapter opens with the "all the code for this chapter here" link to its folder.

**Patterns to follow:** `references/learn-go-with-tests/hello-world.md` + `hello-world/v1..v8/`;
`references/learn-go-with-tests/iteration.md` + `for/`.

**Test scenarios:**
- Happy path (hello-pytest): `greet()`/`hello()` returns expected string for default and named
  input.
- Happy path (numbers): integer division and `divmod` return expected quotient/remainder;
  large-int multiplication is exact.
- Happy path (iteration): `repeat("a", 5) == "aaaaa"`; `enumerate`-based function yields correct
  index/value pairs.
- Edge case (lists-and-slicing): empty list, negative indices, step slices (`[::-1]`,
  `[::2]`), and that a slice is a copy (mutating the slice doesn't affect the original).
- Edge case (iteration): `repeat(x, 0) == ""`.

**Verification:** `uv run pytest` green across all `vN` folders; each chapter's prose matches
its final `vN` code; SUMMARY links resolve.

- [ ] **Unit 5: Exemplar testing-fundamentals chapter (pytest + Hypothesis)**

**Goal:** Teach the testing toolbox the book relies on, including property-based testing — the
Python analog to the Go book's property-based Roman Numerals chapter.

**Requirements:** R3, R7

**Dependencies:** Unit 4

**Files:**
- Author: `pytest-deep-dive.md` + `pytest_deep_dive/` (fixtures, `parametrize`, `raises`,
  markers) with `test_*.py`.
- Author: `property-based-testing.md` + `property_based_testing/v1..vN/` using `hypothesis`.
- Test: `test_*.py` in each folder.

**Execution note:** Test-first; the property-based chapter should show a property catching a
bug that example-based tests miss, then the fix.

**Approach:**
- `pytest-deep-dive`: `assert` introspection, `@pytest.fixture`, `@pytest.mark.parametrize`,
  `pytest.raises`, `-k`/`-m` selection — the toolkit reused by every later chapter.
- `property-based-testing`: introduce `hypothesis` `@given` with strategies; e.g. a
  `to_roman`/`from_roman` round-trip property, or a sorting invariant, demonstrating shrinking.

**Patterns to follow:** `references/learn-go-with-tests/roman-numerals.md` (property-based arc).

**Test scenarios:**
- Happy path: a parametrized test exercises several inputs from one function.
- Integration: a fixture sets up shared state consumed by multiple tests.
- Error path: `pytest.raises(ValueError)` asserts invalid input raises as documented.
- Property (Hypothesis): round-trip invariant holds for all generated inputs
  (`from_roman(to_roman(n)) == n` for n in a bounded range), and Hypothesis reports a minimal
  counterexample when the implementation is deliberately broken.

**Verification:** `uv run pytest` green including Hypothesis runs; the chapter shows a failing
property and its fix.

- [ ] **Unit 6: Exemplar interview-pattern chapters (Two Pointers, Sliding Window, Binary Search)**

**Goal:** Prove the patterns-first format: per-pattern intro + reusable template + multiple
worked problems, each solved test-first.

**Requirements:** R3, R4, R5

**Dependencies:** Unit 3 (templates), Unit 5 (testing toolbox)

**Files:**
- Author: `two-pointers.md` + `two_pointers/_template.py` + `two_pointers/solutions/`
  (`valid_palindrome.py`+test, `two_sum_sorted.py`+test, `remove_duplicates.py`+test)
- Author: `sliding-window.md` + `sliding_window/_template.py` + `sliding_window/solutions/`
  (`longest_substring_no_repeat.py`+test, `subarray_sum_fixed.py`+test, `find_all_anagrams.py`+test)
- Author: `binary-search.md` + `binary_search/_template.py` + `binary_search/solutions/`
  (`first_not_smaller.py`+test, `search_rotated.py`+test, `sqrt.py`+test)
- Test: `test_*.py` alongside every solution.

**Execution note:** Each problem is authored test-first — the chapter shows the failing test,
the minimal pass, then a refactor toward the pattern template.

**Approach:**
- Each chapter: when-to-recognize-the-pattern → walk the `_template.py` → 2–3 worked problems,
  each narrating the TDD loop → "wrapping up" with the pattern's invariant (e.g. Two Pointers
  invariant, window monotonicity).
- Problems are chosen from the AlgoMonster article list for each pattern.

**Patterns to follow:** `references/algomonster/templates.json` (the matching template per
pattern); Go book chapter prose flow.

**Test scenarios:**
- Two Pointers — Happy path: `valid_palindrome("A man, a plan, a canal: Panama") is True`;
  `two_sum_sorted([2,7,11,15], 9) == (0,1)` (or index pair per spec). Edge: empty string is a
  palindrome; no-solution returns the documented sentinel.
- Sliding Window — Happy path: `longest_substring_no_repeat("abcabcbb") == 3`. Edge: empty
  string → 0; all-same chars → 1; `find_all_anagrams("cbaebabacd","abc") == [0,6]`.
- Binary Search — Happy path: `first_not_smaller([1,3,3,5,8,8,10], 5) == 3`. Edge: target
  larger than all elements → out-of-range sentinel; single-element and empty arrays; `sqrt(8)`
  floor `== 2`.
- Error path (where applicable): invalid/`None` input raises the documented exception.

**Verification:** `uv run pytest` green for all pattern solutions; each `_template.py` is
exercised by at least one solution; chapters render in the TOC under Part 4.

- [ ] **Unit 7: Complexity & Python toolbox chapter (cheat sheets + sorting)**

**Goal:** Give the interview-essential reference material — Big-O reasoning, Python's built-in
data structures, and custom-comparator sorting — with small tested examples.

**Requirements:** R2, R4

**Dependencies:** Unit 4

**Files:**
- Author: `complexity.md` (Big-O, common time/space classes, how to reason about Python ops)
- Author: `builtins-cheatsheet.md` (`list`, `dict`, `set`, `collections.deque`, `heapq`,
  `Counter`, `defaultdict`, `bisect` — with complexity notes)
- Author: `sorting-and-comparators.md` + `sorting_and_comparators/` (`key=`,
  `functools.cmp_to_key`, stable sort) with `test_*.py`
- Test: `test_*.py` for the sorting examples.

**Approach:**
- Keep `complexity.md` and `builtins-cheatsheet.md` reference-style (tables + short tested
  snippets where useful); `sorting-and-comparators` is a full tested mini-chapter since it has
  real behavior to verify.

**Patterns to follow:** AlgoMonster "Runtime to Algo / Keyword to Algo" cheat sheets;
`references/learn-go-with-tests` prose style.

**Test scenarios:**
- Happy path: sort a list of tuples by a secondary key via `key=`; sort with `cmp_to_key`
  yields the same order as the equivalent `key=`.
- Edge case: stable sort preserves the relative order of equal keys; sorting an empty list
  returns `[]`.
- Happy path (builtins): a `Counter`/`deque`/`heapq` snippet returns the documented result
  (e.g. `heapq.nsmallest`, `deque.appendleft`).
- Non-behavioral parts (`complexity.md`, `builtins-cheatsheet.md` prose): Test expectation:
  none — reference prose; only the runnable snippets in `sorting_and_comparators/` are tested.

**Verification:** `uv run pytest` green for sorting examples; cheat-sheet chapters render and
are linked in Part 3.

- [ ] **Unit 8: Meta pages (why-TDD, how-to-study, anti-patterns, speedrun)**

**Goal:** Frame the book's philosophy and study strategy so the roadmap has narrative bookends.

**Requirements:** R3, R4

**Dependencies:** Unit 2

**Files:**
- Author: `why-tdd-for-interviews.md`, `how-to-study.md`, `install-python.md` (Part 0)
- Author: `anti-patterns.md`, `speedrun-strategy.md` (Part 5)

**Approach:**
- `why-tdd-for-interviews`: why test-first beats read-the-book / random-LeetCode (echoing the
  Go book's "what didn't work" framing), adapted to interview prep.
- `install-python.md`: install Python 3.12+, `uv`, run the first test, serve the book.
- `how-to-study`: how to use the roadmap (patterns-first, spaced repetition, redo problems
  from a blank file).
- `anti-patterns`: common TDD/interview anti-patterns (over-mocking, testing implementation,
  premature optimization).
- `speedrun-strategy`: timed practice / mock-interview cadence using the pattern chapters.

**Patterns to follow:** `references/learn-go-with-tests/why.md`, `anti-patterns.md`,
`install-go.md`.

**Test scenarios:** Test expectation: none — prose chapters with no executable code. Covered by
the SUMMARY link-integrity test (Unit 2) and `npx honkit build` succeeding.

**Verification:** pages render; linked correctly in Parts 0 and 5; `honkit build` clean.

## System-Wide Impact

- **Interaction graph:** `SUMMARY.md` is the single source of truth for navigation — adding a
  chapter means (1) the `.md`, (2) optional code folder, (3) a SUMMARY link. The link-integrity
  test (Unit 2) is the guardrail tying these together.
- **Error propagation:** A broken SUMMARY link or a failing chapter test should fail CI
  (`honkit build` / `pytest`), not silently ship.
- **State lifecycle risks:** Versioned `vN` folders can drift from chapter prose — verification
  requires the final `vN` to match the chapter's end state.
- **API surface parity:** Every pattern chapter must pair an authored `_template.py` with at
  least one `solutions/` example that exercises it (no orphan templates).
- **Integration coverage:** The SUMMARY link-integrity + `honkit build` + `pytest` trio
  together prove the book is navigable, buildable, and correct — unit tests of individual
  solutions alone wouldn't catch a broken TOC.
- **Unchanged invariants:** The GitBook file contract (`SUMMARY.md`, `book.json`,
  `.gitbook/assets/`) is preserved exactly so GitBook.com rendering stays compatible.

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Scope explosion — trying to author all ~150 problems | Plan fully authors only exemplars per part; rest are template-following stubs. Scope boundary is explicit. |
| AlgoMonster templates are pseudo-code, not runnable | Unit 3 converts each to real, tested Python; a test asserts every `_template.py` imports/lints. |
| SUMMARY links rot as chapters are added | Automated link-integrity test (Unit 2) runs in CI. |
| `references/` accidentally committed | `.gitignore` ignores it (Unit 1); verification checks `git status` is clean. |
| Honkit/GitBook format drift | Reuse the Go book's exact `book.json`/`SUMMARY.md` contract; pin `honkit` in `package.json`. |
| Chapter prose drifting from `vN` code | Verification step requires final `vN` to match chapter end state. |

## Documentation / Operational Notes

- `README.md` (GitHub-facing) covers setup/run/serve; `gb-readme.md` is the in-book landing.
- `CONTRIBUTING.md` documents authoring conventions so the remaining roadmap can be filled in
  consistently over time.
- CI (`.github/workflows/ci.yml`) runs `ruff`, `pytest`, and `honkit build` — the same checks a
  contributor runs locally.

## Sources & References

- Design/structure reference: `references/learn-go-with-tests/` (cloned, gitignored) —
  `SUMMARY.md`, `book.json`, `template.md`, per-chapter `vN` code folders.
- Roadmap taxonomy: `references/algomonster/sidebar.json` (full pattern/article list).
- Pattern templates: `references/algomonster/templates.json` (18 Python pattern skeletons).
- Upstream project: https://github.com/quii/learn-go-with-tests
- Tooling: `uv`, `pytest`, `hypothesis`, `ruff`, `honkit` (maintained GitBook CLI fork).
