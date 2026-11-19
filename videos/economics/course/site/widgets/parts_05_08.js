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

  // ---- Part 6: demand -------------------------------------------------------------------------------------------
  W.demand = function (el) {
    // Bo (Part 5): Cobb-Douglas, 60% on fish, coconuts $6, his usual $60, fish usually $10.
    // The Play-it household (Part 6): 14,000 calories a week; coconuts 1,400 calories, usually $1.20; fish 700
    // calories at $2; taste beta log(s - 3) + (1 - beta) log f with beta = 1/6; its usual $21.
    // (explainer.economics.agora.demand: CobbDouglas and Diet)
    var PURPLE = "#C9A0FF", ORANGE = "#F28C6F", CAL = "#7BD88F", NEWB = "#F2A65A";
    var CS = 1400, CF = 700, NEED = 14000, BETA = 1 / 6, S0 = 3, PF = 2;
    function diet(ps, m) {
      if (m * CS / ps <= NEED) return { s: m / ps, f: 0, zone: "deprived" };
      var free = m - ps * S0, s, f;
      if (free > 0) { s = S0 + BETA * free / ps; f = (1 - BETA) * free / PF; } else { s = m / ps; f = 0; }
      if (CS * s + CF * f >= NEED) return { s: s, f: f, zone: "standard" };
      var D = PF * CS - ps * CF;
      return { s: (NEED * PF - m * CF) / D, f: (m * CS - NEED * ps) / D, zone: "subsistence" };
    }
    function bo(px, m) { return { f: 0.6 * m / px, c: 0.4 * m / 6 }; }
    QB.widget(el, {
      title: "One price, two effects",
      sub: "Move a price and see Slutsky's split: the substitution effect (give the household just enough money to buy " +
           "its old basket at the new prices, and see what it buys instead) and the income effect (the rest). Bo, from " +
           "Part 5, always spends 60% on fish. The Play-it household must eat 14,000 calories a week from coconuts " +
           "(cheap calories) and fish (taste): in its middle zone a dearer coconut means more coconuts.",
      panels: 2, height: 330,
      controls: [
        { k: "dp", label: "Change in the good's price (%)", min: -60, max: 80, step: 1, value: 25,
          fmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(0) + "%"; } },
        { k: "mi", label: "Money, as a share of the household's usual budget (%)", min: 40, max: 170, step: 1, value: 100,
          fmt: function (x) { return x.toFixed(0) + "%"; } },
      ],
      buttons: [
        { label: "The Play-it household (coconuts)", act: function (s) { s.mode = "poor"; } },
        { label: "Bo (fish)", act: function (s) { s.mode = "bo"; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "poor", k = 1 + v.dp / 100, i;
        var a = g[0].axes({ x: [0, mode === "poor" ? 14 : 10], y: [0, mode === "poor" ? 20 : 14],
                            title: mode === "poor" ? "A week's food: fish across, coconuts up"
                                                                            : "Bo's week: fish across, coconuts up",
                            xlabel: "fish" });
        var d, A, Cb, B, total, sub, inc, p0, p1, m, zone = "";
        if (mode === "poor") {
          m = 21 * v.mi / 100; p0 = 1.2; p1 = 1.2 * k;
          a.line([0, 14], [NEED / CS, (NEED - CF * 14) / CS], { color: CAL, width: 2 });
          a.line([0, m / PF], [m / p0, 0], { color: GOLD, width: 1.6 });
          a.line([0, m / PF], [m / p1, 0], { color: NEWB, width: 2.2 });
          var b0 = diet(p0, m), b1 = diet(p1, m), bc = diet(p1, p1 * b0.s + PF * b0.f);
          A = [b0.f, b0.s]; Cb = [b1.f, b1.s]; B = [bc.f, bc.s]; zone = b0.zone;
          total = b1.s - b0.s; sub = bc.s - b0.s; inc = b1.s - bc.s;
          var ps = [], qs = [], zs = [];
          for (i = 0; i <= 200; i++) { var pp = 0.45 + 1.85 * i / 200, bb = diet(pp, m); ps.push(pp); qs.push(bb.s); zs.push(bb.zone); }
          d = g[1].axes({ x: [0, 14], y: [0.4, 2.4], title: "Coconut demand at this money (price up the side)",
                          xlabel: "coconuts a week" });
          ["standard", "subsistence", "deprived"].forEach(function (z) {
            var xs = [], ys = [];
            for (var j = 0; j < ps.length; j++) { if (zs[j] === z) { xs.push(qs[j]); ys.push(ps[j]); } else if (xs.length) { xs.push(NaN); ys.push(NaN); } }
            d.line(xs, ys, { color: z === "subsistence" ? RED : (z === "standard" ? BLUE : GREY_HINT), width: 2.6 });
          });
          d.dots([b0.s, b1.s], [p0, p1], { r: 5, color: function (j) { return j ? NEWB : C.ink; } });
          d.text(0.4, 2.3, "red: the subsistence zone, where demand slopes up", { size: 10.5, color: RED });
        } else {
          m = 60 * v.mi / 100; p0 = 10; p1 = 10 * k;
          a.line([0, m / p0], [m / 6, 0], { color: GOLD, width: 1.6 });
          a.line([0, m / p1], [m / 6, 0], { color: NEWB, width: 2.2 });
          var c0 = bo(p0, m), c1 = bo(p1, m), cc = bo(p1, p1 * c0.f + 6 * c0.c);
          A = [c0.f, c0.c]; Cb = [c1.f, c1.c]; B = [cc.f, cc.c];
          total = c1.f - c0.f; sub = cc.f - c0.f; inc = c1.f - cc.f;
          // welfare: CV = m - e(p1, u0) for Cobb-Douglas (positive when the change makes him better off)
          var e1 = m * Math.pow(p1 / p0, 0.6);
          s.cv = m - e1;
          var xs2 = [], ys2 = [];
          for (i = 0; i <= 200; i++) { var p = 2 + 18 * i / 200; xs2.push(0.6 * m / p); ys2.push(p); }
          d = g[1].axes({ x: [0, 14], y: [0, 20], title: "Bo's demand for fish at this money (price up the side)",
                          xlabel: "fish a week" });
          d.line(xs2, ys2, { color: BLUE, width: 2.6 });
          d.dots([c0.f, c1.f], [p0, p1], { r: 5, color: function (j) { return j ? NEWB : C.ink; } });
        }
        a.line([A[0], B[0]], [A[1], B[1]], { color: PURPLE, width: 4 });
        a.line([B[0], Cb[0]], [B[1], Cb[1]], { color: ORANGE, width: 4 });
        a.dots([A[0], B[0], Cb[0]], [A[1], B[1], Cb[1]], { r: 5, color: function (j) { return [C.ink, PURPLE, NEWB][j]; } });
        a.text(A[0], A[1], "old", { dx: 7, dy: -9, size: 10.5, color: GREY_HINT });
        a.text(Cb[0], Cb[1], "new", { dx: 7, dy: 10, size: 10.5, color: NEWB });
        s.out = { mode: mode, total: total, sub: sub, inc: inc, zone: zone, p0: p0, p1: p1, m: m };
      },
      readout: function (v, s) {
        var o = s.out, good = o.mode === "poor" ? "coconuts" : "fish";
        var rows = [
          ["price of " + good, "$" + o.p0.toFixed(2) + " \u2192 $" + o.p1.toFixed(2) + ", money $" + o.m.toFixed(2)],
          ["change in " + good + " bought", fmt(o.total, 2) + (o.total > 0 && o.p1 > o.p0 ? "  (more, though dearer: Giffen)" : "")],
          ["substitution (purple)", fmt(o.sub, 2)],
          ["income (orange)", fmt(o.inc, 2)],
        ];
        if (o.mode === "poor") rows.push(["zone at the old price", o.zone + (o.zone === "subsistence" ? ": the calorie line binds, so there is no room to substitute" : "")]);
        else rows.push(["compensating variation", (s.cv >= 0 ? "he could give up $" : "he would need $") + Math.abs(s.cv).toFixed(2) + " to be as well off as before"]);
        return rows;
      },
      note: "Slutsky's compensation: just enough money to buy the old basket at the new prices; the substitution effect " +
            "is the move that money makes possible, the income effect the rest. In the subsistence zone the household is " +
            "pinned where its budget and calorie lines cross, so with that money it simply buys the old basket again: the " +
            "whole response is an income effect. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 7: time and risk ------------------------------------------------------------------------------------
  W.risk = function (el) {
    // Bernoulli's game (1738): heads on toss k pays 2^(k-1) dollars, chance 2^-k; cut off after n tosses, the
    // maximum prize 2^n if no heads (Hayden and Platt 2009).  Ana's boat (Part 7, chapter 6): wealth $300, $150 of it
    // the boat, a storm one year in ten, cover at the expected payout times (1 + loading).
    // (explainer.economics.agora.risk: stpetersburg_price, optimal_cover)
    var PURPLE = "#C9A0FF", CORAL = "#F28C6F", TEAL = "#5BD1C4";
    function u(x, g) { return Math.abs(g - 1) < 1e-9 ? Math.log(x) : Math.pow(x, 1 - g) / (1 - g); }
    function game(n) {
      var ps = [], xs = [], k;
      for (k = 1; k <= n; k++) { ps.push(Math.pow(0.5, k)); xs.push(Math.pow(2, k - 1)); }
      ps.push(Math.pow(0.5, n)); xs.push(Math.pow(2, n));
      return { p: ps, x: xs };
    }
    function ev(gm) { var e = 0; for (var i = 0; i < gm.p.length; i++) e += gm.p[i] * gm.x[i]; return e; }
    function price(w, g, gm) {
      if (g < 1e-6) return ev(gm);
      function gap(c) {
        var t = 0;
        for (var i = 0; i < gm.p.length; i++) t += gm.p[i] * u((w - c + gm.x[i]) / w, g);
        return t - u(1, g);
      }
      var lo = 0, hi = w + 0.999, j;
      for (j = 0; j < 80; j++) { var mid = (lo + hi) / 2; if (gap(mid) > 0) lo = mid; else hi = mid; }
      return (lo + hi) / 2;
    }
    function boat(g, ld) {
      var W0 = 300, L = 150, P = 0.1, prem = (1 + ld) * P * L, best = 0, bq = 0, qs = [], eus = [], i;
      for (i = 0; i <= 200; i++) {
        var q = i / 200, e = (1 - P) * u((W0 - prem * q) / W0, g) + P * u((W0 - prem * q - L + q * L) / W0, g);
        qs.push(q); eus.push(e);
        if (i === 0 || e > best) { best = e; bq = q; }
      }
      var euU = (1 - P) * u(1, g) + P * u((W0 - L) / W0, g), ce;
      if (Math.abs(g - 1) < 1e-9) ce = W0 * Math.exp(euU); else ce = W0 * Math.pow(euU * (1 - g), 1 / (1 - g));
      return { q: qs, eu: eus, cover: bq, prem: prem, maxp: W0 - ce };
    }
    QB.widget(el, {
      title: "What is a gamble worth?",
      sub: "Bernoulli's game pays $1 if the first toss is heads and doubles the prize with every tail; its expected prize " +
           "grows without limit as more tosses are allowed. Choose how fast your utility bends (gamma; 1 is Bernoulli's " +
           "logarithm, 0 is risk neutral) and your wealth, and see what the game is worth to you. Or insure Ana's boat " +
           "at a price you set.",
      panels: 2, height: 330,
      controls: [
        { k: "g", label: "Risk aversion, gamma", min: 0, max: 6, step: 0.05, value: 1,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "lw", label: "Your wealth (Bernoulli's game)", min: 1, max: 7, step: 0.05, value: 3,
          fmt: function (x) { return "$" + Math.round(Math.pow(10, x)).toLocaleString("en-US"); } },
        { k: "n", label: "Tosses allowed (Bernoulli's game)", min: 1, max: 40, step: 1, value: 40,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "ld", label: "Insurer's loading on the fair price (Ana's boat, %)", min: 0, max: 100, step: 1, value: 20,
          fmt: function (x) { return x.toFixed(0) + "%"; } },
      ],
      buttons: [
        { label: "Bernoulli's game", act: function (s) { s.mode = "game"; } },
        { label: "Ana's boat", act: function (s) { s.mode = "boat"; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "game", i;
        if (mode === "game") {
          var gm = game(v.n), w = Math.pow(10, v.lw), pr = price(w, v.g, gm), e = ev(gm);
          var a = g[0].axes({ x: [1, 7], y: [0, 24], title: "The game's price against wealth (log scale)",
                              xlabel: "wealth: 10 to 10,000,000 dollars (log10)" });
          var xs = [], ys = [], ys2 = [];
          for (i = 0; i <= 60; i++) {
            var lw = 1 + 6 * i / 60; xs.push(lw);
            ys.push(Math.min(24, price(Math.pow(10, lw), v.g, gm)));
            ys2.push(Math.min(24, price(Math.pow(10, lw), 1, gm)));
          }
          a.line(xs, ys2, { color: GREY_HINT, width: 1.4, dash: [3, 3] });
          a.line(xs, ys, { color: PURPLE, width: 2.6 });
          a.hline(1.75, { color: GREEN, dash: [2, 3] });
          a.text(1.1, 2.6, "what students paid with real money: $1.75", { size: 10.5, color: GREEN });
          a.dots([v.lw], [Math.min(24, pr)], { r: 5, color: function () { return GOLD; } });
          var b = g[1].axes({ x: [0.5, Math.min(v.n, 14) + 0.5], y: [0, 0.55], title: "The prizes: chance of each",
                              xlabel: "toss of the first heads" });
          var kx = [], ky = [];
          for (i = 1; i <= Math.min(v.n, 14); i++) { kx.push(i); ky.push(Math.pow(0.5, i)); }
          b.bars(kx, ky, { color: GOLD, alpha: 0.8 });
          b.text(1, 0.52, "half the games pay $1: the median prize is $1 to $2", { size: 10.5, color: C.ink });
          s.out = { mode: mode, w: w, pr: pr, e: e, n: v.n, g: v.g };
        } else {
          var o = boat(v.g, v.ld / 100);
          var c = g[0].axes({ x: [0, 1], y: [0, 1.05], title: "Ana's expected utility against her cover (scaled)",
                              xlabel: "share of the boat insured" });
          var lo = Math.min.apply(null, o.eu), hi = Math.max.apply(null, o.eu);
          c.line(o.q, o.eu.map(function (e) { return (e - lo) / (hi - lo + 1e-12); }), { color: TEAL, width: 2.6 });
          c.vline(o.cover, { color: GOLD, dash: [2, 3] });
          var f = g[1].axes({ x: [0, 100], y: [0, 1.05], title: "Best cover against the loading, at this gamma",
                              xlabel: "loading on the fair price (%)" });
          var lx = [], ly = [];
          for (i = 0; i <= 50; i++) { var ld = 2 * i; lx.push(ld); ly.push(boat(v.g, ld / 100).cover); }
          f.line(lx, ly, { color: CORAL, width: 2.6 });
          f.dots([v.ld], [o.cover], { r: 5, color: function () { return GOLD; } });
          s.out = { mode: mode, o: o, g: v.g, ld: v.ld };
        }
      },
      readout: function (v, s) {
        var o = s.out;
        if (o.mode === "game") {
          return [
            ["expected prize, " + o.n + " tosses allowed", "$" + o.e.toFixed(2) + (o.n >= 30 ? "  (and without limit as tosses are added)" : "")],
            ["what the game is worth to you", "$" + o.pr.toFixed(2) + (o.g < 1e-6 ? "  (risk neutral: the expected prize)" : "")],
            ["Bernoulli's log price at $1,000 and $1 million", "$5.97 and $10.94 (no cut-off)"],
            ["what people bid (Hayden and Platt 2009)", "median $1.75 with real money (20 students), $1.50 asked hypothetically (220)"],
          ];
        }
        return [
          ["the price of full cover", "$" + o.o.prem.toFixed(2) + " a year (fair: $15)"],
          ["Ana's best cover", (100 * o.o.cover).toFixed(1) + "% of the boat" + (o.ld === 0 ? "  (fair odds: full cover, Mossin 1968)" : "")],
          ["the most she would pay for full cover", "$" + o.o.maxp.toFixed(2) + " at gamma " + o.g.toFixed(2)],
        ];
      },
      note: "The game's prizes are paid in dollars added to your wealth, and the price is the most you could pay and be no " +
            "worse off, on expected utility with the power function (gamma) or the logarithm (gamma = 1). The grey dashed " +
            "curve is Bernoulli's logarithm, for comparison. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
