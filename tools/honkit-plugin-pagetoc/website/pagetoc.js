// Build an "On this page" sidebar from the current chapter's h2/h3 headings, with scroll-spy.
// Rebuilds on Honkit's client-side page changes.
(function () {
  "use strict";

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

    function onScroll() {
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      var active = items[0];
      for (var i = 0; i < items.length; i++) {
        var top = items[i].heading.getBoundingClientRect().top + scrollTop;
        if (top - 100 <= scrollTop) active = items[i];
      }
      items.forEach(function (it) {
        it.link.classList.toggle("active", it === active);
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
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
