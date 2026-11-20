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
  // ---- Part 35: comparative advantage ---------------------------------------------------------------------------
  W.fournumbers = function (el) {
    // Ricardo's model of Part 35 (explainer.economics.agora.trade: ricardo_trade).  Two countries, two goods (fish and
    // cloth), labour only; hours per unit a1, a2 at home and b1, b2 abroad; half of spending on each good.  The world
    // price of cloth in fish is (1 - beta)/beta times world fish over world cloth with full specialization, clamped
    // to the two autarky prices; a country whose autarky price it is makes both goods.
    var TEAL = "#7FD1B9", GOLDC = "#F2C14E", PINK = "#E8A0B4";
    function solve(v) {
      var aH = [v.a1, v.a2], aF = [v.b1, v.b2], LH = 600 * v.size, LF = 600, beta = 0.5;
      var pH = aH[1] / aH[0], pF = aF[1] / aF[0];
      var flip = pH > pF;
      if (flip) { var t = aH; aH = aF; aF = t; var u = LH; LH = LF; LF = u; var x = pH; pH = pF; pF = x; }
      var Q2 = LH / aH[1], Q1 = LF / aF[0];
      var p = Math.min(Math.max((1 - beta) / beta * Q1 / Q2, pH), pF);
      var qH = [0, Q2], qF = [Q1, 0];
      if (p === pH && pH < pF) {          // home also makes good 1: p Q2 = Q1 (equal shares)
        var h = (Q1 + LH / aH[0]) / (p / aH[1] + 1 / aH[0]);
        qH = [(LH - h) / aH[0], h / aH[1]];
      } else if (p === pF && pH < pF) {
        var g = (Q2 * p - LF / aF[0]) / (-(p / aF[1]) - 1 / aF[0]);
        qF = [(LF - g) / aF[0], g / aF[1]];
      }
      function out(q, a, L) {
        var inc = q[0] + p * q[1], c1 = beta * inc, c2 = (1 - beta) * inc / p;
        var aut = Math.pow(beta * L / a[0], beta) * Math.pow((1 - beta) * L / a[1], 1 - beta);
        return { q: q, c: [c1, c2], gain: Math.pow(c1, beta) * Math.pow(c2, 1 - beta) / aut - 1, wage: inc / L };
      }
      var H = out(qH, aH, LH), F = out(qF, aF, LF);
      if (flip) { var tt = H; H = F; F = tt; }
      return { p: p, pH: v.a2 / v.a1, pF: v.b2 / v.b1, H: H, F: F, clothIsland: flip ? false : true };
    }
    function f1(x) { return x.toFixed(1); }
    QB.widget(el, {
      title: "Four numbers",
      sub: "Set the hours each island needs for a fish and for a bolt of cloth, and how big the Island is. Left: " +
           "what a bolt costs each island in fish, and the world price that trade settles on. Right: each " +
           "island's gain in " +
           "consumption from trading.",
      panels: 2, height: 270,
      controls: [
        { k: "a1", label: "The Island: hours per fish", min: 1, max: 6, step: 0.5, value: 3, fmt: f1 },
        { k: "a2", label: "The Island: hours per bolt", min: 1, max: 12, step: 0.5, value: 6, fmt: f1 },
        { k: "b1", label: "The Archipelago: hours per fish", min: 1, max: 6, step: 0.5, value: 1, fmt: f1 },
        { k: "b2", label: "The Archipelago: hours per bolt", min: 1, max: 12, step: 0.5, value: 4, fmt: f1 },
        { k: "size", label: "The Island's hours, relative", min: 0.25, max: 4, step: 0.25, value: 2,
          fmt: function (x) { return x.toFixed(2) + "x"; } },
      ],
      draw: function (g, v, st) {
        var r = solve(v);
        var top = Math.max(r.pH, r.pF) * 1.4;
        var a = g[0].axes({ x: [0, 3], y: [0, top], title: "A bolt of cloth, in fish", xlabel: "" });
        a.bars([0.6, 1.5], [r.pH, r.pF], 0.5, { color: function (j) { return j ? GOLDC : TEAL; } });
        a.hline(r.p, { color: PINK, width: 2 });
        a.text(0.6, r.pH + top * 0.05, "the Island alone " + r.pH.toFixed(2), { align: "center", size: 11 });
        a.text(1.5, r.pF + top * 0.05, "the Archipelago " + r.pF.toFixed(2), { align: "center", size: 11 });
        a.text(2.1, r.p + top * 0.04, "with trade " + r.p.toFixed(2), { color: PINK, size: 11 });
        var gH = 100 * r.H.gain, gF = 100 * r.F.gain, m = Math.max(5, gH, gF) * 1.3;
        var b = g[1].axes({ x: [0, 3], y: [0, m], title: "Gain from trade, %", xlabel: "" });
        b.bars([0.8, 2.0], [gH, gF], 0.6, { color: function (j) { return j ? GOLDC : TEAL; } });
        b.text(0.8, gH + m * 0.05, "the Island +" + gH.toFixed(1) + "%", { align: "center", size: 11 });
        b.text(2.0, gF + m * 0.05, "the Archipelago +" + gF.toFixed(1) + "%", { align: "center", size: 11 });
        st.r = r;
      },
      readout: function (v, st) {
        var r = st.r, same = Math.abs(r.pH - r.pF) < 1e-9;
        var who = same ? "no one: the costs are the same, so there is nothing to trade" :
          (r.pH < r.pF ? "the Island makes cloth, the Archipelago fish" :
                         "the Island makes fish, the Archipelago cloth");
        var better = (v.a1 < v.b1 && v.a2 < v.b2) ? "the Island" : ((v.b1 < v.a1 && v.b2 < v.a2) ? "the Archipelago" :
          "neither");
        return [["who makes what", who],
                ["better at both goods", better + " (it does not decide the pattern)"],
                ["wages, fish per hour", "the Island " + r.H.wage.toFixed(2) + ", the Archipelago " +
                  r.F.wage.toFixed(2)]];
      },
      note: "Ricardo (1817), as computed in Part 35, chapter 1: with 3 and 6 hours on the Island, 1 and 4 in the " +
            "Archipelago and the Island twice as large, the price is 3 fish a bolt and both gain (22% and 15%). " +
            "Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
