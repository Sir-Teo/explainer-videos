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
})();
