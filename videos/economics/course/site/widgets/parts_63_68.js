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
})();
