// Interactives for Stage V, PhD: the research frontier, from selection to shift (Parts 56-60).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // log of the standard normal's upper tail, with small relative error far into the tail (Numerical Recipes' erfc)
  function logQ(z) {
    var x = Math.abs(z) / Math.SQRT2, t = 1 / (1 + 0.5 * x);
    var l = Math.log(0.5 * t) - x * x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
      t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))))));
    return z >= 0 ? l : Math.log(1 - Math.exp(l));
  }

  // ---- Part 56: the selection window, a statistic reported only when it crosses a threshold -------------------
  W.truncpivot = function (el) {
    var sf = function (y, mu, c) { return Math.exp(logQ(y - mu) - logQ(c - mu)); }; // P_mu(Y > y | Y > c), y >= c
    var solve = function (y, c, level) { // sf is increasing in mu
      var lo = -400, hi = y + 12, k, m;
      for (k = 0; k < 60; k++) { m = 0.5 * (lo + hi); if (sf(y, m, c) < level) lo = m; else hi = m; }
      return 0.5 * (lo + hi);
    };
    QB.widget(el, {
      title: "The selection window: an estimate reported only because it crossed a threshold",
      sub: "Y is normal with mean μ and sd 1, and is reported only when it exceeds the threshold. Left: its law (grey), and the law given that it was reported (gold), with the observed value and the tail whose area is the selective pivot. Right: the usual interval y ± 1.96 and the selective interval, for every value that could have been reported. Move the observed value toward the threshold, or the true mean below it.",
      panels: 2, height: 300,
      controls: [
        { k: "mu", label: "True mean μ", min: -2, max: 4, step: 0.1, value: 0, fmt: function (x) { return fmt(x, 1); } },
        { k: "c", label: "Threshold for reporting", min: 0, max: 3, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "d", label: "Observed value above the threshold", min: 0.05, max: 3, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var c = v.c, y = c + v.d, mu = v.mu, i, xs = QB.linspace(-5, 7, 241);
        var mass = Math.exp(logQ(c - mu));
        var dens = xs.map(function (x) { return QB.pdf(x - mu); });
        var top = Math.min(4, Math.max(0.45, QB.pdf(Math.max(0, c - mu)) / Math.max(mass, 1e-12) * 1.08));
        var a = g[0].axes({ x: [-5, 7], y: [0, top], title: "The law of Y, and of Y given that it was reported", xlabel: "y" });
        a.line(xs, dens, { color: C.cash, width: 1.5 });
        var tx = [], ty = [], sx = [], sy = [];
        for (i = 0; i <= 160; i++) {
          var x = c + (7 - c) * i / 160, d = Math.exp(Math.log(QB.pdf(x - mu) + 1e-300) - logQ(c - mu));
          tx.push(x); ty.push(d); if (x >= y) { sx.push(x); sy.push(d); }
        }
        if (sx.length > 1) a.area(sx, sy, 0, { color: C.idea, alpha: 0.35 });
        a.line([c].concat(tx), [0].concat(ty), { color: C.idea, width: 2 });
        a.vline(c, { color: C.loss }); a.vline(y, { color: C.spot, dash: [] , width: 1.6 });
        a.vline(mu, { color: C.gain });
        a.legend([["law of Y", C.cash], ["given Y > threshold", C.idea], ["threshold", C.loss], ["observed y", C.spot], ["true mean", C.gain]], { pos: "tl" });
        var ys = [], lo = [], hi = [], nl = [], nh = [];
        for (i = 0; i <= 40; i++) {
          var yy = c + 0.05 + 3.45 * i / 40;
          ys.push(yy); lo.push(solve(yy, c, 0.025)); hi.push(solve(yy, c, 0.975)); nl.push(yy - 1.96); nh.push(yy + 1.96);
        }
        var b = g[1].axes({ x: [c, c + 3.5], y: [c - 9, c + 6], title: "95% intervals for μ, by the value reported", xlabel: "reported value y" });
        b.area(ys, hi, lo, { color: C.idea, alpha: 0.22 });
        b.line(ys, lo, { color: C.idea }); b.line(ys, hi, { color: C.idea });
        b.line(ys, nl, { color: C.spot, width: 1.4 }); b.line(ys, nh, { color: C.spot, width: 1.4 });
        b.hline(mu, { color: C.gain }); b.vline(y, { color: C.spot });
        b.legend([["selective interval", C.idea], ["usual y ± 1.96", C.spot], ["true mean", C.gain]], { pos: "bl" });
        // exact coverage of y +- 1.96 given the report
        var l = Math.max(c - mu, -1.96), naive = l >= 1.96 ? 0 : (Math.exp(logQ(l)) - Math.exp(logQ(1.96))) / Math.max(mass, 1e-300);
        s.out = { pivot: sf(y, mu, c), lo: solve(y, c, 0.025), hi: solve(y, c, 0.975), y: y, naive: Math.min(1, Math.max(0, naive)), mass: mass };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["chance of being reported", pct(o.mass, 1)], ["pivot at the true mean", fmt(o.pivot, 3)],
          ["usual interval", "(" + fmt(o.y - 1.96, 2) + ", " + fmt(o.y + 1.96, 2) + ")"],
          ["selective interval", "(" + fmt(o.lo, 2) + ", " + fmt(o.hi, 2) + ")"],
          ["usual interval's coverage, given the report", pct(o.naive, 1)], ["selective interval's", "95.0%"]];
      },
      note: "Exact arithmetic for one normal observation with known sd 1 and a one-sided threshold; nothing is simulated. The selective interval inverts the truncated-normal pivot, so it covers 95% of the time among reported values for every μ; its lower end runs away as the observed value approaches the threshold (Kivaranovic and Leeb 2021).",
    });
  };

  function lgamma(x) { // Lanczos, x > 0
    var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.001208650973866179, -0.000005395239384953];
    var y = x, t = x + 5.5, s = 1.000000000190015, j;
    t -= (x + 0.5) * Math.log(t);
    for (j = 0; j < 6; j++) { y += 1; s += c[j] / y; }
    return -t + Math.log(2.5066282746310005 * s / x);
  }

  // ---- Part 57: the quantile lemma, holding for any law and breaking without exchangeability -------------------
  W.quantilelemma = function (el) {
    QB.widget(el, {
      title: "The quantile lemma: coverage k/(n + 1), whatever the distribution",
      sub: "Scores are drawn from a law whose tail you choose. Left: one calibration set, sorted; each bar's height is the share of future scores below it, and the threshold is the k-th (the last green bar). Right: that share for 400 calibration sets, against the Beta(k, n + 1 − k) law. Change the tail: nothing moves. Then make the test point's scores larger than the calibration scores, and the guarantee goes.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Calibration scores n", min: 5, max: 200, step: 1, value: 40, fmt: function (x) { return String(x); } },
        { k: "alpha", label: "Miscoverage α", min: 0.02, max: 0.3, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "tail", label: "Tail weight of the scores", min: 1, max: 4, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "drift", label: "Test score scale ÷ calibration scale", min: 1, max: 3, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New calibration sets", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, k = Math.ceil((n + 1) * (1 - v.alpha) - 1e-9), r = QB.rng(s.seed + 570), sets = 400, i, j;
        // a score is E^tail with E exponential; a test score is drift times that, so P(test <= t) = 1 - exp(-(t/drift)^(1/tail))
        var below = function (t) { return 1 - Math.exp(-Math.pow(t / v.drift, 1 / v.tail)); };
        var draw = function () { var a = new Array(n), q; for (q = 0; q < n; q++) a[q] = Math.pow(-Math.log(1 - r()), v.tail); a.sort(function (x, y) { return x - y; }); return a; };
        var first = draw(), cov = [], finite = k <= n;
        for (i = 0; i < sets; i++) { var a = i === 0 ? first : draw(); cov.push(finite ? below(a[k - 1]) : 1); }
        var xs = [], hs = [];
        for (j = 0; j < n; j++) { xs.push(j + 1); hs.push(below(first[j])); }
        var A = g[0].axes({ x: [0, n + 1], y: [0, 1], title: "One calibration set: share of future scores below each", xlabel: "rank of the calibration score" });
        A.bars(xs, hs, 1, { color: function (q) { return q < k ? C.gain : C.loss; }, gap: n > 80 ? 0 : 1 });
        A.hline(1 - v.alpha, { color: C.muted });
        A.text(0, 1 - v.alpha, "1 − α", { color: C.muted, dx: 6, dy: -9, bg: true });
        if (finite) A.text(k, hs[k - 1], "k = " + k, { color: C.ink, align: "right", dx: -4, dy: -10, bg: true });
        else A.text((n + 1) / 2, 0.5, "k = " + k + " > n: the set is the whole line", { color: C.idea, align: "center", bg: true });
        A.legend([["covered ranks", C.gain], ["missed ranks", C.loss]], { pos: "br" });
        var lo = 0.4, nb = 30, h = QB.hist(cov, lo, 1.0000001, nb), w = (1 - lo) / nb, mids = [], dens = [], top = 0;
        for (i = 0; i < nb; i++) { mids.push(lo + (i + 0.5) * w); dens.push(h[i] / (sets * w)); top = Math.max(top, dens[i]); }
        var bx = [], by = [];
        if (finite) {
          var lg = lgamma(n + 1) - lgamma(k) - lgamma(n + 1 - k);
          for (i = 1; i < 240; i++) { var u = lo + (1 - lo) * i / 240, d = Math.exp(lg + (k - 1) * Math.log(u) + (n - k) * Math.log(1 - u)); bx.push(u); by.push(d); if (d > top) top = d; }
        }
        var B = g[1].axes({ x: [lo, 1], y: [0, Math.max(1, top * 1.12)], title: "Coverage given the calibration set, 400 sets", xlabel: "share of test scores below the threshold" });
        B.bars(mids, dens, w, { color: C.spot, alpha: 0.6 });
        if (finite) B.line(bx, by, { color: C.idea });
        B.vline(1 - v.alpha, { color: C.muted });
        B.legend([["400 calibration sets", C.spot], ["Beta(k, n + 1 − k)", C.idea], ["1 − α", C.muted]], { pos: "tl" });
        s.out = { k: k, exact: finite ? k / (n + 1) : 1, mean: QB.mean(cov), low: QB.quantile(cov, 0.05), finite: finite };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["k", String(o.k) + (o.finite ? "" : " (no finite threshold)")], ["lemma: k/(n + 1)", pct(o.exact, 1)], ["mean coverage over the sets", pct(o.mean, 1)],
          ["5% of sets cover less than", pct(o.low, 1)]];
      },
      note: "Simulated data: a score is an exponential variable raised to the tail weight, so every moment exists but the tail grows heavy; the test score is the same law times the scale. With scale 1 the scores are exchangeable and the mean coverage is k/(n + 1) for every tail. The lemma promises the average over calibration sets, not each set: the Beta law is the spread.",
    });
  };


  // ---- Part 58: peeking with a z-test against a betting test under Ville's inequality ---------------------------
  W.peekville = function (el) {
    QB.widget(el, {
      title: "Looking after every observation: a z-test against a bettor's wealth",
      sub: "Three hundred streams of normal data with sd 1 are watched from the first observation to the last. Left: each stream's z-statistic, with the fixed-n lines at ±1.96. Right: the wealth of a bettor who stakes on a positive mean, with Ville's line at 20. A stream turns gold when it has crossed. With a true mean of 0, count the crossings; then give the data a real effect, and change the bet.",
      panels: 2, height: 300,
      controls: [
        { k: "mu", label: "True mean of the data", min: 0, max: 0.5, step: 0.02, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "bet", label: "The bettor's alternative mean λ", min: 0.05, max: 1, step: 0.05, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Number of looks", min: 20, max: 1000, step: 20, value: 400, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New streams", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 580), reps = 300, show = 14, n = v.n, i, t, zs = [], ws = [], zc = [], wc = [], nz = 0, nw = 0, tw = [];
        var ts = []; for (t = 1; t <= n; t++) ts.push(t);
        for (i = 0; i < reps; i++) {
          var sum = 0, lw = 0, cz = false, cw = false, zp = i < show ? new Array(n) : null, wp = i < show ? new Array(n) : null, first = 0;
          for (t = 1; t <= n; t++) {
            var x = v.mu + r.normal(); sum += x; lw += v.bet * x - 0.5 * v.bet * v.bet;
            var z = sum / Math.sqrt(t);
            if (Math.abs(z) >= 1.96) cz = true;
            if (!cw && lw >= Math.log(20)) { cw = true; first = t; }
            if (zp) { zp[t - 1] = z; wp[t - 1] = Math.max(-3, Math.min(4, lw / Math.LN10)); }
          }
          if (cz) nz++; if (cw) { nw++; tw.push(first); }
          if (zp) { zs.push(zp); ws.push(wp); zc.push(cz); wc.push(cw); }
        }
        var zmax = Math.max(4, v.mu * Math.sqrt(n) + 3);
        var A = g[0].axes({ x: [1, n], y: [-4, zmax], title: "z-statistic of each stream, checked at every look", xlabel: "observations" });
        for (i = 0; i < zs.length; i++) A.line(ts, zs[i], { color: zc[i] ? C.idea : C.spot, width: 1, alpha: zc[i] ? 0.8 : 0.5 });
        A.hline(1.96, { color: C.loss }); A.hline(-1.96, { color: C.loss });
        A.legend([["crossed ±1.96 at some look", C.idea], ["never crossed", C.spot]], { pos: "bl" });
        var B = g[1].axes({ x: [1, n], y: [-3, 4], title: "The bettor's wealth (log scale), starting at 1", xlabel: "observations",
          yticks: [-3, -2, -1, 0, 1, 2, 3, 4], yfmt: function (e) { return e === 0 ? "1" : e > 0 ? String(Math.pow(10, e)) : "1/" + String(Math.pow(10, -e)); } });
        for (i = 0; i < ws.length; i++) B.line(ts, ws[i], { color: wc[i] ? C.idea : C.spot, width: 1, alpha: wc[i] ? 0.8 : 0.5 });
        B.hline(Math.log(20) / Math.LN10, { color: C.loss });
        B.text(n, Math.log(20) / Math.LN10, "wealth 20 = 1/α", { color: C.loss, align: "right", dx: -6, dy: -10, bg: true });
        B.legend([["reached 20 at some look", C.idea], ["never reached 20", C.spot]], { pos: "bl" });
        s.out = { z: nz / reps, w: nw / reps, med: tw.length ? QB.quantile(tw, 0.5) : null };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["z-test rejects at some look", pct(o.z, 1)], ["wealth reaches 20 at some look", pct(o.w, 1)],
          ["Ville's bound when the mean is 0", "5.0%"], ["median look at which wealth reaches 20", o.med === null ? "never" : fmt(o.med, 0)]];
      },
      note: "Simulated data: 300 streams, 14 of them drawn. The wealth is the likelihood ratio of N(λ, 1) against N(0, 1), a nonnegative martingale when the mean is 0, so by Ville's inequality it reaches 20 in at most 5% of null streams however long you watch. The z-test's 5% holds at one look fixed in advance, not at the first look that happens to cross.",
    });
  };


  // ---- Part 59: AMP for the lasso against its state evolution, as a cobweb ------------------------------------
  W.stateevolution = function (el) {
    var soft = function (x, t) { return x > t ? x - t : x < -t ? x + t : 0; };
    var ZS = [], WS = [];
    (function () { var k, tot = 0; for (k = 0; k <= 96; k++) { var z = -6 + k / 8; ZS.push(z); WS.push(QB.pdf(z)); tot += WS[k]; } for (k = 0; k <= 96; k++) WS[k] /= tot; })();
    var step = function (tau2, v) { // tau^2 -> sigma^2 + E[(eta(X + tau Z; theta tau) - X)^2] / delta, X = +-1 with probability eps, else 0
      var tau = Math.sqrt(tau2), thr = v.theta * tau, zero = 0, one = 0, k, a, b;
      for (k = 0; k < ZS.length; k++) { a = soft(tau * ZS[k], thr); b = soft(1 + tau * ZS[k], thr) - 1; zero += WS[k] * a * a; one += WS[k] * b * b; }
      return v.s2 + ((1 - v.eps) * zero + v.eps * one) / v.delta;
    };
    var big = function (x, d) { return x > 100 ? "over 100" : fmt(x, d); };
    QB.widget(el, {
      title: "State evolution: a p-dimensional algorithm tracked by one number",
      sub: "A sparse signal (entries ±1 with probability ε, else 0) is measured n = δp times and recovered by approximate message passing with soft threshold θτ. Left: the state-evolution map for the effective noise τ², with its staircase from the start. Right: the staircase's values (gold line) against AMP's own noise level on one 300-column problem (blue dots). With no noise, lower δ until the staircase stops short of zero: that is the phase transition.",
      panels: 2, height: 300,
      controls: [
        { k: "delta", label: "Undersampling δ = n/p", min: 0.1, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "eps", label: "Share of nonzero entries ε", min: 0.02, max: 0.4, step: 0.02, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "theta", label: "Threshold multiplier θ", min: 0.5, max: 3, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "s2", label: "Noise variance σ²", min: 0, max: 0.05, step: 0.005, value: 0, fmt: function (x) { return x.toFixed(3); } },
      ],
      buttons: [{ label: "New matrix", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var T = 15, t, i, j, start = v.s2 + v.eps / v.delta, se = [start];
        for (t = 0; t < 200; t++) se.push(Math.min(1e6, step(se[t], v)));
        // AMP on one problem
        var p = 300, n = Math.max(2, Math.round(v.delta * p)), k = Math.max(1, Math.round(v.eps * p)), r = QB.rng(s.seed + 590), d = n / p;
        var A = new Float64Array(n * p), x0 = new Float64Array(p), x = new Float64Array(p), y = new Float64Array(n), z = new Float64Array(n), rr = new Float64Array(p);
        var sc = 1 / Math.sqrt(n);
        for (i = 0; i < n * p; i++) A[i] = sc * r.normal();
        var idx = []; for (j = 0; j < p; j++) idx.push(j);
        for (j = 0; j < k; j++) { var q = j + Math.floor(r() * (p - j)), tmp = idx[j]; idx[j] = idx[q]; idx[q] = tmp; x0[idx[j]] = r() < 0.5 ? -1 : 1; }
        for (i = 0; i < n; i++) { var acc = 0, o = i * p; for (j = 0; j < p; j++) acc += A[o + j] * x0[j]; y[i] = acc + Math.sqrt(v.s2) * r.normal(); z[i] = y[i]; }
        var amp = [], mse = 0;
        for (t = 0; t <= T; t++) {
          var m2 = 0; for (i = 0; i < n; i++) m2 += z[i] * z[i]; m2 = Math.min(1e6, m2 / n); amp.push(m2);
          if (t === T) break;
          var thr = v.theta * Math.sqrt(m2), active = 0;
          for (j = 0; j < p; j++) rr[j] = x[j];
          for (i = 0; i < n; i++) { var zi = z[i], o2 = i * p; if (zi !== 0) for (j = 0; j < p; j++) rr[j] += A[o2 + j] * zi; }
          for (j = 0; j < p; j++) { if (Math.abs(rr[j]) > thr) active++; x[j] = Math.max(-1e6, Math.min(1e6, soft(rr[j], thr))); }
          var ons = active / p / d;
          for (i = 0; i < n; i++) { var ax = 0, o3 = i * p; for (j = 0; j < p; j++) ax += A[o3 + j] * x[j]; z[i] = Math.max(-1e6, Math.min(1e6, y[i] - ax + ons * z[i])); }
        }
        for (j = 0; j < p; j++) mse += (x[j] - x0[j]) * (x[j] - x0[j]); mse /= p;
        // the cobweb
        var X = 1.15 * start, xs = QB.linspace(0, X, 120), fs = xs.map(function (u) { return step(u, v); });
        var a = g[0].axes({ x: [0, X], y: [0, X], title: "The map τ² → next τ², and its staircase", xlabel: "τ² at iteration t" });
        a.line([0, X], [0, X], { color: C.muted, width: 1, dash: [4, 4] });
        a.line(xs, fs, { color: C.idea, width: 2 });
        var cx = [se[0]], cy = [0];
        for (t = 0; t < 40; t++) { cx.push(se[t]); cy.push(se[t + 1]); cx.push(se[t + 1]); cy.push(se[t + 1]); }
        a.line(cx, cy, { color: C.realized, width: 1.3 });
        a.dots([se[0]], [0], { color: C.realized, r: 4 });
        a.legend([["state-evolution map", C.idea], ["staircase from the start", C.realized], ["diagonal: fixed points", C.muted]], { pos: "tl" });
        var lo = 1e-4, hi = 10, cl = function (u) { return Math.max(lo, Math.min(hi, u)); }, ts = [];
        for (t = 0; t <= T; t++) ts.push(t);
        var b = g[1].axes({ x: [0, T], y: [lo, hi], logy: true, title: "Effective noise τ² by iteration (log scale)", xlabel: "iteration t" });
        b.line(ts, se.slice(0, T + 1).map(cl), { color: C.idea, width: 2 });
        b.dots(ts, amp.map(cl), { color: C.spot, r: 3.5 });
        if (v.s2 > 0) { b.hline(v.s2, { color: C.muted }); b.text(T, v.s2, "σ²", { color: C.muted, align: "right", dx: -6, dy: -9 }); }
        b.legend([["state evolution", C.idea], ["AMP, n = " + n + ", p = 300", C.spot]], { pos: "bl" });
        var fix = se[200];
        s.out = { start: start, fix: fix, pred: Math.max(0, v.delta * (fix - v.s2)), mse: mse, ok: fix - v.s2 < 1e-6 };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["start τ² = σ² + ε/δ", fmt(o.start, 3)], ["fixed point of the map", big(o.fix, 4)], ["predicted error per entry", big(o.pred, 4)],
          ["AMP's error after 15 iterations", big(o.mse, 4)], ["noiseless verdict", v.s2 > 0 ? "noise is on" : o.ok ? "exact recovery" : "stuck above zero"]];
      },
      note: "Simulated data for the blue dots: one Gaussian matrix with 300 columns, so they scatter around the gold line, which is the limit as p grows. The gold map is computed by quadrature. State evolution is exact for Gaussian matrices; the threshold θ that keeps the staircase falling for the smallest δ traces the Donoho-Tanner curve.",
    });
  };


  // ---- Part 60: covariate shift, importance weights and the effective sample size ------------------------------
  W.shiftweights = function (el) {
    QB.widget(el, {
      title: "Covariate shift: reweighting a source sample to a target population",
      sub: "The source sample has x normal around 0; the target population has x normal around the shift, and y = 1 + 2x + noise in both. Left: the two covariate densities and one source sample, each point drawn with area proportional to its weight. Right: 200 repeated samples, the plain mean of y (red) and the weighted mean (green) against the target's mean (gold). Increase the shift until a handful of points carry all the weight.",
      panels: 2, height: 300,
      controls: [
        { k: "shift", label: "Shift of the target's covariate mean", min: 0, max: 3, step: 0.1, value: 0.8, fmt: function (x) { return x.toFixed(1); } },
        { k: "sd", label: "Target's covariate sd (source: 1)", min: 0.5, max: 1.3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Source sample size n", min: 20, max: 500, step: 20, value: 200, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New samples", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 600), reps = 200, n = v.n, D = v.shift, sd = v.sd, target = 1 + 2 * D, i, k;
        var logw = function (x) { return -0.5 * (x - D) * (x - D) / (sd * sd) + 0.5 * x * x - Math.log(sd); };
        var plain = [], wtd = [], cover = 0, essSum = 0, X0 = [], Y0 = [], W0 = [];
        for (k = 0; k < reps; k++) {
          var xs = new Array(n), ys = new Array(n), lw = new Array(n), mx = -1e300, sy = 0;
          for (i = 0; i < n; i++) { xs[i] = r.normal(); ys[i] = 1 + 2 * xs[i] + r.normal(); lw[i] = logw(xs[i]); if (lw[i] > mx) mx = lw[i]; sy += ys[i]; }
          var sw = 0, sw2 = 0, swy = 0, w = new Array(n);
          for (i = 0; i < n; i++) { w[i] = Math.exp(lw[i] - mx); sw += w[i]; sw2 += w[i] * w[i]; swy += w[i] * ys[i]; }
          var m = swy / sw, se2 = 0;
          for (i = 0; i < n; i++) se2 += w[i] * w[i] * (ys[i] - m) * (ys[i] - m);
          var se = Math.sqrt(se2) / sw;
          plain.push(sy / n); wtd.push(m); essSum += sw * sw / sw2; if (Math.abs(m - target) <= 1.96 * se) cover++;
          if (k === 0) { X0 = xs; Y0 = ys; W0 = w.map(function (u) { return u * n / sw; }); s.ess0 = sw * sw / sw2; }
        }
        var grid = QB.linspace(-4, 7, 221);
        var a = g[0].axes({ x: [-4, 7], y: [0, 1.25], title: "Covariate: source, target, and one weighted sample", xlabel: "x", noY: true });
        a.area(grid, grid.map(function (x) { return QB.pdf(x); }), 0, { color: C.spot, alpha: 0.25 });
        a.line(grid, grid.map(function (x) { return QB.pdf(x); }), { color: C.spot });
        a.line(grid, grid.map(function (x) { return QB.pdf((x - D) / sd) / sd; }), { color: C.idea });
        var c = a.ctx; c.save(); c.beginPath(); c.rect(a.x0, a.y0, a.w, a.h); c.clip(); c.fillStyle = C.gain; c.globalAlpha = 0.55;
        var jit = QB.rng(7);
        for (i = 0; i < n; i++) { var rad = Math.min(16, 1.6 * Math.sqrt(W0[i]) + 0.4); c.beginPath(); c.arc(a.px(X0[i]), a.py(0.92 + 0.22 * jit()), rad, 0, 6.2832); c.fill(); }
        c.restore();
        a.legend([["source density", C.spot], ["target density", C.idea], ["sample, area = weight", C.gain]], { pos: "tr" });
        var lo = Math.min(0, target - 1.5), hi = Math.max(2, target + 1.5), nb = 44, bw = (hi - lo) / nb, mids = [], top = 0;
        var hp = QB.hist(plain, lo, hi, nb), hw = QB.hist(wtd, lo, hi, nb);
        for (i = 0; i < nb; i++) { mids.push(lo + (i + 0.5) * bw); top = Math.max(top, hp[i], hw[i]); }
        var b = g[1].axes({ x: [lo, hi], y: [0, Math.max(5, top * 1.3)], title: "200 samples: plain and weighted mean of y", xlabel: "estimate of the target's mean of y" });
        b.bars(mids, hp, bw, { color: C.loss, alpha: 0.6 });
        b.bars(mids, hw, bw, { color: C.gain, alpha: 0.6 });
        b.vline(target, { color: C.idea, dash: [], width: 2 });
        b.legend([["plain mean", C.loss], ["weighted mean", C.gain], ["target", C.idea]], { pos: D > 1.2 ? "tl" : "tr" });
        var ew2 = Math.exp(D * D / (2 - sd * sd)) / (sd * Math.sqrt(2 - sd * sd));
        s.out = { target: target, plain: QB.mean(plain), wtd: QB.mean(wtd), ess: essSum / reps, th: n / ew2, cover: cover / reps, sdw: QB.sd(wtd), sdp: QB.sd(plain) };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["target mean", fmt(o.target, 2)], ["plain mean, on average", fmt(o.plain, 2)], ["weighted mean, on average", fmt(o.wtd, 2)],
          ["Kish effective sample size", fmt(o.ess, 0) + " of " + v.n], ["n / E w²", fmt(o.th, 0)],
          ["weighted 95% interval covers", pct(o.cover, 0)], ["sd: weighted ÷ plain", fmt(o.sdw / Math.max(o.sdp, 1e-9), 1)]];
      },
      note: "Simulated data, with the true density ratio as weights (in practice it is estimated, which adds error). The weighted mean is self-normalized and its interval uses the delta method. Weighting is unbiased in the limit for any shift with overlap, but its variance grows like E w² = exp(shift² / (2 − sd²)) / (sd √(2 − sd²)): when the effective sample size falls to a few points, the average and the interval both fail.",
    });
  };
})();
