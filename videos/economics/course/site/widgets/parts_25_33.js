// Interactives for Act VI, Money and the Cycle (Parts 25-33).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1", BLUE = "#9FB8F2";

  // ---- Part 25: money ------------------------------------------------------------------------------------------
  W.inflationtax = function (el) {
    // Cagan's economy of Part 25 (explainer.economics.agora.money: cagan_deficit): real balances m = exp(-alpha pe)
    // (alpha in months), a monthly deficit d (as a share of the real balances held at zero inflation) paid by printing;
    // seigniorage (pi/(1+pi)) m; expectations adapt, pe' = pe + lam (pi - pe).  The reader sets the deficit, alpha and
    // how fast expectations adapt, and sees the Laffer curve with its steady states and the path of inflation.
    function laffer(alpha, pi) { return pi / (1 + pi) * Math.exp(-alpha * pi); }
    function steadies(alpha, d) {
      var lo = null, hi = null, prev = laffer(alpha, 0) - d;
      for (var k = 1; k <= 4000; k++) {
        var pi = 4 * k / 4000, g = laffer(alpha, pi) - d;
        if (prev < 0 && g >= 0 && lo === null) lo = pi;
        if (prev >= 0 && g < 0) hi = pi;
        prev = g;
      }
      return { lo: lo, hi: hi };
    }
    function path(alpha, d, lam, months) {
      var pe = 0.01, out = [], mPrev = Math.exp(-alpha * pe);
      for (var t = 0; t < months; t++) {
        var m = Math.exp(-alpha * pe);
        if (m < 1e-12) { out.push(Infinity); break; }
        var growth = 1 + d / m;
        var pi = t ? growth * mPrev / m - 1 : growth - 1;
        out.push(pi);
        pe = pe + lam * (pi - pe);
        mPrev = m;
        if (pi > 1e6) break;
      }
      return out;
    }
    QB.widget(el, {
      title: "Print to pay the bills",
      sub: "A government pays a monthly deficit by printing money. People hold less money the more inflation they " +
           "expect. Left: the inflation tax's Laffer curve, with the deficit as a line; where they cross, inflation " +
           "can settle. Right: inflation month by month, starting from 1%. Can you find a deficit the government " +
           "can finance for ever when expectations adapt slowly, but not when they adapt fast?",
      panels: 2, height: 280,
      controls: [
        { k: "d", label: "Deficit, % of real balances a month", min: 0, max: 0.1, step: 0.002, value: 0.04,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "alpha", label: "Semi-elasticity alpha, months", min: 2, max: 10, step: 0.1, value: 5,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "lam", label: "How fast expectations adapt, a month", min: 0.02, max: 1, step: 0.01, value: 0.1,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
      ],
      draw: function (g, v, st) {
        var xs = [], ys = [], ymax = 0;
        for (var k = 0; k <= 200; k++) { var pi = 1.2 * k / 200; xs.push(100 * pi); var y = laffer(v.alpha, pi); ys.push(100 * y); ymax = Math.max(ymax, y); }
        var a1 = g[0].axes({ x: [0, 120], y: [0, Math.max(12, 100 * ymax * 1.3)], title: "Seigniorage, % of real balances",
                             xlabel: "inflation, % a month" });
        a1.line(xs, ys, { color: RED, width: 2.5 });
        a1.hline(100 * v.d, { color: GOLD });
        var s = steadies(v.alpha, v.d);
        if (s.lo !== null) a1.dots([100 * s.lo], [100 * laffer(v.alpha, s.lo)], { color: GREEN, r: 5 });
        if (s.hi !== null) a1.dots([100 * s.hi], [100 * laffer(v.alpha, s.hi)], { color: RED, r: 5 });
        var p = path(v.alpha, v.d, v.lam, 60), ts = [], ps = [];
        for (var t = 0; t < p.length; t++) { ts.push(t); ps.push(isFinite(p[t]) ? Math.min(100 * p[t], 200) : 200); }
        var a2 = g[1].axes({ x: [0, 60], y: [0, 200], title: "Inflation, % a month", xlabel: "months" });
        a2.line(ts, ps, { color: BLUE, width: 2.5 });
        if (s.lo !== null) a2.hline(100 * s.lo, { color: GREEN });
        st.s = s; st.p = p; st.max = Math.exp(-1) / v.alpha;
      },
      readout: function (v, st) {
        var s = st.s, p = st.p, last = p[p.length - 1];
        var exploded = !isFinite(last) || last > 2 || p.length < 60;
        var settled = !exploded && s.lo !== null && Math.abs(last - s.lo) < 0.01;
        return [["steady states", s.lo === null ? "none: the deficit exceeds what printing can raise" :
                  (100 * s.lo).toFixed(1) + "% and " + (100 * s.hi).toFixed(0) + "% a month"],
                ["most printing can raise", "about " + (100 * st.max).toFixed(1) + "% of real balances a month"],
                ["inflation after the run", exploded ? "it ran away: hyperinflation" : (100 * last).toFixed(1) + "% a month"],
                ["verdict", settled ? "inflation settled at the low steady state" :
                  (exploded ? "with these expectations, printing cannot pay this deficit" : "still moving")]];
      },
      note: "With slowly adapting expectations the low steady state is stable; with fast ones (alpha times the " +
            "speed above one) inflation runs away even when a steady state exists. Only cutting the deficit ends it: " +
            "Part 25, chapters 6-8. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
