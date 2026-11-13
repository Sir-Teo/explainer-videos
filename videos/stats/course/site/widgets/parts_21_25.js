// Interactives for Stage III, Master's: the computational and likelihood core (Parts 21-25).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 21: gradient descent on a bowl of condition number kappa -------------------------------------------
  W.condzigzag = function (el) {
    QB.widget(el, {
      title: "The condition number sets the pace of gradient descent",
      sub: "The objective is the bowl f(a, b) = (a² + κ b²)/2, with curvature 1 along a and κ along b. Gradient descent (blue) uses the step s/κ; Newton (gold) rescales by the curvature and lands in one step. Raise κ and watch the zigzag; push s past 2 and the method diverges.",
      panels: 2, height: 300,
      controls: [
        { k: "lk", label: "Condition number κ", min: 0, max: 3, step: 0.05, value: 1, fmt: function (x) { return Math.pow(10, x).toFixed(x < 1 ? 1 : 0); } },
        { k: "s", label: "Step, in units of 1/κ", min: 0.1, max: 2.2, step: 0.05, value: 1.8, fmt: function (x) { return x.toFixed(2); } },
        { k: "k", label: "Steps taken", min: 1, max: 200, step: 1, value: 40 },
      ],
      draw: function (g, v, s) {
        var kap = Math.pow(10, v.lk), step = v.s / kap, n = Math.round(v.k), i, j;
        var xs = [1], ys = [1], err = [0], clamp = function (z) { return Math.max(-1e6, Math.min(1e6, z)); };
        var f = function (a, b) { return 0.5 * (a * a + kap * b * b); }, f0 = f(1, 1);
        for (i = 0; i < n; i++) {
          xs.push(clamp(xs[i] * (1 - step))); ys.push(clamp(ys[i] * (1 - step * kap)));
          err.push(Math.log10(Math.max(1e-16, Math.min(1e12, f(xs[i + 1], ys[i + 1]) / f0))));
        }
        var ra = Math.abs(1 - step), rb = Math.abs(1 - step * kap), rate = Math.max(ra, rb);
        var best = (kap - 1) / (kap + 1);
        s.out = { rate: rate, per10: rate >= 1 ? "never (diverges)" : rate < 1e-9 ? "1" : String(Math.ceil(-1 / Math.log10(rate))), last: err[n], best: best };
        var a = g[0].axes({ x: [-1.3, 1.3], y: [-1.3, 1.3], title: "The path on the bowl's level curves", xlabel: "a (curvature 1)" });
        var levels = [0.02, 0.1, 0.3, 0.6, 1, 1.6];
        for (j = 0; j < levels.length; j++) {
          var ex = [], ey = [], c = levels[j] * f0;
          for (i = 0; i <= 80; i++) { var t = 2 * Math.PI * i / 80; ex.push(Math.sqrt(2 * c) * Math.cos(t)); ey.push(Math.sqrt(2 * c / kap) * Math.sin(t)); }
          a.line(ex, ey, { color: C.muted, width: 1, alpha: 0.55 });
        }
        a.line([1, 0], [1, 0], { color: C.idea, width: 2 });
        a.line(xs, ys, { color: C.spot, width: 1.6 });
        a.dots(xs, ys, { color: C.spot, r: 2.2 });
        a.dots([1], [1], { color: C.ink, r: 4 });
        a.dots([0], [0], { color: C.gain, r: 4 });
        a.legend([["gradient descent", C.spot], ["Newton, one step", C.idea], ["the minimum", C.gain]], { pos: "bl" });
        var b = g[1].axes({ x: [0, n], y: [-16, 4], title: "log10 of f(step k) / f(start)", xlabel: "step k" });
        var ks = [], bd = [];
        for (i = 0; i <= n; i++) { ks.push(i); bd.push(best > 0 ? Math.max(-16, 2 * i * Math.log10(best)) : (i === 0 ? 0 : -16)); }
        b.hline(0, { color: C.muted });
        b.line(ks, bd, { color: C.gain, dash: [5, 4], width: 1.5 });
        b.line(ks, err, { color: C.spot, width: 2 });
        b.legend([["this step size", C.spot], ["bound at the best step, 2/(1 + κ)", C.gain]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["error factor per step", fmt(s.out.rate, 3)], ["best possible, (κ − 1)/(κ + 1)", fmt(s.out.best, 3)],
          ["steps per factor of ten", s.out.per10], ["log10 f after the last step", fmt(s.out.last, 1)]];
      },
      note: "An exact quadratic, no data. The error factor is the larger of |1 − s/κ| and |1 − s| on the distance to the minimum; the objective falls by its square. The plot floors at 10⁻¹⁶.",
    });
  };

  // ---- Part 22: Wald, score and likelihood ratio on one binomial log likelihood --------------------------------
  W.trinitycurve = function (el) {
    QB.widget(el, {
      title: "Three tests read from one likelihood curve",
      sub: "The blue curve is the binomial log likelihood, measured down from its peak. The likelihood ratio reads its drop at the null value; Wald reads the drop of the parabola fitted at the peak (gold); the score test reads the height of the parabola fitted at the null (purple). Shrink n, or move the estimate towards 0 or 1, and the three part company.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Trials n", min: 10, max: 400, step: 2, value: 20 },
        { k: "ph", label: "Observed proportion", min: 0.05, max: 0.95, step: 0.01, value: 0.7, fmt: function (x) { return x.toFixed(2); } },
        { k: "p0", label: "Null value p₀", min: 0.05, max: 0.95, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var n = Math.round(v.n), x = Math.max(1, Math.min(n - 1, Math.round(n * v.ph))), ph = x / n, p0 = v.p0, i;
        var ll = function (p) { return x * Math.log(p) + (n - x) * Math.log(1 - p); }, top = ll(ph);
        var wald = function (p) { return (ph - p) * (ph - p) * n / (ph * (1 - ph)); };
        var score = function (p) { return (ph - p) * (ph - p) * n / (p * (1 - p)); };
        var lr = function (p) { return 2 * (top - ll(p)); };
        var pv = function (t) { return 2 * (1 - QB.cdf(Math.sqrt(Math.max(0, t)))); };
        var ps = QB.linspace(0.004, 0.996, 249), cl = [], cw = [], cs = [], tw = [], ts = [], tl = [];
        var lo = 1, hi = 0, u0 = (x - n * p0) / (p0 * (1 - p0)), i0 = n / (p0 * (1 - p0)), base = ll(p0) - top;
        for (i = 0; i < ps.length; i++) {
          var p = ps[i];
          cl.push(ll(p) - top); cw.push(-0.5 * wald(p));
          cs.push(base + u0 * (p - p0) - 0.5 * i0 * (p - p0) * (p - p0));
          tw.push(wald(p)); ts.push(score(p)); tl.push(lr(p));
          if (lr(p) <= 3.8415) { lo = Math.min(lo, p); hi = Math.max(hi, p); }
        }
        var half = 1.96 * Math.sqrt(ph * (1 - ph) / n), z2 = 3.8415;
        var mid = (ph + z2 / (2 * n)) / (1 + z2 / n), wh = 1.96 * Math.sqrt(ph * (1 - ph) / n + z2 / (4 * n * n)) / (1 + z2 / n);
        s.out = { x: x, W: wald(p0), S: score(p0), L: lr(p0), pv: pv, wald: [ph - half, ph + half], wilson: [mid - wh, mid + wh], lr: [lo, hi] };
        var a = g[0].axes({ x: [0, 1], y: [-7, 1.2], title: "Log likelihood, from its peak", xlabel: "p" });
        a.hline(0, { color: C.muted });
        a.vline(p0, { color: C.loss });
        a.line(ps, cw, { color: C.idea, width: 1.6 });
        a.line(ps, cs, { color: C.q, width: 1.6 });
        a.line(ps, cl, { color: C.spot, width: 2.2 });
        a.dots([ph], [0], { color: C.spot, r: 4 });
        a.dots([p0, p0], [base, -0.5 * wald(p0)], { color: function (j) { return j ? C.idea : C.spot; }, r: 3.5 });
        a.text(p0, 0.75, "p₀", { color: C.loss, dx: p0 > 0.85 ? -18 : 5 });
        a.legend([["log likelihood (LR)", C.spot], ["parabola at the peak (Wald)", C.idea], ["parabola at p₀ (score)", C.q]], { pos: ph > 0.5 ? "bl" : "br" });
        var b = g[1].axes({ x: [0, 1], y: [0, 10], title: "LR, Wald and score as p₀ moves", xlabel: "null value p₀" });
        b.hline(z2, { color: C.muted });
        b.text(ph > 0.5 ? 0.98 : 0.02, z2, "3.84", { color: C.muted, dy: -9, align: ph > 0.5 ? "right" : "left" });
        b.vline(p0, { color: C.loss });
        b.line(ps, tw, { color: C.idea, width: 1.8 });
        b.line(ps, ts, { color: C.q, width: 1.8 });
        b.line(ps, tl, { color: C.spot, width: 1.8 });
      },
      readout: function (v, s) {
        var o = s.out, iv = function (r) { return "[" + fmt(r[0], 3) + ", " + fmt(r[1], 3) + "]"; };
        var st = function (t) { return fmt(Math.min(t, 9999), 2) + " (p " + fmt(o.pv(t), 3) + ")"; };
        return [["successes", String(o.x)], ["Wald", st(o.W)], ["score", st(o.S)], ["likelihood ratio", st(o.L)],
          ["95% Wald", iv(o.wald)], ["Wilson", iv(o.wilson)], ["LR", iv(o.lr)]];
      },
      note: "Exact formulas, no simulation; each statistic is referred to chi-squared with 1 degree of freedom. The intervals are the null values each test does not reject at 5%: where its curve lies below 3.84. With 14 of 20 against ½ the film's numbers appear: 3.81, 3.20, 3.29.",
    });
  };

  // ---- Part 23: a programme assigned by school; iid against cluster-robust standard errors ---------------------
  W.moultonschools = function (el) {
    QB.widget(el, {
      title: "Pupils in schools: what the iid standard error misses",
      sub: "A programme with no true effect is assigned to half the schools. Left: one study, each dot a school's mean score. Right: the estimate from 400 such studies, against the normal curves the iid (red) and cluster-robust (green) standard errors promise. Raise the intraclass correlation or the school size and the red curve becomes too narrow; cut the schools to six and the green one does too.",
      panels: 2, height: 300,
      controls: [
        { k: "G", label: "Schools", min: 6, max: 80, step: 2, value: 40 },
        { k: "m", label: "Pupils per school", min: 5, max: 80, step: 1, value: 30 },
        { k: "rho", label: "Intraclass correlation ρ", min: 0, max: 0.6, step: 0.01, value: 0.15, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New studies", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var G = Math.round(v.G), m = Math.round(v.m), rho = v.rho, h = G / 2, N = G * m, r = QB.rng(s.seed + 230), reps = 400, i, k;
        var nu = G - 1, z = 1.96, z3 = z * z * z, z5 = z3 * z * z, z7 = z5 * z * z;
        var tq = z + (z3 + z) / (4 * nu) + (5 * z5 + 16 * z3 + 3 * z) / (96 * nu * nu) + (3 * z7 + 19 * z5 + 17 * z3 - 15 * z) / (384 * nu * nu * nu);
        var sdMean = Math.sqrt(rho + (1 - rho) / m), kdf = m - 1, c9 = 2 / (9 * kdf);
        var est = [], sumI = 0, sumC = 0, covI = 0, covC = 0, first = null;
        for (k = 0; k < reps; k++) {
          var mean = [], sums = [0, 0], within = 0;
          for (i = 0; i < G; i++) {
            mean.push(sdMean * r.normal()); sums[i < h ? 0 : 1] += mean[i];
            var wh = 1 - c9 + Math.sqrt(c9) * r.normal(); within += (1 - rho) * kdf * Math.max(0, wh * wh * wh); // chi-squared, Wilson-Hilferty
          }
          var m1 = sums[0] / h, m0 = sums[1] / h, between = 0;
          for (i = 0; i < G; i++) { var d = mean[i] - (i < h ? m1 : m0); between += d * d; }
          var b = m1 - m0, seI = Math.sqrt((within + m * between) / (N - 2) * 4 / N);
          var seC = Math.sqrt(between / (h * h) * G / (G - 1) * (N - 1) / (N - 2));
          est.push(b); sumI += seI; sumC += seC;
          if (Math.abs(b) < 1.96 * seI) covI++;
          if (Math.abs(b) < tq * seC) covC++;
          if (k === 0) first = { mean: mean, m1: m1, m0: m0, b: b, seI: seI, seC: seC };
        }
        var sd = QB.sd(est), mI = sumI / reps, mC = sumC / reps;
        s.out = { moulton: 1 + (m - 1) * rho, ratio: sd / mI, covI: covI / reps, covC: covC / reps, first: first };
        var a = g[0].axes({ x: [0, G + 1], y: [-2, 2], title: "One study: school means (SD units)", xlabel: "school", nx: 4 });
        var idx = [], cols = function (j) { return j < h ? C.idea : C.spot; };
        for (i = 0; i < G; i++) idx.push(i + 1);
        a.hline(0, { color: C.muted });
        a.line([0.5, h + 0.5], [first.m1, first.m1], { color: C.idea, width: 2 });
        a.line([h + 0.5, G + 0.5], [first.m0, first.m0], { color: C.spot, width: 2 });
        a.dots(idx, first.mean, { color: cols, r: G > 50 ? 2.5 : 3.5 });
        a.legend([["programme schools", C.idea], ["other schools", C.spot]], { pos: "bl" });
        var lim = Math.max(4 * sd, 0.02), nb = 31, wd = 2 * lim / nb, hs = QB.hist(est, -lim, lim, nb), xs = [], dens = [], top = 0;
        for (i = 0; i < nb; i++) { xs.push(-lim + (i + 0.5) * wd); dens.push(hs[i] / (reps * wd)); top = Math.max(top, dens[i]); }
        var grid = QB.linspace(-lim, lim, 121), nrm = function (se) { return grid.map(function (x) { return QB.pdf(x / se) / se; }); };
        top = Math.max(top, QB.pdf(0) / mC, Math.min(QB.pdf(0) / mI, 3 * QB.pdf(0) / mC)) * 1.12;
        var c = g[1].axes({ x: [-lim, lim], y: [0, top], title: "400 studies: the estimated effect", xlabel: "estimate (truth 0)", nx: 4, ny: 4 });
        c.bars(xs, dens, wd, { color: C.cash, alpha: 0.55 });
        c.line(grid, nrm(mI), { color: C.loss, width: 2 });
        c.line(grid, nrm(mC), { color: C.gain, width: 2 });
        c.legend([["iid SE", C.loss], ["cluster-robust SE", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["Moulton's factor 1 + (m − 1)ρ", fmt(o.moulton, 2)], ["its square root", fmt(Math.sqrt(o.moulton), 2)],
          ["true sd / iid SE", fmt(o.ratio, 2)], ["95% coverage, iid", QB.pct(o.covI)], ["cluster-robust, t(G − 1)", QB.pct(o.covC)]];
      },
      note: "Simulated data: equal school sizes, total variance 1, a share ρ of it between schools, the regression is score on the programme dummy. When the red curve is more than three times too narrow its peak is cut off. Cluster-robust is CR1; coverage is over the 400 studies, so it moves by a point or two between draws.",
    });
  };

  // ---- Part 24: IRLS on Bliss's beetles, under three links ------------------------------------------------------
  W.beetleirls = function (el) {
    var X = [1.6907, 1.7242, 1.7552, 1.7842, 1.8113, 1.8369, 1.8610, 1.8839], N = [59, 60, 62, 56, 63, 59, 62, 60], K = [6, 13, 18, 28, 52, 53, 61, 60];
    var names = ["logit", "probit", "cloglog"], cols = [C.spot, C.gain, C.idea];
    var clip = function (p) { return Math.max(1e-10, Math.min(1 - 1e-10, p)); };
    var ginv = function (L, e) { return clip(L === 0 ? 1 / (1 + Math.exp(-e)) : L === 1 ? QB.cdf(e) : 1 - Math.exp(-Math.exp(Math.min(e, 30)))); };
    var dmu = function (L, e) { var m = ginv(L, e); return Math.max(1e-12, L === 0 ? m * (1 - m) : L === 1 ? QB.pdf(e) : Math.exp(Math.min(e, 30) - Math.exp(Math.min(e, 30)))); };
    var half = [0, 0, Math.log(Math.log(2))]; // the link at one half
    function deviance(L, b, k) {
      var d = 0;
      for (var i = 0; i < 8; i++) {
        var m = ginv(L, b[0] + b[1] * (X[i] - 1.8)), y = k[i], n = N[i];
        if (y > 0) d += 2 * y * Math.log(y / (n * m));
        if (y < n) d += 2 * (n - y) * Math.log((n - y) / (n * (1 - m)));
      }
      return d;
    }
    function irls(L, k, steps) { // Fisher scoring from beta = 0, on the dose centred at 1.8; halve a step that raises the deviance
      var b = [0, 0], path = [deviance(L, b, k)], bs = [b];
      for (var t = 0; t < steps; t++) {
        var s0 = 0, s1 = 0, s2 = 0, t0 = 0, t1 = 0, i;
        for (i = 0; i < 8; i++) {
          var x = X[i] - 1.8, e = b[0] + b[1] * x, m = ginv(L, e), d = dmu(L, e), w = N[i] * d * d / (m * (1 - m)), z = e + (k[i] / N[i] - m) / d;
          s0 += w; s1 += w * x; s2 += w * x * x; t0 += w * z; t1 += w * x * z;
        }
        var det = s0 * s2 - s1 * s1, nb = Math.abs(det) > 1e-300 ? [(s2 * t0 - s1 * t1) / det, (s0 * t1 - s1 * t0) / det] : b, dv = deviance(L, nb, k);
        for (i = 0; i < 30 && !(dv <= path[t] + 1e-9); i++) { nb = [(nb[0] + b[0]) / 2, (nb[1] + b[1]) / 2]; dv = deviance(L, nb, k); }
        b = nb; path.push(dv); bs.push(b);
      }
      return { b: b, path: path, bs: bs };
    }
    QB.widget(el, {
      title: "Bliss's beetles: one algorithm, three links",
      sub: "Eight doses of carbon disulphide and the share of beetles killed at each (Bliss 1935). Step IRLS forward from β = 0 and watch the curve of the chosen link (drawn thick) settle and its deviance fall. Then change how many of the 56 beetles died at the fourth dose: the curve cannot follow one point, and the deviance pays.",
      panels: 2, height: 300,
      controls: [
        { k: "link", label: "Link", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return names[Math.round(x)]; } },
        { k: "steps", label: "IRLS steps from β = 0", min: 0, max: 8, step: 1, value: 2 },
        { k: "k4", label: "Deaths at the fourth dose (of 56)", min: 0, max: 56, step: 1, value: 28 },
      ],
      draw: function (g, v, s) {
        var L = Math.round(v.link), steps = Math.round(v.steps), k = K.slice(), j, i;
        k[3] = Math.round(v.k4);
        var fits = [0, 1, 2].map(function (l) { return irls(l, k, 8); }), b = fits[L].bs[steps], end = fits[L].bs[8];
        var ld = Math.abs(b[1]) > 1e-6 ? 1.8 + (half[L] - b[0]) / b[1] : null;
        s.out = { dev: fits[L].path[steps], fin: fits[L].path[8], slope: b[1], ld: ld !== null && ld > 1.5 && ld < 2.1 ? ld : null, all: fits.map(function (f) { return f.path[8]; }) };
        var a = g[0].axes({ x: [1.66, 1.91], y: [0, 1.05], yticks: [0, 0.2, 0.4, 0.6, 0.8, 1], title: "Share killed against log10 dose", xlabel: "log10 dose of CS₂", nx: 5 });
        var grid = QB.linspace(1.66, 1.91, 101);
        for (j = 0; j < 3; j++) if (j !== L) a.line(grid, grid.map(function (x) { return ginv(j, fits[j].bs[8][0] + fits[j].bs[8][1] * (x - 1.8)); }), { color: cols[j], width: 1, alpha: 0.55 });
        a.line(grid, grid.map(function (x) { return ginv(L, end[0] + end[1] * (x - 1.8)); }), { color: cols[L], width: 1, dash: [4, 4] });
        a.line(grid, grid.map(function (x) { return ginv(L, b[0] + b[1] * (x - 1.8)); }), { color: cols[L], width: 2.4 });
        if (s.out.ld !== null) { a.line([s.out.ld, s.out.ld], [0, 0.5], { color: C.muted, dash: [3, 3], width: 1 }); a.text(s.out.ld, 0.06, "LD50", { color: C.muted, dx: 5 }); }
        a.dots(X, k.map(function (y, q) { return y / N[q]; }), { color: function (q) { return q === 3 ? C.loss : C.ink; }, r: 4 });
        a.legend([["logit", cols[0]], ["probit", cols[1]], ["cloglog", cols[2]]], { pos: "tl" });
        var lg = function (d) { return Math.log10(Math.max(1, d)); }, top = 1;
        for (j = 0; j < 3; j++) for (i = 0; i <= 8; i++) top = Math.max(top, lg(fits[j].path[i]));
        var c = g[1].axes({ x: [0, 8], y: [0, Math.ceil(top * 2 + 0.2) / 2], title: "log10 deviance after each step", xlabel: "IRLS step" });
        var it = [0, 1, 2, 3, 4, 5, 6, 7, 8];
        c.hline(lg(12.59), { color: C.loss });
        c.text(8, lg(12.59), "12.59: the 5% point of χ² on 6 df", { color: C.loss, align: "right", dy: -9, bg: true });
        for (j = 0; j < 3; j++) c.line(it, fits[j].path.map(lg), { color: cols[j], width: j === L ? 2.4 : 1, alpha: j === L ? 1 : 0.6 });
        c.dots([steps], [lg(fits[L].path[steps])], { color: cols[L], r: 5 });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["deviance now", fmt(o.dev, 2)], ["at convergence", fmt(o.fin, 2)], ["slope now", fmt(o.slope, 2)],
          ["LD50 (log dose)", o.ld === null ? "none yet" : fmt(o.ld, 4)],
          ["converged deviances: logit / probit / cloglog", fmt(o.all[0], 2) + " / " + fmt(o.all[1], 2) + " / " + fmt(o.all[2], 2)]];
      },
      note: "Bliss's data: 481 beetles at eight doses. The red dot is the dose you can change; set it back to 28 for the real experiment. The dashed curve is the converged fit of the chosen link, the thin curves the other two links at convergence. Deviances below 1 are drawn at 1.",
    });
  };

  // ---- Part 25: shrinking p noisy estimates towards their mean -------------------------------------------------
  W.steinrails = function (el) {
    QB.widget(el, {
      title: "Shrink them all: the total improves, one of them may not",
      sub: "Each unit has a true value (green rail) and one noisy measurement with unit variance (blue rail). The gold rail keeps a fraction of every measurement's distance from the common mean. Slide the fraction to find the smallest total squared error, and compare it with the fraction James-Stein chooses from the data. Then move the red unit far from the rest: the total still gains, and that unit pays.",
      panels: 2, height: 310,
      controls: [
        { k: "p", label: "Units p", min: 4, max: 40, step: 1, value: 18 },
        { k: "tau", label: "Spread of the true values", min: 0, max: 4, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "out", label: "True value of the red unit", min: 0, max: 10, step: 0.5, value: 0, fmt: function (x) { return x.toFixed(1); } },
        { k: "keep", label: "Fraction of each distance kept", min: 0, max: 1, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var p = Math.round(v.p), r = QB.rng(s.seed + 250), th = [], x = [], i;
        for (i = 0; i < p; i++) { var z = r.normal(), e = r.normal(); th.push(i === 0 ? v.out : v.tau * z); x.push(th[i] + e); }
        var xb = QB.mean(x), S = 0;
        for (i = 0; i < p; i++) S += (x[i] - xb) * (x[i] - xb);
        var cjs = 1 - Math.min(1, (p - 3) / Math.max(S, 1e-9));
        var sse = function (c) { var t = 0; for (var j = 0; j < p; j++) { var d = xb + c * (x[j] - xb) - th[j]; t += d * d; } return t; };
        var est = x.map(function (xi) { return xb + v.keep * (xi - xb); }), js = x.map(function (xi) { return xb + cjs * (xi - xb); }), closer = 0;
        for (i = 0; i < p; i++) if (Math.abs(js[i] - th[i]) < Math.abs(x[i] - th[i])) closer++;
        var cs = QB.linspace(0, 1, 101), curve = cs.map(sse), best = 0;
        for (i = 1; i < cs.length; i++) if (curve[i] < curve[best]) best = i;
        s.out = { raw: sse(1), mine: sse(v.keep), js: sse(cjs), cjs: cjs, closer: closer, p: p, red: [Math.abs(x[0] - th[0]), Math.abs(js[0] - th[0])], best: cs[best] };
        var half = Math.max(4, 3 * v.tau + 3);
        var a = g[0].axes({ x: [-half, Math.max(half, v.out + 3.5)], y: [-0.45, 2.45], title: "Measured, shrunk, true", xlabel: "value", yticks: [0, 1, 2], yfmt: function (y) { return ["true", "shrunk", "raw"][y]; } });
        var colr = function (base) { return function (j) { return j === 0 ? C.loss : base; }; };
        for (i = p - 1; i >= 0; i--) a.line([x[i], est[i], th[i]], [2, 1, 0], { color: i === 0 ? C.loss : C.muted, width: i === 0 ? 1.8 : 1, alpha: i === 0 ? 1 : 0.6 });
        a.vline(xb, { color: C.muted });
        a.dots(x, x.map(function () { return 2; }), { color: colr(C.spot), r: 3.2 });
        a.dots(est, est.map(function () { return 1; }), { color: colr(C.idea), r: 3.2 });
        a.dots(th, th.map(function () { return 0; }), { color: colr(C.gain), r: 3.2 });
        a.text(xb, 2.3, "mean", { color: C.muted, dx: 5 });
        var top = Math.max(curve[0], curve[100], 1) * 1.15;
        var b = g[1].axes({ x: [0, 1], y: [0, top], title: "Total squared error against the fraction kept", xlabel: "fraction kept (1 = raw measurements)" });
        b.hline(curve[100], { color: C.spot });
        b.line(cs, curve, { color: C.ink, width: 2 });
        b.vline(cjs, { color: C.q });
        b.dots([cjs], [sse(cjs)], { color: C.q, r: 5 });
        b.dots([v.keep], [sse(v.keep)], { color: C.idea, r: 5 });
        b.legend([["your fraction", C.idea], ["James-Stein's fraction", C.q], ["raw measurements", C.spot]], { pos: cjs > 0.5 ? "bl" : "br" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["total squared error: raw", fmt(o.raw, 1)], ["yours", fmt(o.mine, 1)], ["James-Stein", fmt(o.js, 1)],
          ["James-Stein keeps", fmt(o.cjs, 2)], ["best for this sample", fmt(o.best, 2)], ["units it brings closer", o.closer + " of " + o.p],
          ["red unit's error: raw, James-Stein", fmt(o.red[0], 2) + ", " + fmt(o.red[1], 2)]];
      },
      note: "Simulated data: normal true values, unit-variance normal noise, positive-part James-Stein towards the grand mean, keeping 1 − (p − 3)/Σ(x − x̄)². Its guarantee is on the expected total over repeated samples, not on any one sample or any one unit.",
    });
  };
})();
