---
title: "refactor: Separate reader workflow from authoring scaffolding and clean up repo structure"
type: refactor
status: active
date: 2026-06-05
---

# refactor: Separate reader workflow from authoring scaffolding and clean up repo structure

## Overview

"Learn Python with Tests" currently leaks its authoring and CI scaffolding onto the reader. The
install page tells readers to clone the repo and `uv sync` to get a green baseline; several
chapters tell readers to create `vN/` version folders and mirror the repo's package layout; every
test in the repo uses package-relative imports (`from .hello_pytest import hello`) backed by 174
`__init__.py` files. The repo root mixes ~62 prose markdown files, ~50 chapter code folders, five
deployment config files, and gitignored screenshots in one flat directory.

This refactor draws a clean line between **what the reader does** and **what the repo does for CI**:

- The reader writes their own code in a single, flat practice directory, one pair of files per
  chapter (`hello_pytest.py` + `test_hello_pytest.py`), absolute imports, no `__init__.py`, no
  `vN/` folders, editing in place. Cloning the repo is for contributors only.
- The repo keeps one folder per chapter (so 50 chapters don't pile into one directory) but adopts
  the **same** absolute-import, no-`__init__.py` style the book teaches, so the reference code looks
  exactly like what a reader would write.
- Prose, chapter code, and deployment config get separated into `book/`, `code/`, and the repo root
  respectively, while keeping the Honkit site build and pytest discovery green.

## Problem Frame

The book is modeled on Chris James's "Learn Go with Tests," where the reader writes code alongside
the prose and the repo is reference, not a starting point. The current book inverts this in three
places (install flow, `vN` folder instructions, package-relative imports) and presents a confusing
root directory. A learner reading chapter one is told to create `hello_pytest/v1/hello_pytest.py`,
which implies they must reproduce the maintainer's CI folder layout. They should instead create one
`hello_pytest.py`, write a failing test, and edit it in place.

User-stated requirements (verbatim intent):
1. Two cheap fixes applied to **every** page: stop telling readers to clone to get started; stop
   telling readers to mirror the `vN/` layout.
2. Reader-facing imports look like `from hello_pytest import hello` (flat, absolute, no dotted
   package path).
3. A specific failing-test error block is used in the hello-pytest chapter (see R3 below).
4. The hosted site URL is `learnpython.scol.xyz`.
5. The GitHub README links to the hosted book in a Quick Start / Getting Started section; clone
   instructions are for contributors only.
6. The root directory is cleaned up so prose, code, and deployment config are separated, without
   breaking the Honkit build or pytest discovery.
7. The reader's folder structure is standardized and lightweight: no required `__init__.py`, either
   a flat single directory or a lightweight per-chapter folder. The repo's CI needs are reconciled
   with this simpler reader model.
8. The book's front page (`gb-readme.md`) is cleaned up: the bottom blockquote referencing the
   internal `SUMMARY.md` is removed (it is authoring detail, not reader-facing), and the
   "Clone the repo, run `uv run pytest`" line is replaced with reader-appropriate guidance.
9. A persistent "home" button/link appears at the top of every page on the hosted site, taking the
   reader back to the landing page (the same convenience Learn Go with Tests offers).

## Requirements Trace

- R1. Every chapter page stops instructing readers to clone the repo as a starting point.
- R2. Every chapter page stops instructing readers to create or mirror `vN/` version folders;
  the narrative is "edit your one file in place."
- R3. Reader-facing imports use the flat absolute form `from hello_pytest import hello`. The
  hello-pytest chapter uses exactly this import and this failing-test output:
  ```
      def test_hello_pytest():
  >       assert hello() == "hello"
  E       AssertionError: assert '' == 'hello'
  E
  E         - hello
  ```
- R4. The hosted URL `learnpython.scol.xyz` is used wherever the book references its live site.
- R5. `README.md` has a Quick Start / Getting Started section linking to the hosted book; clone /
  contributor setup lives in `CONTRIBUTING.md` (and a clearly-labeled "Contributing" area of the
  README), not presented as the reader's path.
- R6. Root is reorganized: prose in `book/`, chapter code in `code/`, deployment config at root;
  Honkit build and `uv run pytest` both stay green.
- R8. `book/gb-readme.md` drops the `SUMMARY.md` blockquote and the clone-to-read line; the front
  page reads cleanly for someone landing on the hosted site.
- R9. Every page on the hosted site shows a home link/button at the top that returns to the landing
  page, mirroring Learn Go with Tests.
- R7. Standardized reader structure: flat practice directory, one `<chapter>.py` + `test_<chapter>.py`
  pair per chapter, no `__init__.py`, no `vN/`. The repo adopts the same absolute-import,
  no-`__init__.py` style (per-chapter folders) so reference code matches what readers write.

## Scope Boundaries

- Not rewriting chapter pedagogy or adding new chapters. Prose edits are limited to the structural
  fixes above plus the mechanical import/path/URL updates each fix requires.
- Not changing the solution algorithms or test assertions, except where collapsing `vN` folders
  means keeping the final version and where converting relative-to-absolute imports requires editing
  import lines.
- Not introducing `--import-mode=importlib`. Default `prepend` mode is retained because it is what
  makes the reader's flat `from hello_pytest import hello` resolve with zero configuration; the repo
  is made compatible with it by guaranteeing globally-unique module/test basenames instead.
- Not moving deployment config into a subdirectory. `Dockerfile`, `netlify.toml`, `railpack.json`,
  `docker/`, `tools/`, `package.json` stay at root (deploy platforms expect them there); only their
  build commands change to target `book/`.
- The gitignored `site-*.png` screenshots are not tracked and are out of scope (left as local
  artifacts).

### Deferred to Separate Tasks

- A future pass could offer readers an optional per-chapter-folder layout in addition to the flat
  directory; this plan standardizes on the flat directory as the taught default and only mentions
  the folder option briefly.

## Context & Research

### Relevant Code and Patterns

- `pyproject.toml` — pytest config: `python_files`, `norecursedirs`, `addopts = "-ra"`, ruff
  `extend-exclude = ["references", "_book"]`. No `import-mode`, `pythonpath`, or `testpaths` set
  today (default `prepend` mode, rootdir-based collection from repo root).
- `book.json` — `structure.readme: gb-readme.md`, `styles.website: styles/website.css`, plugins
  `code` + `pagetoc` (the latter is `file:tools/honkit-plugin-pagetoc`).
- `SUMMARY.md` — table of contents; entries are root-relative markdown paths (e.g.
  `install-python.md`). Moving all prose into `book/` keeps these relative links valid as long as
  the build root is `book/`.
- Build commands all use `honkit build . _book` and live in: `package.json` (`build` script),
  `netlify.toml` (`command`), `railpack.json` (build step), `Dockerfile` (`RUN npx honkit build . _book`).
- Current import convention (to be changed): `hello_pytest/v1/test_hello_pytest.py` does
  `from .hello_pytest import hello`; `two_pointers/solutions/test_two_sum_sorted.py` does
  `from .two_sum_sorted import two_sum`. Both rely on `__init__.py` packages + relative imports.
- `test_organization/conftest.py` uses `from .cart import ShoppingCart` (package-relative); it is
  the one chapter whose conftest fixture demo depends on the package form. Convert to
  `from cart import ShoppingCart` (resolves via prepend mode with no `__init__.py`).
- Chapters using `vN/` code folders: `hello_pytest`, `iteration`, `lists_and_slicing`,
  `number_basics`, `property_based_testing`. Prose referencing `vN`: `hello-pytest.md`,
  `iteration.md`, `lists-and-slicing.md`, `numbers.md` (verify `property-based-testing.md` during work).
- The code-link line at the top of each chapter points to
  `https://github.com/samcolmanetti/learn-python-with-tests/tree/main/<folder>`; after the move these
  become `.../tree/main/code/<folder>`.
- `.claude/skills/article-writer/SKILL.md` lines 114-122 encode the OLD conventions: "package-relative
  imports (`from .module import fn`); every folder has an `__init__.py`"; "never name a code folder
  after a stdlib module"; verify with `uv run pytest <folder>/`.
- `.claude/skills/article-writer/scripts/validate_article.py` enforces the code-link GitHub tree URL
  (lines 89-109) and the full TDD loop (line 129+), and computes repo root from the script path
  (line 148: `parents[4]`).
- `template.md` is a chapter scaffold that also carries the conventions.

### Collision Analysis (decisive for R7)

- Duplicate test basenames today: `test_hello_pytest.py`, `test_iteration.py`,
  `test_lists_and_slicing.py`, `test_number_basics.py`, `test_roman.py` are duplicated **only inside
  `vN/` folders** (collapsing `vN` removes them); `test_template.py` is duplicated across **11
  chapters** (`graphs_traversal`, `linked_lists`, `union_find`, `dijkstra`, `trees_bfs`, `dp_1d`,
  `bit_manipulation`, `dp_knapsack`, `dp_grid`, `trees_dfs`, `backtracking`).
- In default `prepend` mode with no `__init__.py`, duplicate basenames across directories raise an
  import-file-mismatch error and duplicate **module** names collide via `sys.modules` caching. So the
  repo can drop `__init__.py` only if module + test basenames are globally unique.
- No chapter module shadows a stdlib name (`numbers`, `string`, `math`, etc.) — verified.
- Therefore the only real work to make the repo collision-free under prepend mode is the
  `_template.py` / `test_template.py` scaffolding. Resolve by excluding the template scaffold from
  collection (preferred: it is a copy-me starter, not a real test) or renaming per chapter.

### Institutional Learnings

- `docs/plans/2026-06-04-001-feat-python-with-tests-plan.md` is the original build plan; consult for
  any conventions it established before overriding them here.

### External References

- Honkit accepts an explicit book root as the first build argument (`honkit build <root> <out>`),
  so prose can live in `book/` while config stays buildable.
- pytest `prepend` import mode inserts the first non-package parent directory of a test file onto
  `sys.path[0]`, which is exactly why a reader's flat `from hello_pytest import hello` resolves with
  no configuration when `hello_pytest.py` sits next to `test_hello_pytest.py`.

## Key Technical Decisions

- **Reader structure = one flat practice directory.** Taught default: the reader makes a directory
  they own, and per chapter adds `<chapter>.py` + `test_<chapter>.py` as siblings. Absolute imports,
  no `__init__.py`, no `vN/`, edit in place, run `pytest` from that directory. Rationale: smallest
  possible mental model; `from hello_pytest import hello` resolves with zero config in prepend mode;
  names never collide because there is one file per chapter.
- **Repo flattens fundamentals only; pattern chapters stay packages.** (Decided during execution
  after discovering `_template.py` is shared pattern code imported by `solutions/` across ~49
  chapters, one directory up from its importers.) The single-file fundamentals chapters readers
  literally mirror (`hello_pytest`, `numbers`, `strings`, ...) drop their `__init__.py` and use
  absolute imports (`from hello_pytest import hello`), matching the book exactly. The multi-file
  pattern/applied chapters (`_template.py` + `solutions/`, and the `test_organization` conftest
  package) keep `__init__.py` and package-relative imports internally, because flattening them would
  require renaming 49 templates, moving files, and rewiring hundreds of imports for no reader-facing
  benefit. **The book prose shows flat absolute imports for both shapes** (that is the reader fix);
  only pattern-chapter reference files retain a leading-dot import the reader never types.
- **Stay on default `prepend` import mode; enforce unique basenames.** Rationale: `importlib` mode
  would break the reader's zero-config sibling import; uniqueness is cheap (only the template scaffold
  collides) and keeps reader and repo on one mode.
