---
title: "feat: Sticky top bar, reactive on-this-page, and content/TOC layout fixes for the book site"
type: feat
status: active
date: 2026-06-05
---

# feat: Sticky top bar, reactive on-this-page, and content/TOC layout fixes for the book site

## Overview

The "Learn Python with Tests" Honkit site has four chrome problems: the session's home-link hack
renders as a wrong "← back" arrow at the top of every page (including the home page); the "On this
page" right sidebar never updates its active highlight while scrolling; the centered content is
partly hidden behind that fixed sidebar on wide viewports; and the site lacks the always-visible
top bar (logo + title + search) that gives Learn Go with Tests its recognizable reading experience.
This plan replaces the home-link hack with a proper sticky top bar, fixes the scroll-spy and the
content/TOC overlap, and removes a not-ready "Later (out of scope for now)" navigation section.

All work is frontend chrome: `book/styles/website.css` and the local Honkit plugin under
`tools/honkit-plugin-pagetoc/`. No Python or chapter-content changes, so the 716-test suite is
untouched; verification is a Honkit build plus a browser check (Playwright is available).

## Problem Frame

The site runs Honkit's default GitBook theme. Honkit's DOM is `.book > .book-summary` (left nav,
300px, contains `#book-search-input`) and `.book-body > .body-inner > .page-wrapper > .page-inner`
(content; `.page-inner` is `max-width:800px; margin:0 auto`). `.book-body` is
`position:absolute; overflow-y:auto`, so **the content scrolls inside `.book-body`, not the
window**. The `.book-header` (50px top bar) exists but its `h1` title is `opacity:0` until hover and
hidden under 1000px, so it reads as empty. A session-added home-link (`homelink.js`/`homelink.css`)
injects an `← Learn Python with Tests` anchor into `.page-inner`, and the `pagetoc` plugin injects a
fixed right "On this page" nav whose scroll-spy binds `window` scroll (which never fires).

The user wants the Learn Go with Tests chrome: a top bar that stays visible while scrolling, with a
small image/logo + title on the left that links home, and a search box on the right. Note: the LGWT
**repo** (`references/learn-go-with-tests/`) has no theme to copy. Its `book.json` is just
`{structure:{readme:gb-readme.md}}` and it is plain markdown. The look the user likes is gitbook.io's
hosted platform UI, so this plan **rebuilds** that look on top of honkit rather than importing it.

## Requirements Trace

- R1. Remove the wrong home-link affordance: no "← back" arrow injected into page content, and
  nothing home-related shown on the home page as if it were content. The home affordance moves into
  the top bar (R5).
- R2. The "On this page" sidebar highlights the current section reactively as the reader scrolls.
- R3. The main content stays centered/readable and is never hidden behind the right "On this page"
  sidebar on any viewport width.
- R4. Remove the "Later (out of scope for now)" section from `book/SUMMARY.md` and from `README.md`'s
  roadmap; reconcile the orphan-page guard in `code/tests/test_summary_links.py`.
- R5. A top bar stays fixed/visible while scrolling, with a small logo (red/green/blue TDD dots) plus
  the book title on the left linking to the home page, and a working search box on the right.
- R6. The Honkit build stays green, `uv run pytest` stays at 716 passing, and the existing good
  styling (per-line code hover, copy button, the `pagetoc` TOC itself) keeps working.

## Scope Boundaries

- Not changing chapter prose, code, or tests (no `.md` chapter edits beyond the two roadmap/section
  removals in R4; no `code/` changes except the test-guard reconciliation).
- Not building a brand-new Honkit theme package or swapping themes. We restyle the default theme via
  CSS overrides plus small plugin JS, the lowest-risk path.
- Not sourcing or generating a raster logo image this pass. The mark is CSS-drawn red/green/blue
  dots (the TDD cycle). A real image can drop into the reserved logo slot later.
- Not redesigning the left summary sidebar, typography scale, or color palette beyond what the top
  bar and overlap fixes require.
- Not deleting the out-of-scope draft chapters; they move to `docs/drafts/` to preserve the work.

## Context & Research

### Relevant Code and Patterns

- `tools/honkit-plugin-pagetoc/index.js` registers website assets: currently
  `js: ["pagetoc.js","homelink.js"]`, `css: ["pagetoc.css","homelink.css"]`. This is the injection
  seam for all custom JS/CSS.
