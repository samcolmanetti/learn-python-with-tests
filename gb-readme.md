# Learn Python with Tests

<p align="center"><em>Learn Python for coding interviews — one failing test at a time.</em></p>

## What this is

A hands-on course that teaches you **Python** and the **algorithmic patterns** that show up in
coding interviews, using **test-driven development** the whole way through. It is modelled on
[Learn Go with Tests](https://github.com/quii/learn-go-with-tests) — same incremental,
test-first rhythm — but aimed squarely at interview preparation in Python.

You will:

* **Learn Python by writing tests.** Every language feature is introduced with a failing test,
  then the smallest code that makes it pass, then a refactor. The test *is* the spec.
* **Drill interview patterns, not random problems.** The core of the book is organised by
  **pattern** — Two Pointers, Sliding Window, Binary Search, DFS/BFS, Backtracking, Graphs,
  Heaps, Dynamic Programming, and more. Each pattern comes with a reusable Python template and
  several worked problems.
* **Build the habit that wins interviews.** Writing a small failing test before you code is the
  single best way to clarify a problem under pressure, catch your own bugs, and refactor with
  confidence.

## Who it's for

* You can program (in some language) and want to get fluent in **Python for interviews**.
* You like learning by doing, and you want **runnable, tested** examples — not walls of prose.
* You want a **roadmap**, so you always know what to study next.

## How to read it

Work top to bottom, or jump to a pattern you want to drill:

1. **Getting started** — install the tools, understand why TDD pays off in interviews.
2. **Python fundamentals** — the language, taught test-first.
3. **Testing fundamentals** — `pytest`, mocking, and property-based testing with Hypothesis.
4. **Complexity & Python's toolbox** — Big-O, and the built-ins (`deque`, `heapq`, `Counter`,
   `bisect`, …) that make Python interview code short and fast.
5. **Interview patterns** — the main event. One chapter per pattern, each with a template and
   worked problems.
6. **Meta** — anti-patterns to avoid, and how to run timed "speedrun" practice.

Every chapter links to its runnable code. Clone the repo, run `pytest`, and change things —
that is the whole point.

> The full roadmap is in the sidebar (`SUMMARY.md`). Chapters marked *coming soon* are
> scaffolded and waiting to be written following the same template — contributions welcome.