- **Directory split: `book/` (prose + site config) and `code/` (chapter code); deploy config stays at
  root.** Rationale: separates the three concerns the user called out while minimizing breakage to
  deploy platforms that expect root-level config.
- **Collapse `vN/` folders to a single final solution + test per chapter.** Rationale: matches Learn
  Go with Tests (repo holds final code; prose shows the progression); directly answers "why a folder
  per lesson just for two files" and "v1 isn't a requirement."
- **Clone is a contributor action.** README leads with the hosted book; `CONTRIBUTING.md` owns the
  clone + `uv sync` flow.

## Open Questions

### Resolved During Planning

- How do reader and repo imports stay identical? Both use absolute imports + prepend mode + no
  `__init__.py`; the repo guarantees unique basenames to make that safe across 50 chapters.
- Where does deployment config go? Stays at root; only build commands change to target `book/`.
- What happens to intermediate `vN` code under CI? It is dropped; only the final per-chapter solution
  is tested, and the prose shows earlier steps as illustrative fenced blocks (same as LGWT).

### Deferred to Implementation

- Exact handling of `test_template.py` collisions (exclude from collection via a `collect_ignore` /
  `norecursedirs`-style rule, or rename per chapter) — decide once the suite is running under the new
  mode and the real error surface is visible.
