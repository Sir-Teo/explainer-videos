// Interactives for Act VII, The World Economy (Parts 34-37).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREY_HINT = "#8B93A1", TEAL = "#7FD1B9";

  // ---- Part 34: the open economy -------------------------------------------------------------------------------
  W.peg = function (el) {
    // Obstfeld's self-fulfilling crises in Part 34's form (explainer.economics.agora.openecon: obstfeld_regions,
    // obstfeld_outcome).  A government defends a peg while the pain of defending, (u + gamma x)^2, is below the
    // cost C of giving up; u is the slack in the economy and x the devaluation traders expect (0, or delta).  With
    // no attack expected it defends while u < sqrt(C); with one expected it gives up once u > sqrt(C) - gamma delta.
    function regions(v) {
      var hi = Math.sqrt(v.C), lo = hi - v.g * v.d;
      return { lo: lo, hi: hi };
    }
    function outcome(u, x, v) { return Math.pow(u + v.g * x, 2) > v.C ? "abandon" : "defend"; }
    QB.widget(el, {
      title: "The governor's dilemma",
      sub: "Your economy is in a recession and your currency is pegged. Left: the pain of defending the peg against " +
           "how deep the recession is, if traders expect no devaluation (teal) or one (red), and the cost of giving " +
           "up (gold). Right: your peg, in each case. Set the slack, and how much a devaluation traders expect " +
           "would raise the rate you need.",
      panels: 2, height: 280,
      controls: [
        { k: "u", label: "Slack in the economy, u", min: 0, max: 1.4, step: 0.01, value: 0.75,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "d", label: "Devaluation traders expect, delta", min: 0, max: 1, step: 0.05, value: 0.5,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "g", label: "Its effect on the rate you need, gamma", min: 0.5, max: 2, step: 0.1, value: 1,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "C", label: "Cost of giving up, C", min: 0.25, max: 2, step: 0.05, value: 1,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var R = regions(v), us = [], calm = [], att = [], i, top = 4;
        for (i = 0; i <= 140; i++) {
          var u = i / 100;
          us.push(u); calm.push(u * u); att.push(Math.pow(u + v.g * v.d, 2));
        }
        var a = g[0].axes({ x: [0, 1.4], y: [0, top], title: "The pain of defending", xlabel: "slack, u" });
        var lo = Math.max(0, R.lo), hi = Math.min(1.4, R.hi);
        if (lo > 0) a.area([0, lo], [top, top], 0, { color: TEAL, alpha: 0.12 });
        if (hi > lo) a.area([lo, hi], [top, top], 0, { color: GOLD, alpha: 0.14 });
        if (hi < 1.4) a.area([hi, 1.4], [top, top], 0, { color: RED, alpha: 0.12 });
        a.line(us, calm, { color: TEAL, width: 2.5 });
        a.line(us, att.map(function (y) { return Math.min(y, top + 1); }), { color: RED, width: 2.5 });
        a.hline(v.C, { color: GOLD, width: 2 });
        a.vline(v.u, { color: "#FFFFFF" });
        a.dots([v.u, v.u], [Math.min(v.u * v.u, top), Math.min(Math.pow(v.u + v.g * v.d, 2), top)],
               { color: function (j) { return j ? RED : TEAL; }, r: 5 });
        a.text(0.03, v.C + 0.15, "cost of giving up", { color: GOLD, size: 11 });
        var p0 = v.u * v.u, p1 = Math.pow(v.u + v.g * v.d, 2);
        var b = g[1].axes({ x: [0, 3], y: [0, top], title: "Your peg", xlabel: "" });
        b.bars([0.8, 2.0], [Math.min(p0, top), Math.min(p1, top)], 0.6,
               { color: function (j) { return (j ? p1 : p0) > v.C ? RED : TEAL; } });
        b.hline(v.C, { color: GOLD, width: 2 });
        b.text(0.8, Math.min(p0, top) + 0.18, "no attack expected", { align: "center", size: 11 });
        b.text(2.0, Math.min(p1, top) + 0.18, "attack expected", { align: "center", size: 11 });
        st.R = R; st.o0 = outcome(v.u, 0, v); st.o1 = outcome(v.u, v.d, v);
      },
      readout: function (v, st) {
        var z = st.o0 === st.o1 ? (st.o0 === "defend" ? "the peg holds whatever traders think"
                                                       : "the peg falls whatever traders think")
                                : "two equilibria: the peg falls if, and because, traders expect it to";
        return [["your zone", z],
                ["the band with two equilibria", "u from " + Math.max(0, st.R.lo).toFixed(2) + " to " +
                  st.R.hi.toFixed(2) + " (width gamma x delta = " + (v.g * v.d).toFixed(2) + ")"],
                ["no attack expected / attack expected", st.o0 + " / " + st.o1]];
      },
      note: "Obstfeld (1996), in the simple form computed in Part 34, chapter 2: with C = 1, gamma = 1 and " +
            "delta = 0.5, a peg with slack between 0.5 and 1 falls if traders expect it to, and the Island, at " +
            "0.75, is inside. " +
            "Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
