// Inject a "home" link at the top of every page's content, so the reader can always get back to
// the landing page (the same convenience Learn Go with Tests offers). The built site is flat, so a
// relative "index.html" href resolves from any chapter page.
(function () {
  "use strict";

  function inject() {
    var inner = document.querySelector(".page-inner");
    if (!inner) return;
    if (inner.querySelector("#home-link")) return; // already injected for this page

    var a = document.createElement("a");
    a.id = "home-link";
    a.href = "index.html";
    a.textContent = "Learn Python with Tests";
    a.setAttribute("aria-label", "Back to the home page");

    inner.insertBefore(a, inner.firstChild);
  }

  if (window.gitbook && window.gitbook.events) {
    // Fires on first load and on every client-side page change.
    window.gitbook.events.bind("page.change", function () {
      setTimeout(inject, 50);
    });
  } else {
    document.addEventListener("DOMContentLoaded", inject);
    setTimeout(inject, 400);
  }
})();