- Whether any non-template module names collide across chapters surfaces only when the full suite runs
  under prepend mode without packages; fix names as the import errors reveal them.
- Whether `property-based-testing.md` prose needs `vN` edits (its code has `vN` but the prose grep did
  not flag it) — confirm by reading during Unit 3/6.

## Output Structure

    python-with-tests/
    ├── README.md                  # GitHub landing: Quick Start -> hosted book; Contributing -> clone
    ├── CONTRIBUTING.md            # contributor clone + uv sync + authoring conventions
    ├── pyproject.toml             # pytest/ruff config; testpaths=["code"]
    ├── package.json / lock        # honkit toolchain; build targets book/
    ├── Dockerfile                 # build targets book/
    ├── netlify.toml               # build targets book/
    ├── railpack.json              # build targets book/
    ├── docker/                    # nginx.conf (unchanged)
    ├── tools/                     # honkit-plugin-pagetoc (unchanged)
    ├── docs/                      # plans, etc.
    ├── book/                      # ALL prose + site config
    │   ├── book.json
    │   ├── SUMMARY.md
    │   ├── gb-readme.md
    │   ├── install-python.md
    │   ├── hello-pytest.md
    │   ├── ... (all chapter .md)
    │   └── styles/website.css
    └── code/                      # ALL chapter code, no __init__.py, absolute imports
        ├── hello_pytest/
        │   ├── hello_pytest.py
        │   └── test_hello_pytest.py
        ├── two_pointers/
        │   └── solutions/...
        └── ...

