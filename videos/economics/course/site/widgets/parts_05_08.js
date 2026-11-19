// Interactives for Act II, Choosing (Parts 5-8).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", BLUE = "#9FB8F2", GREY_HINT = "#8B93A1";

  // ---- Part 5: what people want --------------------------------------------------------------------------------
  W.wants = function (el) {
    // the eleven Play-it lines: the most fish and the most coconuts each $60 buys (explainer.economics.island, Part 5)
    var LINES = [[6, 6], [12, 3], [4, 9], [9, 4], [3, 12], [7, 5], [5, 7], [11, 4], [4, 8], [10, 6], [6, 7]];
    var N = LINES.length, M = 60;
    var P = LINES.map(function (l) { return [M / l[0], M / l[1]]; });

    function bundles(fish) { // fish on each line -> (fish, coconuts)
      return fish.map(function (f, i) { var A = LINES[i][0], B = LINES[i][1]; f = Math.max(0, Math.min(A, f));
        return [f, B * (1 - f / A)]; });
    }
    function cost(i, x) { return P[i][0] * x[0] + P[i][1] * x[1]; }
    function violations(X, e) { // GARP at efficiency e: pairs (i, j) with x_i R x_j and e p_j.x_j > p_j.x_i
      var R = [], i, j, k;
      for (i = 0; i < N; i++) { R.push([]); for (j = 0; j < N; j++) R[i].push(e * cost(i, X[i]) >= cost(i, X[j]) - 1e-9); }
      for (k = 0; k < N; k++) for (i = 0; i < N; i++) if (R[i][k]) for (j = 0; j < N; j++) if (R[k][j]) R[i][j] = true;
      var out = [];
      for (i = 0; i < N; i++) for (j = 0; j < N; j++)
        if (i !== j && R[i][j] && e * cost(j, X[j]) > cost(j, X[i]) + 1e-9) out.push([i, j]);
      return out;
    }
    function ccei(X) {
      if (!violations(X, 1).length) return 1;
      var lo = 0, hi = 1, k;
      for (k = 0; k < 50; k++) { var mid = (lo + hi) / 2; if (violations(X, mid).length) hi = mid; else lo = mid; }
      return hi;
    }
    function presetBo() { return LINES.map(function (l) { return 0.6 * l[0]; }); }
    function presetRandom(seed) { var r = QB.rng(seed * 13 + 5); return LINES.map(function (l) { return r() * l[0]; }); }

    var controls = LINES.map(function (l, i) {
      return { k: "f" + i, label: "Line " + (i + 1) + ": " + l[0] + " fish or " + l[1] + " coconuts. Fish you buy",
               min: 0, max: l[0], step: 0.1, value: +(l[0] / 2).toFixed(1), fmt: function (x) { return x.toFixed(1); } };
    });
    QB.widget(el, {
      title: "Eleven budgets: do your choices fit together?",
      sub: "Each line is $60 at the Island market: the most fish you could buy, or the most coconuts, or any mix between. " +
           "On each line, set how many fish you'd buy; the rest of the money buys coconuts. The game checks every pair " +
           "and chain of your choices for contradictions (GARP) and scores you with Afriat's efficiency index. There is no " +
           "right bundle, only choices that fit together or don't. Try Bo (a steady 60% on fish) or a random chooser.",
      panels: 2, height: 330,
      controls: controls,
      buttons: [
        { label: "Use my sliders", act: function (s) { s.mode = "mine"; } },
        { label: "Show Bo", act: function (s) { s.mode = "bo"; } },
        { label: "Show a random chooser", act: function (s) { s.mode = "random"; s.seed++; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "mine", fish, i;
        if (mode === "bo") fish = presetBo();
        else if (mode === "random") fish = presetRandom(s.seed);
        else fish = LINES.map(function (l, k) { return v["f" + k]; });
        var X = bundles(fish), bad = violations(X, 1), score = ccei(X), inCycle = {};
        bad.forEach(function (p) { inCycle[p[0]] = true; inCycle[p[1]] = true; });
        var a = g[0].axes({ x: [0, 13], y: [0, 13], title: "Your eleven choices", xlabel: "fish" });
        for (i = 0; i < N; i++) a.line([0, LINES[i][0]], [LINES[i][1], 0], { color: inCycle[i] ? RED : GREY_HINT, width: inCycle[i] ? 2 : 1.2, alpha: 0.8 });
        a.dots(X.map(function (x) { return x[0]; }), X.map(function (x) { return x[1]; }),
               { r: 5, color: function (k) { return inCycle[k] ? RED : (mode === "bo" ? BLUE : GOLD); } });
        for (i = 0; i < N; i++) a.text(X[i][0], X[i][1], String(i + 1), { dx: 7, dy: -7, size: 10, color: GREY_HINT });
        // the score against random choosers on the same lines (5,000 simulated: 97.5% violate, mean index 0.79)
        var b = g[1].axes({ x: [0, 2], y: [0.5, 1.0], title: "Afriat's index: yours against random choosers", xlabel: "" });
        b.bars([0.5, 1.5], [score, 0.789], 0.6, { color: function (k) { return [score >= 1 ? GREEN : GOLD, GREY_HINT][k]; } });
        b.text(0.5, score, fmt(score, 3), { align: "center", dy: -10, color: C.ink });
        b.text(1.5, 0.789, "0.789", { align: "center", dy: -10, color: GREY_HINT });
        b.text(0.5, 0.52, mode === "bo" ? "Bo" : (mode === "random" ? "random" : "you"), { align: "center", dy: -8, color: GREY_HINT });
        b.text(1.5, 0.52, "random, average", { align: "center", dy: -8, color: GREY_HINT });
        b.hline(0.95, { color: GREY_HINT, dash: [4, 4] });
        s.out = { score: score, pairs: bad.length, cycles: Object.keys(inCycle).length, mode: mode };
      },
      readout: function (v, s) {
        var o = s.out;
        return [
          ["choices shown", o.mode === "mine" ? "yours" : (o.mode === "bo" ? "Bo's" : "a random chooser's")],
          ["contradictions (pairs in GARP cycles)", String(o.pairs)],
          ["choices caught in a cycle", o.cycles + " of 11"],
          ["Afriat's efficiency index", fmt(o.score, 3) + (o.score >= 1 ? ": perfectly consistent" : ": shrink every budget to this share to remove them")],
          ["for comparison", "97.5% of random choosers on these lines violate GARP; Berkeley students averaged 0.954 on 50 budgets"],
        ];
      },
      note: "A choice on one line reveals that you prefer it to everything else you could afford there. A contradiction " +
            "is two choices each revealed better than the other, directly or through a chain (Warshall's algorithm finds " +
            "them). Afriat's index is the largest share of every budget at which the contradictions vanish. Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
})();
