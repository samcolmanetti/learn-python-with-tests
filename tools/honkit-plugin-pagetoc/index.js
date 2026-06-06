// Local Honkit plugin: inject the "On this page" sidebar and a "home" link into every website page.
module.exports = {
  website: {
    assets: "./website",
    js: ["pagetoc.js", "homelink.js"],
    css: ["pagetoc.css", "homelink.css"],
  },
};