## Implementation Units

- [x] **Unit 1: Convert the repo to absolute imports with no `__init__.py` (prepend-safe)**

**Goal:** Make the whole test suite pass under default prepend mode using absolute imports and zero
`__init__.py`, so the repo's code matches the import style the book will teach. Done first because
every later unit depends on the new import model being green.

**Requirements:** R7 (and the foundation for R2/R3).

**Dependencies:** None.

**Files:**
- Modify: every `test_*.py` in chapter folders — change `from .module import fn` to
  `from module import fn`.
- Modify: any solution module doing intra-chapter relative imports — change to absolute.
- Modify: `test_organization/conftest.py` — `from .cart import ShoppingCart` ->
  `from cart import ShoppingCart`.
- Delete: all 174 `__init__.py` under chapter folders (not under `.venv`/`references`/`_book`).
- Modify: `pyproject.toml` — exclude the template scaffold from collection (e.g. ignore
  `test_template.py` / `_template.py`) so the 11 duplicates don't break prepend mode; keep `addopts`.
- Test: the existing suite is the test — it must stay green.

**Approach:**
- Mechanical relative-to-absolute import rewrite across all test and solution files.
- Resolve the `test_template.py` collision by excluding the copy-me template scaffold from collection
  (it is a starter, not a real test); if any genuine cross-chapter module-name collision surfaces,
  rename the offending module to a chapter-qualified name.
- Run the full suite; iterate on any residual `sys.modules` collisions revealed by prepend mode.

**Execution note:** Characterization-first — capture the current `uv run pytest` pass count as the
baseline before edits, and treat "same tests green, zero new failures" as the bar.

**Patterns to follow:** existing assertions stay byte-for-byte identical; only import lines and
`__init__.py` presence change.

**Test scenarios:**
- Happy path: `uv run pytest` collects and passes the same number of tests as the pre-change baseline.
- Edge case: the `test_organization` conftest fixtures (`cart`, `stocked_cart`) still resolve and
  that chapter's tests pass with the absolute `from cart import ...` import.
- Edge case: the 11 template scaffolds no longer cause import-file-mismatch errors (excluded or
  uniquely named).
