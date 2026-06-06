// Build an "On this page" sidebar from the current chapter's h2/h3 headings, with scroll-spy.
// Rebuilds on Honkit's client-side page changes.
(function () {
  "use strict";

  // Keep in step with --topbar-h in book/styles/website.css.
  var TOPBAR_H = 50;

  // Honkit scrolls the content inside `.book-body` (an absolutely-positioned,
  // overflow-y:auto container), not the window. Bind scroll-spy to whichever of
  // these actually scrolls, falling back to the window for other layouts.
  function pickScroller() {
    var candidates = [
      document.querySelector(".book-body"),
      document.querySelector(".book-body .body-inner"),
    ];
    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      if (el && el.scrollHeight - el.clientHeight > 4) return el;
    }
    return window;
  }

  function slugify(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/[^\w]+/g, "-")
      .replace(/(^-|-$)/g, "");
  }

  function build() {
    var existing = document.getElementById("page-toc");
    if (existing) existing.parentNode.removeChild(existing);

    var content = document.querySelector(".page-inner section") ||
                  document.querySelector(".page-inner");
    if (!content) return;

    var headings = content.querySelectorAll("h2, h3");
    if (headings.length < 2) return; // not worth a TOC

    var nav = document.createElement("nav");
    nav.id = "page-toc";

    var title = document.createElement("div");
    title.className = "page-toc-title";
    title.textContent = "On this page";
    nav.appendChild(title);

    var ul = document.createElement("ul");
    var items = [];

    Array.prototype.forEach.call(headings, function (h) {
      if (!h.id) h.id = slugify(h.textContent);
      var li = document.createElement("li");
      li.className = "page-toc-" + h.tagName.toLowerCase();
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      a.addEventListener("click", function (e) {
        e.preventDefault();
        h.scrollIntoView({ behavior: "smooth", block: "start" });
        if (history.replaceState) history.replaceState(null, "", "#" + h.id);
      });
      li.appendChild(a);
      ul.appendChild(li);
      items.push({ heading: h, link: a });
    });

    nav.appendChild(ul);
    document.body.appendChild(nav);

    var scroller = pickScroller();
    // A heading counts as "current" once it has scrolled up to just below the bar.
    var threshold = TOPBAR_H + 24;

    function atBottom() {
      if (scroller === window) {
        return window.innerHeight + window.pageYOffset >= document.body.scrollHeight - 2;
      }
      return scroller.scrollTop + scroller.clientHeight >= scroller.scrollHeight - 2;
    }

    function onScroll() {
      var active = items[0];
      if (atBottom()) {
        // Once we can't scroll further, pin the last entry so the bottom section reads as active.
        active = items[items.length - 1];
      } else {
        // getBoundingClientRect().top is viewport-relative, so this works whatever the scroller is:
        // the active heading is the last one whose top has crossed below the bar.
        for (var i = 0; i < items.length; i++) {
          if (items[i].heading.getBoundingClientRect().top <= threshold) active = items[i];
        }
      }
      items.forEach(function (it) {
        it.link.classList.toggle("active", it === active);
      });
    }

    scroller.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    onScroll();
  }

  if (window.gitbook && window.gitbook.events) {
    // Fires on first load and on every client-side page change.
    window.gitbook.events.bind("page.change", function () {
      // let the new page render first
      setTimeout(build, 50);
    });
  } else {
    document.addEventListener("DOMContentLoaded", build);
    setTimeout(build, 400);
  }
})();