- `tools/honkit-plugin-pagetoc/website/pagetoc.js` builds the right TOC from `h2/h3`, appends it to
  `document.body`, and binds scroll-spy. It already re-runs on Honkit's `gitbook.events` `page.change`
  event (the proven re-injection pattern). Its `onScroll` reads `window.pageYOffset` and binds
  `window` scroll, which is the R2 bug.
- `tools/honkit-plugin-pagetoc/website/pagetoc.css` positions `#page-toc` as `position:fixed;
  top:90px; right:28px; width:200px`, hidden under 1300px. This fixed element causes the R3 overlap.
- `tools/honkit-plugin-pagetoc/website/homelink.js` + `homelink.css` are the session's home-link to
  be removed (R1).
- `book/styles/website.css` holds the per-line code hover and copy-button styling (must be preserved)
  and is the place for the top-bar and layout CSS.
- Honkit default theme facts (from the built `_book/gitbook/style.css`): `.book-header` is 50px,
  `h1` opacity:0 until `.book-header:hover`, title hidden under 1000px; `.book-summary` is the 300px
  left nav holding `#book-search-input` (wired by the `search`/`lunr` plugins); `.book-body` starts
  at `left:300px` (with summary) and is the scroll container; `.page-inner` is `max-width:800px;
  margin:0 auto`.
- `book/SUMMARY.md` "Later (out of scope for now)" section links `system-design.md` and
  `company-oas.md`. `README.md` has the same grouping. `code/tests/test_summary_links.py` enforces
  both "every SUMMARY link resolves" and "no orphan `book/*.md`", so the two pages must leave `book/`
  when their links are removed (move to `docs/drafts/`).

### Institutional Learnings

- Session learning (memory `reader-not-repo-internals`): keep reader-facing surfaces clean of
  scaffolding. The home-link-as-content was exactly that kind of leak; the top bar is the right home.
- Honkit client-side navigation (`page.change`) replaces `.page-inner` content, so any injected DOM
  must re-apply on that event. `pagetoc.js` is the working reference for this.
- Honkit resolves a relative build-output path against the **book root** (`honkit build book ../_book`
  lands at repo-root `_book`); preview is `npm run serve` at http://localhost:4000.

### External References

- The desired look is gitbook.io's hosted reading UI (sticky header, logo+title left, search right,
  left nav, right "on this page"). There is no theme artifact in `references/learn-go-with-tests/` to
  import; it is plain markdown. This plan reconstructs the look with CSS + plugin JS.

## Key Technical Decisions

- **Restyle, don't replace, the theme.** Override Honkit's default theme with CSS in
  `book/styles/website.css` plus small JS in the existing local plugin. Rationale: lowest risk,
  keeps the search/lunr/navigation plugins working, no theme-package maintenance.
- **The top bar is the home affordance; delete the in-content home link.** Make `.book-header` a
  sticky, always-visible bar; put a CSS dots-logo + title on the left wrapped in an `<a href>` to the
  site root; remove `homelink.js`/`homelink.css` and deregister them. Rationale: fixes R1 cleanly and
  satisfies R5's "title/logo links home."
- **Relocate the existing search node into the top bar; do not clone it.** Move the live
  `#book-search-input` DOM node from `.book-summary` into the top bar's right slot so its plugin event
  handlers travel with it. Rationale: keeps search functional without re-wiring lunr. Re-apply on
  `page.change` only if Honkit re-renders the header (verify during implementation).
- **Scroll-spy listens on the real scroll container.** Bind scroll on `.book-body` (fallback
  `.body-inner`/`window`) and compute heading offsets relative to that container's `scrollTop`.
  Rationale: that is where scrolling actually happens; fixes R2.
- **Reserve a right gutter so content and TOC never overlap.** Constrain the content column and/or
  add right padding on `.page-inner`/`.page-wrapper` at the widths where `#page-toc` is visible, so
  the centered text column and the fixed 200px TOC occupy disjoint horizontal space. Rationale:
  fixes R3 without removing the TOC.
- **Unship, don't delete, out-of-scope pages.** Move `book/system-design.md` and
  `book/company-oas.md` to `docs/drafts/`, remove their `SUMMARY.md`/`README.md` entries and the
  "Later" heading. Rationale: satisfies "don't include it" while preserving the drafts and keeping
  the orphan-guard green.

## Open Questions

### Resolved During Planning

