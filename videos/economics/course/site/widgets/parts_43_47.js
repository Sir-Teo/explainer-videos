// Interactives for Act IX, The Fields (Parts 43-50, first block: 43-47).  Each is a game the reader plays (the kit:
// 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", TEAL = "#7FD1B9", PINK = "#E8A0B4", GREY = "#9AA3B2";

  // ---- Part 43: measuring market power ---------------------------------------------------------------------------
  W.merger = function (el) {
    // The merger game of Part 43 (explainer.economics.agora.io: nested_shares, bertrand, merger): five cereals in three
    // nests (sweet, nutty, bran), each with its own owner, nested logit with price coefficient 1 and nesting
    // parameter sigma; Bertrand-Nash prices by damped iteration on the first-order conditions,
    // p - c = -(Omega o J)^-1 s, with J[j][k] = ds_k/dp_j.
    var NAMES = ["Sun Flakes", "Honey Puffs", "Nut Clusters", "Bran Buds", "Bran Twigs"];
    var NEST = [0, 0, 1, 2, 2], Q = [0.8, 0.0, 1.0, -0.5, -0.5], MC = [1.5, 1.2, 1.6, 1.0, 1.0];
    var COL = [GOLD, GOLD, PINK, TEAL, TEAL];
    var PAIRS = [];
    for (var a = 0; a < 5; a++) for (var b = a + 1; b < 5; b++) PAIRS.push([a, b]);
    function shares(p, sg) {
      var d = [], D = [0, 0, 0], j, s = [], cond = [];
      for (j = 0; j < 5; j++) { d.push(Math.exp((Q[j] - p[j]) / (1 - sg))); D[NEST[j]] += d[j]; }
      var den = 1; for (var g = 0; g < 3; g++) den += Math.pow(D[g], 1 - sg);
      for (j = 0; j < 5; j++) { cond.push(d[j] / D[NEST[j]]); s.push(cond[j] * Math.pow(D[NEST[j]], 1 - sg) / den); }
      return { s: s, cond: cond, cs: Math.log(den) };
    }
    function jac(p, sg) { // J[j][k] = ds_k / dp_j
      var r = shares(p, sg), s = r.s, c = r.cond, J = [], j, k;
      for (j = 0; j < 5; j++) {
        J.push([]);
        for (k = 0; k < 5; k++) {
          var v;
          if (j === k) v = -s[j] * (1 / (1 - sg) - sg / (1 - sg) * c[j] - s[j]);
          else if (NEST[j] === NEST[k]) v = s[k] * (sg / (1 - sg) * c[j] + s[j]);
          else v = s[k] * s[j];
          J[j].push(v);
        }
      }
      return { J: J, s: s, cs: r.cs };
    }
    function solve(A, y) { // Gaussian elimination with partial pivoting
      var n = y.length, M = A.map(function (row, i) { return row.slice().concat([y[i]]); }), i, k, r;
      for (i = 0; i < n; i++) {
        var piv = i; for (r = i + 1; r < n; r++) if (Math.abs(M[r][i]) > Math.abs(M[piv][i])) piv = r;
        var t = M[i]; M[i] = M[piv]; M[piv] = t;
        for (r = i + 1; r < n; r++) { var f = M[r][i] / M[i][i]; for (k = i; k <= n; k++) M[r][k] -= f * M[i][k]; }
      }
      var x = new Array(n).fill(0);
      for (i = n - 1; i >= 0; i--) { var sum = M[i][n]; for (k = i + 1; k < n; k++) sum -= M[i][k] * x[k]; x[i] = sum / M[i][i]; }
      return x;
    }
    function bertrand(mc, owner, sg, p0) {
      var p = (p0 || mc.map(function (c) { return 1.4 * c; })).slice(), it, j, k;
      for (it = 0; it < 400; it++) {
        var r = jac(p, sg), A = [];
        for (j = 0; j < 5; j++) { A.push([]); for (k = 0; k < 5; k++) A[j].push(owner[j] === owner[k] ? r.J[j][k] : 0); }
        var m = solve(A, r.s.map(function (x) { return -x; })), diff = 0;
        for (j = 0; j < 5; j++) { var nw = mc[j] + m[j]; diff = Math.max(diff, Math.abs(nw - p[j])); p[j] = 0.5 * p[j] + 0.5 * nw; }
        if (diff < 1e-10) break;
      }
      return p;
    }
    function simulate(sg, pair, save) {
      var own0 = [0, 1, 2, 3, 4], own1 = own0.slice(); own1[pair[1]] = pair[0];
      var p0 = bertrand(MC, own0, sg), mc1 = MC.slice();
      mc1[pair[0]] *= 1 - save; mc1[pair[1]] *= 1 - save;
      var p1 = bertrand(mc1, own1, sg, p0);
      var r0 = jac(p0, sg), r1 = shares(p1, sg);
      var tot = r0.s.reduce(function (x, y) { return x + y; }, 0);
      var hhi0 = 0, j; for (j = 0; j < 5; j++) hhi0 += Math.pow(100 * r0.s[j] / tot, 2);
      var dhhi = 2 * (100 * r0.s[pair[0]] / tot) * (100 * r0.s[pair[1]] / tot);
      var div = -r0.J[pair[0]][pair[1]] / r0.J[pair[0]][pair[0]];
      return { p0: p0, p1: p1, dp: p1.map(function (x, k) { return x / p0[k] - 1; }), hhi0: hhi0, dhhi: dhhi,
               dcs: r1.cs / r0.cs - 1, div: div,
               upp: div * (p0[pair[1]] - MC[pair[1]]) - save * MC[pair[0]] };
    }
    QB.widget(el, {
      title: "Simulate a merger",
      sub: "Left: each brand's price change after the merger you choose (the merging pair outlined in white). " +
           "Right: the merging brands' average price rise against the nesting parameter, for your pair (green) " +
           "and for the game's two mergers, the bran twins (teal) and the two largest (gold).",
      panels: 2, height: 270,
      controls: [
        { k: "pair", label: "Which two brands merge", min: 0, max: 9, step: 1, value: 9,
          fmt: function (x) { var q = PAIRS[Math.round(x)]; return NAMES[q[0]] + " + " + NAMES[q[1]]; } },
        { k: "sg", label: "Nesting parameter, sigma", min: 0, max: 0.9, step: 0.01, value: 0.6,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "save", label: "Cost savings for the merging brands", min: 0, max: 0.3, step: 0.01, value: 0,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
      ],
      draw: function (g, v, st) {
        var pair = PAIRS[Math.round(v.pair)], r = simulate(v.sg, pair, v.save), k;
        var lo = Math.min(-0.1, Math.min.apply(null, r.dp) * 1.2), hi = Math.max(0.1, Math.max.apply(null, r.dp) * 1.2);
        var A = g[0].axes({ x: [-0.5, 4.5], y: [lo, hi], title: "price change by brand", xlabel: "brand" });
        A.bars([0, 1, 2, 3, 4], r.dp, 0.6, { color: function (i) { return COL[i]; } });
        A.hline(0, { color: GREY });
        for (k = 0; k < 2; k++) A.text(pair[k], r.dp[pair[k]], (100 * r.dp[pair[k]]).toFixed(1) + "%",
                                       { align: "center", dy: r.dp[pair[k]] >= 0 ? -10 : 10, bg: true });
        var sgs = [], mine = [], xs = [], ys = [];
        for (k = 0; k <= 18; k++) {
          var s = k * 0.05; sgs.push(s);
          var a = simulate(s, pair, v.save), x = simulate(s, [3, 4], v.save), y = simulate(s, [0, 2], v.save);
          mine.push((a.dp[pair[0]] + a.dp[pair[1]]) / 2);
          xs.push((x.dp[3] + x.dp[4]) / 2); ys.push((y.dp[0] + y.dp[2]) / 2);
        }
        var top = Math.max(0.05, Math.max.apply(null, mine.concat(xs, ys)) * 1.1);
        var B = g[1].axes({ x: [0, 0.9], y: [Math.min(0, Math.min.apply(null, mine.concat(xs, ys))), top],
                            title: "merging brands' price rise", xlabel: "nesting parameter sigma" });
        B.line(sgs, xs, { color: TEAL, width: 2 });
        B.line(sgs, ys, { color: GOLD, width: 2 });
        B.line(sgs, mine, { color: "#7BD88F", width: 2.5, dash: [5, 3] });
        B.vline(v.sg, { color: GREY });
        st.r = r; st.pair = pair;
      },
      readout: function (v, st) {
        var r = st.r, p = st.pair;
        return [["merging brands' prices", (100 * (r.dp[p[0]] + r.dp[p[1]]) / 2).toFixed(1) + "%"],
                ["Herfindahl index", r.hhi0.toFixed(0) + " + " + r.dhhi.toFixed(0)],
                ["diversion from " + NAMES[p[0]] + " to " + NAMES[p[1]], (100 * r.div).toFixed(0) + "%"],
                ["upward pricing pressure on " + NAMES[p[0]], r.upp.toFixed(3)],
                ["shoppers' surplus", (100 * r.dcs).toFixed(1) + "%"]];
      },
      note: "Part 43, chapters 2, 9 and 14. Costs and qualities are the game's; the Herfindahl index counts shares of " +
            "cereal sales. Computed in your browser; nothing you do here is stored or sent.",
    });
  };

  // ---- Part 44: dynamics, platforms and antitrust ----------------------------------------------------------------
  W.rebuild = function (el) {
    // Zurcher's problem without surprises (explainer.economics.agora.io: Rust.average_cost): rebuild an engine once it
    // reaches T steps of 5,000 miles.  Monthly mileage moves 0, 1 or 2 steps with Rust's probabilities.  By renewal,
    // the average monthly cost is (upkeep over a cycle + RC) / (months in a cycle), with the expected months spent at
    // each mileage found by a short recursion.
    var P = [0.3561, 0.6323, 0.0116];
    function avg(RC, c, T) {
      var v = [], k, up = 0, n = 0;
      for (k = 0; k < T; k++) {
        var init = k < 3 ? P[k] : 0;
        v.push((init + (k >= 1 ? P[1] * v[k - 1] : 0) + (k >= 2 ? P[2] * v[k - 2] : 0)) / (1 - P[0]));
        up += v[k] * c * k; n += v[k];
      }
      return (up + RC) / (n + 1);
    }
    QB.widget(el, {
      title: "Rebuild the engine",
      sub: "The average monthly cost per bus of rebuilding at each mileage (green), with your rule (gold) and the " +
           "best one (dashed). Upkeep rises with the miles on the engine; a rebuild resets them.",
      panels: 1, height: 290,
      controls: [
        { k: "RC", label: "Cost of a rebuild, dollars", min: 1000, max: 12000, step: 100, value: 4000,
          fmt: function (x) { return "$" + x.toFixed(0); } },
        { k: "c", label: "Upkeep per month for every 5,000 miles", min: 1, max: 20, step: 0.5, value: 6,
          fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "T", label: "Your rule: rebuild at (thousand miles)", min: 20, max: 440, step: 5, value: 250,
          fmt: function (x) { return x.toFixed(0) + "k"; } },
      ],
      draw: function (g, v, st) {
        var xs = [], ys = [], k, best = 0, bestC = 1e18;
        for (k = 2; k <= 89; k++) {
          var cost = avg(v.RC, v.c, k); xs.push(k * 5); ys.push(cost);
          if (cost < bestC) { bestC = cost; best = k * 5; }
        }
        var mine = avg(v.RC, v.c, Math.max(1, Math.round(v.T / 5)));
        var top = Math.min(Math.max.apply(null, ys), 3 * bestC);
        var A = g[0].axes({ x: [0, 450], y: [0, top * 1.05], title: "average cost per bus per month, dollars",
                            xlabel: "rebuild at (thousand miles)" });
        A.line(xs, ys.map(function (y) { return Math.min(y, top * 1.05); }), { color: "#7BD88F", width: 2.5 });
        A.vline(best, { color: "#9AA3B2", width: 1.5 });
        A.dots([v.T], [Math.min(mine, top * 1.05)], { color: GOLD, r: 6 });
        st.best = best; st.bestC = bestC; st.mine = mine;
      },
      readout: function (v, st) {
        return [["your rule costs", "$" + st.mine.toFixed(0) + " a month"],
                ["the best rule", st.best.toFixed(0) + "k miles, $" + st.bestC.toFixed(0) + " a month"],
                ["you pay extra", (100 * (st.mine / st.bestC - 1)).toFixed(1) + "%"]];
      },
      note: "Part 44, chapter 1. Rust's estimates on Zurcher's buses put the rebuild cost at about 123 months of " +
            "upkeep at 150,000 miles; surprises each month make real rebuilds earlier or later. Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
  W.gym = function (el) {
    // The Island's gym (explainer.economics.agora.behave: gym_member, gym_choice).  On a share of the 30 days the
    // member cannot go; on the others today's cost of going is uniform on [0, 60] and the member goes when it is below
    // beta times the later benefit b (less the price of a visit).  At sign-up the member forecasts with beta_hat and
    // the busy share they expect, and picks the monthly contract ($70, free visits), the pass ($10 a visit) or
    // nothing, by forecast; the visits that follow use the true beta and busy share.
    var N = 30, C = 60, FEE = 70, PASS = 10, BUSY = 0.55;
    function member(beta, bh, b, p, busyHat) {
      var xt = Math.min(Math.max(beta * b - p, 0), C), xh = Math.min(Math.max(bh * b - p, 0), C);
      function val(x, free) { return N * (1 - free) / C * ((b - p) * x - x * x / 2); }
      return { visits: N * (1 - BUSY) * xt / C, forecast: N * (1 - busyHat) * xh / C,
               perceived: val(xh, busyHat), realized: val(xt, BUSY) };
    }
    QB.widget(el, {
      title: "Join the gym",
      sub: "What you forecast at sign-up (blue) and what you then do (red), on the monthly contract and on the " +
           "pass. Your choice is made by forecast; the bill comes by visits.",
      panels: 1, height: 290,
      controls: [
        { k: "beta", label: "Your present bias, beta (1 = none)", min: 0.3, max: 1, step: 0.01, value: 0.7,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "bh", label: "What you believe your beta is", min: 0.3, max: 1, step: 0.01, value: 1,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "busyHat", label: "Days you expect to be too busy", min: 0, max: 0.8, step: 0.05, value: 0,
          fmt: function (x) { return (100 * x).toFixed(0) + "% (really 55%)"; } },
        { k: "b", label: "What a workout is worth to you later, dollars", min: 10, max: 40, step: 1, value: 24,
          fmt: function (x) { return "$" + x.toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var m = member(v.beta, v.bh, v.b, 0, v.busyHat), q = member(v.beta, v.bh, v.b, PASS, v.busyHat);
        var per = { monthly: m.perceived - FEE, pass: q.perceived, none: 0 };
        var real = { monthly: m.realized - FEE, pass: q.realized, none: 0 };
        var pick = "none";
        if (per.monthly >= per.pass && per.monthly > 0) pick = "monthly";
        else if (per.pass > 0) pick = "pass";
        var best = "none";
        if (real.monthly >= real.pass && real.monthly > 0) best = "monthly";
        else if (real.pass > 0) best = "pass";
        var top = Math.max(m.forecast, m.visits, q.forecast, q.visits, 4) * 1.15;
        var A = g[0].axes({ x: [0, 4], y: [0, top], title: "visits a month",
                            xlabel: "monthly: forecast, made          pass: forecast, made" });
        A.bars([0.5, 1.5, 2.5, 3.5], [m.forecast, m.visits, q.forecast, q.visits], 0.6,
               { color: function (i) { return ["#7EC8F5", "#F25F5C", "#7EC8F5", "#F25F5C"][i]; } });
        st.pick = pick; st.best = best; st.m = m; st.q = q; st.real = real;
      },
      readout: function (v, st) {
        var paid = st.pick === "monthly" ? FEE : (st.pick === "pass" ? PASS * st.q.visits : 0);
        var vis = st.pick === "monthly" ? st.m.visits : (st.pick === "pass" ? st.q.visits : 0);
        var what = st.pick === "none" ? "not to join" : (st.pick === "pass" ? "the pass" : "the monthly contract");
        return [["you choose", what],
                ["you pay per visit", vis > 0 ? "$" + (paid / vis).toFixed(2) : "-"],
                ["in hindsight, best", st.best === "none" ? "not joining" : "the " + st.best],
                ["your choice costs you", "$" + (st.real[st.best] - st.real[st.pick]).toFixed(2) + " a month"]];
      },
      note: "Part 45, chapter 5. Set what you believe equal to the truth, beta and busy days alike, and the regret " +
            "disappears: the cost of present bias here is the cost of not knowing it. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };
  W.aidbudget = function (el) {
    // The Island's aid budget (explainer.economics.agora.village: aid_benefit, aid_allocate).  Each programme buys
    // a s (1 - exp(-x/s)) thousand healthy years with x million dollars: a per million at first, flattening at s.
    // If the reader's split spends more than the budget, every share is scaled down to fit.
    var BUDGET = 10;
    var P = [["deworming", 4.0, 1.5, "#7FD1B9"], ["cash", 2.0, 6.0, "#7BD88F"], ["nets", 5.0, 1.0, "#F2C14E"],
             ["tutoring", 3.0, 2.5, "#7EC8F5"], ["credit", 0.8, 5.0, "#C9A0FF"], ["graduation", 2.2, 3.0, "#E8A0B4"]];
    function ben(i, x) { return P[i][1] * P[i][2] * (1 - Math.exp(-x / P[i][2])); }
    function marg(i, x) { return P[i][1] * Math.exp(-x / P[i][2]); }
    var best = (function () {
      var a = [0, 0, 0, 0, 0, 0], step = 0.05;
      for (var n = 0; n < BUDGET / step; n++) {
        var k = 0, gk = -1;
        for (var i = 0; i < 6; i++) { var gi = ben(i, a[i] + step) - ben(i, a[i]); if (gi > gk) { gk = gi; k = i; } }
        a[k] += step;
      }
      var t = 0; for (var j = 0; j < 6; j++) t += ben(j, a[j]);
      return { alloc: a, total: t };
    })();
    var controls = P.map(function (p, i) {
      return { k: "x" + i, label: p[0] + ", millions", min: 0, max: 10, step: 0.1, value: BUDGET / 6,
               fmt: function (x) { return "$" + x.toFixed(1) + "m"; } };
    });
    QB.widget(el, {
      title: "Spend the aid budget",
      sub: "Ten million dollars, six programmes. Bars: what each buys with your split (coloured) and with the best " +
           "split (grey outline). Each programme's next million buys less than its last.",
      panels: 1, height: 300, controls: controls,
      draw: function (g, v, st) {
        var x = P.map(function (p, i) { return v["x" + i]; });
        var tot = x.reduce(function (a, b) { return a + b; }, 0);
        var f = tot > BUDGET ? BUDGET / tot : 1;
        x = x.map(function (z) { return z * f; });
        var mine = x.map(function (z, i) { return ben(i, z); });
        var opt = best.alloc.map(function (z, i) { return ben(i, z); });
        var top = Math.max.apply(null, mine.concat(opt).concat([2])) * 1.15;
        var A = g[0].axes({ x: [0, 6], y: [0, top], title: "thousands of healthy years",
                            xlabel: "deworming   cash   nets   tutoring   credit   graduation" });
        A.bars([0.35, 1.35, 2.35, 3.35, 4.35, 5.35], mine, 0.35, { color: function (i) { return P[i][3]; } });
        A.bars([0.7, 1.7, 2.7, 3.7, 4.7, 5.7], opt, 0.25, { color: function () { return "#6B7280"; } });
        st.x = x; st.tot = tot; st.f = f;
        st.total = mine.reduce(function (a, b) { return a + b; }, 0);
        st.margs = x.map(function (z, i) { return marg(i, z); });
      },
      readout: function (v, st) {
        var lo = Math.min.apply(null, st.margs), hi = Math.max.apply(null, st.margs);
        var iLo = st.margs.indexOf(lo), iHi = st.margs.indexOf(hi);
        return [["you spend", "$" + Math.min(st.tot, BUDGET).toFixed(1) + "m" +
                 (st.f < 1 ? " (scaled down from $" + st.tot.toFixed(1) + "m)" : "")],
                ["you buy", st.total.toFixed(2) + " thousand healthy years"],
                ["the best split buys", best.total.toFixed(2) + " (" +
                 (100 * st.total / best.total).toFixed(0) + "% of it is yours)"],
                ["move money", "from " + P[iLo][0] + " (next million buys " + lo.toFixed(2) + ") to " + P[iHi][0] +
                 " (" + hi.toFixed(2) + ")"]];
      },
      note: "Part 46, chapter 2. At the best split the next million buys the same in every funded programme; " +
            "microcredit's first million buys less than that, so it gets nothing. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };
  // ---- Part 47: political economy --------------------------------------------------------------------------------
  W.buildlobby = function (el) {
    // The Play-it game of Part 47 (explainer.economics.agora.politics: tokens_game).  Ten players with 100 tokens
    // each keep them (worth 1), build (each token returns 0.3 to every player) or lobby (a prize of 400 is shared
    // in proportion to lobbying, equally if nobody lobbies).  If a player's build and lobby exceed 100, both are
    // scaled down to fit.
    var N = 10, END = 100, MPCR = 0.3, PRIZE = 400;
    function fit(b, l) { var t = b + l; return t > END ? [b * END / t, l * END / t] : [b, l]; }
    function payoffs(b, l, ob, ol) {
      var B = b + (N - 1) * ob, L = l + (N - 1) * ol;
      var sMe = L > 0 ? l / L : 1 / N, sOt = L > 0 ? ol / L : 1 / N;
      return [END - b - l + MPCR * B + PRIZE * sMe, END - ob - ol + MPCR * B + PRIZE * sOt];
    }
    function best(ob, ol) {
      // building costs you 1 and returns 0.3 to you, so never build; lobby to maximize 400 l/(l + L) - l
      var L = (N - 1) * ol, l = L > 0 ? Math.max(0, Math.min(END, Math.sqrt(PRIZE * L) - L)) : 0.01;
      return { l: l, pay: payoffs(0, l, ob, ol)[0] };
    }
    var NASH = PRIZE * (N - 1) / (N * N);
    QB.widget(el, {
      title: "Build or lobby?",
      sub: "You and nine others each have 100 tokens. Left: what you, each of the others, and everyone together end " +
           "with. Right: what you end with as your lobbying varies, with your building fixed; the dot is your choice.",
      panels: 2, height: 270,
      controls: [
        { k: "b", label: "You build with", min: 0, max: 100, step: 1, value: 50,
          fmt: function (x) { return x.toFixed(0) + " tokens"; } },
        { k: "l", label: "You lobby with", min: 0, max: 100, step: 1, value: 10,
          fmt: function (x) { return x.toFixed(0) + " tokens"; } },
        { k: "ob", label: "Each other player builds with", min: 0, max: 100, step: 1, value: 50,
          fmt: function (x) { return x.toFixed(0) + " tokens"; } },
        { k: "ol", label: "Each other player lobbies with", min: 0, max: 100, step: 1, value: 10,
          fmt: function (x) { return x.toFixed(0) + " tokens"; } },
      ],
      draw: function (g, v, st) {
        var me = fit(v.b, v.l), ot = fit(v.ob, v.ol), p = payoffs(me[0], me[1], ot[0], ot[1]);
        var avg = (p[0] + (N - 1) * p[1]) / N;
        var A = g[0].axes({ x: [0, 4], y: [0, 450], title: "tokens at the end",
                            xlabel: "you   each other   average   all build" });
        A.bars([0.5, 1.5, 2.5, 3.5], [p[0], p[1], avg, END * N * MPCR + PRIZE / N], 0.6,
               { color: function (i) { return ["#F2C14E", "#7EC8F5", "#C9A0FF", "#6B7280"][i]; } });
        A.hline(PRIZE * (1 / N) + END - NASH, { color: "#E8A0B4", dash: [4, 3] });
        A.text(3.9, PRIZE / N + END - NASH, "everyone lobbies " + NASH.toFixed(0) + ": " +
               (PRIZE / N + END - NASH).toFixed(0), { align: "right", dy: -8, bg: true });
        var ls = [], ys = [], top = 0;
        for (var k = 0; k <= 100 - Math.round(me[0]); k += 1) {
          var y = payoffs(me[0], k, ot[0], ot[1])[0]; ls.push(k); ys.push(y); top = Math.max(top, y);
        }
        var B = g[1].axes({ x: [0, 100], y: [0, Math.max(450, top * 1.1)], title: "what you end with",
                            xlabel: "your lobbying, tokens" });
        B.line(ls, ys, { color: "#F2C14E", width: 2.5 });
        B.dots([me[1]], [p[0]], { color: "#FFFFFF", r: 5 });
        var br = best(ot[0], ot[1]);
        B.vline(Math.min(br.l, 100 - me[0]), { color: "#E8A0B4", dash: [4, 3] });
        st.me = me; st.ot = ot; st.p = p; st.avg = avg; st.br = br;
      },
      readout: function (v, st) {
        return [["you keep, build, lobby", (END - st.me[0] - st.me[1]).toFixed(0) + ", " + st.me[0].toFixed(0) +
                 ", " + st.me[1].toFixed(0)],
                ["you end with", st.p[0].toFixed(1) + " tokens"],
                ["each other player ends with", st.p[1].toFixed(1)],
                ["your best reply", "build 0, lobby " + st.br.l.toFixed(0) + ": " + st.br.pay.toFixed(1) + " tokens"],
                ["the average player", st.avg.toFixed(1) + " (340 if all build, 104 if all lobby " +
                 NASH.toFixed(0) + ")"]];
      },
      note: "Part 47, chapters 2 and 3. A token you build with returns 0.3 to you, so whatever the others do, " +
            "building never pays you, and lobbying pays until your share of the prize stops growing fast enough. " +
            "Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
