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
  // ---- Part 36: gravity ---------------------------------------------------------------------------------------
  W.gravity = function (el) {
    // The gravity equation of Part 36 (explainer.economics.agora.trade: gravity_ols, ppml_fe), with the least-squares
    // GDP elasticities estimated on CEPII's 2019 data (1.32 for the exporter, 0.97 for the importer) and a distance
    // elasticity the reader chooses.  The prediction is scaled to Spain's exports to Portugal in 2019 ($26.0bn),
    // so the reader can compare it with Spain's real exports to Japan ($3.2bn) and Brazil ($3.0bn).
    var PINK = "#E8A0B4", TEAL = "#7FD1B9", GOLDC = "#F2C14E";
    var base = { gdp_o: 1.39, gdp_d: 0.24, dist: 596, trade: 26.0 };     // Spain to Portugal, 2019
    var real = [["Portugal", 0.24, 596, 26.0], ["Japan", 5.12, 10632, 3.2], ["Brazil", 1.87, 7791, 3.0]];
    function f1(x) { return x.toFixed(2); }
    function predict(gd, dist, v) {
      return base.trade * Math.pow(gd / base.gdp_d, 0.97) * Math.pow(dist / base.dist, -v.delta);
    }
    QB.widget(el, {
      title: "Gravity",
      sub: "Spain's exports to a partner, predicted from the partner's size and distance. Left: the prediction for " +
           "your partner against distance. Right: what the same equation says for Portugal, Japan and Brazil, " +
           "against what Spain actually sold them in 2019.",
      panels: 2, height: 270,
      controls: [
        { k: "gdp", label: "The partner's GDP, $ trillion", min: 0.1, max: 25, step: 0.1, value: 2, fmt: f1 },
        { k: "dist", label: "Distance from Spain, km", min: 300, max: 18000, step: 100, value: 3000,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "delta", label: "Distance elasticity", min: 0.3, max: 2.0, step: 0.05, value: 1.0, fmt: f1 },
      ],
      draw: function (g, v, st) {
        var ds = [], ps = [], k;
        for (k = 0; k <= 60; k++) {
          var d = 300 * Math.pow(60, k / 60);
          ds.push(Math.log10(d)); ps.push(predict(v.gdp, d, v));
        }
        var me = predict(v.gdp, v.dist, v), top = Math.max(30, me * 1.2);
        var a = g[0].axes({ x: [Math.log10(300), Math.log10(18000)], y: [0, top], title: "Predicted exports, $bn",
                            xlabel: "distance (log10 km)" });
        a.line(ds, ps.map(function (p) { return Math.min(p, top); }), { color: GOLDC, width: 2.5 });
        a.dots([Math.log10(v.dist)], [Math.min(me, top)], { color: PINK, r: 6 });
        var b = g[1].axes({ x: [0, 3.6], y: [0, 40], title: "Actual (bars) and predicted (dots), $bn", xlabel: "" });
        b.bars([0.6, 1.8, 3.0], real.map(function (r) { return r[3]; }), 0.6, { color: TEAL });
        b.dots([0.6, 1.8, 3.0], real.map(function (r) { return Math.min(predict(r[1], r[2], v), 40); }),
               { color: PINK, r: 5 });
        real.forEach(function (r, i) { b.text(0.6 + 1.2 * i, 37, r[0], { align: "center", size: 11 }); });
        st.me = me;
        st.err = real.map(function (r) { return predict(r[1], r[2], v) / r[3]; });
      },
      readout: function (v, st) {
        return [["predicted exports to your partner", "$" + st.me.toFixed(1) + "bn"],
                ["predicted over actual: Portugal, Japan, Brazil", st.err.map(function (x) { return x.toFixed(2); })
                  .join(", ")],
                ["doubling the distance multiplies trade by", Math.pow(2, -v.delta).toFixed(2)]];
      },
      note: "Gravity as estimated in Part 36, chapter 4, on CEPII's 2019 data (least squares: distance -1.18; PPML " +
            "with fixed effects: -0.71). Computed in your browser; nothing you do here is stored or sent.",
    });
  };

  W.schelling = function (el) {
    // Schelling's checkerboard of Part 37 (explainer.economics.agora.city.schelling): two kinds of coin on a board
    // whose edges wrap; a coin is content if at least the chosen share of its occupied neighbours (of eight) are its
    // own kind; discontented coins, in random order, move to a random empty square where they would be content.
    var TEALC = "#7FD1B9", GOLDC = "#F2C14E", N = 30;
    function rng(seed) {
      var a = seed >>> 0;
      return function () {
        a = (a + 0x6D2B79F5) >>> 0;
        var t = a;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    }
    function nb(g, r, c, kind) {
      var own = 0, tot = 0, dr, dc;
      for (dr = -1; dr <= 1; dr++) {
        for (dc = -1; dc <= 1; dc++) {
          if (!dr && !dc) continue;
          var v = g[((r + dr + N) % N) * N + ((c + dc + N) % N)];
          if (v) { tot++; if (v === kind) own++; }
        }
      }
      return [own, tot];
    }
    function likeShare(g) {
      var s = 0, n = 0, i;
      for (i = 0; i < N * N; i++) {
        if (!g[i]) continue;
        var o = nb(g, Math.floor(i / N), i % N, g[i]);
        if (o[1]) { s += o[0] / o[1]; n++; }
      }
      return n ? s / n : 0;
    }
    function run(th, empty, seed) {
      var R = rng(seed), g = new Array(N * N).fill(0), idx = [], i, k;
      for (i = 0; i < N * N; i++) idx.push(i);
      for (i = idx.length - 1; i > 0; i--) { k = Math.floor(R() * (i + 1)); var t = idx[i]; idx[i] = idx[k]; idx[k] = t; }
      var agents = N * N - Math.round(empty * N * N);
      for (i = 0; i < agents; i++) g[idx[i]] = i < agents / 2 ? 1 : 2;
      var like = [likeShare(g)], rounds = 0, settled = false;
      for (var round = 0; round < 40; round++) {
        var unhappy = [];
        for (i = 0; i < N * N; i++) {
          if (!g[i]) continue;
          var o = nb(g, Math.floor(i / N), i % N, g[i]);
          if (o[1] && o[0] / o[1] < th) unhappy.push(i);
        }
        if (!unhappy.length) { settled = true; break; }
        for (i = unhappy.length - 1; i > 0; i--) {
          k = Math.floor(R() * (i + 1)); var u = unhappy[i]; unhappy[i] = unhappy[k]; unhappy[k] = u;
        }
        unhappy.forEach(function (cell) {
          var kind = g[cell];
          var me = nb(g, Math.floor(cell / N), cell % N, kind);
          if (!me[1] || me[0] / me[1] >= th) return;
          g[cell] = 0;
          var ok = [];
          for (var j = 0; j < N * N; j++) {
            if (g[j] || j === cell) continue;
            var q = nb(g, Math.floor(j / N), j % N, kind);
            if (!q[1] || q[0] / q[1] >= th) ok.push(j);
          }
          if (!ok.length) { g[cell] = kind; return; }
          g[ok[Math.floor(R() * ok.length)]] = kind;
        });
        rounds = round + 1;
        like.push(likeShare(g));
      }
      return { g: g, like: like, rounds: rounds, settled: settled };
    }
    QB.widget(el, {
      title: "Schelling's checkerboard",
      sub: "Two kinds of coin on a 30 by 30 board. Each is content if at least the share you choose of its " +
           "neighbours are its own kind; otherwise it moves. Left: the board when it stops. Right: the share of a " +
           "coin's neighbours who are its own kind, round by round.",
      panels: 2, height: 280,
      controls: [
        { k: "th", label: "Share of like neighbours each coin wants", min: 0, max: 0.8, step: 0.05, value: 0.35,
          fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "empty", label: "Share of squares empty", min: 0.05, max: 0.4, step: 0.05, value: 0.1,
          fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "seed", label: "Another board (seed)", min: 1, max: 20, step: 1, value: 3,
          fmt: function (x) { return x.toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var res = run(v.th, v.empty, v.seed), xs1 = [], ys1 = [], xs2 = [], ys2 = [], i;
        for (i = 0; i < N * N; i++) {
          var x = i % N, y = N - 1 - Math.floor(i / N);
          if (res.g[i] === 1) { xs1.push(x); ys1.push(y); } else if (res.g[i] === 2) { xs2.push(x); ys2.push(y); }
        }
        var a = g[0].axes({ x: [-1, N], y: [-1, N], title: "the board when it stops", xlabel: "" });
        a.dots(xs1, ys1, { color: TEALC, r: 3.2 });
        a.dots(xs2, ys2, { color: GOLDC, r: 3.2 });
        var b = g[1].axes({ x: [0, Math.max(5, res.like.length - 1)], y: [0.4, 1], title: "like neighbours",
                            xlabel: "round" });
        b.line(res.like.map(function (_, k) { return k; }), res.like, { color: GOLDC, width: 2.5 });
        b.hline(v.th, { color: TEALC });
        st.res = res;
      },
      readout: function (v, st) {
        var r = st.res;
        return [["like neighbours: at the start, at the end", Math.round(100 * r.like[0]) + "%, " +
                 Math.round(100 * r.like[r.like.length - 1]) + "%"],
                ["rounds", r.settled ? r.rounds + " (everyone content)" : "40 and still moving"],
                ["what each coin asked for", Math.round(100 * v.th) + "%"]];
      },
      note: "The model of Part 37, chapter 1; Agora's version is explainer/economics/agora/city.py. A possibility, not " +
            "a diagnosis: prices, laws and discrimination sort people too. Computed in your browser; nothing you do " +
            "here is stored or sent.",
    });
  };
})();
