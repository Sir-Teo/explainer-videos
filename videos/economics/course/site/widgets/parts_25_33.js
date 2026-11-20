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

  // ---- Part 26: banks and runs ---------------------------------------------------------------------------------
  W.bankrun = function (el) {
    // The global game of Part 26 (explainer.economics.agora.bank: global_game): a bank of strength theta fails if the
    // share of depositors withdrawing reaches theta.  A withdrawer gets c; a stayer gets R = 2 if the bank survives and
    // nothing if it fails.  Each depositor sees theta + sigma e and withdraws below a cutoff.  The reader sets the
    // cutoff everyone else uses and finds their own best reply; the unique equilibrium is where the two agree, and
    // the bank then fails exactly when theta < c / R.
    var R = 2;
    function failPoint(xo, sig) {
      // the bank fails while theta <= share withdrawing = Phi((xo - theta)/sig); find the crossing by bisection
      var lo = -1, hi = 2;
      for (var k = 0; k < 80; k++) {
        var m = (lo + hi) / 2;
        if (m - QB.cdf((xo - m) / sig) < 0) lo = m; else hi = m;
      }
      return (lo + hi) / 2;
    }
    function bestReply(xo, c, sig) {
      // staying pays R * P(theta > theta_f | x) = R * Phi((x - theta_f)/sig): indifferent where that equals c
      return failPoint(xo, sig) + sig * QB.inv(Math.min(Math.max(c / R, 1e-6), 1 - 1e-6));
    }
    QB.widget(el, {
      title: "Run on the bank",
      sub: "You are one depositor among thousands. Each of you sees a slightly noisy reading of how strong the bank " +
           "is, and withdraws if it looks weak enough. Set the cutoff everyone else uses. Left: the share who " +
           "withdraw at each strength, and where the bank fails (above the dashed line). Right: your best cutoff " +
           "against theirs. Can you find the cutoff at which you would do exactly what everyone else does?",
      panels: 2, height: 280,
      controls: [
        { k: "xo", label: "Everyone else's cutoff", min: 0, max: 1, step: 0.005, value: 0.3,
          fmt: function (x) { return x.toFixed(3); } },
        { k: "c", label: "What a withdrawal pays (staying pays 2 if the bank survives)", min: 0.2, max: 1.8,
          step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "sig", label: "Noise in each depositor's reading", min: 0.01, max: 0.2, step: 0.005, value: 0.05,
          fmt: function (x) { return x.toFixed(3); } },
      ],
      draw: function (g, v, st) {
        var th = [], sh = [], k;
        for (k = 0; k <= 200; k++) { var t = k / 200; th.push(t); sh.push(QB.cdf((v.xo - t) / v.sig)); }
        var tf = failPoint(v.xo, v.sig);
        var a1 = g[0].axes({ x: [0, 1], y: [0, 1], title: "Share withdrawing", xlabel: "the bank's strength" });
        a1.line([0, 1], [0, 1], { color: GREY_HINT, width: 1, dash: [4, 4] });
        a1.line(th, sh, { color: RED, width: 2.5 });
        if (tf > 0 && tf < 1) a1.vline(tf, { color: GOLD, width: 2, dash: [] });
        var xs = [], br = [];
        for (k = 0; k <= 100; k++) { var x = k / 100; xs.push(x); br.push(bestReply(x, v.c, v.sig)); }
        var a2 = g[1].axes({ x: [0, 1], y: [0, 1], title: "Your best cutoff", xlabel: "everyone else's cutoff" });
        a2.line([0, 1], [0, 1], { color: GREY_HINT, width: 1, dash: [4, 4] });
        a2.line(xs, br, { color: BLUE, width: 2.5 });
        var mine = bestReply(v.xo, v.c, v.sig);
        a2.dots([v.xo], [Math.min(Math.max(mine, 0), 1)], { color: GOLD, r: 5 });
        var ts = v.c / R, xstar = ts + v.sig * QB.inv(Math.min(Math.max(ts, 1e-6), 1 - 1e-6));
        a2.dots([xstar], [xstar], { color: GREEN, r: 5 });
        st.tf = tf; st.mine = mine; st.ts = ts; st.xstar = xstar;
      },
      readout: function (v, st) {
        var gap = Math.abs(st.mine - v.xo);
        return [["the bank fails below", st.tf.toFixed(3)],
                ["your best cutoff", st.mine.toFixed(3) + (st.mine > v.xo ? " (run sooner than the others)" :
                                                                         " (run later than the others)")],
                ["the equilibrium", "everyone at " + st.xstar.toFixed(3) + "; the bank fails below c/R = " +
                  st.ts.toFixed(2)],
                ["verdict", gap < 0.01 ? "you found it: nobody wants a different cutoff" :
                  "not yet: if everyone used your best cutoff, your best cutoff would move"]];
      },
      note: "However small the noise, there is only one cutoff that is everyone's best reply to itself (Morris and " +
            "Shin 1998). Raise what a withdrawal pays and the failure threshold c/R rises: better insurance for the " +
            "impatient means more runs (Goldstein and Pauzner 2005). Part 26, chapter 10. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };

  // ---- Part 27: the co-op ----------------------------------------------------------------------------------------
  W.coop = function (el) {
    // The babysitting co-op of Part 27 (explainer.economics.agora.keynes: coop): 150 couples, each wanting a reserve
    // of coupons; a couple wants to go out with probability p min(1, b/target) and is willing to sit with probability
    // p clip(2 - b/target, 0, 1) if it is not going out; evenings are the shorter queue and each costs a coupon.
    // The reader is the board: set the coupons per couple and the reserve couples want, and watch a year of weeks.
    var N = 150, P = 0.3, WEEKS = 52;
    function run(coupons, target, seed) {
      var r = QB.rng(seed), b = [], k;
      for (k = 0; k < N; k++) b.push(Math.floor(coupons));
      var extra = Math.round((coupons - Math.floor(coupons)) * N);
      for (k = 0; k < extra; k++) b[k] += 1;
      var ev = [];
      for (var w = 0; w < WEEKS; w++) {
        var go = [], sit = [];
        for (k = 0; k < N; k++) {
          var g = b[k] >= 1 && r() < P * Math.min(1, b[k] / target);
          if (g) go.push(k);
          else if (r() < P * Math.min(1, Math.max(0, 2 - b[k] / target))) sit.push(k);
        }
        var n = Math.min(go.length, sit.length);
        for (k = 0; k < n; k++) { b[go[k]] -= 1; b[sit[k]] += 1; }
        ev.push(n / N);
      }
      return ev;
    }
    QB.widget(el, {
      title: "Run the co-op",
      sub: "You are the co-op's board. 150 couples pay for babysitting with coupons, and each wants a reserve of " +
           "coupons for later. Set how many coupons there are and how big a reserve couples want, and watch a year " +
           "of weeks. Left: evenings out each week. Right: evenings against the number of coupons. Can you find the " +
           "number of coupons that gets the most evenings, and see why too few and too many both fail?",
      panels: 2, height: 280,
      controls: [
        { k: "m", label: "Coupons per couple", min: 1, max: 24, step: 0.5, value: 4,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "t", label: "The reserve each couple wants", min: 4, max: 16, step: 1, value: 10,
          fmt: function (x) { return x.toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var ev = run(v.m, v.t, 7), ws = [], k;
        for (k = 0; k < ev.length; k++) ws.push(k + 1);
        var a1 = g[0].axes({ x: [1, WEEKS], y: [0, 0.3], title: "Evenings per couple, week by week", xlabel: "week" });
        a1.line(ws, ev, { color: GOLD, width: 2 });
        a1.hline(P * (1 - P), { color: GREEN });
        var ms = [], es = [];
        for (var m = 1; m <= 24; m += 1) { ms.push(m); var e = run(m, v.t, 11); es.push(QB.mean(e.slice(12))); }
        var a2 = g[1].axes({ x: [0, 24], y: [0, 0.3], title: "Evenings against coupons", xlabel: "coupons per couple" });
        a2.line(ms, es, { color: BLUE, width: 2.5 });
        var mine = QB.mean(ev.slice(12));
        a2.dots([v.m], [mine], { color: GOLD, r: 5 });
        a2.vline(v.t, { color: GREY_HINT });
        var best = 0;
        for (k = 1; k < es.length; k++) if (es[k] > es[best]) best = k;
        st.mine = mine; st.best = ms[best]; st.bestEv = es[best];
      },
      readout: function (v, st) {
        var verdict = st.mine > 0.9 * st.bestEv ? "close to the most the co-op can do" :
          (v.m < st.best ? "a recession: everyone is hoarding, so nobody earns" :
                           "too many coupons: nobody needs to sit, so evenings are scarce");
        return [["evenings per couple a week", st.mine.toFixed(3)],
                ["the best number of coupons", "about " + st.best.toFixed(0) + " per couple (" + st.bestEv.toFixed(3) +
                  " evenings)"],
                ["verdict", verdict]];
      },
      note: "Nobody in the co-op is lazy or unskilled, and nobody's taste for evenings out changes: only the quantity " +
            "of money against the reserve people want. Part 27, chapters 0-3 (Sweeney and Sweeney 1977). Computed " +
            "in your browser; nothing you do here is stored or sent.",
    });
  };
})();
