---
name: article-writer
description: Write or revise a chapter for the "Learn Python with Tests" book in Chris James's Learn-Go-with-Tests voice. Use when authoring a new chapter, rewriting a stub, or fixing a chapter that reads as AI-generated. Enforces a strict house style (zero em-dashes, contractions, show-the-failing-test-then-explain) with a mechanical validator plus student and reviewer agents.
---

# Article Writer

Write chapters for **Learn Python with Tests** that read like a human wrote them, in the voice
of Chris James's *Learn Go with Tests*. The book teaches Python interview patterns test-first.
Every chapter walks the TDD loop with real, runnable, tested code.

This skill exists because AI-generated technical prose has a tell: em-dashes everywhere,
marketing adjectives, bullet-summary-itis, define-before-show, and a flat encouraging register
that no real author uses. The rules below kill those tells.

## The agent flow

Authoring one chapter is three agents plus a mechanical gate, orchestrated in a pipeline with one
bounded loop. The orchestrator (you, the main session) runs the steps; the agents do not talk to
each other.

```
                    ┌──────────────────────────────────────────────┐
                    │                  (fix loop, max 2)            │
                    ▼                                               │
  article-writer ──> validate_article.py ──> article-student  ┐    │
   writes chapter +   mechanical gate:        (does it teach   │    │
   code + tests,      em-dashes, links,        and flow?)      ├──> orchestrator
   self-validates     uv, structure.                           │    decides:
        ▲             MUST be 0 errors    ──> article-reviewer  ┘    ship / revise / rework
        │             before review.         (voice + accuracy,          │
        │                                      re-runs validator           │
        └────────────── revise/rework ◀──────── and the tests)  ───────────┘
                         with specific fixes
```

Ordering, precisely:

1. **Write** (`article-writer`). Produces the chapter markdown plus its runnable, tested code
   folder. Runs the validator itself and returns only when it is green and `uv run pytest`/`ruff`
   on its folder pass.
2. **Validate** (mechanical, deterministic, no model). The gate. Zero errors required before any
   review agent runs. Cheap, so it runs first and runs again after every fix.
   ```bash
   uv run python .claude/skills/article-writer/scripts/validate_article.py <chapter>.md
   ```
3. **Review** (`article-student` and `article-reviewer`, dispatched **in parallel**). They are two
   independent lenses and never see each other's output:
   - `article-student` reads as a learner: where does it stop making sense, where is a leap too
     big, does the failing-test output match the code, does the order help comprehension.
   - `article-reviewer` guards voice and accuracy: re-runs the validator and the tests, checks the
     prose against the voice profile, verifies every claim and worked example.
4. **Decide and loop** (orchestrator). Merge both reports. If the reviewer says ship, done. If it
   says revise or rework, hand the specific fixes back to the writer, who edits and re-validates.
   Bound the loop to two passes; anything still open after that is reported, not silently retried.

For a **batch**, run one `article-writer` per chapter (they touch disjoint files: only their own
`<slug>.md` and `<code_dir>/`), then validate and review each. The writers run concurrently; the
per-chapter validate/review/fix loop is independent per chapter.

## The voice, in one breath

Read `references/voice-and-format.md` for the full profile. The non-negotiables:

- **No em-dashes. None.** Not the em-dash character, not an en-dash, not ` -- ` as a dash. Use a comma, a colon,
  parentheses, or two sentences. This is the rule the reader cares about most, and the validator
  fails the build on it.
- **Contractions throughout.** `we'll`, `it's`, `don't`, `you'll`. Their absence reads as a robot.
- **Mix `we`, `you`, and `I`.** `we` for the shared journey through the code, `you` for direct
  instructions, `I` for a personal opinion or a confession. Do not pick one and stick to it.
- **Show, then name, then explain.** Put the new feature in working code first. Then name it.
  Then explain it in a sentence or two. Never define a concept before the reader has seen it.
- **Show failing output verbatim, before you explain it.** After "Try to run the test", paste the
  real `NameError` / `AssertionError`, then say what it means in one line.
- **Short paragraphs.** One to three sentences. Single-sentence paragraphs are good for emphasis.
- **Bold for takeaways and warnings only. Italics for a term being introduced.** Not for decoration.
- **State opinions flatly.** "This is slow and wrong." No hedging, no "you might want to consider".
- **One light joke per chapter, maximum.** State it, let it land, move on. Never announce it.
- **No marketing register.** No "powerful", "seamless", "robust", "unlock", "leverage", "simply".
- **`uv` for commands.** `uv run pytest`, `uv sync`, `uv add`. Never `python -m venv` or `pip install`.

## Chapter structure

Open with the title, then the bolded relative code link, then at most three sentences of setup:

```markdown
# Sliding Window

**[You can find all the code for this chapter here](sliding_window/)**

A sliding window is two pointers with a job: ...
```

Then walk the TDD loop, repeating it once per new requirement. Use these headings verbatim:

```
## Write the test first
## Try to run the test
## Write the minimal amount of code for the test to run and check the failing test output
## Write enough code to make it pass
## Refactor
```

Close with `## Wrapping up`: a short bullet list that *names* what was learned, and a one-line
link to the next chapter. The wrap-up names things, it does not re-teach them.

Pattern chapters add a "when to reach for it" section before the first problem and walk the
pattern's `_template.py`. See `two-pointers.md` and `sliding-window.md` for the exemplars.

## Code conventions (so the chapter's code actually runs)

Follow `CONTRIBUTING.md`. In short:

- Prose lives in `book/<chapter>.md`; code lives in `code/<chapter>/`. The code-link line points
  at `https://github.com/USER/learn-python-with-tests/tree/main/code/<folder>`.
- Standard library only in solution code. Python 3.9+; add `from __future__ import annotations`
  when using `list[int]` style hints.
- **Fundamentals chapters are flat:** `code/<chapter>/<chapter>.py` + `test_<chapter>.py`, no
  `__init__.py`, no `vN/` folders, **absolute imports** (`from chapter import fn`). This is the
  shape the reader mirrors, so the prose shows the same flat import.
- **Pattern chapters stay packages:** keep/extend the existing `_template.py`, add a `solutions/`
  subpackage with one `problem.py` + `test_problem.py` per worked problem, each `__init__.py`
  present and using package-relative imports (`from .problem import fn`). The **prose still shows
  flat imports** (`from problem import fn`), because the reader writes one problem flat.
- The prose never tells the reader to clone the repo or create `vN/` folders, that's the reader
  editing two files in place. Cloning is a contributor action (`CONTRIBUTING.md`).
- Never name a code folder after a stdlib module (`math`, `string`, `queue`). Use `math_problems`.
- Verify before declaring done: `uv run pytest code/<folder>/` is green and
  `uv run ruff check code/<folder>` is clean.

## Validation rules (what the validator enforces)

The validator (`scripts/validate_article.py`) fails on: any em-dash or en-dash, ` -- ` as a dash,
banned marketing phrases, an absolute-URL code link, and raw `venv`/`pip` commands. It warns on:
spaced-hyphen dashes, filler words (`simply`, `obviously`), missing contractions, a missing
code-link line, and a missing TDD structure. Fix every error and read every warning.

Run it on one file, several, or the whole book:

```bash
uv run python .claude/skills/article-writer/scripts/validate_article.py sliding-window.md
uv run python .claude/skills/article-writer/scripts/validate_article.py --all
```

## References

- `references/voice-and-format.md`, the full Chris James voice and format profile.
- `references/banned-patterns.md`, the AI-slop checklist with human rewrites.
