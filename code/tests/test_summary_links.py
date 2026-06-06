"""Guardrail tests for the book's navigation.

`SUMMARY.md` is the single source of truth for the table of contents. These tests keep it
honest:

1. Every chapter linked from `SUMMARY.md` must exist on disk (no dead links).
2. Every chapter markdown file at the repo root must be reachable from `SUMMARY.md`
   (no orphan pages a reader can never navigate to).

If you add a chapter, add it to `SUMMARY.md`. If you link a chapter, create the file.
"""

import re
from pathlib import Path

# The prose lives under book/; this test file lives at code/tests/, so the repo root is
# parents[2] and the book root is repo_root/book.
BOOK_ROOT = Path(__file__).resolve().parents[2] / "book"
SUMMARY = BOOK_ROOT / "SUMMARY.md"

# Markdown in book/ that is intentionally NOT a SUMMARY chapter.
NON_CHAPTER_MARKDOWN = {
    "gb-readme.md",   # the in-book readme, wired up via book.json (not listed as a chapter)
    "SUMMARY.md",     # the table of contents itself
}

# Markdown link to a local .md file, e.g. [Title](iteration.md)
LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")


def summary_linked_files():
    text = SUMMARY.read_text(encoding="utf-8")
    return [m.group(1) for m in LINK_RE.finditer(text)]


def test_summary_exists():
    assert SUMMARY.is_file(), "SUMMARY.md (the table of contents) must exist"


def test_every_summary_link_resolves():
    missing = []
    for rel in summary_linked_files():
        if not (BOOK_ROOT / rel).is_file():
            missing.append(rel)
    assert not missing, f"SUMMARY.md links to files that do not exist: {missing}"


def test_no_duplicate_summary_links():
    links = summary_linked_files()
    seen, dupes = set(), []
    for link in links:
        if link in seen:
            dupes.append(link)
        seen.add(link)
    assert not dupes, f"SUMMARY.md links to the same file more than once: {dupes}"


def test_no_orphan_book_chapters():
    linked = set(summary_linked_files())
    orphans = []
    for md in BOOK_ROOT.glob("*.md"):
        if md.name in NON_CHAPTER_MARKDOWN:
            continue
        if md.name not in linked:
            orphans.append(md.name)
    assert not orphans, (
        "These book/ chapters are not reachable from SUMMARY.md "
        f"(add them to the table of contents): {sorted(orphans)}"
    )