- Error path: confirm no module shadows a stdlib name now that bare module names are importable
  (suite import phase surfaces this).

**Verification:** `uv run pytest` is green with the baseline test count; `uv run ruff check` is clean;
no `__init__.py` remain under chapter folders; no test uses a leading-dot import.

- [x] **Unit 2: Split the repo into `book/` and `code/`, keep site + suite green**

**Goal:** Move all prose + site config into `book/` and all chapter code into `code/`, update every
build and test command, and confirm both the Honkit build and pytest still work.

**Requirements:** R6.

**Dependencies:** Unit 1 (import model must be green before code moves, so failures are unambiguous).

**Files:**
- Move into `book/`: all chapter `*.md`, `SUMMARY.md`, `book.json`, `gb-readme.md`, `styles/`.
- Move into `code/`: all chapter code folders (`hello_pytest/`, `two_pointers/`, `tests/`,
  `test_organization/`, etc.).
- Modify: `package.json` (`build`: `honkit build book _book`; `serve`: `honkit serve book`).
- Modify: `netlify.toml` (`command = "npm install && npx honkit build book _book"`).
- Modify: `railpack.json` (build command -> `npx honkit build book _book`).
- Modify: `Dockerfile` (`RUN npx honkit build book _book`).
- Modify: `pyproject.toml` (`testpaths = ["code"]`; update `norecursedirs` and ruff
  `extend-exclude` to reference `book`, `_book`, `references`).
- Verify: `book/book.json` `styles.website: styles/website.css` resolves (styles moved alongside),
  and `structure.readme: gb-readme.md` resolves inside `book/`.

**Approach:**
- Keep `SUMMARY.md` entries root-relative (they already are); since the build root becomes `book/`,
  inter-chapter links and the TOC stay valid without rewriting paths.
- Leave deploy config, `docker/`, `tools/`, `docs/`, `README.md`, `CONTRIBUTING.md`, `pyproject.toml`,
  `package.json` at the repo root.
- Run `npx honkit build book _book` and `uv run pytest` to confirm both roots build cleanly.

**Test scenarios:**
- Happy path: `npx honkit build book _book` produces `_book/` with the same pages as before
  (spot-check `install-python.html`, `hello-pytest.html`, the TOC, and CSS load).
- Happy path: `uv run pytest` (now rooted at `code/`) passes the same baseline count.
- Edge case: the `pagetoc` and `code` honkit plugins still load (build emits no plugin-missing
  warnings).
- Integration: an inter-chapter markdown link (e.g. install -> hello-pytest) still resolves in the
  built site.

**Verification:** site builds from `book/`; suite green from `code/`; ruff clean; no path in build
config still references `honkit build . _book`.

- [x] **Unit 3: Collapse `vN/` folders to one final solution + test per chapter**

**Goal:** Remove the `vN/` version folders from chapter code, keeping each chapter's final solution +
test, so the repo has one folder of two-ish files per chapter.

**Requirements:** R2, R7.

**Dependencies:** Unit 1, Unit 2.

**Files:**
- Modify under `code/`: `hello_pytest/`, `iteration/`, `lists_and_slicing/`, `number_basics/`,
  `property_based_testing/` — replace each `vN/` tree with the final-version files directly in the
  chapter folder (`code/hello_pytest/hello_pytest.py` + `code/hello_pytest/test_hello_pytest.py`).
- Delete: the `vN/` subfolders and their now-duplicated test files.

**Approach:**
- For each chapter, identify the final version (highest `vN`), promote its solution + test up to the
  chapter folder, and delete the rest. Preserve the final assertions exactly.
- Confirm no remaining duplicate test basenames after promotion.

**Test scenarios:**
- Happy path: each collapsed chapter's final test passes from its new flat location.
- Edge case: `property_based_testing` (Hypothesis-based `test_roman`) still passes after promotion.
- Edge case: no `vN/` directory remains anywhere under `code/`.

**Verification:** `uv run pytest` green at baseline-minus-removed-duplicate-versions count (document
the new expected count); no `vN/` folders remain; each affected chapter has a single solution + test.

