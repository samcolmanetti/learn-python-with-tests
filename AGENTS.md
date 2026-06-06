# AGENTS.md

Guidance for AI agents working on **Learn Python with Tests**. Human contributors should read
`CONTRIBUTING.md`; this file captures the conventions an agent needs to work here safely.

## Git workflow

- **All changes land on `main`.** This repo ships from `main` (the deploy build serves it). When you
  finish a unit of work, get it onto `main` and push it to GitHub: `git push origin main`.
- If you do work on a short-lived feature branch, fast-forward it into `main` when done
  (`git checkout main && git merge --ff-only <branch>`) and push `main`; don't leave finished work
  stranded on a side branch.
- Only commit/push when the work is green (see Verify below). Never push a red suite.
- Use clean conventional commit messages (`feat(...)`, `fix(...)`, `refactor(...)`). Do not add
  attribution footers.

## Repo layout

- `book/` — the reader-facing prose (one Markdown file per chapter). `book/SUMMARY.md` is the table
  of contents and the single source of truth for navigation.
- `code/` — the runnable, tested code for the chapters (`uv run pytest` discovers it here).
- `tools/honkit-plugin-pagetoc/` — the local Honkit plugin: the "On this page" sidebar (`pagetoc.*`)
  and the sticky top bar (`topbar.js`). Top-bar/layout *styling* lives in `book/styles/website.css`
  (loaded after the theme, so plain selectors win without `!important`).
- `docs/plans/` — plans. `docs/drafts/` — unshipped draft chapters (kept out of `book/` so the
  orphan-link guard stays green).

## Verify before you push

```bash
uv run pytest        # every chapter's test suite must pass
uv run ruff check    # lint must pass
npm run build        # Honkit build must succeed (honkit build book ../_book)
```

For site/chrome changes, also preview with `npm run serve` (http://localhost:4000) and check a
chapter page, since much of the behaviour is client-side.

## Ground rules (see CONTRIBUTING.md for the full list)

- Test-first: every behaviour starts as a failing `pytest` test.
- Standard library only inside chapter solutions.
- Python 3.9+; add `from __future__ import annotations` when using `list[int]`-style annotations.
- Keep `book/SUMMARY.md` honest: every linked chapter must exist, and every `book/*.md` chapter must
  be reachable from it (`code/tests/test_summary_links.py` enforces this).