- Logo image? Red/green/blue CSS dots (the TDD cycle) for now; no raster asset. A real image can drop
  into the reserved slot later (user: "dots could be good enough for now").
- Delete vs keep the out-of-scope pages? Move to `docs/drafts/` (preserve, unship).
- Is there an LGWT theme to copy? No; the reference repo is plain markdown. Rebuild the look.

### Deferred to Implementation

- Whether Honkit re-renders `.book-header` on `page.change` (deciding if search/logo relocation must
  re-apply per navigation, like `pagetoc.js` does). Resolve by observing the DOM during the browser
  check.
- Exact breakpoints for the content/TOC gutter and when to collapse the top-bar title/search on
  narrow widths. Tune against the live build at a few viewport widths.
- Whether the relocated search box needs minor restyle to read well on the top bar background.

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation
> specification. The implementing agent should treat it as context, not code to reproduce.*

Target chrome (desktop):

    +----------------------------------------------------------------------+
    | ●●●  Learn Python with Tests                       [ search...    ]   |  <- sticky .book-header
    +-------------------+--------------------------------------+-----------+
    | summary nav       |   centered content column            | On this   |
    | (chapters)        |   (.page-inner, gutter on the right)  | page TOC  |
    | scrolls           |   scrolls inside .book-body           | (fixed)   |
    +-------------------+--------------------------------------+-----------+

- Top bar: `.book-header` becomes `position:fixed/sticky`, full width above the body, always opaque.
  Left: `<a href=root>` containing a CSS dots mark + the title. Right: the moved `#book-search-input`.
- Body offset down by the bar height so content starts below it.
- Scroll-spy: container = `.book-body`; on its scroll event, find the last heading whose offset (top
  relative to container) is above a threshold, mark its TOC link active.
- Overlap: at >=1300px (where `#page-toc` shows), the content column leaves a >=240px right gutter so
  text never sits under the 200px fixed TOC.

## Implementation Units

- [ ] **Unit 1: Remove the in-content home-link hack**

**Goal:** Delete the `← Learn Python with Tests` injection so nothing home-related renders as page
content (and nothing wrong shows on the home page).

**Requirements:** R1.

**Dependencies:** None (but the home affordance it provided is re-established in Unit 2; land Unit 2
in the same change so there is never a window with no home link).

**Files:**
- Delete: `tools/honkit-plugin-pagetoc/website/homelink.js`, `tools/honkit-plugin-pagetoc/website/homelink.css`
- Modify: `tools/honkit-plugin-pagetoc/index.js` (drop `homelink.js`/`homelink.css` from the asset arrays)

**Approach:**
- Revert the session's homelink registration so the plugin injects only the pagetoc assets (plus the
  new top-bar asset from Unit 2).

**Test scenarios:** Test expectation: none -- asset removal, verified visually in Unit 6 (no
`#home-link` in the DOM, no `← ` arrow at the top of any page including the index).

**Verification:** After build, no page contains the injected `#home-link`; the home page shows no
stray back-link.

- [ ] **Unit 2: Sticky top bar with dots logo, home-linked title, and relocated search**

**Goal:** Give the site an always-visible top bar: CSS dots mark + title on the left linking home,
and the working search box on the right.

