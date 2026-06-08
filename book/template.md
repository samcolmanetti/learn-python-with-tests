# Chapter templates

There are two kinds of chapter, and they have two shapes. Read the one that fits before you start,
then follow its headings. Both walk the same TDD loop. The difference is that an interview-pattern
chapter has a reusable template and several worked problems, so its TDD cycles live under each
problem as `###` headings.

The code-link line at the top of every chapter points at the chapter's code folder on GitHub, so it
resolves on the published site. Replace `USER` with the repo owner and `CHAPTER_FOLDER` with the
chapter's snake_case code directory.

## Template A: a fundamentals chapter

Use this for language chapters (control flow, strings, OOP, file handling, and so on). It is one or
more strict TDD cycles, each adding one requirement, with these headings in this order:

1. `# [Chapter title]`
2. `**[You can find all the code for this chapter here](https://github.com/USER/python-with-tests/tree/main/code/CHAPTER_FOLDER)**`
3. One or two sentences of setup. No "by the end you will learn" preamble.
4. `## Write the test first` (the smallest behaviour, as a failing pytest test)
5. `## Try to run the test` (paste the real failing output, then one sentence on what it means)
6. `## Write the minimal amount of code for the test to run and check the failing test output`
   (a stub that runs but returns the wrong thing, shown failing for the right reason)
7. `## Write enough code to make it pass` (the simplest real code, shown green)
8. `## Refactor` (tidy with the tests as a safety net, then re-run them)
9. `## Repeat for new requirements` (introduce the next behaviour and walk the loop again from
   "Write the test first"; most chapters cycle a few times)
10. `## Wrapping up` (a short bullet list naming what was learned; end there, no "Next:" link.
    Honkit renders the prev/next navigation from `SUMMARY.md` automatically)

## Template B: an interview-pattern chapter

Use this for pattern chapters (Two Pointers, Sliding Window, DP, and so on). It opens with when to
reach for the pattern, walks the reusable `_template.py`, then solves two or three problems. Each
problem walks the full TDD cycle, so the cycle steps are `###` headings under each `## Problem`:

1. `# [Pattern name]`
2. `**[You can find all the code for this chapter here](https://github.com/USER/python-with-tests/tree/main/code/CHAPTER_FOLDER)**`
3. One or two sentences naming the pattern and what it buys you.
4. `## When to reach for [pattern]` (the signals that say "use this", two or three concrete bullets)
5. `## The template` (show and walk the skeleton from `CHAPTER_FOLDER/_template.py`, and name the
   invariant it maintains)
6. `## Problem 1: [name]`, with a one or two line problem statement as a blockquote, then the full
   cycle as sub-steps:
   - `### Write the test first`
   - `### Try to run the test`
   - `### Write the minimal amount of code for the test to run and check the failing test output`
   - `### Write enough code to make it pass`
   - `### Refactor` (or a sentence saying none is needed and why)
7. `## Problem 2: [name]` and optionally `## Problem 3: [name]`, each repeating the cycle. The later
   problems can move a little faster, but still show the test first, the failure, the passing code,
   and a refactor or a note that none is needed.
8. `## Wrapping up` (bullets naming the pattern, its invariant or trigger, and a common variant;
   end there, no "Next:" link. Honkit builds the prev/next navigation from `SUMMARY.md`)

## The rules that hold for both

- No em-dashes anywhere. See `.claude/skills/article-writer/references/banned-patterns.md`.
- Contractions throughout. Mix `we`, `you`, and `I`.
- Show the failing output before you explain it. Keep the minimal-code step honestly wrong.
- `uv` commands in prose: `uv run pytest`, `uv add`. Cloning and `uv sync` are contributor-only,
  the reader writes their own two files in a flat folder, no `vN/`, no `__init__.py`.
- Standard library only in solution code. Tests are `test_*.py`, and the prose shows **flat
  imports** (`from chapter import fn`), the shape the reader writes.

Run the validator before you call a chapter done:

```
uv run python .claude/skills/article-writer/scripts/validate_article.py <slug>.md
```