- [x] **Unit 4: Rewrite `book/install-python.md` for the no-clone, flat-practice-dir reader model**

**Goal:** Replace the "clone + `uv sync` for a green baseline" framing with "set up your own flat
practice directory," and teach the reader structure (R7) and import style (R3).

**Requirements:** R1, R3, R4, R7.

**Dependencies:** Units 1-3 (so the taught structure matches the repo reality).

**Files:**
- Modify: `book/install-python.md`.

**Approach:**
- Install Python; install `uv`; create your own practice directory; `uv init` + `uv add --dev pytest
  hypothesis ruff` (records deps; reader never hand-writes `pyproject.toml`); go to chapter one.
- Show the flat layout: one `<chapter>.py` + `test_<chapter>.py` pair per chapter, no `__init__.py`,
  no `vN/`, run `pytest` from the directory.
- Reference the hosted site `learnpython.scol.xyz` where the page mentions reading the book online.
- Move any "clone this repo" content out (point contributors to `CONTRIBUTING.md`).
- Keep house style: no em-dashes, contractions, show-the-failing-test-then-explain.

**Test scenarios:** Test expectation: none — prose page. Validation is the article-writer validator
plus a manual read for the no-clone, flat-structure, absolute-import guarantees.

**Verification:** page no longer instructs cloning as the start path; shows the flat practice-dir
layout and `from hello_pytest import hello`; references `learnpython.scol.xyz`; validator passes.

- [x] **Unit 5: README Quick Start to hosted book; clone moves to CONTRIBUTING**

**Goal:** Make the GitHub landing lead readers to the hosted book and confine clone/`uv sync` to a
contributor section; clean up the book's front page (`gb-readme.md`).

**Requirements:** R4, R5, R8.

**Dependencies:** Unit 2 (paths), Unit 4 (consistent reader story).

**Files:**
- Modify: `README.md` (rework `## Quickstart` into a reader-facing "Getting Started" that links to
  `https://learnpython.scol.xyz`; keep a short "Contributing" pointer).
- Modify/Create: `CONTRIBUTING.md` (own the clone + `uv sync` + authoring conventions; reflect the new
  `book/` + `code/` layout and absolute-import/no-`__init__.py` rules).
- Modify: `book/gb-readme.md` if it duplicates the start-here framing (align with hosted-book-first).

**Approach:**
- README: badges, one-paragraph pitch, "Read it online at learnpython.scol.xyz," link into the first
  chapter, then a brief "Want to contribute? See CONTRIBUTING.md."
- CONTRIBUTING: clone, `uv sync`, `uv run pytest`, `npx honkit build book _book`, and the conventions
  (absolute imports, no `__init__.py`, one folder per chapter under `code/`, no `vN`).
- `book/gb-readme.md`: in "How to read it," replace "Clone the repo, run `uv run pytest`, and change
  things" with reader guidance (read online, or follow along in your own practice directory); delete
  the closing blockquote that references `SUMMARY.md` (it leaks authoring/scaffolding detail and the
  "coming soon"/"Contributions welcome" note belongs in CONTRIBUTING). Keep the sidebar as the
  roadmap without naming the internal file.

**Test scenarios:** Test expectation: none — docs. Manual check that no reader-facing section presents
cloning as the path to start learning.

**Verification:** README Getting Started links to `learnpython.scol.xyz`; clone/`uv sync` appears only
under contributor-facing docs; CONTRIBUTING describes the new structure accurately.

- [x] **Unit 6: Sweep every chapter page for the two cheap fixes, imports, URLs, and code links**

**Goal:** Apply R1 and R2 to all ~60 chapter pages, update code-link URLs for the `code/` move, switch
any shown imports to the flat absolute form, and fix hello-pytest specifically with the required import
and error block (R3).

**Requirements:** R1, R2, R3, R4.

**Dependencies:** Units 1-5.

**Files:**
- Modify: all `book/*.md` chapter pages.
- Specifically: `book/hello-pytest.md`, `book/iteration.md`, `book/lists-and-slicing.md`,
  `book/numbers.md`, `book/property-based-testing.md` (the `vN`-referencing pages) get narrative
  rewrites from "create `vN/...`" to "create `<chapter>.py`, then change it."