**Requirements:** R5 (and completes R1's replacement affordance).

**Dependencies:** Unit 1.

**Files:**
- Create: `tools/honkit-plugin-pagetoc/website/topbar.js` (build logo+title link; relocate
  `#book-search-input` into the bar; re-apply on `page.change` if needed)
- Create: `tools/honkit-plugin-pagetoc/website/topbar.css` (sticky bar, dots mark, layout) -- or fold
  this CSS into `book/styles/website.css`; pick one home and note it
- Modify: `tools/honkit-plugin-pagetoc/index.js` (register `topbar.js`/`topbar.css`)
- Modify: `book/styles/website.css` if the bar styling lives there

**Approach:**
- Make `.book-header` sticky/fixed, full-width, opaque, above `.book-body`; offset the body content
  down by the bar height so nothing hides under it.
- Left: an `<a>` to the site root (`index.html`, flat site) containing three small red/green/blue
  dots (CSS) and the book title; force the title visible (override the theme's hover-only opacity and
  the <1000px hide).
- Right: move the live `#book-search-input` node from `.book-summary` into the bar so its lunr/search
  handlers keep working; restyle minimally to suit the bar.
- Re-apply the relocation/logo on `page.change` if Honkit re-renders the header (mirror `pagetoc.js`).

**Patterns to follow:** `tools/honkit-plugin-pagetoc/website/pagetoc.js` for the `gitbook.events`
`page.change` re-injection pattern and the website-asset registration shape in `index.js`.

**Test scenarios:**
- Happy path: top bar is visible on load and stays visible while scrolling a long chapter.
- Happy path: clicking the logo/title navigates to the home page from a deep chapter.
- Integration: typing in the relocated search box still produces lunr search results (the move
  preserved the plugin's handlers).
- Edge case: on a narrow viewport the bar degrades gracefully (title and/or search collapse without
  overlapping).
- Edge case: after client-side navigation to another chapter, the bar, logo link, and search are
  still present and functional.

**Verification:** Sticky bar with dots+title (home link) left and a working search box right, on both
the index and a chapter page, on load and after a client-side nav.

- [ ] **Unit 3: Make the "On this page" scroll-spy reactive**

**Goal:** The right TOC highlights the section currently in view as the reader scrolls.

**Requirements:** R2.

**Dependencies:** None (independent of the top bar).

**Files:**
- Modify: `tools/honkit-plugin-pagetoc/website/pagetoc.js` (bind scroll on the real container; compute
  offsets relative to it)

**Approach:**
- Identify the scroll container (`.book-body`, fallback `.body-inner`, then `window`), bind its
  `scroll` event, and compute each heading's position relative to the container's scroll position so
  the active link tracks correctly. Account for the new top-bar height in the active-threshold.

**Patterns to follow:** the existing `onScroll`/`page.change` structure in `pagetoc.js`; keep the
`active` class contract the CSS already styles.

**Test scenarios:**
- Happy path: scrolling down a multi-section chapter moves the `active` highlight from section to
  section in step with the content.
- Edge case: at the very top, the first heading is active; at the very bottom, the last heading is
  active.
- Edge case: a chapter with fewer than 2 headings still suppresses the TOC (existing behavior intact).
- Integration: after client-side navigation, scroll-spy rebinds to the new page's container and works
  without a full reload.

**Verification:** On a long chapter, the highlighted TOC entry tracks the scroll position smoothly,
both on first load and after navigating between chapters.

- [ ] **Unit 4: Fix content/TOC overlap and centering**

**Goal:** Keep the content column centered and readable, never hidden behind the fixed right TOC.

**Requirements:** R3.

**Dependencies:** None functionally, but tune alongside Unit 2 (the top bar changes vertical space)
and Unit 3 (same TOC element).

**Files:**
- Modify: `tools/honkit-plugin-pagetoc/website/pagetoc.css` and/or `book/styles/website.css`

**Approach:**
- At the widths where `#page-toc` is shown (>=1300px), reserve a right gutter so the content column
  and the 200px fixed TOC occupy disjoint horizontal space (constrain/shift `.page-inner`, or pad
  `.page-wrapper`, so centered text never sits under the TOC). Below that width the TOC stays hidden
  and content uses the full column.

**Test scenarios:**
- Happy path (>=1300px): the last words of long lines are fully visible, not under the TOC; content
  reads as an intentional centered column with the TOC beside it.
- Edge case (~1024-1299px): TOC hidden, content uses the available width without a dead right gutter.
- Edge case (mobile <600px): summary collapses (theme behavior) and content is full-width and
  readable.

**Verification:** At 1440px, 1280px, and 768px the content is readable with no text hidden behind the
TOC and no awkward off-center column.

- [ ] **Unit 5: Remove the "Later (out of scope for now)" navigation**

**Goal:** Stop advertising not-ready pages; keep the nav honest and the orphan-guard green.

**Requirements:** R4.

**Dependencies:** None.

**Files:**
- Modify: `book/SUMMARY.md` (remove the "Later (out of scope for now)" heading and its two links)
- Modify: `README.md` (remove the same roadmap grouping/links)
- Move: `book/system-design.md` -> `docs/drafts/system-design.md`, `book/company-oas.md` ->
  `docs/drafts/company-oas.md`
- Verify: `code/tests/test_summary_links.py` still passes (no orphan `book/*.md`, every SUMMARY link
  resolves)

**Approach:**
- Delete the heading and the two list items from both files; relocate the two pages out of `book/` so
  the orphan check no longer sees them. No test-code change should be needed if the pages leave
  `book/`; only touch the test if relocation proves insufficient.

**Test scenarios:**
- Integration: `uv run pytest code/tests/test_summary_links.py` passes (every SUMMARY link resolves;
  no orphan book pages).
- Happy path: the built site's nav no longer shows "Later (out of scope for now)" or the two pages.
- Edge case: `README.md` has no dangling link to the moved pages.

**Verification:** Suite green; the "Later" section is gone from the sidebar and the README; the two
drafts live under `docs/drafts/`.

- [ ] **Unit 6: Build-and-browser verification pass**

**Goal:** Confirm the whole chrome works together across pages and widths.

**Requirements:** R6 (and end-to-end validation of R1-R5).

**Dependencies:** Units 1-5.

**Files:**
- No source changes expected; this is verification. Any fix it surfaces lands in the relevant unit's
  files.

**Approach:**
- Build (`npm run serve` or `honkit build book ../_book`), then drive a browser (Playwright) over the
  index and a long chapter: check the sticky bar, home link, search, scroll-spy tracking, and
  content/TOC layout at a few widths. Confirm `uv run pytest` is 716 and the build has no errors.

**Test scenarios:**
- Integration: from a deep chapter, the bar stays put while scrolling, the logo/title returns home,
  search returns results, the TOC highlight tracks scroll, and no text hides behind the TOC.
- Edge case: client-side navigation between two chapters preserves all of the above without a reload.
- Happy path: `uv run pytest` reports 716 passed; Honkit build reports success with no plugin/asset
  errors.

**Verification:** A browser walkthrough shows all five fixes working on index + chapter at 1440/1280/
768px; suite 716 green; build clean.

## System-Wide Impact

- **Interaction graph:** All changes are client-side chrome injected by the one local plugin plus CSS.
  The only cross-plugin touch is relocating the `search` plugin's `#book-search-input` node; moving
  (not cloning) the node preserves its handlers.
- **State lifecycle risks:** Honkit `page.change` replaces page content; any injected/relocated DOM
  (top bar contents, scroll-spy) must re-apply or rebind on that event, exactly as `pagetoc.js`
  already does. Missing this would make search/logo/scroll-spy work on first load but break after a
  client-side navigation.
- **API surface parity:** The home affordance moves from an in-content link to the top bar; ensure it
  exists on every page type (index and chapters).
- **Unchanged invariants:** Chapter prose/code/tests, the build-output path (`../_book` to repo-root
  `_book`), pytest discovery, and the existing code-hover/copy-button styling are unchanged. The
  716-test suite should not move except via Unit 5's guard check.

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Relocating `#book-search-input` breaks lunr search (lost handlers) | Move the live node rather than cloning; verify search returns results in the browser pass; if Honkit re-renders the header on nav, re-apply on `page.change` |
| Scroll-spy still inert if the wrong scroll container is chosen | Detect container in priority order (`.book-body` -> `.body-inner` -> `window`); verify highlight tracks in-browser at top, middle, bottom |
| Sticky top bar overlaps content or the left summary | Offset body content by the bar height; verify no clipped first heading and that the summary nav still scrolls |
| Removing SUMMARY links without moving pages trips the orphan guard | Move both pages to `docs/drafts/` in the same unit; run `test_summary_links.py` |
| Top-bar/TOC CSS regresses narrow/mobile layouts | Test at 1440/1280/768px; keep `#page-toc` hidden under 1300px; let the summary collapse per theme defaults |

## Documentation / Operational Notes

- `docs/drafts/` becomes the home for unshipped chapters; note in `CONTRIBUTING.md` only if the team
  wants a documented drafts workflow (optional, not required by this plan).
- No deploy-config changes; the build command and output path are unchanged.

## Sources & References

- Prior plan (this restructure): `docs/plans/2026-06-05-001-refactor-book-repo-structure-plan.md`
- Theme/plugin: `tools/honkit-plugin-pagetoc/` (index.js, website/pagetoc.js, website/pagetoc.css,
  website/homelink.js, website/homelink.css), `book/styles/website.css`, `book/book.json`
- Nav/guard: `book/SUMMARY.md`, `README.md`, `code/tests/test_summary_links.py`
- Reference look (no importable theme): `references/learn-go-with-tests/` (plain markdown + minimal
  `book.json`); target is gitbook.io's hosted reading UI
