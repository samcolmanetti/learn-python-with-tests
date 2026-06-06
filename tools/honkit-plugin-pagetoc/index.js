// Local Honkit plugin: inject the "On this page" sidebar (pagetoc) and the sticky top bar (topbar)
// into every website page. The top bar's *styling* lives in book/styles/website.css, which Honkit
// loads after the theme stylesheet so the overrides win without !important; this file only registers
// the behaviour scripts and the pagetoc styling.
module.exports = {
  website: {
    assets: "./website",
    js: ["pagetoc.js", "topbar.js"],
    css: ["pagetoc.css"],
  },
};
