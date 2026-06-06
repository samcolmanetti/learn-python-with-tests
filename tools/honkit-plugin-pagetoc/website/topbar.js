// Turn Honkit's near-empty `.book-header` into a real top bar: a red/green/blue TDD-dots logo plus
// the book title on the left (the existing `<a href=".">` is already a home link), and the live
// search box relocated to the right.
//
// Honkit re-fetches each page client-side and does `$(".book").replaceWith(newBook)`, so the header,
// summary, and search input are *fresh nodes* after every navigation. We therefore (re)apply the bar
// on each `page.change`, mirroring pagetoc.js. Moving the live `#book-search-input` node preserves
// the search plugin's handlers, and the plugin re-binds to it by id on the same event, so search
// keeps working from its new home. The sticky/layout styling lives in book/styles/website.css.
(function () {
  "use strict";

  // Honkit renders the *current page's* title in `.book-header h1` (so a chapter would otherwise
  // show "Numbers" beside a home-linking logo). The bar is a brand/home affordance, so we show the
  // book's title consistently instead. Kept in step with book.json's "title".
  var BOOK_TITLE = "Learn Python with Tests";

  function build() {
    var header = document.querySelector(".book-header");
    if (!header) return;

    // Rebuild the title anchor as [dots logo][title text] so the whole thing is the home link, and
    // the title can be wrapped/collapsed independently of the logo on narrow screens. Idempotent:
    // skip if this header already has the mark.
    var anchor = header.querySelector("h1 a");
    if (anchor && !anchor.querySelector(".topbar-logo")) {
      anchor.textContent = "";

      var logo = document.createElement("span");
      logo.className = "topbar-logo";
      logo.setAttribute("aria-hidden", "true");
      ["red", "green", "blue"].forEach(function (name) {
        var dot = document.createElement("span");
        dot.className = "topbar-dot topbar-dot-" + name;
        logo.appendChild(dot);
      });
      anchor.appendChild(logo);

      var title = document.createElement("span");
      title.className = "topbar-title";
      title.textContent = BOOK_TITLE;
      anchor.appendChild(title);
    }

    // Relocate the live search node into the bar's right slot so its lunr handlers travel with it.
    var search = document.getElementById("book-search-input");
    if (search && search.parentNode !== header) {
      header.appendChild(search);
    }

    header.classList.add("topbar-ready");
  }

  if (window.gitbook && window.gitbook.events) {
    // Fires on first load and on every client-side page change. Run immediately
    // so the (CSS-hidden) header reveals with the right content in the same frame
    // and never flashes the raw page title; the delayed pass is a safety net in
    // case another plugin hasn't injected the search node yet.
    window.gitbook.events.bind("page.change", function () {
      build();
      setTimeout(build, 50);
    });
  } else {
    document.addEventListener("DOMContentLoaded", build);
    setTimeout(build, 400);
  }
})();
