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

## The pipeline

Authoring one chapter is three roles. Run them in order.

1. **Write** (the `article-writer` agent, or you directly). Produce the chapter markdown plus its
   code folder, following the voice guide and the TDD loop. All code must be runnable and tested.
2. **Validate** (mechanical). Run the validator. It must pass with zero errors before review:
   ```bash
   uv run python .claude/skills/article-writer/scripts/validate_article.py <chapter>.md
   ```
3. **Review** (two agents, in parallel):
   - `article-student` reads the chapter as a learner and reports where it stops making sense,
     where a leap is too big, or where the flow breaks.
   - `article-reviewer` checks voice, accuracy, and the rules the validator can't see (does the
     prose actually explain the concept? is the humor forced? does the failing-test output match
     the code?).

   Apply their feedback, re-validate, and only then consider the chapter done.

For a batch of chapters, run one `article-writer` agent per chapter (they touch disjoint files),
then validate and review each.

## The voice, in one breath

Read `references/voice-and-format.md` for the full profile. The non-negotiables:

- **No em-dashes. None.** Not `—`, not `–`, not ` -- ` as a dash. Use a comma, a colon,
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

- Standard library only in solution code. Python 3.9+; add `from __future__ import annotations`
  when using `list[int]` style hints.
- Tests are `test_*.py` with **package-relative imports** (`from .module import fn`); every
  folder has an `__init__.py`.
- Pattern chapters: keep/extend the existing `_template.py`, add a `solutions/` subpackage with
  one `problem.py` + `test_problem.py` per worked problem.
- Never name a code folder after a stdlib module (`math`, `string`, `queue`). Use `math_problems`.
- Verify before declaring done: `uv run pytest <folder>/` is green and
  `uv run ruff check <folder>` is clean.

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

- `references/voice-and-format.md` — the full Chris James voice and format profile.
- `references/banned-patterns.md` — the AI-slop checklist with human rewrites.
