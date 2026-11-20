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

  // ---- Part 28: the natural rate ---------------------------------------------------------------------------------
  W.natural = function (el) {
    // The expectations-augmented Phillips curve of Part 28 (explainer.economics.agora.expectations: accelerate):
    // pi_t = pi^e_t - beta (u_t - u*), with expectations adapting at rate lambda.  The reader is the central bank:
    // choose the unemployment rate to hold for twenty years, and how fast people learn; watch inflation, and the
    // short-run curves shift.
    var USTAR = 5, BETA = 0.5, YEARS = 20;
    function run(u, lam, pi0) {
      var pe = pi0, pis = [], pes = [];
      for (var t = 0; t < YEARS; t++) {
        var p = pe - BETA * (u - USTAR);
        pis.push(p); pes.push(pe);
        pe = pe + lam * (p - pe);
      }
      return { pi: pis, pe: pes };
    }
    QB.widget(el, {
      title: "Hold unemployment down",
      sub: "You run the central bank. The natural rate of unemployment is 5%. Choose the unemployment rate to hold for " +
           "twenty years, and how quickly people learn from inflation they did not expect. Left: inflation year by " +
           "year. Right: the short-run Phillips curve in year 1, 10 and 20. Can you find any unemployment rate below " +
           "5% that does not make inflation run away?",
      panels: 2, height: 280,
      controls: [
        { k: "u", label: "Unemployment you hold, %", min: 3, max: 7, step: 0.1, value: 4,
          fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "lam", label: "How fast expectations learn (share of each surprise)", min: 0, max: 1, step: 0.05, value: 1,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
      ],
      draw: function (g, v, st) {
        var r = run(v.u, v.lam, 2), ys = [], k;
        for (k = 0; k < YEARS; k++) ys.push(k + 1);
        var top = Math.max(12, Math.max.apply(null, r.pi) + 1), bot = Math.min(-4, Math.min.apply(null, r.pi) - 1);
        var a1 = g[0].axes({ x: [1, YEARS], y: [bot, top], title: "Inflation, %", xlabel: "year" });
        a1.line(ys, r.pi, { color: RED, width: 2.5 });
        a1.line(ys, r.pe, { color: GOLD, width: 1.5 });
        a1.hline(2, { color: GREY_HINT });
        var a2 = g[1].axes({ x: [2, 8], y: [bot, top], title: "Short-run curves", xlabel: "unemployment, %" });
        [0, 9, 19].forEach(function (t, i) {
          var us = [2, 8], ps = us.map(function (uu) { return r.pe[t] - BETA * (uu - USTAR); });
          a2.line(us, ps, { color: [BLUE, GOLD, RED][i], width: 2 });
        });
        a2.vline(USTAR, { color: GREEN });
        a2.dots([v.u, v.u, v.u], [r.pi[0], r.pi[9], r.pi[19]], { color: "#ffffff", r: 4 });
        st.r = r;
      },
      readout: function (v, st) {
        var last = st.r.pi[YEARS - 1], first = st.r.pi[0];
        var verdict = Math.abs(v.u - USTAR) < 0.05 ? "at the natural rate, inflation stays where people expect it" :
          (v.lam === 0 ? "people never learn, so the trade-off lasts: the 1960s menu, which did not survive" :
           (v.u < USTAR ? "inflation keeps rising: every year needs a bigger surprise" :
                          "inflation keeps falling: the cost of holding unemployment above the natural rate"));
        return [["inflation in year 1", first.toFixed(1) + "%"], ["inflation in year 20", last.toFixed(1) + "%"],
                ["verdict", verdict]];
      },
      note: "Friedman (1968) and Phelps (1967): there is no permanent trade-off unless people never learn. Part 28, " +
            "chapter 3. Computed in your browser; nothing you do here is stored or sent.",
    });
  };

  // ---- Part 29: the cake -----------------------------------------------------------------------------------------
  W.cake = function (el) {
    // The cake of Part 29 (explainer.economics.agora.dp: cake): V(w) = max_c log c + beta V(w - c) on a grid of cake
    // sizes, by value function iteration from V = 0.  The reader sets patience, the grid and the number of
    // iterations, and watches V_n approach the exact value and the gap between iterates shrink by beta each step.
    function solve(beta, n, iters) {
      var w = [], i, j, k;
      for (i = 0; i < n; i++) w.push((i + 1) / n);
      var V = new Float64Array(n), gaps = [], pol = new Int32Array(n);
      for (k = 0; k < iters; k++) {
        var Vn = new Float64Array(n), gap = 0;
        for (i = 0; i < n; i++) {
          var best = (i === 0) ? Math.log(w[0]) + beta * V[0] : -1e300, arg = 0;
          for (j = 0; j < i; j++) {
            var v = Math.log(w[i] - w[j]) + beta * V[j];
            if (v > best) { best = v; arg = j; }
          }
          Vn[i] = best; pol[i] = arg;
          gap = Math.max(gap, Math.abs(best - V[i]));
        }
        V = Vn; gaps.push(gap);
      }
      return { w: w, V: V, gaps: gaps, pol: pol };
    }
    function exact(beta, x) {
      return Math.log(1 - beta) / (1 - beta) + beta * Math.log(beta) / Math.pow(1 - beta, 2) + Math.log(x) / (1 - beta);
    }
    QB.widget(el, {
      title: "Eat the cake by iteration",
      sub: "A cake of size 1 must last for ever; each day you eat some, valued by its logarithm, and tomorrow counts " +
           "beta as much as today. The computer starts from V = 0 and applies the Bellman equation again and again. " +
           "Left: the value after n iterations (the best you can do if the world ends after n days) against the " +
           "exact answer, dashed. Right: the largest change between successive iterations, on a log scale. How many " +
           "iterations does a patient eater need?",
      panels: 2, height: 280,
      controls: [
        { k: "beta", label: "Patience beta", min: 0.5, max: 0.97, step: 0.01, value: 0.9,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Cake sizes on the grid", min: 21, max: 201, step: 10, value: 101,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "it", label: "Iterations", min: 1, max: 300, step: 1, value: 20,
          fmt: function (x) { return x.toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var r = solve(v.beta, Math.round(v.n), Math.round(v.it)), i;
        var lo = Math.max(1, Math.round(0.05 * r.w.length)), xs = [], ys = [], ex = [];
        for (i = lo; i < r.w.length; i++) { xs.push(r.w[i]); ys.push(r.V[i]); ex.push(exact(v.beta, r.w[i])); }
        var bot = Math.min(Math.min.apply(null, ex), Math.min.apply(null, ys)) - 1;
        var a1 = g[0].axes({ x: [0, 1], y: [bot, 1], title: "Value after n iterations", xlabel: "cake" });
        a1.line(xs, ex, { color: GREY_HINT, width: 1.5, dash: [5, 4] });
        a1.line(xs, ys, { color: GREEN, width: 2.5 });
        var its = [], lg = [], ref = [];
        for (i = 0; i < r.gaps.length; i++) {
          its.push(i + 1); lg.push(Math.log10(Math.max(r.gaps[i], 1e-16)));
          ref.push(Math.log10(r.gaps[0]) + i * Math.log10(v.beta));
        }
        var a2 = g[1].axes({ x: [1, Math.max(2, r.gaps.length)], y: [-12, 2], title: "Largest change (log10)",
                             xlabel: "iteration" });
        a2.line(its, ref, { color: GREY_HINT, width: 1, dash: [4, 4] });
        a2.line(its, lg, { color: GOLD, width: 2.5 });
        var m = r.w.length, share = 0, cnt = 0;
        for (i = Math.round(0.2 * m); i < m; i++) {
          var c = r.w[i] - r.w[r.pol[i]];
          share += c / r.w[i]; cnt += 1;
        }
        st.share = share / cnt; st.gap = r.gaps[r.gaps.length - 1];
        st.need = Math.ceil(Math.log(1e-6 / r.gaps[0]) / Math.log(v.beta));
      },
      readout: function (v, st) {
        return [["share of the cake eaten each day", (100 * st.share).toFixed(1) + "% (exact: " +
                  (100 * (1 - v.beta)).toFixed(1) + "%)"],
                ["last change", st.gap.toExponential(2)],
                ["iterations to reach a change of one in a million", "about " + st.need],
                ["verdict", st.gap < 1e-6 ? "converged: more iterations change nothing you could see" :
                  "not yet: each iteration shrinks the change by a factor beta"]];
      },
      note: "The Bellman operator is a contraction with modulus beta (Blackwell 1965), so the dashed line on the " +
            "right, falling by log10(beta) per step, bounds the gold one. A coarse grid eats a little too much, " +
            "because it can only cut the cake in whole grid steps. Part 29, chapters 3-4. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };

  // ---- Part 30: the three equations ----------------------------------------------------------------------------
  W.nk = function (el) {
    // The three-equation New Keynesian model of Part 30 (explainer.economics.agora.nk: irf_ar1, determinacy), with
    // Gali's calibration: pi = beta E pi' + kappa x + u; x = E x' - (i - E pi' - r^n)/sigma; i = phi_pi pi + phi_x x
    // + v.  AR(1) shocks with persistence 0.5, solved by undetermined coefficients.  The reader sets the central
    // bank's response to inflation, how sticky prices are, and which shock hits.
    var BETA = 0.99, SIGMA = 1, PHI = 1, ALPHA = 1 / 3, EPS = 6, PHIX = 0.125, RHO = 0.5, Q = 12;
    function kappa(theta) {
      var lam = (1 - theta) * (1 - BETA * theta) / theta * (1 - ALPHA) / (1 - ALPHA + ALPHA * EPS);
      return lam * (SIGMA + (PHI + ALPHA) / (1 - ALPHA));
    }
    function solve(fp, theta, shock) {
      var k = kappa(theta);
      var a11 = 1 - RHO + PHIX / SIGMA, a12 = (fp - RHO) / SIGMA, a21 = -k, a22 = 1 - BETA * RHO;
      var b = shock === 1 ? [-1 / SIGMA, 0] : (shock === 2 ? [1 / SIGMA, 0] : [0, 1]);
      var det = a11 * a22 - a12 * a21;
      var px = (b[0] * a22 - a12 * b[1]) / det, pp = (a11 * b[1] - a21 * b[0]) / det;
      var x = [], pi = [], i = [], q = [];
      for (var t = 0; t < Q; t++) {
        var s = 0.25 * Math.pow(RHO, t);
        q.push(t); x.push(px * s); pi.push(4 * pp * s);
        i.push(4 * (fp * pp * s + PHIX * px * s + (shock === 1 ? s : 0)));
      }
      var unique = k * (fp - 1) + (1 - BETA) * PHIX > 0;
      return { q: q, x: x, pi: pi, i: i, kappa: k, unique: unique };
    }
    QB.widget(el, {
      title: "Run the three equations",
      sub: "You set the central bank's response to inflation and how long prices last, and choose a shock: 1, a " +
           "monetary tightening; 2, a rise in demand; 3, a cost-push shock (each one point a year, fading by half " +
           "each quarter). Left: the output gap. Right: inflation and the policy rate, at annual rates. What happens " +
           "when the response to inflation falls below one?",
      panels: 2, height: 280,
      controls: [
        { k: "fp", label: "Response to inflation, phi_pi", min: 0.5, max: 3, step: 0.05, value: 1.5,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "theta", label: "Chance a price survives a quarter, theta", min: 0.3, max: 0.9, step: 0.01,
          value: 0.67, fmt: function (x) { return x.toFixed(2) + " (" + (3 / (1 - x)).toFixed(1) + " months)"; } },
        { k: "shock", label: "Shock: 1 monetary, 2 demand, 3 cost-push", min: 1, max: 3, step: 1, value: 1,
          fmt: function (x) { return ["", "monetary", "demand", "cost-push"][Math.round(x)]; } },
      ],
      draw: function (g, v, st) {
        var r = solve(v.fp, v.theta, Math.round(v.shock));
        var lo = Math.min(-0.5, Math.min.apply(null, r.x)), hi = Math.max(0.5, Math.max.apply(null, r.x));
        var a1 = g[0].axes({ x: [0, Q - 1], y: [lo, hi], title: "Output gap, %", xlabel: "quarters" });
        a1.hline(0, { color: GREY_HINT });
        if (r.unique) a1.line(r.q, r.x, { color: GREEN, width: 2.5 });
        var all = r.pi.concat(r.i);
        var lo2 = Math.min(-0.5, Math.min.apply(null, all)), hi2 = Math.max(0.5, Math.max.apply(null, all));
        var a2 = g[1].axes({ x: [0, Q - 1], y: [lo2, hi2], title: "Inflation and the policy rate, % a year",
                             xlabel: "quarters" });
        a2.hline(0, { color: GREY_HINT });
        if (r.unique) {
          a2.line(r.q, r.pi, { color: RED, width: 2.5 });
          a2.line(r.q, r.i, { color: GOLD, width: 2 });
        }
        st.r = r;
      },
      readout: function (v, st) {
        var r = st.r;
        if (!r.unique) {
          return [["kappa, the Phillips curve's slope", r.kappa.toFixed(3)],
                  ["verdict", "no unique equilibrium: with the rate rising less than inflation, any inflation people " +
                    "expect can come true (the Taylor principle fails)"]];
        }
        return [["kappa, the Phillips curve's slope", r.kappa.toFixed(3)],
                ["on impact", "gap " + r.x[0].toFixed(2) + "%, inflation " + r.pi[0].toFixed(2) + ", policy rate " +
                  r.i[0].toFixed(2)],
                ["verdict", Math.round(v.shock) === 3 ? "a cost-push shock moves output and inflation apart: the " +
                  "central bank must choose" : "output and inflation move together: stickier prices mean more " +
                  "output and less inflation"]];
      },
      note: "Gali's calibration (2015, ch. 3): beta 0.99, sigma 1, phi 1, alpha 1/3, epsilon 6, phi_x 0.125. " +
            "Part 30, chapters 5-9. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 31: the chair ---------------------------------------------------------------------------------------
  W.chair = function (el) {
    // The chair of Part 31 (videos/economics/econ31/compute.py, item realtime): for each year, CPI inflation over the
    // year before, the output gap at the end of that year as the data of the day showed it (a log-linear trend fitted
    // to the Philadelphia Fed's first-quarter vintage) and as the CBO's potential shows it today, and the federal
    // funds rate in the first quarter.  The reader sets the rate year by year; the page compares Taylor's rule with
    // each gap, and what the Federal Reserve did.
    var D = [
      [1966, 1.78, 3.38, 4.60, 4.56],
      [1967, 3.57, 4.20, 4.67, 4.82],
      [1968, 2.99, 3.11, 2.87, 4.79],
      [1969, 4.63, 4.13, 3.29, 6.57],
      [1970, 5.83, 1.46, 1.30, 8.57],
      [1971, 5.60, -3.23, -2.31, 3.86],
      [1972, 3.54, -2.18, -1.21, 3.55],
      [1973, 3.33, 1.77, 2.22, 6.54],
      [1974, 8.42, 1.50, 2.74, 9.32],
      [1975, 12.05, -6.67, -2.70, 6.30],
      [1976, 7.38, -6.88, -3.35, 4.83],
      [1977, 5.19, -4.69, -2.23, 4.66],
      [1978, 6.59, -2.03, -0.63, 6.76],
      [1979, 8.93, -1.47, 2.34, 10.07],
      [1980, 12.64, -3.02, 0.28, 15.05],
      [1981, 12.54, -4.61, -2.02, 16.57],
      [1982, 9.58, -7.13, -3.23, 14.23],
      [1983, 4.44, -10.92, -7.57, 8.65],
      [1984, 3.23, -7.06, -2.97, 9.69],
      [1985, 4.15, -4.30, -0.88, 8.48],
      [1986, 3.51, -5.82, -0.19, 7.83],
      [1987, 1.35, -5.78, -0.63, 6.22],
      [1988, 4.41, -4.10, 0.61, 6.66],
      [1989, 4.31, -3.16, 1.37, 9.44],
      [1990, 4.63, -2.76, 1.23, 8.25]
    ];
    var chosen = {}, TEAL = "#7FD1B9", PINK = "#E8A0B4";
    function rule(pi, gap) { return 2 + pi + 0.5 * (pi - 2) + 0.5 * gap; }
    QB.widget(el, {
      title: "Take the chair, 1966-1990",
      sub: "Pick a year and set the federal funds rate for its first quarter. You see what was known then: last " +
           "year's inflation and the output gap as that winter's data showed it. Left: the rate the Federal Reserve " +
           "set (pink), Taylor's rule with the gap of the day (green) and with today's estimate of the gap (teal, " +
           "dashed), and your choices (gold). Right: the two gaps. In which years did the data of the day mislead?",
      panels: 2, height: 280,
      controls: [
        { k: "year", label: "Year", min: 1966, max: 1990, step: 1, value: 1979,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "rate", label: "Your funds rate, %", min: 0, max: 20, step: 0.25, value: 10,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var y = Math.round(v.year), row = null, i;
        for (i = 0; i < D.length; i++) if (D[i][0] === y) row = D[i];
        if (row) chosen[y] = v.rate;
        var yr = [], ff = [], rrt = [], rtd = [], grt = [], gtd = [];
        for (i = 0; i < D.length; i++) {
          yr.push(D[i][0]); ff.push(D[i][4]); rrt.push(rule(D[i][1], D[i][2])); rtd.push(rule(D[i][1], D[i][3]));
          grt.push(D[i][2]); gtd.push(D[i][3]);
        }
        var a1 = g[0].axes({ x: [1966, 1990], y: [0, 22], title: "The funds rate and the rule, %", xlabel: "year" });
        a1.line(yr, rtd, { color: TEAL, width: 1.8, dash: [5, 4] });
        a1.line(yr, rrt, { color: GREEN, width: 2 });
        a1.line(yr, ff, { color: PINK, width: 2.5 });
        var cx = [], cy = [];
        for (var k in chosen) { cx.push(+k); cy.push(chosen[k]); }
        a1.dots(cx, cy, { color: GOLD, r: 4 });
        var a2 = g[1].axes({ x: [1966, 1990], y: [-12, 6], title: "The output gap, %", xlabel: "year" });
        a2.hline(0, { color: GREY_HINT });
        a2.line(yr, gtd, { color: TEAL, width: 2, dash: [5, 4] });
        a2.line(yr, grt, { color: GREEN, width: 2.5 });
        if (row) a2.dots([y], [row[2]], { color: GOLD, r: 5 });
        st.row = row;
      },
      readout: function (v, st) {
        var r = st.row;
        if (!r) return [["year", "no data"]];
        var rt = rule(r[1], r[2]), td = rule(r[1], r[3]);
        return [["known then", "inflation " + r[1].toFixed(1) + "%; output " + r[2].toFixed(1) + "% from trend"],
                ["the rule with that gap", rt.toFixed(1) + "%; with today's gap (" + r[3].toFixed(1) + "%): " +
                  td.toFixed(1) + "%"],
                ["you set", v.rate.toFixed(2) + "%; the Federal Reserve set " + r[4].toFixed(1) + "%"],
                ["verdict", Math.abs(r[2] - r[3]) > 2 ? "the data of the day misread the gap by " +
                  Math.abs(r[2] - r[3]).toFixed(1) + " points" : "the gap of the day was close to today's estimate"]];
      },
      note: "Taylor's rule as in Part 30: i = 2 + pi + 0.5(pi - 2) + 0.5x. Real-time GDP from the Philadelphia Fed's " +
            "Real-Time Data Set; the CBO's potential, the CPI and the funds rate from FRED. Part 31, chapters 2 and 7. " +
            "Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 32: the minister's budget ----------------------------------------------------------------------------
  W.budget = function (el) {
    // The minister's budget of Part 32 (explainer.economics.agora.fiscal: debt_path, stabilizing_surplus): debt to
    // GDP evolves as b' = b (1 + r)/(1 + g) - s; a consolidation of size c (points of GDP, phased in over the years
    // chosen) lowers output by multiplier * c while it is in place, and output recovers as the multiplier's effect
    // fades; a smaller output makes the same debt a larger ratio.
    var PINK = "#E8A0B4", TEAL = "#7FD1B9", LILAC = "#C9A0FF";
    function run(r, g, b0, d0, c, phase, m, years) {
      var b = [b0], gap = [0], s0 = -d0, t, cons;
      var B = b0, Y = 1, Ypot = 1;
      for (t = 1; t <= years; t++) {
        cons = Math.min(1, t / Math.max(1, phase)) * c;          // consolidation in place, points of GDP
        var gapt = -m * cons * Math.pow(0.6, Math.max(0, t - phase));  // the multiplier's bite fades after phasing
        Ypot = Ypot * (1 + g);
        Y = Ypot * (1 + gapt / 100);
        var s = s0 + cons / 100 + 0.5 * gapt / 100;            // a slump lowers the surplus (stabilizers)
        B = B * (1 + r) - s * Y;
        b.push(B / Y); gap.push(gapt);
      }
      return { b: b, gap: gap };
    }
    QB.widget(el, {
      title: "The minister's budget",
      sub: "Debt to GDP evolves with the interest rate, growth and the primary surplus. You choose a consolidation, " +
           "how fast to phase it in, and how big the multiplier is. Left: debt as a share of output (teal) and, " +
           "dashed, with no consolidation. Right: the output gap. With a large multiplier, can austerity raise the " +
           "debt ratio before it lowers it?",
      panels: 2, height: 280,
      controls: [
        { k: "r", label: "Interest rate, %", min: 0, max: 8, step: 0.25, value: 3,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "g", label: "Growth, %", min: -1, max: 6, step: 0.25, value: 2,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "b0", label: "Starting debt, % of GDP", min: 20, max: 200, step: 5, value: 100,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "c", label: "Consolidation, points of GDP", min: 0, max: 8, step: 0.5, value: 3,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "phase", label: "Years to phase it in", min: 1, max: 6, step: 1, value: 1,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "m", label: "Multiplier", min: 0, max: 2.5, step: 0.1, value: 1.0,
          fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, st) {
        var Y = 20, i;
        var a = run(v.r / 100, v.g / 100, v.b0 / 100, 2, v.c, Math.round(v.phase), v.m, Y);
        var z = run(v.r / 100, v.g / 100, v.b0 / 100, 2, 0, 1, v.m, Y);
        var yrs = []; for (i = 0; i <= Y; i++) yrs.push(i);
        var pa = a.b.map(function (x) { return 100 * x; }), pz = z.b.map(function (x) { return 100 * x; });
        var all = pa.concat(pz);
        var a1 = g[0].axes({ x: [0, Y], y: [Math.min(0, Math.min.apply(null, all)) , Math.max.apply(null, all) * 1.1],
                             title: "Debt, % of GDP", xlabel: "years" });
        a1.line(yrs, pz, { color: GREY_HINT, width: 1.5, dash: [5, 4] });
        a1.line(yrs, pa, { color: TEAL, width: 2.5 });
        var lo = Math.min(-0.5, Math.min.apply(null, a.gap));
        var a2 = g[1].axes({ x: [0, Y], y: [lo * 1.1, 0.5], title: "Output gap, %", xlabel: "years" });
        a2.hline(0, { color: GREY_HINT });
        a2.line(yrs, a.gap, { color: PINK, width: 2.5 });
        st.a = a; st.z = z;
        st.peak = Math.max.apply(null, pa.slice(0, 4)); st.start = pa[0];
      },
      readout: function (v, st) {
        var stab = (v.r - v.g) / (100 + v.g) * v.b0;
        return [["surplus that holds the starting debt steady", stab.toFixed(2) + "% of GDP"],
                ["debt after 20 years", (100 * st.a.b[20]).toFixed(0) + "% (without the plan: " +
                  (100 * st.z.b[20]).toFixed(0) + "%)"],
                ["deepest output gap", Math.min.apply(null, st.a.gap).toFixed(1) + "%"],
                ["verdict", st.peak > st.start + 0.5 ? "the debt ratio rose first: the slump shrank output faster " +
                  "than the plan cut the deficit" : "the debt ratio falls from the start"]];
      },
      note: "A sketch, not a forecast: the multiplier's effect fades by 40% a year once the plan is fully in place, " +
            "and a slump lowers the surplus by half the output gap. Part 32, chapters 1-2. Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
  W.leverage = function (el) {
    // Geanakoplos's leverage cycle of Part 33 (explainer.economics.agora.credit: leverage_static, leverage_cycle).
    // Agents h in [0, 1] each hold one unit of cash and one of an asset paying 1, or d after bad news; agent h thinks
    // good news has probability h.  One period: the marginal buyer h values the asset at p = h + (1 - h) d, and buyers
    // spend their cash plus what lenders allow, lambda * d per unit: p h = 1 - h + lambda d.  Two periods (lambda = 1):
    // the asset pays d only after bad news twice; four equations solved by nested bisection.
    var PINK = "#E8A0B4", TEAL = "#7FD1B9", LILAC = "#C9A0FF";
    function bisect(f, a, b) {
      var fa = f(a), i, m, fm;
      for (i = 0; i < 80; i++) { m = 0.5 * (a + b); fm = f(m); if ((fm > 0) === (fa > 0)) { a = m; fa = fm; } else b = m; }
      return 0.5 * (a + b);
    }
    function oneShot(d, lam) {
      var h = bisect(function (x) { return (x + (1 - x) * d) * x - (1 - x) - lam * d; }, 1e-6, 1 - 1e-6);
      return { h: h, p: h + (1 - h) * d };
    }
    function cycle(d) {
      // for a given h0, find hD from the market at D; then h0 from the marginal buyer today
      function atD(h0) {
        var hD = bisect(function (x) {
          var pD = x + (1 - x) * d, p0 = (1 - h0 + pD) / h0;
          return pD - (h0 - x) * (1 + p0) - d;
        }, 1e-6, h0 - 1e-9);
        var pD = hD + (1 - hD) * d, p0 = (1 - h0 + pD) / h0;
        return { h0: h0, hD: hD, pD: pD, p0: p0 };
      }
      function gap(h0) {
        var s = atD(h0);
        var lev = h0 * (1 - s.pD) / Math.max(s.p0 - s.pD, 1e-9);
        var cash = h0 + (1 - h0) * h0 * (1 - d) / Math.max(s.pD - d, 1e-9);
        return lev - cash;
      }
      var grid = [], k, lo = 0.5, hi = 0.999, prev = gap(lo), cur;
      for (k = 1; k <= 60; k++) {
        var x = 0.5 + k * (0.499 / 60); cur = gap(x);
        if ((cur > 0) !== (prev > 0)) { lo = x - 0.499 / 60; hi = x; break; }
        prev = cur;
      }
      var s = atD(bisect(gap, lo, hi));
      s.m0 = (s.p0 - s.pD) / s.p0; s.mD = (s.pD - d) / s.pD;
      return s;
    }
    QB.widget(el, {
      title: "The leverage cycle",
      sub: "An asset pays 1, or d if the news is bad; people differ in how likely they think good news is. Left: the " +
           "price against how much lenders will lend (as a share of the safe amount d), with no borrowing (grey " +
           "dot) and your choice (pink). Right: the two-period cycle with full borrowing: the price today and after " +
           "bad news, against the value to today's marginal buyer.",
      panels: 2, height: 280,
      controls: [
        { k: "d", label: "Payoff after bad news, d", min: 0.05, max: 0.5, step: 0.01, value: 0.2,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "lam", label: "Lenders lend, share of d", min: 0, max: 1, step: 0.05, value: 1,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var lams = [], ps = [], i;
        for (i = 0; i <= 20; i++) { lams.push(i / 20); ps.push(oneShot(v.d, i / 20).p); }
        var me = oneShot(v.d, v.lam), none = oneShot(v.d, 0);
        var a1 = g[0].axes({ x: [0, 1], y: [0.4, 1], title: "Price, one period", xlabel: "lending, share of d" });
        a1.line(lams, ps, { color: LILAC, width: 2.5 });
        a1.hline(0.5 + 0.5 * v.d, { color: GREY_HINT });
        a1.text(0.02, 0.5 + 0.5 * v.d + 0.03, "the average opinion", { color: GREY_HINT, size: 11 });
        a1.dots([0], [none.p], { color: GREY_HINT, r: 5 });
        a1.dots([v.lam], [me.p], { color: PINK, r: 6 });
        var c = cycle(v.d);
        var a2 = g[1].axes({ x: [0, 3], y: [0, 1.05], title: "Two periods, full borrowing", xlabel: "" });
        a2.bars([0.6, 1.5], [c.p0, c.pD], 0.5, { color: function (j) { return j ? RED : TEAL; } });
        var v0 = c.h0 + (1 - c.h0) * (c.h0 + (1 - c.h0) * v.d), vD = c.h0 + (1 - c.h0) * v.d;
        a2.dots([0.6, 1.5], [v0, vD], { color: GOLD, r: 5 });
        a2.text(0.6, c.p0 + 0.05, "today " + c.p0.toFixed(2), { align: "center", size: 11 });
        a2.text(1.5, c.pD + 0.05, "after bad news " + c.pD.toFixed(2), { align: "center", size: 11 });
        a2.text(2.1, 0.9, "gold: the old marginal buyer's value", { color: GOLD, size: 11 });
        st.me = me; st.none = none; st.c = c; st.v0 = v0; st.vD = vD;
      },
      readout: function (v, st) {
        return [["price with no borrowing / with yours", st.none.p.toFixed(3) + " / " + st.me.p.toFixed(3) +
                  " (marginal buyer h = " + st.me.h.toFixed(2) + ")"],
                ["two periods: price today, after bad news", st.c.p0.toFixed(3) + " -> " + st.c.pD.toFixed(3) + " (" +
                  (100 * (1 - st.c.pD / st.c.p0)).toFixed(0) + "% fall)"],
                ["the news itself, to today's marginal buyer", (100 * (1 - st.vD / st.v0)).toFixed(0) + "% fall"],
                ["margins: today, after bad news", (100 * st.c.m0).toFixed(0) + "% -> " + (100 * st.c.mD).toFixed(0) +
                  "%"]];
      },
      note: "Geanakoplos (2010), as computed in Part 33, chapter 6: with d = 0.2 the price is 0.95 today and 0.69 after " +
            "bad news, while margins rise from 27% to 71%. Computed in your browser; nothing you do here is stored or " +
            "sent.",
    });
  };
})();
