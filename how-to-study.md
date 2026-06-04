# How to study with this book

The roadmap (the sidebar) is ordered deliberately. Here's how to get the most out of it.

## The path

1. **Getting started** — install the tools, read [Why TDD for interviews](why-tdd-for-interviews.md).
2. **Python fundamentals** — even if you know another language, skim these. Python's slicing,
   immutability, and built-ins are where interview bugs hide.
3. **Testing fundamentals** — `pytest` and Hypothesis. You'll use them in every later chapter.
4. **Complexity & Python's toolbox** — Big-O and the standard-library data structures. Don't
   skip this; the right structure is half of most solutions.
5. **Interview patterns** — the main event. Work them roughly in order; later patterns (graphs,
   DP) lean on earlier ones (DFS/BFS, recursion).
6. **Meta** — [anti-patterns](anti-patterns.md) and [speedrun strategy](speedrun-strategy.md)
   once you've got a few patterns under your belt.

## Study one pattern at a time

For each pattern chapter:

1. **Read the "when to reach for it" section first.** Recognising *which* pattern a problem
   wants is the skill interviews actually test. Train the trigger, not just the technique.
2. **Walk the template** until you can reproduce its skeleton from memory.
3. **Do the worked problems test-first** — and genuinely write the test before peeking at the
   solution. Cover the screen if you have to.
4. **Then redo each problem from a blank file.** This is the highest-value step (see below).

## The blank-file rule

Reading a solution teaches you almost nothing durable. The learning happens when you reproduce
it from nothing. After you've worked a problem:

- Open a new file. Write the tests from memory first.
- Solve it with no reference. If you get stuck for more than a few minutes, peek, close the
  reference, and start the function over from the top.
- A problem isn't "done" until you can go test → green from a blank file without help.

## Spaced repetition beats cramming

Patterns fade. Re-derive a problem the next day, then a few days later, then a week later. The
re-derivations get fast, and *fast* is the goal — in an interview you want the pattern to surface
in seconds. A simple system: keep a list of problems you've solved with the date; re-do the
oldest few at the start of each session.

## Use brute force as scaffolding

Stuck on the optimal approach? Write the obvious O(n²) (or O(2ⁿ)) version first and get it green.
Now you have a **correctness oracle**: property-test your clever version against the brute force
(`@given(...)` then `assert fast(xs) == slow(xs)`). This both unblocks you and demonstrates
exactly the "make it work, then make it fast" progression interviewers want to see.

## Track your patterns, not your problem count

"I did 300 problems" is a weak signal. "I can recognise and execute all 25 patterns from a blank
file" is the real bar. Keep a checklist of patterns and your confidence in each; spend your time
on the reds, not on padding the green count.

## A realistic cadence

- **Per session (~60–90 min):** one new pattern (read + worked problems), then re-derive 2–3
  problems from previous sessions.
- **Weekly:** one [speedrun](speedrun-strategy.md) — timed, no reference, mixed patterns — to
  simulate interview pressure.

Next: start with [Hello, pytest](hello-pytest.md), or jump to the patterns with
[Two Pointers](two-pointers.md).
