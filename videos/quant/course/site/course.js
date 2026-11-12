// Quant, Built course site: math rendering, the track buttons, the map filter.
(function () {
  "use strict";

  function renderMath(root) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(root, {
      delimiters: [
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false },
      ],
      throwOnError: false,
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "canvas"],
    });
  }

  // Track buttons on a part's page: dim the chapters a track does not watch.
  function trackButtons() {
    document.querySelectorAll("#chapters .track-buttons").forEach(function (bar) {
      var items = document.querySelectorAll("#chapters .chapters li");
      bar.addEventListener("click", function (e) {
        var b = e.target.closest("button");
        if (!b) return;
        bar.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
        var tiers = b.dataset.tiers || "";
        items.forEach(function (li) {
          var t = li.dataset.tier;
          li.classList.toggle("off", !!tiers && t !== "*" && tiers.indexOf(t) < 0);
        });
        try { localStorage.setItem("quant-track", b.dataset.track || ""); } catch (err) { /* private mode */ }
      });
      var saved = "";
      try { saved = localStorage.getItem("quant-track") || ""; } catch (err) { /* private mode */ }
      if (saved) {
        var b = bar.querySelector('button[data-track="' + saved + '"]');
        if (b) b.click();
      }
    });
  }

  // Map filter on the course page.
  function mapFilter() {
    var bar = document.querySelector(".map-filter");
    if (!bar) return;
    var cards = document.querySelectorAll(".pcard");
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      bar.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
      var level = b.dataset.level;
      cards.forEach(function (c) { c.classList.toggle("dim", !!level && c.dataset.level !== level); });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderMath(document.body);
    trackButtons();
    mapFilter();
  });
})();