- Code-link lines: `.../tree/main/<folder>` -> `.../tree/main/code/<folder>` on every chapter.

**Approach:**
- Grep-and-review each page for: `clone`, `uv sync`, `/v1/`, `/v2/`, `/v3/`, leading-dot imports,
  `tree/main/<folder>` links, and any mention of the live site.
- For `hello-pytest.md`, use exactly:
  ```python
  from hello_pytest import hello

  def test_hello_pytest():
      assert hello() == "hello"
  ```
  and the failing output:
  ```
      def test_hello_pytest():
  >       assert hello() == "hello"
  E       AssertionError: assert '' == 'hello'
  E
  E         - hello
  ```
  then narrate editing the one file through the TDD loop (no `vN/`).
- Preserve house style throughout; keep each page's existing teaching intact apart from the
  structural fixes.

**Test scenarios:**
- Integration: the code-link URL on a sampled chapter resolves to the new `code/<folder>` path on the
  GitHub layout.
- Edge case: no chapter page still contains `/v1/`, `/v2/`, `/v3/`, a leading-dot import, or a
  "clone to start" instruction (grep returns nothing).
- Happy path: the article-writer validator passes on each modified page.

**Verification:** repo-wide grep for `from \.`, `/v1/`, `git clone` in `book/*.md` returns nothing
reader-facing; hello-pytest shows the required import + error block; validator green on all pages.

- [x] **Unit 7: Update authoring guardrails (article-writer skill, template, validator)**

**Goal:** Make the authoring tooling teach the new conventions so future chapters follow them instead
of regenerating the old `__init__.py`/relative-import/`vN` structure.

**Requirements:** R2, R5, R7 (durability).

**Dependencies:** Units 1-6.

**Files:**
- Modify: `.claude/skills/article-writer/SKILL.md` (lines ~114-122): absolute imports
  (`from module import fn`), no `__init__.py`, one folder per chapter under `code/`, no `vN`
  requirement, clone-is-contributor-only.
- Modify: `.claude/skills/article-writer/scripts/validate_article.py`: code-link URL now expects
  `tree/main/code/<folder>`; recompute repo-root/path assumptions for the `book/` + `code/` split
  (the `parents[4]` root derivation and any folder-existence checks); keep the full-TDD-loop check.
- Modify: `template.md` (move to `book/` if it is prose, or keep as a code scaffold under `code/`):
  reflect absolute imports and no `__init__.py`.

**Approach:**
- Rewrite the conventions block to match Units 1-6.
- Update validator path logic and the expected GitHub tree URL; run it against a couple of finished
  chapters to confirm it passes on the new structure and fails on the old.

**Test scenarios:**
- Happy path: `validate_article.py` passes on a representative migrated chapter (e.g. hello-pytest).
- Error path: the validator flags a deliberately old-style page (leading-dot import or
  `tree/main/<folder>` link) as failing.
- Edge case: the validator's repo-root derivation still resolves correctly from
  `.claude/skills/article-writer/scripts/` under the new layout.

**Verification:** SKILL.md and template describe the new model; validator passes on migrated chapters
and rejects old-style ones; running the article-writer pipeline on a chapter produces the new layout.

- [x] **Unit 8: Add a persistent home button to the hosted site**

**Goal:** Put a small "home" link/button at the top of every page on the built site that returns the
reader to the landing page, matching the convenience Learn Go with Tests offers.

**Requirements:** R9.

**Dependencies:** Unit 2 (build now targets `book/`).

**Files:**
- Modify: `tools/honkit-plugin-pagetoc/index.js` and `tools/honkit-plugin-pagetoc/website/pagetoc.js`
  (inject a home link into each page), OR add a sibling website JS asset registered by the plugin.
- Modify: `book/styles/website.css` (style the home button).
- Modify: `book/book.json` only if a new asset needs registering.

**Approach:**
- Honkit's default theme already links the book title (top-left of the sidebar) to the index, but the
  ask is a clearer in-content home affordance. Inject a single anchor (e.g. "Learn Python with Tests"
  or a small home glyph) at the top of `.book .page-inner`, pointing at the site root (the generated
  `index.html`, reachable via a root-relative or computed-relative href), reusing the local-plugin JS
  injection mechanism the pagetoc plugin already uses.
