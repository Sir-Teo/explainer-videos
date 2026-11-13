// Interactives for Stage V, PhD: the research frontier, from optimal transport to the dissertation (Parts 61-65).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- Part 61: transport on a line, by quantiles --------------------------------------------------------------
  W.quantiletransport = function (el) {
    var N = 200;
    QB.widget(el, {
      title: "Monge on a line: match the quantiles",
      sub: "Blue earth (a standard normal law) must fill the gold holes (a second law, drawn below the axis). The optimal plan for any convex cost sends each quantile to the same quantile: the green routes never cross. Shift the holes, widen them, then split them in two and watch W2 squared divide into location, spread and shape.",
      panels: 2, height: 300,
      controls: [
        { k: "m", label: "Shift of the holes", min: -1, max: 4, step: 0.1, value: 2, fmt: function (x) { return fmt(x, 1); } },
        { k: "s", label: "Their spread (sd)", min: 0.5, max: 2.5, step: 0.05, value: 1.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "b", label: "Bimodality of the holes", min: 0, max: 2.5, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var i, k, us = [], q1 = [], q2 = [], sc = v.s / Math.sqrt(1 + v.b * v.b);
        var mixcdf = function (z) { return 0.5 * QB.cdf(z - v.b) + 0.5 * QB.cdf(z + v.b); };
        for (i = 0; i < N; i++) {
          var u = (i + 0.5) / N, lo = -v.b - 7, hi = v.b + 7;
          for (k = 0; k < 40; k++) { var mid = 0.5 * (lo + hi); if (mixcdf(mid) < u) lo = mid; else hi = mid; }
          us.push(u); q1.push(QB.inv(u)); q2.push(v.m + sc * 0.5 * (lo + hi));
        }
        var m1 = QB.mean(q1), m2 = QB.mean(q2), s1 = 0, s2 = 0, cv = 0, w1 = 0, w2 = 0;
        for (i = 0; i < N; i++) {
          s1 += (q1[i] - m1) * (q1[i] - m1) / N; s2 += (q2[i] - m2) * (q2[i] - m2) / N; cv += (q1[i] - m1) * (q2[i] - m2) / N;
          w1 += Math.abs(q1[i] - q2[i]) / N; w2 += (q1[i] - q2[i]) * (q1[i] - q2[i]) / N;
        }
        s1 = Math.sqrt(s1); s2 = Math.sqrt(s2);
        s.out = { w1: w1, w2: Math.sqrt(w2), loc: (m1 - m2) * (m1 - m2), spr: (s1 - s2) * (s1 - s2), shp: Math.max(0, 2 * (s1 * s2 - cv)) };
        var f1 = function (x) { return QB.pdf(x); };
        var f2 = function (x) { var z = (x - v.m) / sc; return 0.5 * (QB.pdf(z - v.b) + QB.pdf(z + v.b)) / sc; };
        var xs = QB.linspace(-5, 9, 281), d1 = xs.map(f1), d2 = xs.map(f2), top = 0;
        for (i = 0; i < d2.length; i++) top = Math.max(top, d2[i]);
        var d2n = d2.map(function (y) { return -0.42 * y / top; });
        var a = g[0].axes({ x: [-5, 9], y: [-0.5, 0.62], title: "The monotone plan", xlabel: "position on the line", noY: true });
        a.area(xs, d1, 0, { color: C.spot, alpha: 0.35 }).line(xs, d1, { color: C.spot });
        a.area(xs, d2n, 0, { color: C.idea, alpha: 0.3 }).line(xs, d2n, { color: C.idea });
        for (k = 1; k <= 9; k++) {
          i = Math.round(k * N / 10 - 0.5);
          a.line([q1[i], q2[i]], [f1(q1[i]), -0.42 * f2(q2[i]) / top], { color: C.gain, width: 1.3, alpha: 0.9 });
        }
        a.legend([["earth: N(0, 1)", C.spot], ["holes", C.idea], ["routes at the deciles", C.gain]], { pos: "tr" });
        var b = g[1].axes({ x: [0, 1], y: [-5, 9], title: "W1 is the area between the quantile curves", xlabel: "probability level u" });
        b.area(us, q2, q1, { color: C.gain, alpha: 0.28 });
        b.line(us, q1, { color: C.spot }).line(us, q2, { color: C.idea });
        b.legend([["quantiles of the earth", C.spot], ["quantiles of the holes", C.idea], ["area = W1", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["W1", fmt(o.w1, 3)], ["W2", fmt(o.w2, 3)], ["W2² = location", fmt(o.loc, 3)], ["+ spread", fmt(o.spr, 3)], ["+ shape", fmt(o.shp, 3)],
          ["W2 if the holes were normal", fmt(Math.sqrt(v.m * v.m + (v.s - 1) * (v.s - 1)), 3)]];
      },
      note: "Exact quantile functions on a grid of 200 levels; no data. Location is the squared difference of means, spread the squared difference of standard deviations, and shape is 2(sd1·sd2 − covariance of the two quantile functions), which is zero when the holes are a shifted and rescaled copy of the earth.",
    });
  };

  // ---- Part 62: proximal inference with two proxies -------------------------------------------------------------
  W.proxybridge = function (el) {
    // covariances of (A, Z, W, Y) -> [effect by OLS of Y on (A, Z, W), effect by 2SLS of Y on (A, W) with instruments (A, Z)]
    var solve = function (c) {
      var aa = c[0], az = c[1], aw = c[2], zz = c[3], zw = c[4], ww = c[5], ay = c[6], zy = c[7], wy = c[8];
      var det3 = aa * (zz * ww - zw * zw) - az * (az * ww - zw * aw) + aw * (az * zw - zz * aw);
      var num3 = ay * (zz * ww - zw * zw) - az * (zy * ww - zw * wy) + aw * (zy * zw - zz * wy);
      var det2 = aa * zw - aw * az, num2 = ay * zw - aw * zy;
      if (Math.abs(det3) < 1e-9) det3 = 1e-9;
      if (Math.abs(det2) < 1e-6) det2 = det2 < 0 ? -1e-6 : 1e-6;
      return [num3 / det3, num2 / det2];
    };
    var pop = function (gam, sig, del) { // A = U + e, Z = U + sig e, W = U + sig e, Y = A + gam U + del Z + e
      var v = 1 + sig * sig;
      return solve([2, 1, 1, v, 1, v, 2 + gam + del, 1 + gam + del * v, 1 + gam + del]);
    };
    var median = function (x) { return QB.quantile(x, 0.5); };
    QB.widget(el, {
      title: "A hidden confounder, seen through two proxies",
      sub: "U causes both the treatment A and the outcome Y but is never observed; Z and W are U plus noise. Red adjusts for the proxies by regression; green uses Z as an instrument for W (proximal two-stage least squares). The true effect is 1. Raise the proxies' noise, then give Z its own effect on Y and watch the green estimate leave the truth.",
      panels: 2, height: 300,
      controls: [
        { k: "gam", label: "Effect of the hidden U on Y", min: 0, max: 2, step: 0.05, value: 1.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "sig", label: "Noise sd of each proxy", min: 0.2, max: 2.5, step: 0.05, value: 0.7, fmt: function (x) { return x.toFixed(2); } },
        { k: "del", label: "Direct effect of Z on Y (should be 0)", min: -0.5, max: 0.5, step: 0.02, value: 0, fmt: function (x) { return fmt(x, 2); } },
      ],
      buttons: [{ label: "New samples", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 620), reps = 100, n = 250, ols = [], prox = [], i, k;
        for (k = 0; k < reps; k++) {
          var m = [0, 0, 0, 0], c = [0, 0, 0, 0, 0, 0, 0, 0, 0];
          for (i = 0; i < n; i++) {
            var u = r.normal(), a = u + r.normal(), z = u + v.sig * r.normal(), w = u + v.sig * r.normal();
            var y = a + v.gam * u + v.del * z + r.normal();
            m[0] += a; m[1] += z; m[2] += w; m[3] += y;
            c[0] += a * a; c[1] += a * z; c[2] += a * w; c[3] += z * z; c[4] += z * w; c[5] += w * w; c[6] += a * y; c[7] += z * y; c[8] += w * y;
          }
          var ix = [[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3]];
          for (i = 0; i < 9; i++) c[i] = c[i] / n - m[ix[i][0]] * m[ix[i][1]] / (n * n);
          var e = solve(c); ols.push(e[0]); prox.push(e[1]);
        }
        var p = pop(v.gam, v.sig, v.del);
        s.out = [median(ols), median(prox), p[0] - 1, p[1] - 1];
        var nb = 40, lo = -0.5, hi = 3, bw = (hi - lo) / nb, mids = QB.linspace(lo + bw / 2, hi - bw / 2, nb);
        var h1 = QB.hist(ols, lo, hi, nb), h2 = QB.hist(prox, lo, hi, nb), top = 5;
        for (i = 0; i < nb; i++) top = Math.max(top, h1[i], h2[i]);
        var a1 = g[0].axes({ x: [lo, hi], y: [0, top * 1.25], title: "100 samples of 250: the estimated effect", xlabel: "estimated effect of A on Y" });
        a1.bars(mids, h1, bw, { color: C.loss, alpha: 0.7 }).bars(mids, h2, bw, { color: C.gain, alpha: 0.7 });
        a1.vline(1, { color: C.ink });
        a1.legend([["adjust for Z and W", C.loss], ["proximal 2SLS", C.gain], ["truth", C.ink]], { pos: "tr" });
        var sg = QB.linspace(0.2, 2.5, 60), b1 = [], b2 = [];
        for (i = 0; i < sg.length; i++) { var q = pop(v.gam, sg[i], v.del); b1.push(q[0] - 1); b2.push(q[1] - 1); }
        var a2 = g[1].axes({ x: [0.2, 2.5], y: [-1.2, 1.2], title: "Large-sample bias against the proxies' noise", xlabel: "noise sd of each proxy" });
        a2.hline(0, { color: C.muted });
        a2.line(sg, b1, { color: C.loss, width: 2.2 }).line(sg, b2, { color: C.gain, width: 2.2 });
        a2.vline(v.sig, { color: C.idea });
        a2.dots([v.sig, v.sig], [Math.max(-1.2, Math.min(1.2, p[0] - 1)), Math.max(-1.2, Math.min(1.2, p[1] - 1))], { color: function (j) { return j ? C.gain : C.loss; }, r: 4.5 });
      },
      readout: function (v, s) {
        return [["median, adjusting for proxies", fmt(s.out[0], 2)], ["median, proximal", fmt(s.out[1], 2)], ["large-sample bias: adjusting", fmt(s.out[2], 2)], ["proximal", fmt(s.out[3], 2)]];
      },
      note: "Simulated data: U, the noises and A = U + noise are standard normal, Y = A + (effect)·U + (direct)·Z + noise, Z and W are U plus independent noise. The proximal estimate needs Z to affect Y only through U, W not to be caused by A, and Z and W to be correlated; with very noisy proxies it stays unbiased in large samples but its spread grows.",
    });
  };

  // ---- Part 63: differential privacy as a hypothesis test, and its price ----------------------------------------
  W.privacytradeoff = function (el) {
    var clip = function (a) { return Math.max(1e-9, Math.min(1 - 1e-9, a)); };
    var fEps = function (a, e) { return Math.max(0, 1 - Math.exp(e) * a, Math.exp(-e) * (1 - a)); };
    var fGauss = function (a, mu) { return QB.cdf(QB.inv(clip(1 - a)) - mu); };
    var fLap = function (a, e) { // Laplace noise of scale 1/e on a count that changes by 1
      a = clip(a); var t = a < 0.5 ? -Math.log(2 * a) / e : Math.log(2 * (1 - a)) / e;
      return t >= 1 ? 1 - 0.5 * Math.exp(-(t - 1) * e) : 0.5 * Math.exp((t - 1) * e);
    };
    QB.widget(el, {
      title: "What an attacker can test, and what the noise costs",
      sub: "Left: an attacker tests 'this person is in the data' against 'is not'. Privacy is a floor under the attacker's type II error at every type I error; the diagonal is perfect privacy. Raise epsilon or the number of releases and the floors fall, linearly in k for the basic bound and like the square root of k for Gaussian noise. Right: the mean squared error of a proportion from n people, with no privacy, with noise added centrally, and with each person randomizing their own answer.",
      panels: 2, height: 310,
      controls: [
        { k: "eps", label: "Epsilon per release", min: 0.1, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "k", label: "Number of releases k", min: 1, max: 16, step: 1, value: 1, fmt: function (x) { return String(x); } },
        { k: "p", label: "True proportion p", min: 0.05, max: 0.5, step: 0.01, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var al = QB.linspace(0, 1, 201), i, e = v.eps, k = v.k;
        var a = g[0].axes({ x: [0, 1], y: [0, 1], title: "Trade-off curves: the attacker's two errors", xlabel: "type I error of the attack" });
        a.line([0, 1], [1, 0], { color: C.muted, width: 1.2, dash: [4, 4] });
        a.line(al, al.map(function (x) { return fEps(x, k * e); }), { color: C.loss, width: 2.6 });
        a.line(al, al.map(function (x) { return fLap(x, e); }), { color: C.gain, width: 1.4 });
        a.line(al, al.map(function (x) { return fGauss(x, e * Math.sqrt(k)); }), { color: C.idea, width: 2.2 });
        a.legend([["perfect privacy", C.muted], ["one Laplace release", C.gain], ["k releases: (k·eps)-DP floor", C.loss], ["k Gaussian releases, mu = eps", C.idea]], { pos: "tr" });
        var pi = Math.exp(e) / (1 + Math.exp(e)), q = (2 * pi - 1) * v.p + 1 - pi, pq = v.p * (1 - v.p);
        var ns = [], m0 = [], mc = [], ml = [];
        for (i = 0; i <= 60; i++) {
          var n = Math.pow(10, 1 + 5 * i / 60); ns.push(n);
          m0.push(pq / n); mc.push(pq / n + 2 / (n * n * e * e)); ml.push(q * (1 - q) / (n * (2 * pi - 1) * (2 * pi - 1)));
        }
        var b = g[1].axes({ x: [10, 1e6], y: [1e-8, 10], logx: true, logy: true, title: "Mean squared error of a private proportion", xlabel: "sample size n (one release at epsilon)" });
        b.line(ns, ml, { color: C.loss, width: 2.2 }).line(ns, mc, { color: C.gain, width: 2.2 }).line(ns, m0, { color: C.ink, width: 1.4, dash: [4, 4] });
        b.legend([["local: randomized response", C.loss], ["central: Laplace on the count", C.gain], ["no privacy: p(1 − p)/n", C.ink]], { pos: "bl" });
        s.out = { be: fEps(0.05, k * e), bg: fGauss(0.05, e * Math.sqrt(k)), n10: 18 / (e * e * pq), ratio: q * (1 - q) / ((2 * pi - 1) * (2 * pi - 1) * pq) };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["best attack's power at 5% type I: (k·eps)-DP floor allows", pct(1 - o.be, 1)], ["k Gaussian releases allow", pct(1 - o.bg, 1)],
          ["n where central noise is a tenth of the variance", o.n10.toFixed(0)], ["local privacy multiplies the sample needed by", o.ratio.toFixed(1)]];
      },
      note: "Exact formulas, no data. The red floor is max(0, 1 − e^(k·eps)·a, e^(−k·eps)·(1 − a)), basic composition of pure epsilon-DP. The gold curve is k independent Gaussian mechanisms with sensitivity over noise sd equal to epsilon each, which compose exactly to mu = eps·√k; a Gaussian mechanism is not pure epsilon-DP, so gold may cross red. The Laplace curve is one release of a count that one person changes by 1.",
    });
  };

  // ---- Part 64: two models on one benchmark ------------------------------------------------------------------------
  W.leaderboardgap = function (el) {
    var PB = 0.847;
    var calc = function (n, gap, d) { // gap and d as proportions; sd of the difference, paired and as if independent
      var pa = PB + gap, sp = Math.sqrt(Math.max(d - gap * gap, 1e-9) / n), su = Math.sqrt((pa * (1 - pa) + PB * (1 - PB)) / n);
      return { sp: sp, su: su, powP: QB.cdf(gap / sp - 1.96) + QB.cdf(-gap / sp - 1.96), powU: QB.cdf((gap - 1.96 * su) / sp) + QB.cdf((-gap - 1.96 * su) / sp), flip: QB.cdf(-gap / sp) };
    };
    QB.widget(el, {
      title: "Is the new model better, or is it the questions?",
      sub: "The old model is right on 84.7% of all possible questions, the new one on a little more. Both answer the same n questions. Green compares them question by question (paired); red treats the two scores as independent samples. Shrink the share of questions on which they disagree and the paired interval tightens while the red one does not move; then set the true gap to 0.5 and ask how large n must be.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Questions in the benchmark", min: 100, max: 10000, step: 100, value: 1000, fmt: function (x) { return String(x); } },
        { k: "gap", label: "True gap (points)", min: 0, max: 3, step: 0.1, value: 0.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "d", label: "Questions the models disagree on (%)", min: 3, max: 26, step: 0.5, value: 14.5, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New benchmark", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var gap = v.gap / 100, d = v.d / 100, n = v.n, r = QB.rng(s.seed + 644), i, n10 = 0, n01 = 0;
        var p10 = (d + gap) / 2, p01 = (d - gap) / 2;
        for (i = 0; i < n; i++) { var u = r(); if (u < p10) n10++; else if (u < p10 + p01) n01++; }
        var diff = (n10 - n01) / n, c = calc(n, gap, d);
        var seP = Math.sqrt(Math.max((n10 + n01) / n - diff * diff, 0) / Math.max(n - 1, 1));
        var lim = Math.max(2.5, 100 * (Math.abs(diff) + 2.2 * c.su), 100 * 2.4 * c.su + v.gap);
        var a = g[0].axes({ x: [-lim, lim], y: [0, 3], title: "One benchmark: 95% intervals for the gap", xlabel: "new model minus old model (points)", noY: true });
        a.vline(0, { color: C.muted }); a.vline(v.gap, { color: C.idea, dash: [2, 3] });
        var bar = function (y, half, col, name) {
          a.line([100 * diff - half, 100 * diff + half], [y, y], { color: col, width: 4 });
          a.dots([100 * diff], [y], { color: col, r: 4.5 });
          a.text(-lim, y + 0.32, name, { color: col, dx: 8 });
        };
        bar(2, 100 * 1.96 * seP, C.gain, "paired: ± " + fmt(100 * 1.96 * seP, 2));
        bar(1, 100 * 1.96 * c.su, C.loss, "as if independent: ± " + fmt(100 * 1.96 * c.su, 2));
        a.legend([["true gap", C.idea], ["no difference", C.muted]], { pos: "bl" });
        var ns = [], pp = [], pu = [], fl = [];
        for (i = 0; i <= 60; i++) { var m = Math.pow(10, 2 + 3 * i / 60), q = calc(m, gap, d); ns.push(m); pp.push(q.powP); pu.push(q.powU); fl.push(q.flip); }
        var b = g[1].axes({ x: [100, 1e5], y: [0, 1], logx: true, title: "Against the number of questions", xlabel: "questions n" });
        b.line(ns, pp, { color: C.gain, width: 2.2 }).line(ns, pu, { color: C.loss, width: 2.2 }).line(ns, fl, { color: C.idea, width: 1.8 });
        b.vline(n, { color: C.ink });
        b.legend([["power, paired test", C.gain], ["power, as if independent", C.loss], ["P(old model scores higher)", C.idea]], { pos: "tl" });
        s.out = { diff: diff, n10: n10, n01: n01, c: c };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["observed gap", fmt(100 * o.diff, 2) + " points"], ["new only right / old only right", o.n10 + " / " + o.n01],
          ["power, paired", pct(o.c.powP, 0)], ["as if independent", pct(o.c.powU, 0)], ["P(old model scores higher)", pct(o.c.flip, 0)]];
      },
      note: "Simulated benchmark; independent questions. The paired variance is (share of disagreements − gap²)/n, so only the questions on which the models disagree carry information. Power is for a two-sided 5% z test by the normal approximation; at a true gap of 0 it is the test's size, which the independent-samples analysis leaves far below 5%. With independent errors the two models would disagree on about 26% of questions.",
    });
  };

  // ---- Part 65: weighted conformal with imperfect weights, against the thesis's bound ---------------------------------
  W.tiltedconformal = function (el) {
    var ALPHA = 0.1, Z = QB.linspace(-6, 6, 61), WZ = Z.map(function (z) { return QB.pdf(z) * 0.2; });
    // P(|eps| e^{gam X} <= q) for X ~ N(center, 1): the score's distribution function, by quadrature
    var scoreCdf = function (q, center, gam) {
      var t = 0, j; for (j = 0; j < Z.length; j++) t += WZ[j] * (2 * QB.cdf(q * Math.exp(-gam * (center + Z[j]))) - 1);
      return t;
    };
    var coverage = function (mu, lam, gam) { // calibrate under the reweighted source N(lam mu, 1), test under N(mu, 1)
      var lo = -14, hi = 14, k;
      for (k = 0; k < 40; k++) { var mid = 0.5 * (lo + hi); if (scoreCdf(Math.exp(mid), lam * mu, gam) < 1 - ALPHA) lo = mid; else hi = mid; }
      return scoreCdf(Math.exp(0.5 * (lo + hi)), mu, gam);
    };
    var tv = function (mu, lam) { return 2 * QB.cdf(Math.abs(1 - lam) * Math.abs(mu) / 2) - 1; };
    QB.widget(el, {
      title: "How much coverage do wrong weights cost?",
      sub: "Calibration points have X ~ N(0, 1), test points X ~ N(mu, 1), and the noise in Y grows like exp(gamma·x). Weights exp(lambda·mu·x) are exact at lambda = 1 and absent at lambda = 0. Blue is the coverage of the 90% weighted conformal interval on the target, red the theorem's floor, 0.9 minus a total variation. Set gamma to 0: the coverage no longer needs weights, and the floor does not know it.",
      panels: 2, height: 300,
      controls: [
        { k: "mu", label: "Shift mu of the target", min: 0, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "lam", label: "Temper lambda of the weights", min: 0, max: 1.5, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "gam", label: "Growth gamma of the noise with x", min: 0, max: 1, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var ls = QB.linspace(0, 1.5, 41), cov = [], bd = [], i;
        for (i = 0; i < ls.length; i++) { cov.push(coverage(v.mu, ls[i], v.gam)); bd.push(1 - ALPHA - tv(v.mu, ls[i])); }
        var c0 = coverage(v.mu, v.lam, v.gam), t0 = tv(v.mu, v.lam);
        s.out = [c0, 1 - ALPHA - t0, t0, Math.abs(1 - v.lam) * v.mu / 2];
        var a = g[0].axes({ x: [0, 1.5], y: [0.2, 1], title: "Coverage on the target against the temper", xlabel: "lambda (1 = exact weights)" });
        a.hline(1 - ALPHA, { color: C.muted });
        a.area(ls, cov, bd, { color: C.spot, alpha: 0.12 });
        a.line(ls, bd, { color: C.loss, width: 2.2 }).line(ls, cov, { color: C.spot, width: 2.2 });
        a.vline(v.lam, { color: C.idea });
        a.dots([v.lam, v.lam], [c0, 1 - ALPHA - t0], { color: function (j) { return j ? C.loss : C.spot; }, r: 4.5 });
        a.legend([["coverage", C.spot], ["floor: 0.9 − TV", C.loss], ["nominal 90%", C.muted]], { pos: "br" });
        var xs = QB.linspace(-4, 6, 201), src = [], rw = [], tg = [], hi = [];
        for (i = 0; i < xs.length; i++) {
          src.push(QB.pdf(xs[i])); rw.push(QB.pdf(xs[i] - v.lam * v.mu)); tg.push(QB.pdf(xs[i] - v.mu));
          hi.push(Math.max(rw[i], tg[i]));
        }
        var b = g[1].axes({ x: [-4, 6], y: [0, 0.6], title: "What the weights fail to move", xlabel: "x" });
        b.area(xs, hi, rw, { color: C.loss, alpha: 0.45 });
        b.line(xs, src, { color: C.muted, width: 1.4, dash: [4, 4] }).line(xs, rw, { color: C.idea, width: 2 }).line(xs, tg, { color: C.gain, width: 2 });
        b.legend([["source N(0, 1)", C.muted], ["source, reweighted", C.idea], ["target N(mu, 1)", C.gain], ["TV (shaded)", C.loss]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["coverage on the target", pct(s.out[0], 1)], ["the theorem's floor", pct(s.out[1], 1)], ["total variation", fmt(s.out[2], 3)], ["Pinsker's bound on it", fmt(s.out[3], 3)]];
      },
      note: "Exact calculation in the limit of a large calibration sample, with the mean of Y known and scores |Y − mean|: no simulation noise, no finite-sample correction and no infinite intervals. Reweighting N(0, 1) by exp(lambda·mu·x) gives N(lambda·mu, 1), so the total variation is 2Φ(|1 − lambda|·mu/2) − 1. The floor is a guarantee, not a prediction: at gamma = 0 the scores do not depend on x and coverage is 90% for any weights.",
    });
  };
})();
