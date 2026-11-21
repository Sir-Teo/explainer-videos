// Interactives for Act XII, The Frontier (Parts 63-68).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;

  // ---- Part 63: the economy as a network -----------------------------------------------------------------------
  W.network = function (el) {
    // Agora's network module (explainer.economics.agora.network): the Island's eight sectors, input shares OMEGA
    // (rows buyers, columns suppliers; labour the rest) and consumption shares BETA.  Prices with the wage as
    // numeraire solve p_i^(1-t) = A_i^(t-1) (l_i + sum_j w_ij p_j^(1-t)) for an elasticity t between inputs (t = 1:
    // log p = -log A + OMEGA log p); log GDP = -sum_i beta_i log p_i.  Hulten's rule: d log GDP = lambda_i d log A_i
    // with Domar weights lambda' = beta' (I - OMEGA)^(-1).
    var NAMES = ["farms", "energy", "chips", "metals", "factories", "transport", "services", "retail"];
    var OM = [
      [0.10, 0.10, 0.00, 0.02, 0.08, 0.05, 0.05, 0.00],
      [0.00, 0.20, 0.02, 0.08, 0.05, 0.05, 0.05, 0.00],
      [0.00, 0.10, 0.10, 0.10, 0.05, 0.03, 0.10, 0.00],
      [0.00, 0.25, 0.00, 0.15, 0.05, 0.08, 0.05, 0.00],
      [0.02, 0.08, 0.10, 0.20, 0.10, 0.06, 0.08, 0.00],
      [0.00, 0.25, 0.02, 0.02, 0.08, 0.05, 0.08, 0.00],
      [0.01, 0.05, 0.05, 0.00, 0.02, 0.03, 0.15, 0.01],
      [0.15, 0.05, 0.01, 0.00, 0.20, 0.10, 0.10, 0.05]];
    var BETA = [0.05, 0.05, 0.02, 0.00, 0.10, 0.05, 0.45, 0.28];
    var N = 8, LAB = OM.map(function (r) { return 1 - r.reduce(function (a, b) { return a + b; }, 0); });
    var LAMBDA = (function () {
      var lam = BETA.slice();
      for (var it = 0; it < 400; it++) {
        var nx = BETA.slice();
        for (var i = 0; i < N; i++) { for (var j = 0; j < N; j++) { nx[i] += OM[j][i] * lam[j]; } }
        lam = nx;
      }
      return lam;
    })();
    function logGDP(logA, t) {
      var p = new Array(N).fill(1), i, j, it;
      if (Math.abs(t - 1) < 1e-9) {
        var lp = new Array(N).fill(0);
        for (it = 0; it < 600; it++) {
          var nl = [];
          for (i = 0; i < N; i++) { var s = -logA[i]; for (j = 0; j < N; j++) { s += OM[i][j] * lp[j]; } nl.push(s); }
          lp = nl;
        }
        p = lp.map(Math.exp);
      } else {
        for (it = 0; it < 3000; it++) {
          var np = [], diff = 0;
          for (i = 0; i < N; i++) {
            var s2 = LAB[i];
            for (j = 0; j < N; j++) { s2 += OM[i][j] * Math.pow(p[j], 1 - t); }
            var v = Math.pow(Math.exp((t - 1) * logA[i]) * s2, 1 / (1 - t));
            diff = Math.max(diff, Math.abs(v - p[i]));
            np.push(v);
          }
          p = np;
          if (diff < 1e-12) { break; }
        }
      }
      var y = 0;
      for (i = 0; i < N; i++) { y -= BETA[i] * Math.log(p[i]); }
      return y;
    }
    function shockOne(k, s, t) { var a = new Array(N).fill(0); a[k] = s; return logGDP(a, t); }
    QB.widget(el, {
      title: "Which failure costs the Island most?",
      sub: "Hit one of the Island's eight sectors with a productivity shock, choose how easily firms can swap one " +
           "input for another, and compare the fall in GDP with Hulten's rule, the sector's sales times the shock.",
      panels: 2, height: 280,
      controls: [
        { k: "sector", label: "Sector hit", min: 0, max: 7, step: 1, value: 1,
          fmt: function (x) { return NAMES[x]; } },
        { k: "shock", label: "Productivity change (log points)", min: -80, max: 30, step: 5, value: -50,
          fmt: function (x) { return (x > 0 ? "+" : "") + x; } },
        { k: "theta", label: "Elasticity of substitution between inputs", min: 0.05, max: 2, step: 0.05,
          value: 0.15, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var k = v.sector, t = v.theta, xs = [], ys = [], hs = [], s;
        for (s = -80; s <= 30; s += 2.5) {
          xs.push(s); ys.push(100 * shockOne(k, s / 100, t)); hs.push(LAMBDA[k] * s);
        }
        st.loss = 100 * shockOne(k, v.shock / 100, t);
        st.hulten = LAMBDA[k] * v.shock;
        var lo = Math.min(Math.min.apply(null, ys), Math.min.apply(null, hs)) - 2;
        var hi = Math.max(Math.max.apply(null, ys), Math.max.apply(null, hs)) + 2;
        var A = g[0].axes({ x: [-80, 30], y: [lo, hi], title: "GDP's change (log points), " + NAMES[k] + " hit",
                            xlabel: "the sector's productivity change (log points)" });
        A.line(xs, hs, { color: "#FFFFFF", width: 1.5, dash: [5, 4] });
        A.line(xs, ys, { color: "#F25F5C", width: 2.5 });
        A.vline(v.shock, { color: "#F2C14E" });
        A.hline(0, { color: "#9AA3B2" });
        A.legend([["computed", "#F25F5C"], ["Hulten: sales x shock", "#FFFFFF"]], "tl");
        var all = [], hul = [], ix = [];
        for (var j = 0; j < N; j++) {
          ix.push(j); all.push(-100 * shockOne(j, v.shock / 100, t)); hul.push(-LAMBDA[j] * v.shock);
        }
        st.rank = all.map(function (x, q) { return [Math.abs(x), NAMES[q]]; })
          .sort(function (a, b) { return b[0] - a[0]; });
        var top = Math.max(Math.max.apply(null, all), Math.max.apply(null, hul), 1) * 1.15;
        var bot = Math.min(Math.min.apply(null, all), Math.min.apply(null, hul), 0) * 1.15;
        var B = g[1].axes({ x: [-0.6, 7.6], y: [bot, top], xticks: ix,
                            xfmt: function (q) { return NAMES[q].slice(0, 5); },
                            title: "every sector hit the same way: GDP's fall (%); dots: Hulten" });
        B.bars(ix, all, 0.55, { color: "#7EC8F5" });
        B.dots(ix, hul, { color: "#FFFFFF", r: 3 });
      },
      readout: function (v, st) {
        return [["sales over GDP (Domar weight)", LAMBDA[v.sector].toFixed(3)],
                ["GDP's change: computed", st.loss.toFixed(1) + " log points"],
                ["GDP's change: Hulten's rule", st.hulten.toFixed(1) + " log points"],
                ["the sector that moves GDP most at this shock", st.rank[0][1]]];
      },
      note: "Part 63, chapters 2 to 5. Computed in your browser; nothing you do here is stored or sent.",
    });
  };

  // ---- Part 64: machines that learn -------------------------------------------------------------------------------
  W.bail = function (el) {
    // Agora's learn module (explainer.economics.agora.learn.courts), simplified: defendants with records (age,
    // priors, missed court dates, a charge, a job) and a courtroom signal s that only the judge sees.  The true
    // chance of failing to appear is logistic in the records and w s.  The algorithm ranks by the best prediction
    // from the records alone, E[p | records] (averaging over s by Gauss-Hermite); the judge ranks by an index that
    // weights the charge by c, uses w s, and adds noise.  Expected failures per 100 defendants are computed for
    // every detention rate, for both rankings; the reader sets w, c and the judge's strictness.
    var GH = [[-2.0201828705, 0.0199532421], [-0.9585724646, 0.3936193232], [0, 0.9453087205],
              [0.9585724646, 0.3936193232], [2.0201828705, 0.0199532421]];
    function sig(z) { return 1 / (1 + Math.exp(-z)); }
    function people(seed) {
      var u = QB.rng(6400 + seed), N = 4000, D = [];
      for (var i = 0; i < N; i++) {
        var age = 18 + Math.floor(u() * 43), lam = 0.4 + 2.2 * Math.exp(-(age - 18) / 12), pr = 0, L = Math.exp(-lam),
            prod = u();
        while (prod > L) { pr += 1; prod *= u(); }
        var ms = 0; for (var k = 0; k < Math.min(pr, 6); k++) { if (u() < 0.3) { ms += 1; } }
        var r = u(), ch = r < 0.35 ? 0 : (r < 0.65 ? 1 : (r < 0.85 ? 2 : 3));
        var job = u() < 0.40 + 0.25 * (age > 25 ? 1 : 0) ? 1 : 0;
        var z0 = -2.35 + 0.55 * Math.log(1 + pr) + 0.65 * Math.min(ms, 3) + 0.55 * (age < 23 ? 1 : 0) +
                 0.45 * (age < 23 && pr >= 2 ? 1 : 0) - 0.45 * job + 0.25 * (ch === 2 ? 1 : 0) -
                 0.25 * (ch === 3 ? 1 : 0);
        D.push({ z0: z0, s: u.normal(), e: u.normal(), pr: pr, ms: ms, ch: ch, job: job });
      }
      return D;
    }
    var POP = people(0);
    function frontier(order, p) {
      var N = p.length, xs = [], ys = [], tot = 0, k;
      for (k = 0; k < N; k++) { tot += p[k]; }
      var cum = 0, j = 0;
      for (var d = 0; d <= 60; d += 2) {
        var m = Math.round(d / 100 * N);
        while (j < m) { cum += p[order[j]]; j += 1; }
        xs.push(d); ys.push(100 * (tot - cum) / N);
      }
      return { x: xs, y: ys };
    }
    QB.widget(el, {
      title: "The judge, the algorithm, and what the judge can see",
      sub: "Detaining more defendants prevents more failures to appear. Choose how much the judge sees in court that " +
           "the records do not, how heavily the judge weighs the charge (which barely predicts coming back), and how " +
           "strict the judge is; compare the judge's failures with an algorithm that ranks by the records alone.",
      panels: 1, height: 300,
      controls: [
        { k: "w", label: "What the judge sees beyond the records", min: 0, max: 1.8, step: 0.15, value: 0.45,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "c", label: "Weight the judge gives the charge", min: 0, max: 1.2, step: 0.1, value: 0.55,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "d", label: "Judge's detention rate", min: 10, max: 50, step: 2, value: 28,
          fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, st) {
        var N = POP.length, p = [], alg = [], jud = [], i, q;
        for (i = 0; i < N; i++) {
          var a = POP[i];
          p.push(sig(a.z0 + v.w * a.s));
          var ea = 0; for (q = 0; q < GH.length; q++) { ea += GH[q][1] * sig(a.z0 + v.w * Math.SQRT2 * GH[q][0]); }
          alg.push(ea / Math.sqrt(Math.PI));
          jud.push(0.35 * a.pr + 0.30 * a.ms + v.c * a.ch - 0.20 * a.job + v.w * a.s + 0.7 * a.e);
        }
        var idx = []; for (i = 0; i < N; i++) { idx.push(i); }
        var oa = idx.slice().sort(function (x, y) { return alg[y] - alg[x]; });
        var oj = idx.slice().sort(function (x, y) { return jud[y] - jud[x]; });
        var fa = frontier(oa, p), fj = frontier(oj, p);
        var k = Math.round(v.d / 2);
        st.alg = fa.y[k]; st.jud = fj.y[k];
        var top = Math.max.apply(null, fj.y.concat(fa.y)) * 1.05;
        var A = g[0].axes({ x: [0, 60], y: [0, top], title: "failures to appear per 100 defendants",
                            xlabel: "share detained, %" });
        A.line(fj.x, fj.y, { color: "#E8A0B4", width: 2.5 });
        A.line(fa.x, fa.y, { color: "#7EC8F5", width: 2.5 });
        A.vline(v.d, { color: "#F2C14E" });
        A.dots([v.d, v.d], [st.jud, st.alg], { color: function (j) { return j ? "#7EC8F5" : "#E8A0B4"; }, r: 5 });
        A.legend([["the judge", "#E8A0B4"], ["the algorithm (records only)", "#7EC8F5"]], "tr");
      },
      readout: function (v, st) {
        var diff = 100 * (1 - st.alg / st.jud);
        return [["judge's failures per 100", st.jud.toFixed(1)],
                ["algorithm's, same detention", st.alg.toFixed(1)],
                ["the algorithm prevents", (diff >= 0 ? "" : "minus ") + Math.abs(diff).toFixed(0) +
                 "% of the judge's failures"]];
      },
      note: "Part 64, chapters 2, 3 and 15. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
