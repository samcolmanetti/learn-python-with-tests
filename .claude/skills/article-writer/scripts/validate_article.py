#!/usr/bin/env python3
"""Validate a Learn-Python-with-Tests chapter against the house style.

Mechanical, fast, no dependencies. Catches the things humans miss and the things that
make prose read as AI-generated. Prose checks run only OUTSIDE fenced code blocks and
inline `code`, so CLI flags like `--fix` and dashes in code never trip a rule.

Usage:
    python3 validate_article.py path/to/chapter.md [more.md ...]
    python3 validate_article.py --all          # every root *.md chapter

Exit code 0 = clean, 1 = at least one ERROR. Warnings never fail the build.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Files that are not chapters and should not be style-checked.
NON_CHAPTERS = {"README.md", "SUMMARY.md", "CONTRIBUTING.md", "template.md"}

# AI-slop / marketing tells. Case-insensitive substring match in prose.
# Keep this list opinionated: every entry is a phrase Chris James's book never uses.
BANNED_PHRASES = [
    "let's dive in", "dive into", "in today's", "fast-paced", "ever-evolving",
    "seamless", "seamlessly", "robust solution", "powerful tool", "powerful feature",
    "leverage", "leveraging", "unlock", "unleash", "supercharge", "elevate",
    "game-changer", "game changer", "delve", "treasure trove", "in the world of",
    "when it comes to", "it's worth noting", "it is worth noting", "needless to say",
    "in conclusion", "to sum up", "by the end of this chapter, you will",
    "by the end of this chapter you will", "in this chapter, we will explore",
    "effortless", "cutting-edge", "best-in-class", "first and foremost",
    "rest assured", "look no further", "the beauty of", "magic happens",
    "boilerplate aside", "without further ado", "buckle up",
]

# Words that are usually filler or condescending. Warnings, not errors.
WEAK_WORDS = ["simply", "obviously", "just simply", "of course,", "basically,", "essentially,"]

CODE_LINK_RE = re.compile(r"\*\*\[You can find all the code for this chapter here\]\(([^)]+)\)\*\*")
FENCE_RE = re.compile(r"^(```|~~~)")


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so prose checks ignore code."""
    out_lines = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # drop inline `code`
        out_lines.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out_lines)


def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    raw = path.read_text(encoding="utf-8")
    prose = strip_code(raw)
    prose_lower = prose.lower()

    # --- HARD RULES (errors) ---------------------------------------------------------

    # 1. No em-dashes or en-dashes. The single most important rule.
    for i, line in enumerate(prose.splitlines(), 1):
        if "—" in line:
            errors.append(f"L{i}: em-dash (—) found. Use a comma, colon, parentheses, or a new sentence.")
        if "–" in line:
            errors.append(f"L{i}: en-dash (–) found. Use a hyphen or the word 'to' for ranges.")
        # spaced double-hyphen used as a dash
        if re.search(r"\s--\s", line):
            errors.append(f"L{i}: ' -- ' used as a dash. Rewrite without a dash.")
        # spaced single hyphen used as a dash (e.g. "the result - which is wrong")
        if re.search(r"\S\s-\s\S", line):
            warnings.append(f"L{i}: ' - ' reads like a dash. Prefer a comma, colon, or parentheses.")

    # 2. AI-slop / marketing phrases.
    for phrase in BANNED_PHRASES:
        if phrase in prose_lower:
            errors.append(f"banned phrase: '{phrase}'. Cut it or say the concrete thing instead.")

    # 3. Code-link line must exist and be a RELATIVE path (not an absolute URL).
    m = CODE_LINK_RE.search(raw)
    if not m:
        warnings.append(
            "no code-link line found. Chapters with a code folder should open with "
            "**[You can find all the code for this chapter here](folder/)**."
        )
    elif m.group(1).startswith("http"):
        errors.append(
            f"code-link points to an absolute URL ({m.group(1)}). Use a relative path like (two_pointers/)."
        )

    # 4. Tooling commands must use uv, not raw venv/pip.
    if re.search(r"python3?\s+-m\s+venv", prose) or re.search(r"\bpip\s+install\b", prose):
        errors.append("raw venv/pip command in prose. Use uv: `uv sync`, `uv run pytest`, `uv add`.")
    if re.search(r"(?<!uv run )\bpytest\b", prose) and "uv run pytest" not in prose and "`pytest`" not in raw:
        warnings.append("bare 'pytest' in prose. Prefer `uv run pytest` (or note it once, then shorthand).")

    # --- SOFT RULES (warnings) -------------------------------------------------------

    for w in WEAK_WORDS:
        if w in prose_lower:
            warnings.append(f"weak/filler word: '{w.strip()}'. The book avoids it.")

    # Contractions are a human tell. Flag their total absence in a non-trivial chapter.
    if len(prose.split()) > 250:
        if not re.search(r"\b\w+'(s|t|ll|re|ve|d|m)\b", prose):
            warnings.append("no contractions found. The book uses them throughout (we'll, it's, don't).")

    # TDD chapters should walk the loop. Heuristic: a code folder link but no 'test first'.
    if m and "write the test first" not in prose_lower and "wrapping up" not in prose_lower:
        warnings.append("no 'Write the test first' or 'Wrapping up' heading. Most chapters walk the TDD loop.")

    return errors, warnings


def iter_targets(args: list[str]) -> list[Path]:
    if args == ["--all"]:
        root = Path(__file__).resolve().parents[4]  # repo root from .claude/skills/article-writer/scripts/
        return sorted(p for p in root.glob("*.md") if p.name not in NON_CHAPTERS)
    return [Path(a) for a in args]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    total_errors = 0
    for path in iter_targets(argv):
        if not path.is_file():
            print(f"SKIP {path} (not found)")
            continue
        errors, warnings = check(path)
        if not errors and not warnings:
            print(f"OK   {path.name}")
            continue
        status = "FAIL" if errors else "WARN"
        print(f"{status} {path.name}")
        for e in errors:
            print(f"  ERROR  {e}")
        for w in warnings:
            print(f"  warn   {w}")
        total_errors += len(errors)
    print()
    print(f"{'FAILED' if total_errors else 'passed'}: {total_errors} error(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
