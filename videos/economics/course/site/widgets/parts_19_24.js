// Interactives for Act V, The Long Run (Parts 19-24).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1", BLUE = "#9FB8F2";

  // ---- Part 19: the great escape ---------------------------------------------------------------------------------
  W.malthus = function (el) {
    // the Malthusian island of Part 19 (explainer.economics.agora.malthus: simulate): income per head A (X / L)^beta on
    // fixed land, population growing at lambda ln(y / ybar) a year, here capped at a maximum rate (the reader's
    // demographic transition); a plague in year 100, a better plough in year 250, and technology that may also grow
    // steadily every year.  Can the reader find a setting in which income per head keeps rising?
    var T = 400;
    function run(v) {
      var L = 1, A = 1, ys = [], Ls = [], ts = [];
      for (var t = 0; t <= T; t++) {
        if (t === 100) L *= 1 - v.plague;
        if (t === 250) A *= 1 + v.plough;
        var y = A * Math.pow(1 / L, v.beta);
        ts.push(t); ys.push(y); Ls.push(L);
        var grow = Math.min(v.lam * Math.log(y), v.cap);
        L *= Math.exp(grow);
        A *= 1 + v.g;
      }
      return { t: ts, y: ys, L: Ls };
    }
    QB.widget(el, {
      title: "Can the island escape?",
      sub: "Income per head is technology times land per person to the power beta, and the population grows when " +
           "income is above subsistence (1 on the left chart). A plague strikes in year 100 and a better plough " +
           "arrives in year 250. Then add steady technological progress, and cap how fast the population can grow, " +
           "as a demographic transition would. Which settings let income per head keep rising?",
      panels: 2, height: 300,
      controls: [
        { k: "beta", label: "Diminishing returns, beta", min: 0.2, max: 1.0, step: 0.05, value: 0.6 },
        { k: "lam", label: "How fast population follows income, lambda", min: 0.005, max: 0.05, step: 0.005,
          value: 0.02 },
        { k: "plague", label: "Share killed by the plague in year 100", min: 0, max: 0.6, step: 0.05, value: 0.45,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "plough", label: "Gain from the better plough in year 250", min: 0, max: 1.0, step: 0.1, value: 0.5,
          fmt: function (x) { return "+" + (100 * x).toFixed(0) + "%"; } },
        { k: "g", label: "Steady technological progress, a year", min: 0, max: 0.02, step: 0.001, value: 0,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "cap", label: "Fastest the population can grow, a year", min: 0, max: 0.03, step: 0.001, value: 0.03,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = run(v);
        s.r = r;
        var ymax = Math.max(2, Math.max.apply(null, r.y) * 1.1);
        var a = g[0].axes({ x: [0, T], y: [0, ymax], title: "Income per head (subsistence = 1)", xlabel: "year" });
        a.line(r.t, r.y, { color: GOLD, width: 2.5 });
        a.hline(1, { color: GREY_HINT });
        var Lmax = Math.max(2, Math.max.apply(null, r.L) * 1.1);
        var b = g[1].axes({ x: [0, T], y: [0, Lmax], title: "Population (year 0 = 1)", xlabel: "year" });
        b.line(r.t, r.L, { color: RED, width: 2.5 });
      },
      readout: function (v, s) {
        var r = s.r;
        if (!r) return [];
        var yEnd = r.y[r.y.length - 1], y300 = r.y[300], hl = Math.log(2) / (v.lam * v.beta);
        var rising = yEnd > y300 * 1.05;
        return [["income per head in year 400", yEnd.toFixed(2) + " (subsistence 1)"],
                ["population in year 400", r.L[r.L.length - 1].toFixed(2)],
                ["half-life of a shock, without progress", hl.toFixed(0) + " years"],
                ["still rising at the end?", rising ? "yes: the island is escaping" :
                  (yEnd > 1.2 ? "no: a higher plateau, but not rising" : "no: back in the trap")]];
      },
      note: "With no steady progress the island always returns to subsistence: technology buys people, not income " +
            "(Part 19, chapter 2). Steady progress alone lifts income only to a higher plateau. Income keeps rising " +
            "only when progress outruns the fastest the population can grow. Computed in your browser; nothing you do " +
            "here is stored or sent.",
    });
  };
  // ---- Part 20: the island saves ---------------------------------------------------------------------------------
  W.solow = function (el) {
    // the Solow island of Part 20 (explainer.economics.agora.growth: solow_path): k' = k + s k^alpha - (n+g+delta) k
    // per effective worker, starting at the steady state of a 15% saving rate; the reader picks a new saving rate for
    // a century and sees consumption per worker against staying at 15%, and the steady state's consumption against
    // the saving rate, whose peak is the golden rule.
    var T = 100, S0 = 0.15;
    function kstar(s, v) { return Math.pow(s / (v.n + v.g + v.delta), 1 / (1 - v.alpha)); }
    function run(s, v) {
      var k = kstar(S0, v), cs = [], ts = [];
      for (var t = 0; t <= T; t++) {
        var y = Math.pow(k, v.alpha);
        ts.push(t); cs.push((1 - s) * y * Math.pow(1 + v.g, t));
        k = k + s * y - (v.n + v.g + v.delta) * k;
      }
      return { t: ts, c: cs };
    }
    QB.widget(el, {
      title: "How much should the island save?",
      sub: "The island has been saving 15% of its output. Choose a new saving rate for the next hundred years, and the " +
           "technology: capital's share, population growth, technological progress and depreciation. The left chart " +
           "shows consumption per worker relative to staying at 15%; the right, steady-state consumption for every " +
           "saving rate. Can you find the rate that leaves the most to eat in year 100?",
      panels: 2, height: 300,
      controls: [
        { k: "s", label: "New saving rate", min: 0.05, max: 0.9, step: 0.01, value: 0.25,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "alpha", label: "Capital's share, alpha", min: 0.2, max: 0.6, step: 0.01, value: 1 / 3,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Population growth, a year", min: 0, max: 0.03, step: 0.001, value: 0.01,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "g", label: "Technological progress, a year", min: 0, max: 0.04, step: 0.001, value: 0.02,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "delta", label: "Depreciation, a year", min: 0.02, max: 0.1, step: 0.005, value: 0.05,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (gr, v, st) {
        var a = run(v.s, v), b = run(S0, v);
        var rel = a.c.map(function (x, i) { return x / b.c[i]; });
        st.rel = rel;
        var lo = Math.min(0.9, Math.min.apply(null, rel) * 0.95), hi = Math.max(1.1, Math.max.apply(null, rel) * 1.05);
        var ax = gr[0].axes({ x: [0, T], y: [lo, hi], title: "Consumption per worker, relative to staying at 15%",
                              xlabel: "year" });
        ax.hline(1, { color: GREY_HINT });
        ax.line(a.t, rel, { color: GREEN, width: 2.5 });
        var ss = [], cc = [];
        for (var i = 1; i < 100; i++) {
          var s = i / 100, k = kstar(s, v);
          ss.push(s); cc.push((1 - s) * Math.pow(k, v.alpha));
        }
        var cmax = Math.max.apply(null, cc);
        var bx = gr[1].axes({ x: [0, 1], y: [0, cmax * 1.15], title: "Steady-state consumption per effective worker",
                              xlabel: "saving rate" });
        bx.line(ss, cc, { color: GOLD, width: 2.5 });
        bx.vline(v.alpha, { color: GREY_HINT });
        bx.vline(v.s, { color: GREEN });
      },
      readout: function (v, st) {
        var rel = st.rel;
        if (!rel) return [];
        var lam = (1 - v.alpha) * (v.n + v.g + v.delta);
        var end = rel[rel.length - 1], best = v.alpha;
        var cross = null;
        for (var i = 1; i < rel.length; i++) { if ((v.s > S0 && rel[i] >= 1) || (v.s < S0 && rel[i] < 1)) { cross = i; break; } }
        var verdict = Math.abs(v.s - best) < 0.015 ? "at the golden rule: the most to eat in the long run" :
          (v.s > best ? "above the golden rule: dynamically inefficient, the island could eat more now and later" :
                        "below the golden rule: more saving would pay off, after a lean start");
        return [["consumption in year 100, against staying at 15%", (end >= 1 ? "+" : "") + (100 * (end - 1)).toFixed(1) + "%"],
                [v.s > S0 ? "year the new rate overtakes 15%" : "year the new rate falls behind 15%",
                 cross === null ? (v.s === S0 ? "the same rate" : "never, within a century") : String(cross)],
                ["the golden rule saving rate (= alpha)", (100 * best).toFixed(0) + "%"],
                ["half-life of the transition, ln 2 / lambda", (Math.log(2) / lam).toFixed(0) + " years"],
                ["verdict", verdict]];
      },
      note: "The golden rule maximizes consumption in the steady state, not in every year: every rate above 15% starts " +
            "with a cut in consumption, and whether the later gain is worth it depends on how patient the islanders " +
            "are (Part 20, chapter 11). Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 21: move the workers ----------------------------------------------------------------------------------
  W.misallocation = function (el) {
    // Hsieh and Klenow's economy of Part 21 (explainer.economics.agora.ge: misallocation): four plants making
    // varieties of one good (elasticity of substitution 3) with labour only, physical productivities A = 1, 1.5, 2 and
    // 3.  Output is (sum (A_i L_i)^e)^(1/e), e = 2/3.  The reader moves workers between plants; the marginal revenue
    // products show where a worker adds most.  The efficient allocation makes them equal (L_i proportional to A_i^2).
    var A = [1.0, 1.5, 2.0, 3.0], SIG = 3, E = (SIG - 1) / SIG;
    var NAMES = ["plant 1", "plant 2", "plant 3", "plant 4"];
    var COLS = [BLUE, GREEN, GOLD, RED];
    function output(L) {
      var s = 0;
      for (var i = 0; i < 4; i++) s += Math.pow(A[i] * L[i], E);
      return Math.pow(s, 1 / E);
    }
    function mrpl(L) {
      // dY/dL_i = Y^(1/sigma) * e^(-1)... up to a common factor: Y^(1/sigma) A_i^e L_i^(e-1)
      var Y = output(L), out = [];
      for (var i = 0; i < 4; i++) out.push(Math.pow(Y, 1 / SIG) * Math.pow(A[i], E) * Math.pow(Math.max(L[i], 1e-6), E - 1));
      return out;
    }
    function efficient() {
      var w = A.map(function (a) { return Math.pow(a, SIG - 1); });
      var t = w.reduce(function (x, y) { return x + y; }, 0);
      return w.map(function (x) { return x / t; });
    }
    QB.widget(el, {
      title: "Move the workers",
      sub: "Four plants make varieties of one good. Plant 4 is three times as productive as plant 1. Choose how many " +
           "of the island's 100 workers each plant gets (plant 4 takes whoever is left). The right chart shows what " +
           "one more worker would add in each plant. Can you find the allocation that makes the most output?",
      panels: 2, height: 280,
      controls: [
        { k: "l1", label: "Workers in plant 1", min: 0, max: 60, step: 1, value: 25 },
        { k: "l2", label: "Workers in plant 2", min: 0, max: 60, step: 1, value: 25 },
        { k: "l3", label: "Workers in plant 3", min: 0, max: 60, step: 1, value: 25 },
      ],
      draw: function (g, v, st) {
        var l4 = Math.max(0, 100 - v.l1 - v.l2 - v.l3);
        var L = [v.l1 / 100, v.l2 / 100, v.l3 / 100, l4 / 100];
        st.L = L;
        var a = g[0].axes({ x: [0, 4], y: [0, 100], title: "Workers in each plant", xlabel: "plant 1 to 4" });
        a.bars([0.5, 1.5, 2.5, 3.5], L.map(function (x) { return 100 * x; }), 0.6,
               { color: function (i) { return COLS[i]; } });
        var m = mrpl(L), top = Math.max.apply(null, m) * 1.15;
        var b = g[1].axes({ x: [0, 4], y: [0, Math.min(top, 20)], title: "What one more worker adds",
                            xlabel: "plant 1 to 4" });
        b.bars([0.5, 1.5, 2.5, 3.5], m.map(function (x) { return Math.min(x, 20); }), 0.6,
               { color: function (i) { return COLS[i]; } });
      },
      readout: function (v, st) {
        var L = st.L;
        if (!L) return [];
        var over = v.l1 + v.l2 + v.l3 > 100;
        var Y = output(L), Ye = output(efficient()), share = Y / Ye;
        var eff = efficient().map(function (x) { return Math.round(100 * x); });
        return [["output, against the best possible", (100 * share).toFixed(1) + "%"],
                ["workers in plant 4", over ? "none left (you assigned more than 100)" : String(100 - v.l1 - v.l2 - v.l3)],
                ["verdict", share > 0.995 ? "efficient: one more worker adds the same everywhere" :
                  "move workers toward the plants where one more adds most"],
                ["the efficient split (workers proportional to A squared)", eff.join(", ")]];
      },
      note: "With an elasticity of substitution of 3, the efficient allocation gives each plant workers in proportion to " +
            "its productivity squared, and equalizes what one more worker adds. Taxes, subsidies, cheap credit for some " +
            "firms and red tape for others push plants away from it (Part 21, chapter 8). Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };
  // ---- Part 22: consumption and saving ---------------------------------------------------------------------------
  W.bufferstock = function (el) {
    // Carroll's buffer-stock household of Part 22 (explainer.economics.agora.household: buffer_stock), solved here
    // by the same endogenous grid method: cash on hand m per unit of permanent income, CRRA utility (gamma 2),
    // R = 1.03, income growth G = 1.02, seven-point lognormal permanent and transitory shocks (permanent spread 10%)
    // and a small chance of no income.  The reader sets patience, transitory risk and the chance of a jobless year.
    var R = 1.03, G = 1.02, GAM = 2, PSD = 0.1;
    var Z = [-1.46523, -0.79164, -0.36611, 0.0, 0.36611, 0.79164, 1.46523];
    function shocks(sd) {
      if (sd <= 0) return [1];
      var x = Z.map(function (z) { return Math.exp(sd * z - sd * sd / 2); });
      var m = x.reduce(function (a, b) { return a + b; }, 0) / x.length;
      return x.map(function (v) { return v / m; });
    }
    function interp(x, xs, ys) {
      var n = xs.length;
      if (x <= xs[0]) return ys[0];
      if (x >= xs[n - 1]) {
        var sl = (ys[n - 1] - ys[n - 2]) / (xs[n - 1] - xs[n - 2]);
        return ys[n - 1] + sl * (x - xs[n - 1]);
      }
      var lo = 0, hi = n - 1;
      while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (xs[mid] <= x) lo = mid; else hi = mid; }
      var t = (x - xs[lo]) / (xs[hi] - xs[lo]);
      return ys[lo] + t * (ys[hi] - ys[lo]);
    }
    function solve(beta, tsd, p0) {
      var psi = shocks(PSD), th = shocks(tsd), wt = [];
      th = th.map(function (v) { return v / (1 - p0); });
      for (var i = 0; i < th.length; i++) wt.push((1 - p0) / th.length);
      if (p0 > 0) { th = [0].concat(th); wt = [p0].concat(wt); }
      var A = [0];
      for (var k = 0; k < 59; k++) A.push(Math.exp(Math.log(1e-4) + k * (Math.log(20) - Math.log(1e-4)) / 58));
      var mg = A.map(function (a) { return a + 1e-6; }), cg = mg.slice();
      for (var it = 0; it < 600; it++) {
        var nm = [0], nc = [0], diff = 0;
        for (var j = 0; j < A.length; j++) {
          var rhs = 0;
          for (var p = 0; p < psi.length; p++) for (var q = 0; q < th.length; q++) {
            var m1 = R * A[j] / (G * psi[p]) + th[q];
            var c1 = Math.max(interp(m1, mg, cg), 1e-10);
            rhs += wt[q] / psi.length * Math.pow(G * psi[p] * c1, -GAM);
          }
          var c = Math.pow(beta * R * rhs, -1 / GAM);
          nc.push(c); nm.push(A[j] + c);
        }
        for (var t = 1; t < nm.length; t += 7) diff = Math.max(diff, Math.abs(interp(nm[t], mg, cg) - nc[t]));
        mg = nm; cg = nc;
        if (it > 5 && diff < 1e-6) break;
      }
      return { m: mg, c: cg };
    }
    QB.widget(el, {
      title: "How much would you spend?",
      sub: "A household that cannot borrow, facing income risk, decides how much of its cash on hand to spend each " +
           "year (cash is measured in years of its permanent income). Change its patience, how uncertain its income " +
           "is, and the chance of a year with no income at all. The left chart is its consumption function, against " +
           "the same household with no risk; the right, the share of an extra dollar it would spend.",
      panels: 2, height: 290,
      controls: [
        { k: "beta", label: "Patience, beta", min: 0.88, max: 0.99, step: 0.005, value: 0.96,
          fmt: function (x) { return x.toFixed(3); } },
        { k: "tsd", label: "Transitory income risk (spread)", min: 0.0, max: 0.3, step: 0.01, value: 0.1,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "p0", label: "Chance of a year with no income", min: 0.0, max: 0.03, step: 0.001, value: 0.005,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (g, v, st) {
        var risky = solve(v.beta, v.tsd, v.p0), sure = solve(v.beta, 0, 0);
        var ms = [], cr = [], cs = [], mpc = [];
        for (var k = 0; k <= 100; k++) {
          var m = 5 * k / 100;
          ms.push(m); cr.push(interp(m, risky.m, risky.c)); cs.push(interp(m, sure.m, sure.c));
        }
        for (k = 0; k < 100; k++) mpc.push((cr[k + 1] - cr[k]) / (ms[k + 1] - ms[k]));
        var a = g[0].axes({ x: [0, 5], y: [0, 2], title: "Consumption against cash on hand",
                            xlabel: "cash on hand (years of income)" });
        a.line([0, 2], [0, 2], { color: GREY_HINT, width: 1 });
        a.line(ms, cs, { color: BLUE, width: 2 });
        a.line(ms, cr, { color: GREEN, width: 2.5 });
        // the target: E m' = m, with E[1/psi] close to one
        var target = null;
        for (k = 1; k <= 100; k++) {
          var nxt = R * (ms[k] - cr[k]) / G + 1;
          if (nxt <= ms[k]) { target = ms[k]; break; }
        }
        if (target !== null) a.vline(target, { color: GOLD });
        var b = g[1].axes({ x: [0, 5], y: [0, 1], title: "Share of an extra dollar spent",
                            xlabel: "cash on hand (years of income)" });
        b.line(ms.slice(0, 100), mpc.map(function (x) { return Math.min(Math.max(x, 0), 1); }),
               { color: GREEN, width: 2.5 });
        st.target = target; st.ms = ms; st.mpc = mpc;
        st.imp = Math.pow(R * v.beta, 1 / GAM) / G;
      },
      readout: function (v, st) {
        if (!st.ms) return [];
        function at(x) { return st.mpc[Math.min(99, Math.round(x * 20))].toFixed(2); }
        return [["target cash on hand (gold line)", st.target === null ? "none in view" : st.target.toFixed(2) +
                 " years of income"],
                ["share of an extra dollar spent at half a year's cash", at(0.5)],
                ["at one year's cash; at three years'", at(1.0) + "; " + at(3.0)],
                ["impatience, (beta R)^(1/gamma) / G", st.imp.toFixed(3) + (st.imp < 1 ? " (impatient: a target exists)" :
                  " (patient: wealth grows without limit)")]];
      },
      note: "More risk, or a larger chance of a jobless year, makes the household hold back at every level of cash and " +
            "bends the consumption function: prudence (Part 22, chapter 6). Near zero cash it spends most of an extra " +
            "dollar; with a cushion, almost none. Computed in your browser by the endogenous grid method; nothing you " +
            "do here is stored or sent.",
    });
  };
  // ---- Part 23: capital and asset prices --------------------------------------------------------------------------
  W.tree = function (el) {
    // the Lucas tree of Part 23 (explainer.economics.agora.assets: disasters), in closed form: consumption growth
    // exp(g + s z) (here g = 2.5%, s = 2%) times (1 - b) in a disaster year; equity is the claim to consumption.
    // The reader sets risk aversion, patience and the chance of a disaster (sizes 15-65%, average about 30%), and sees
    // the premium and the safe rate against the US record (about 5.5 and 2 percent).
    var G = 0.025, S = 0.02;
    var SIZES = [0.15, 0.25, 0.35, 0.50, 0.65], W8 = [0.35, 0.25, 0.20, 0.12, 0.08];
    function E(power, p) {
      var normal = Math.exp(power * G + power * power * S * S / 2), d = 0;
      for (var i = 0; i < SIZES.length; i++) d += W8[i] * Math.pow(1 - SIZES[i], power);
      return normal * (1 - p + p * d);
    }
    function solve(gamma, rho, p) {
      var beta = Math.exp(-rho);
      var rf = 1 / (beta * E(-gamma, p)) - 1;
      var x = beta * E(1 - gamma, p);
      if (x >= 1) return null;
      var pd = x / (1 - x);
      var re = E(1, p) * (1 + pd) / pd - 1;
      return { rf: rf, re: re, premium: re - (rf), pd: pd };
    }
    QB.widget(el, {
      title: "Price the risk",
      sub: "A tree economy: everyone owns the trees and eats the fruit. Set how much people dislike risk, how patient " +
           "they are, and the yearly chance of a disaster that cuts consumption by 15 to 65 percent. The left chart " +
           "shows the equity premium against risk aversion, the right the safe interest rate. Can you match the US " +
           "record of about 5.5 percent and 2 percent with a risk aversion below 5?",
      panels: 2, height: 280,
      controls: [
        { k: "gamma", label: "Risk aversion, gamma", min: 0.5, max: 10, step: 0.1, value: 2,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "rho", label: "Impatience, a year", min: 0.0, max: 0.06, step: 0.002, value: 0.03,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "p", label: "Chance of a disaster, a year", min: 0, max: 0.04, step: 0.001, value: 0.017,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (g, v, st) {
        var gs = [], pr = [], rf = [], pr0 = [], rf0 = [];
        for (var k = 0; k <= 60; k++) {
          var gm = 0.5 + 9.5 * k / 60, a = solve(gm, v.rho, v.p), b = solve(gm, v.rho, 0);
          gs.push(gm);
          pr.push(a ? Math.min(100 * a.premium, 15) : NaN); rf.push(a ? Math.max(Math.min(100 * a.rf, 30), -10) : NaN);
          pr0.push(b ? Math.min(100 * b.premium, 15) : NaN); rf0.push(b ? Math.max(Math.min(100 * b.rf, 30), -10) : NaN);
        }
        var a1 = g[0].axes({ x: [0.5, 10], y: [0, 15], title: "Equity premium, % a year", xlabel: "risk aversion" });
        a1.hline(5.5, { color: GREY_HINT });
        a1.line(gs, pr0, { color: BLUE, width: 2 });
        a1.line(gs, pr, { color: RED, width: 2.5 });
        a1.vline(v.gamma, { color: GOLD });
        var a2 = g[1].axes({ x: [0.5, 10], y: [-10, 30], title: "Safe interest rate, % a year", xlabel: "risk aversion" });
        a2.hline(2, { color: GREY_HINT });
        a2.line(gs, rf0, { color: BLUE, width: 2 });
        a2.line(gs, rf, { color: RED, width: 2.5 });
        a2.vline(v.gamma, { color: GOLD });
        st.now = solve(v.gamma, v.rho, v.p);
      },
      readout: function (v, st) {
        var s = st.now;
        if (!s) return [["at this risk aversion", "no finite price: the tree would be worth more than everything"]];
        var hit = Math.abs(100 * s.premium - 5.5) < 1.0 && Math.abs(100 * s.rf - 2) < 1.5 && v.gamma < 5;
        return [["equity premium (red; blue without disasters)", (100 * s.premium).toFixed(2) + "%"],
                ["safe interest rate", (100 * s.rf).toFixed(2) + "%"],
                ["price-dividend ratio", s.pd.toFixed(1)],
                ["verdict", hit ? "you matched the record with ordinary risk aversion" :
                  "the record: a premium near 5.5% and a safe rate near 2% (grey lines)"]];
      },
      note: "Without disasters (blue), no plausible risk aversion gives a premium above a fraction of a percent, and " +
            "raising risk aversion sends the safe rate soaring: the equity premium and risk-free rate puzzles (Part " +
            "23, chapters 8-9). Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 24: looking for work -----------------------------------------------------------------------------------
  W.labour = function (el) {
    // the Diamond-Mortensen-Pissarides model of Part 24 (explainer.economics.agora.search: dmp_steady), monthly:
    // matching f = A theta^(1-eta), q = A theta^(-eta) with eta = 0.5; free entry c/q = (p - w)/(r + s); the Nash wage
    // w = (1 - beta) b + beta (p + c theta); so (r + s) c / q + beta c theta = (1 - beta)(p - b), solved by bisection.
    // The reader moves the benefit, the worker's share, separations and matching efficiency, and sees the two curves,
    // the Beveridge curve, and how much a 1% rise in productivity moves tightness (the volatility puzzle).
    var P = 1, ETA = 0.5, R = 0.004, C0 = 0.3;
    var BASE = { b: 0.4, beta: 0.5, s: 0.03, A: 0.6 };
    function steady(v, p) {
      p = p || P;
      var gap = function (th) { return (R + v.s) * C0 / (v.A * Math.pow(th, -ETA)) + v.beta * C0 * th - (1 - v.beta) * (p - v.b); };
      if (gap(1e-8) > 0) return null;
      var lo = 1e-8, hi = 1e4;
      for (var i = 0; i < 200; i++) { var mid = Math.sqrt(lo * hi); if (gap(mid) > 0) hi = mid; else lo = mid; }
      var th = Math.sqrt(lo * hi), f = v.A * Math.pow(th, 1 - ETA), u = v.s / (v.s + f);
      return { theta: th, f: f, u: u, v: th * u, w: (1 - v.beta) * v.b + v.beta * (p + C0 * th) };
    }
    QB.widget(el, {
      title: "Run the labour market",
      sub: "Workers and firms must find each other. Firms open vacancies until hiring costs what a worker is worth; " +
           "wages split each match's surplus. Move the benefit, the worker's share of the surplus, how often jobs " +
           "end, and how efficiently workers and jobs meet. Left: job creation (gold) and the wage curve (blue), with " +
           "the Island in grey. Right: the Beveridge curve and where the market sits. Can you find a benefit at which " +
           "a 1% rise in productivity moves tightness by 10% or more?",
      panels: 2, height: 280,
      controls: [
        { k: "b", label: "Benefit while unemployed, b (output = 1)", min: 0, max: 0.96, step: 0.01, value: 0.4,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "beta", label: "Worker's share of the surplus, beta", min: 0.05, max: 0.95, step: 0.01, value: 0.5,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "s", label: "Chance a job ends, a month", min: 0.01, max: 0.06, step: 0.001, value: 0.03,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "A", label: "Matching efficiency, A", min: 0.3, max: 1.0, step: 0.01, value: 0.6,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var th = [], jc = [], wc = [], jc0 = [], wc0 = [];
        for (var k = 0; k <= 120; k++) {
          var t = 0.02 + 5.98 * k / 120;
          th.push(t);
          jc.push(P - (R + v.s) * C0 / (v.A * Math.pow(t, -ETA)));
          wc.push((1 - v.beta) * v.b + v.beta * (P + C0 * t));
          jc0.push(P - (R + BASE.s) * C0 / (BASE.A * Math.pow(t, -ETA)));
          wc0.push((1 - BASE.beta) * BASE.b + BASE.beta * (P + C0 * t));
        }
        var now = steady(v), base = steady(BASE);
        var a1 = g[0].axes({ x: [0, 6], y: [0.8, 1.1], title: "Wage against tightness (openings per searcher)",
                             xlabel: "tightness, theta" });
        a1.line(th, jc0, { color: GREY_HINT, width: 1.5, dash: [4, 4] });
        a1.line(th, wc0, { color: GREY_HINT, width: 1.5, dash: [4, 4] });
        a1.line(th, jc, { color: GOLD, width: 2.5 });
        a1.line(th, wc, { color: BLUE, width: 2.5 });
        if (now) a1.dots([now.theta], [now.w], { color: RED, r: 5 });
        var us = [], vs = [];
        for (var j = 0; j <= 120; j++) {
          var t2 = Math.exp(Math.log(0.05) + (Math.log(20) - Math.log(0.05)) * j / 120);
          var f2 = v.A * Math.pow(t2, 1 - ETA), u2 = v.s / (v.s + f2);
          us.push(100 * u2); vs.push(100 * t2 * u2);
        }
        var a2 = g[1].axes({ x: [0, 15], y: [0, 15], title: "Vacancies against unemployment, %", xlabel: "unemployment, %" });
        a2.line(us, vs, { color: GREEN, width: 2.5 });
        if (base) a2.dots([100 * base.u], [100 * base.v], { color: GREY_HINT, r: 4 });
        if (now) {
          a2.line([0, 15], [0, 15 * now.theta], { color: GOLD, width: 1.5, dash: [5, 4] });
          a2.dots([100 * now.u], [100 * now.v], { color: RED, r: 5 });
        }
        st.now = now;
        st.el = null;
        if (now) {
          var up = steady(v, 1.01), dn = steady(v, 0.99);
          if (up && dn) st.el = (Math.log(up.theta) - Math.log(dn.theta)) / (Math.log(1.01) - Math.log(0.99));
        }
      },
      readout: function (v, st) {
        var s = st.now;
        if (!s) return [["the market", "no firm opens a vacancy: the benefit leaves nothing to share"]];
        var hos = Math.abs(v.beta - ETA) < 0.03 ? "efficient (beta = eta = 0.5, Hosios)" :
          (v.beta < ETA ? "too many vacancies (beta below eta)" : "too few vacancies (beta above eta)");
        return [["tightness; wage", s.theta.toFixed(2) + "; " + s.w.toFixed(3)],
                ["unemployment; vacancies", (100 * s.u).toFixed(2) + "%; " + (100 * s.v).toFixed(2) + "%"],
                ["job finding a month", (100 * s.f).toFixed(0) + "%"],
                ["1% more productivity moves tightness by", st.el === null ? "n/a" : st.el.toFixed(1) + "%" +
                  (st.el >= 10 ? ": volatile, as in the data" : ": too little, as in Shimer's puzzle")],
                ["efficiency", hos]];
      },
      note: "Raising the benefit toward output shrinks the 'fundamental surplus' p - b, and tightness becomes far more " +
            "sensitive to productivity: Hagedorn and Manovskii's answer to the volatility puzzle, and Ljungqvist and " +
            "Sargent's diagnosis (Part 24, chapter 9). Lower matching efficiency shifts the Beveridge curve out. " +
            "Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
