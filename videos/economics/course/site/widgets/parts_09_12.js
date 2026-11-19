// Interactives for Act III, Markets (Parts 9-12).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1";
  var ANA = "#F29E8E", BO = "#9FB8F2", LENS = "#C9A0FF";

  // ---- Part 9: the invisible hand, proved ---------------------------------------------------------------------
  W.box = function (el) {
    // the Edgeworth box of Part 9 (explainer.economics.island, Part 9; explainer.economics.agora.ge): ten fish and ten
    // baskets of coconuts; Ana has 8 and 1.5 and spends 40% on fish, Bo has 2 and 8.5 and spends 60%
    var X = 10, Y = 10, aA = 0.4, aB = 0.6, eA = [8, 1.5], eB = [2, 8.5];
    function uA(x, y) { return aA * Math.log(x) + (1 - aA) * Math.log(y); }
    function uB(x, y) { return aB * Math.log(x) + (1 - aB) * Math.log(y); }
    function indA(u, x) { return Math.exp((u - aA * Math.log(x)) / (1 - aA)); }
    function indB(u, x) { return Y - Math.exp((u - aB * Math.log(X - x)) / (1 - aB)); } // in Ana's coordinates
    function cc(x) { var kA = aA / (1 - aA), kB = aB / (1 - aB); return kB * x * Y / (kA * (X - x) + kB * x); }
    var uA0 = uA(eA[0], eA[1]), uB0 = uB(eB[0], eB[1]);
    var pStar = (aA * eA[1] + aB * eB[1]) / ((1 - aA) * eA[0] + (1 - aB) * eB[0]);
    function demand(a, e, p) { var m = p * e[0] + e[1]; return [a * m / p, (1 - a) * m]; }
    function grid(n, lo, hi) { var o = []; for (var i = 0; i < n; i++) o.push(lo + (hi - lo) * i / (n - 1)); return o; }

    QB.widget(el, {
      title: "Trade in the box",
      sub: "Ana has 8 fish and 1.5 baskets of coconuts; Bo has 2 fish and 8.5 baskets. Propose a trade: how many fish " +
           "Ana gives, and how many baskets she gets. Both accept it only if it lands in the purple lens. Keep " +
           "trading until there is nothing left that both would want, or switch to prices and find the one that " +
           "clears both markets.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [
        { k: "give", label: "Fish Ana gives", min: 0, max: 7.5, step: 0.1, value: 2,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "get", label: "Baskets Ana gets", min: 0, max: 8, step: 0.1, value: 1,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "p", label: "Price of a fish, in baskets (price mode)", min: 0.3, max: 3, step: 0.01, value: 2,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [
        { label: "Propose a trade", act: function (s) { s.mode = "trade"; } },
        { label: "Set a price", act: function (s) { s.mode = "price"; } },
        { label: "Show the contract curve", act: function (s) { s.cc = !s.cc; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "trade";
        var b = g[0].axes({ x: [0, X], y: [0, Y], title: "Ana's fish across, her coconuts up (Bo's from the top right)",
                            xlabel: "Ana's fish" });
        var xs = grid(200, 0.05, X - 0.05), ia = [], ib = [], lx = [], lA = [], lB = [];
        xs.forEach(function (x) { ia.push(indA(uA0, x)); ib.push(indB(uB0, x)); });
        for (var i = 0; i < xs.length; i++) if (ia[i] < ib[i]) { lx.push(xs[i]); lA.push(ia[i]); lB.push(ib[i]); }
        if (lx.length > 1) b.area(lx, lB, lA, { color: LENS, alpha: 0.25 });
        b.line(xs, ia, { color: ANA, width: 2 });
        b.line(xs, ib, { color: BO, width: 2 });
        if (s.cc) { var cy = xs.map(cc); b.line(xs, cy, { color: GOLD, width: 2.2 }); }
        b.dots([eA[0]], [eA[1]], { r: 5, color: function () { return C.ink; } });
        var out = { mode: mode };
        if (mode === "trade") {
          var x = eA[0] - v.give, y = eA[1] + v.get, ok = x > 0 && y > 0 && x < X && y < Y;
          var dA = ok ? uA(x, y) - uA0 : -Infinity, dB = ok ? uB(X - x, Y - y) - uB0 : -Infinity;
          var onCC = ok && Math.abs(y - cc(x)) < 0.1;
          if (ok) {
            b.line(xs, xs.map(function (z) { return indA(uA(x, y), z); }), { color: ANA, width: 1.2, dash: [3, 3] });
            b.line(xs, xs.map(function (z) { return indB(uB(X - x, Y - y), z); }), { color: BO, width: 1.2, dash: [3, 3] });
          }
          b.dots([x], [y], { r: 6, color: function () { return dA > 0 && dB > 0 ? (onCC ? GREEN : GOLD) : RED; } });
          var c = g[1].axes({ x: [0.5, 2.5], y: [-40, 60], title: "Better off than at the start (%)", xlabel: "Ana, Bo" });
          var gA = ok ? 100 * (Math.exp(dA) - 1) : -40, gB = ok ? 100 * (Math.exp(dB) - 1) : -40;
          c.bars([1, 2], [gA, gB], 0.6, { color: function (j) { return [ANA, BO][j]; }, alpha: 0.85 });
          c.hline(0, { color: GREY_HINT });
          out.ok = ok; out.dA = gA; out.dB = gB; out.both = dA > 0 && dB > 0; out.onCC = onCC; out.x = x; out.y = y;
        } else {
          var p = v.p, dAp = demand(aA, eA, p), dBp = demand(aB, eB, p);
          var lxs = grid(2, 0, X), ly = lxs.map(function (z) { return eA[1] - p * (z - eA[0]); });
          b.line(lxs, ly, { color: C.ink, width: 1.6 });
          b.dots([dAp[0]], [dAp[1]], { r: 5, color: function () { return ANA; } });
          b.dots([X - dBp[0]], [Y - dBp[1]], { r: 5, color: function () { return BO; } });
          var ps = grid(120, 0.3, 3), z = ps.map(function (q) { return demand(aA, eA, q)[0] + demand(aB, eB, q)[0] - X; });
          var d = g[1].axes({ x: [0.3, 3], y: [-6, 6], title: "Excess demand for fish", xlabel: "price of a fish (baskets)" });
          d.line(ps, z, { color: GOLD, width: 2.2 });
          d.hline(0, { color: GREY_HINT });
          d.vline(p, { color: C.ink, dash: [3, 3] });
          var zz = dAp[0] + dBp[0] - X;
          d.dots([p], [zz], { r: 5, color: function () { return Math.abs(zz) < 0.05 ? GREEN : RED; } });
          out.p = p; out.z = zz; out.sell = eA[0] - dAp[0]; out.buy = dBp[0] - eB[0];
        }
        s.out = out;
      },
      readout: function (v, s) {
        var o = s.out;
        if (o.mode === "trade") {
          var verdict = !o.ok ? "impossible: there aren't that many goods" :
                        !o.both ? (o.dA <= 0 ? "Ana refuses" : "Bo refuses") :
                        o.onCC ? "both accept, and there is almost nothing more to gain" : "both accept, but more trade would help both";
          return [["verdict", verdict], ["Ana", (o.dA >= 0 ? "+" : "") + o.dA.toFixed(1) + "%"],
                  ["Bo", (o.dB >= 0 ? "+" : "") + o.dB.toFixed(1) + "%"]];
        }
        return [["Ana would sell", o.sell.toFixed(2) + " fish"], ["Bo would buy", o.buy.toFixed(2) + " fish"],
                ["excess demand for fish", o.z.toFixed(2) + (Math.abs(o.z) < 0.05 ? " (both markets clear)" : "")],
                ["the clearing price", Math.abs(o.z) < 0.05 ? "found: " + pStar.toFixed(3) + " baskets a fish" :
                                       "move the price toward where excess demand is zero"]];
      },
      note: "Percent better off is the proportional change in a bundle the trader likes as much. Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 10: the price maker ------------------------------------------------------------------------------
  W.ferry = function (el) {
    // Bo's ferry of Part 10 (explainer.economics.island, Part 10; videos/economics/econ10/compute.py, "ferry"): the
    // hundred islanders' values for a crossing that costs Bo nothing, sorted; and chapter 5's students
    // (q = 60 - 10p) and townsfolk (q = 100 - 5p) at a cost of $1 a crossing
    var V = [9.91, 9.90, 9.89, 9.76, 9.74, 9.65, 9.55, 9.55, 9.31, 9.23, 9.22, 9.01, 8.86, 8.83, 8.78, 8.72, 8.63, 8.59,
             8.48, 8.42, 8.20, 8.09, 8.09, 7.87, 7.79, 7.50, 7.35, 7.24, 7.24, 7.10, 6.84, 6.56, 6.31, 6.22, 6.17, 6.13,
             6.07, 6.03, 5.98, 5.98, 5.90, 5.84, 5.74, 5.70, 5.67, 5.65, 5.63, 5.59, 5.45, 5.34, 5.19, 5.13, 4.77, 4.74,
             4.71, 4.68, 4.55, 4.41, 4.36, 4.32, 4.19, 4.16, 4.11, 4.01, 3.76, 3.73, 3.65, 3.46, 3.33, 2.93, 2.88, 2.86,
             2.74, 2.71, 2.67, 2.65, 2.58, 2.53, 2.39, 2.25, 2.22, 2.11, 2.00, 1.97, 1.91, 1.86, 1.83, 1.82, 1.78, 1.59,
             1.59, 0.91, 0.84, 0.79, 0.52, 0.48, 0.30, 0.12, 0.10, 0.01];
    var TOTAL = V.reduce(function (a, b) { return a + b; }, 0);
    function at(f) {
      var n = 0, rev = 0, cs = 0;
      V.forEach(function (v) { if (v >= f) { n += 1; rev += f; cs += v - f; } });
      return { n: n, rev: rev, cs: cs, lost: TOTAL - rev - cs };
    }
    var fares = [], revs = [];
    for (var i = 0; i <= 1000; i++) { fares.push(i / 100); revs.push(at(i / 100).rev); }
    var best = 0; revs.forEach(function (r, j) { if (r > revs[best]) best = j; });
    // students and townsfolk, linear demands, cost 1
    var C1 = 1;
    function qS(p) { return Math.max(60 - 10 * p, 0); }
    function qT(p) { return Math.max(100 - 5 * p, 0); }
    function csS(p) { return 0.5 * qS(p) * (6 - Math.min(p, 6)); }
    function csT(p) { return 0.5 * qT(p) * (20 - Math.min(p, 20)); }
    function two(ps, pt) {
      var prof = (ps - C1) * qS(ps) + (pt - C1) * qT(pt), cs = csS(ps) + csT(pt);
      return { q: qS(ps) + qT(pt), prof: prof, cs: cs, w: prof + cs };
    }
    var one = two(10.5, 10.5);   // the best single fare serves only the townsfolk (chapter 5)

    QB.widget(el, {
      title: "Set the fare",
      sub: "A hundred islanders would cross on Bo's ferry; each crosses if the crossing is worth at least the fare, " +
           "and one more passenger costs Bo nothing. Find the fare that earns him most, and watch what it turns " +
           "away. Then let him charge each islander their value, or give students a fare of their own.",
      panels: 2, height: 330, weights: [1.15, 1],
      controls: [
        { k: "fare", label: "The fare ($)", min: 0, max: 10, step: 0.01, value: 4,
          fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "student", label: "The student fare ($, students and townsfolk)", min: 1, max: 6, step: 0.05, value: 6,
          fmt: function (x) { return "$" + x.toFixed(2); } },
      ],
      buttons: [
        { label: "One fare for everyone", act: function (s) { s.mode = "one"; } },
        { label: "Charge each islander their value", act: function (s) { s.mode = "each"; } },
        { label: "Students and townsfolk", act: function (s) { s.mode = "two"; } },
        { label: "Show Bo's best single fare", act: function (s) { s.best = !s.best; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "one", out = { mode: mode };
        if (mode !== "two") {
          var b = g[0].axes({ x: [0, 101], y: [0, 10.5], title: "What a crossing is worth to each islander ($)",
                              xlabel: "islanders, most eager first" });
          var xs = V.map(function (_, j) { return j + 1; });
          if (mode === "each") {
            b.bars(xs, V, 0.8, { color: function () { return GOLD; }, alpha: 0.9 });
            out.n = 100; out.rev = TOTAL; out.cs = 0; out.lost = 0;
          } else {
            var r = at(v.fare);
            b.bars(xs, V, 0.8, { color: function (j) { return V[j] >= v.fare ? GREEN : GREY_HINT; }, alpha: 0.85 });
            b.hline(v.fare, { color: GOLD, width: 2 });
            out.n = r.n; out.rev = r.rev; out.cs = r.cs; out.lost = r.lost;
          }
          var c = g[1].axes({ x: [0, 10], y: [0, 300], title: "Bo's takings ($)", xlabel: "the fare ($)" });
          c.line(fares, revs, { color: GOLD, width: 2.2 });
          if (mode === "one") c.dots([v.fare], [at(v.fare).rev], { r: 6, color: function () { return C.ink; } });
          if (s.best) {
            c.vline(fares[best], { color: GREEN, dash: [4, 3] });
            c.text(fares[best] + 0.15, 285, "best: $" + fares[best].toFixed(2), { color: GREEN });
          }
        } else {
          var ps = v.student, pt = v.fare, t = two(ps, pt);
          var d = g[0].axes({ x: [0, 110], y: [0, 21], title: "Fares ($): students (purple), townsfolk (pink)",
                              xlabel: "crossings" });
          var pp = []; for (var k = 0; k <= 200; k++) pp.push(k / 10);
          d.line(pp.map(qS), pp, { color: LENS, width: 2 });
          d.line(pp.map(qT), pp, { color: ANA, width: 2 });
          d.hline(C1, { color: GREY_HINT, dash: [3, 3] });
          d.dots([qS(ps)], [ps], { r: 6, color: function () { return LENS; } });
          d.dots([qT(pt)], [pt], { r: 6, color: function () { return ANA; } });
          var e = g[1].axes({ x: [0.4, 3.6], y: [0, 820], title: "One fare ($10.50) against yours",
                              xlabel: "Bo's profit, passengers' surplus, total" });
          e.bars([0.8, 1.8, 2.8], [one.prof, one.cs, one.w], 0.35, { color: function () { return GREY_HINT; }, alpha: 0.8 });
          e.bars([1.2, 2.2, 3.2], [t.prof, t.cs, t.w], 0.35,
                 { color: function (j) { return [GOLD, GREEN, BO][j]; }, alpha: 0.9 });
          out.t = t; out.ps = ps; out.pt = pt;
        }
        s.out = out;
      },
      readout: function (v, s) {
        var o = s.out;
        if (o.mode === "two") {
          var t = o.t;
          return [["crossings", t.q.toFixed(1) + " (one fare: 47.5)"],
                  ["Bo's profit", "$" + t.prof.toFixed(2) + " (one fare: $451.25)"],
                  ["passengers' surplus", "$" + t.cs.toFixed(2) + " (one fare: $225.63)"],
                  ["total", "$" + t.w.toFixed(2) + (t.w > one.w + 0.01 ? ": better than one fare" : "")],
                  ["hint", Math.abs(o.ps - 3.5) < 0.03 && Math.abs(o.pt - 10.5) < 0.03 ?
                           "each group at its own monopoly price: the best Bo can do" :
                           "each group's best fare is halfway between cost and its top price"]];
        }
        var rows = [["islanders who cross", String(o.n)], ["Bo's takings", "$" + o.rev.toFixed(2)],
                    ["passengers' surplus", "$" + o.cs.toFixed(2)],
                    ["value lost (crossings worth more than they cost, not made)", "$" + o.lost.toFixed(2)]];
        if (o.mode === "each") rows.push(["verdict", "all the value, to Bo: nothing lost, nothing left to passengers"]);
        else if (o.rev >= revs[best] - 0.005) rows.push(["verdict", "you found Bo's best fare"]);
        return rows;
      },
      note: "The values are those of the film's hundred islanders, rounded to the cent. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };
})();