- Style it unobtrusively via `website.css` so it reads as navigation, not page content.
- The href must resolve from any depth of the built site; prefer the gitbook/honkit "home" page
  variable or a computed relative path over a hardcoded absolute path.

**Execution note:** Verify visually with a real `honkit build book _book` and a browser check, since
this is site chrome that unit checks won't fully prove.

**Test scenarios:**
- Happy path: after build, the landing page and a deep chapter page both render a home link at the top
  of the content area, and clicking it lands on the index.
- Edge case: the home href resolves correctly from a nested page (not a 404), proving relative-path
  handling.
- Edge case: the link does not duplicate or overlap the pagetoc "on this page" widget.

**Verification:** `honkit build book _book` succeeds; a sampled chapter page shows a working home
button that returns to the landing page; no regression to the pagetoc widget or code-line styling.

## System-Wide Impact

- **Interaction graph:** Honkit build (`book/`) and pytest discovery (`code/`) are the two consumers
  of the directory layout; both build/test config files and the article-writer validator hard-code
  paths and must move in lockstep with Units 2 and 7.
- **Error propagation:** Converting to prepend mode without `__init__.py` turns previously-isolated
  package imports into a shared flat namespace; collisions surface as import errors at collection
  time (Unit 1 is where they must be resolved).
- **State lifecycle risks:** Collapsing `vN` permanently drops intermediate tested snapshots; the
  prose becomes the only record of earlier steps, so Unit 6's narrative edits must preserve the
  pedagogical progression that the `vN` folders used to guarantee.
- **API surface parity:** The reader-facing import style, the repo's import style, and the
  article-writer conventions must all agree (`from module import fn`, no `__init__.py`); a drift in
  any one re-introduces the confusion this refactor removes.
- **Integration coverage:** Only a real `honkit build book _book` and a full `uv run pytest` prove the
  move worked; unit-level checks alone won't catch a broken plugin path or a residual relative import.
- **Unchanged invariants:** Test assertions, solution algorithms, chapter teaching content, and the
  deploy platforms' root-level config locations are unchanged; only structure, imports, install/README
  framing, and the four `vN` narratives change.

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Dropping `__init__.py` breaks prepend-mode imports via duplicate module/test basenames | Unit 1 enforces global uniqueness (exclude/rename the template scaffold) and runs the full suite before any directory move |
| Moving prose into `book/` breaks the Honkit build (plugin paths, readme/styles resolution) | Unit 2 verifies a full `honkit build book _book` and checks `book.json` readme/styles + plugin loading before moving on |
| Collapsing `vN` loses the visible TDD progression | Unit 6 rewrites the four affected chapters so the progression lives in prose (LGWT model) |
| Validator/skill still enforce old conventions and fight new chapters | Unit 7 updates SKILL.md, template, and `validate_article.py` to the new model and tests both pass-on-new and fail-on-old |
| A non-template module name collides across chapters under the flat namespace | Surfaces as an import error when the suite runs in Unit 1; rename the offending module chapter-qualified |
| Reader-facing baseline test count changes (badge says "740 passing") | Recompute and update the README badge to the new count as part of Unit 5 |

## Documentation / Operational Notes

- README badge ("tests-740-passing") will drift after `vN` collapse and template exclusion; update it
  to the recomputed count.
- Deploy platforms (Netlify, Railpack, Dokploy/Docker) read root config; after Unit 2 their build
  command changes to `honkit build book _book` — a redeploy should be validated once merged.
- `CONTRIBUTING.md` becomes the single source for contributor setup and authoring conventions.

## Sources & References

- Related plan: `docs/plans/2026-06-04-001-feat-python-with-tests-plan.md`
- Build config: `package.json`, `netlify.toml`, `railpack.json`, `Dockerfile`, `book.json`,
  `pyproject.toml`, `SUMMARY.md`
- Authoring guardrails: `.claude/skills/article-writer/SKILL.md`,
  `.claude/skills/article-writer/scripts/validate_article.py`, `template.md`
- Reader model reference: Chris James, "Learn Go with Tests" (repo-as-reference, write-your-own-code)
