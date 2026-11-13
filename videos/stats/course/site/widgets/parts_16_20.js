// Interactives for Stage II, Bachelor's: Methods (Parts 16-20).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- Part 16: the bootstrap world against the real world, for a mean, a median and a maximum ----------------
  W.bootspike = function (el) {
    var NAMES = ["mean", "median", "maximum"], TRUTH = [0.5, 0.5, 1], R = 1000;
    var stat = function (x, which) {
      var i, s = 0, n = x.length;
      if (which === 0) { for (i = 0; i < n; i++) s += x[i]; return s / n; }
      if (which === 2) { s = x[0]; for (i = 1; i < n; i++) if (x[i] > s) s = x[i]; return s; }
      var c = Array.prototype.slice.call(x).sort(function (a, b) { return a - b; });
      return n % 2 ? c[(n - 1) / 2] : 0.5 * (c[n / 2 - 1] + c[n / 2]);
    };
    QB.widget(el, {
      title: "Two worlds: real samples and resamples",
      sub: "Left: the statistic over 1,000 fresh samples from Uniform(0, 1), minus the truth. Right: the same statistic over 1,000 resamples of one sample, minus that sample's value. For the mean the two pictures agree. Move the statistic to the maximum: the bootstrap world collapses onto a spike.",
      panels: 2, height: 300,
      controls: [
        { k: "which", label: "Statistic", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return NAMES[x]; } },
        { k: "n", label: "Sample size n", min: 5, max: 100, step: 1, value: 50, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, which = v.which, r = QB.rng(977 + 13 * s.seed), i, j, x = new Array(n), real = [], boot = [];
        for (i = 0; i < R; i++) { for (j = 0; j < n; j++) x[j] = r(); real.push(stat(x, which) - TRUTH[which]); }
        var sample = new Array(n); for (j = 0; j < n; j++) sample[j] = r();
        var est = stat(sample, which), same = 0, raw = [];
        for (i = 0; i < R; i++) {
          for (j = 0; j < n; j++) x[j] = sample[Math.floor(r() * n)];
          var t = stat(x, which); raw.push(t); boot.push(t - est); if (t === est) same++;
        }
        var lo = QB.quantile(raw, 0.025), hi = QB.quantile(raw, 0.975), sdr = QB.sd(real), sdb = QB.sd(boot);
        var range = which === 2 ? [-6 / n, 2 / n] : [-4 * sdr, 4 * sdr], nb = 40, bw = (range[1] - range[0]) / nb;
        var mids = QB.linspace(range[0] + bw / 2, range[1] - bw / 2, nb);
        var hr = QB.hist(real, range[0], range[1], nb).map(function (c) { return c / R; });
        var hb = QB.hist(boot, range[0] - 1e-12, range[1] - 1e-12, nb).map(function (c) { return c / R; });
        var top = 1.12 * Math.max(0.05, Math.max.apply(null, hr), Math.max.apply(null, hb));
        var xf = function (t) { return fmt(t, 2); };
        var a = g[0].axes({ x: range, y: [0, top], nx: 4, xfmt: xf, title: "Real world: " + NAMES[which] + " − truth", xlabel: "1,000 fresh samples" });
        a.bars(mids, hr, bw, { color: C.gain });
        a.vline(0, { color: C.ink });
        var b = g[1].axes({ x: range, y: [0, top], nx: 4, xfmt: xf, title: "Bootstrap world: " + NAMES[which] + "* − " + NAMES[which], xlabel: "1,000 resamples of one sample" });
        b.bars(mids, hb, bw, { color: same / R > 0.3 ? C.loss : C.spot });
        b.vline(0, { color: C.ink });
        if (same / R > 0.3) b.text(0, 0.9 * top, pct(same / R, 0) + " repeat the estimate", { color: C.loss, align: "right", dx: -8, bg: true });
        s.out = { sdr: sdr, sdb: sdb, same: same / R, lo: lo, hi: hi, covers: lo <= TRUTH[which] && TRUTH[which] <= hi, theory: 1 - Math.pow(1 - 1 / n, n) };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["real sd", fmt(o.sdr, 4)], ["bootstrap sd", fmt(o.sdb, 4)],
          ["resamples equal to the estimate", pct(o.same, 1) + (v.which === 2 ? " (theory " + pct(o.theory, 1) + ")" : "")],
          ["95% percentile interval", "[" + fmt(o.lo, 3) + ", " + fmt(o.hi, 3) + "]"],
          ["contains the truth " + fmt(TRUTH[v.which], 1), o.covers ? "yes" : "no"]];
      },
      note: "Simulated data: Uniform(0, 1), so the true mean and median are 0.5 and the true maximum is 1. Green is the real sampling distribution, blue the bootstrap's, red a bootstrap that has failed. For the maximum the share of resamples that repeat the estimate is 1 − (1 − 1/n)ⁿ, about 63% for every n, and the percentile interval always ends below 1. The median's bootstrap is lumpy as well, but its lumps shrink as n grows.",
    });
  };

  // ---- Part 17: an AR(2), its roots, its pseudo-cycle and its correlogram ----------------------------------------
  W.ar2cycle = function (el) {
    var T = 150, L = 24;
    QB.widget(el, {
      title: "An AR(2): from two coefficients to a cycle that is not there",
      sub: "The series is X(t) = φ₁X(t−1) + φ₂X(t−2) + shock, driven by the same random shocks whatever the sliders say. Make φ₂ more negative and waves appear, though nothing periodic drives them. Push the pair out of the stationarity triangle and the series explodes.",
      panels: 2, height: 300,
      controls: [
        { k: "p1", label: "φ₁", min: -1.9, max: 1.9, step: 0.05, value: 1.3, fmt: function (x) { return fmt(x, 2); } },
        { k: "p2", label: "φ₂", min: -0.95, max: 0.95, step: 0.05, value: -0.6, fmt: function (x) { return fmt(x, 2); } },
      ],
      buttons: [{ label: "New shocks", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var p1 = v.p1, p2 = v.p2, r = QB.rng(311 + 7 * s.seed), i, h;
        var stat = p1 + p2 < 1 - 1e-9 && p2 - p1 < 1 - 1e-9 && Math.abs(p2) < 1;
        var burn = stat ? 200 : 0, x = [], a1 = 0, a2 = 0;
        for (i = 0; i < burn + T; i++) { var e = r.normal(), xt = p1 * a1 + p2 * a2 + e; a2 = a1; a1 = xt; if (i >= burn) x.push(xt); }
        var m = QB.mean(x), c0 = 0, big = 0;
        for (i = 0; i < T; i++) { c0 += (x[i] - m) * (x[i] - m); big = Math.max(big, Math.abs(x[i])); }
        var lags = [], samp = [], theo = [];
        for (h = 0; h <= L; h++) {
          var c = 0; for (i = h; i < T; i++) c += (x[i] - m) * (x[i - h] - m);
          lags.push(h); samp.push(c0 > 0 ? c / c0 : 0);
        }
        if (stat) { theo = [1, p1 / (1 - p2)]; for (h = 2; h <= L; h++) theo.push(p1 * theo[h - 1] + p2 * theo[h - 2]); }
        var disc = p1 * p1 + 4 * p2, mod, period = 0;
        if (disc < 0) { mod = Math.sqrt(-p2); period = 2 * Math.PI / Math.acos(Math.max(-0.999999, Math.min(0.999999, p1 / (2 * Math.sqrt(-p2))))); }
        else mod = Math.max(Math.abs(p1 + Math.sqrt(disc)), Math.abs(p1 - Math.sqrt(disc))) / 2;
        s.out = { stat: stat, complex: disc < 0, mod: mod, period: period, r1: samp[1] };
        var yr = stat ? Math.max(4, 1.15 * big) : 40;
        var a = g[0].axes({ x: [0, T], y: [-yr, yr], title: stat ? "One realization, 150 steps" : "Not stationary: the series leaves the frame", xlabel: "time" });
        a.hline(0, { color: C.muted });
        a.line(QB.linspace(0, T - 1, T), x, { color: stat ? C.spot : C.loss, width: 1.6 });
        var b = g[1].axes({ x: [-0.7, L + 0.7], y: [-1.05, 1.05], title: "Autocorrelation by lag", xlabel: "lag" });
        b.hline(0, { color: C.muted, dash: [] });
        var band = 1.96 / Math.sqrt(T);
        b.hline(band, { color: C.muted }); b.hline(-band, { color: C.muted });
        if (stat) b.bars(lags, theo, 0.62, { color: C.idea, alpha: 0.75 });
        b.dots(lags, samp, { color: stat ? C.spot : C.loss, r: 3 });
        b.legend(stat ? [["the model's ACF", C.idea], ["this sample's ACF", C.spot]] : [["this sample's ACF", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["stationary", o.stat ? "yes" : "no"], ["roots", o.complex ? "complex" : "real"], ["largest inverse root, modulus", fmt(o.mod, 3)],
          ["pseudo-period", o.complex ? fmt(o.period, 1) + " steps" : "none"], ["sample ACF at lag 1", fmt(o.r1, 2)]];
      },
      note: "Simulated data: Gaussian shocks with unit variance. The model is stationary when φ₁ + φ₂ < 1, φ₂ − φ₁ < 1 and |φ₂| < 1, that is, when both inverse roots lie inside the unit circle. Complex roots (φ₁² + 4φ₂ < 0) give a damped cosine ACF with period 2π / arccos(φ₁ / (2√(−φ₂))). The dashed lines are the bands ±1.96/√n for white noise.",
    });
  };

  // ---- Part 18: a large self-selected sample against a small random one (Meng's identity) ------------------------
  W.digestpoll = function (el) {
    var N = 100000, P = 0.382, SIG = Math.sqrt(P * (1 - P)), REPS = 300;
    QB.widget(el, {
      title: "Who answered? A mailed ballot against a random sample",
      sub: "An island of 100,000 adults, 38.2% for Blue. Everyone is mailed a ballot; Blue and Red voters return it at the rates you set. A pollster draws a simple random sample instead. Start with equal return rates, then let Blue voters answer a little more often.",
      panels: 2, height: 300,
      controls: [
        { k: "rb", label: "Blue voters who return the ballot", min: 1, max: 60, step: 1, value: 21, fmt: function (x) { return x + "%"; } },
        { k: "rr", label: "Red voters who return the ballot", min: 1, max: 60, step: 1, value: 13, fmt: function (x) { return x + "%"; } },
        { k: "n", label: "Size of the random sample", min: 100, max: 5000, step: 100, value: 1000, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New draws", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rb = v.rb / 100, rr = v.rr / 100, n = v.n, r = QB.rng(523 + 11 * s.seed), i;
        var f = P * rb + (1 - P) * rr, rho = SIG * (rb - rr) / Math.sqrt(f * (1 - f));
        var bias = rho * Math.sqrt((1 - f) / f) * SIG, sdSrs = SIG * Math.sqrt((1 - n / N) / n);
        var mail = [], srs = [];
        for (i = 0; i < REPS; i++) {
          var nb = Math.max(1, Math.round(N * P * rb + Math.sqrt(N * P * rb * (1 - rb)) * r.normal()));
          var nr = Math.max(1, Math.round(N * (1 - P) * rr + Math.sqrt(N * (1 - P) * rr * (1 - rr)) * r.normal()));
          mail.push(100 * nb / (nb + nr));
          srs.push(100 * Math.max(0, Math.min(1, P + sdSrs * r.normal())));
        }
        var mse = bias * bias + P * (1 - P) * (1 - f) / (f * N), neff = Math.min(f * N, SIG * SIG / mse);
        s.out = { f: f, rho: rho, bias: bias, sd: sdSrs, neff: neff, returns: f * N };
        var lo = 0, hi = 100, nbins = 100, mids = QB.linspace(lo + 0.5, hi - 0.5, nbins);
        var norm = function (h) { var mx = Math.max.apply(null, h); return h.map(function (c) { return mx > 0 ? c / mx : 0; }); };
        var a = g[0].axes({ x: [lo, hi], y: [0, 1.25], noY: true, title: "300 repeats of each survey", xlabel: "estimate of Blue's share (%)" });
        a.bars(mids, norm(QB.hist(srs, lo, hi, nbins)), 1, { color: C.spot, alpha: 0.8 });
        a.bars(mids, norm(QB.hist(mail, lo, hi, nbins)), 1, { color: C.loss, alpha: 0.8 });
        a.vline(100 * P, { color: C.gain, dash: [], width: 1.5 });
        a.legend([["random sample of " + n, C.spot], ["the " + Math.round(f * N) + " returned ballots", C.loss], ["truth 38.2%", C.gain]], { pos: P + bias > 0.55 ? "tl" : "tr" });
        var fs = [], k; for (k = 0; k <= 120; k++) fs.push(Math.min(1, 0.001 * Math.pow(1000, k / 120)));
        var floor = function (e) { return Math.max(0.011, 100 * Math.abs(e)); };
        var b = g[1].axes({ x: [100, N], y: [0.01, 100], logx: true, logy: true, title: "Root mean squared error against sample size", xlabel: "sample size (log scale)",
          yfmt: function (t) { return t >= 1 ? String(t) : String(+t.toPrecision(1)); }, xfmt: function (t) { return t >= 1000 ? t / 1000 + "k" : String(t); } });
        b.line(fs.map(function (q) { return q * N; }), fs.map(function (q) { return floor(SIG * Math.sqrt((1 - q) / (q * N))); }), { color: C.spot });
        var ratio = rb / rr, fixedRatio = function (q) { // the error when q of the island answers, at the same ratio of return rates
          var red = q / (P * ratio + 1 - P), blue = ratio * red;
          if (blue > 1) { blue = 1; red = (q - P) / (1 - P); } else if (red > 1) { red = 1; blue = (q - (1 - P)) / P; }
          return P * blue / q - P;
        };
        b.line(fs.map(function (q) { return q * N; }), fs.map(function (q) { var e = fixedRatio(q); return floor(Math.sqrt(e * e + P * (1 - P) * (1 - q) / (q * N))); }), { color: C.loss });
        b.dots([n], [floor(sdSrs)], { color: C.spot, r: 5 });
        b.dots([f * N], [floor(Math.sqrt(mse))], { color: C.loss, r: 5 });
        b.legend([["returned ballots, same ratio of rates", C.loss], ["random sample", C.spot]], { pos: "bl" });
        b.text(100, 100, "points", { color: C.muted, dx: 4, dy: 9 });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["ballots returned", String(Math.round(o.returns))], ["correlation ρ of answering with voting Blue", fmt(o.rho, 4)],
          ["error of the returns", fmt(100 * o.bias, 1) + " points"], ["sd of the random sample", fmt(100 * o.sd, 1) + " points"],
          ["the returns are worth a random sample of", String(Math.max(1, Math.round(o.neff)))]];
      },
      note: "Simulated data (normal approximations to the counts). Meng's identity: error = ρ × √((1 − f)/f) × σ, with f the share of the population that answered and σ = 0.486. A random sample's error shrinks like 1/√n. The red curve keeps the ratio of the two return rates and varies how many ballots come back: the error stays where it is until nearly everyone of one colour has answered. The last readout is the size of the simple random sample with the same mean squared error.",
    });
  };

  // ---- Part 19: k nearest neighbours, training error against test error ------------------------------------------
  W.knntradeoff = function (el) {
    var KMAX = 40, G = 200;
    var truth = function (x) { return Math.sin(2 * Math.PI * x) + x / 2; };
    QB.widget(el, {
      title: "How many neighbours? Bias, variance and the two errors",
      sub: "Points scatter around the curve sin 2πx + x/2. The gold line predicts at each x by averaging the k nearest points. With k = 1 it passes through every point: training error zero, test error high. Raise k and it smooths, then flattens and misses the curve.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Neighbours k", min: 1, max: KMAX, step: 1, value: 8, fmt: function (x) { return String(x); } },
        { k: "n", label: "Training points n", min: 40, max: 200, step: 10, value: 100, fmt: function (x) { return String(x); } },
        { k: "sd", label: "Noise sd", min: 0.1, max: 0.8, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New training set", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, r = QB.rng(191 + 17 * s.seed), i, j, pts = [];
        for (i = 0; i < n; i++) { var x = r(); pts.push([x, truth(x) + v.sd * r.normal()]); }
        pts.sort(function (a, b) { return a[0] - b[0]; });
        var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
        // the running mean of the j nearest points to x0, for j = 1..KMAX, by widening a window around x0
        var sweep = function (x0, each) {
          var hi = 0; while (hi < n && xs[hi] < x0) hi++;
          var lo = hi - 1, sum = 0;
          for (j = 1; j <= KMAX; j++) {
            if (hi >= n || (lo >= 0 && x0 - xs[lo] <= xs[hi] - x0)) { sum += ys[lo]; lo--; } else { sum += ys[hi]; hi++; }
            each(j, sum / j);
          }
        };
        var test = new Array(KMAX + 1).fill(0), train = new Array(KMAX + 1).fill(0), gx = QB.linspace(0, 1, G), fit = [];
        for (i = 0; i < G; i++) {
          var f0 = truth(gx[i]);
          sweep(gx[i], function (k, m) { test[k] += (m - f0) * (m - f0) / G; if (k === v.k) fit.push(m); });
        }
        for (i = 0; i < n; i++) sweep(xs[i], function (k, m) { train[k] += (m - ys[i]) * (m - ys[i]) / n; });
        var ks = [], te = [], tr = [], best = 1, s2 = v.sd * v.sd;
        for (j = 1; j <= KMAX; j++) { ks.push(j); te.push(test[j] + s2); tr.push(train[j]); if (test[j] < test[best]) best = j; }
        s.out = { train: train[v.k], test: test[v.k] + s2, best: best, bestErr: test[best] + s2, s2: s2 };
        var a = g[0].axes({ x: [0, 1], y: [-2.2, 2.6], title: "The " + v.k + "-nearest-neighbour fit", xlabel: "x" });
        a.dots(xs, ys, { color: C.spot, r: 2.2, alpha: 0.7 });
        a.line(gx, gx.map(truth), { color: C.gain, dash: [5, 4], width: 1.6 });
        a.line(gx, fit, { color: C.idea, width: 2 });
        a.legend([["k-NN fit", C.idea], ["truth", C.gain], ["training points", C.spot]], { pos: "bl" });
        var top = 1.3 * Math.max(1.4 * s2, Math.min(Math.max.apply(null, te), 4 * s2 + 0.3));
        var b = g[1].axes({ x: [0, KMAX + 1], y: [0, top], title: "Mean squared error against k", xlabel: "k (flexible on the left, stiff on the right)" });
        b.hline(s2, { color: C.muted });
        b.text(KMAX + 1, s2, "noise σ²", { color: C.muted, align: "right", dx: -4, dy: -9 });
        b.line(ks, tr, { color: C.spot });
        b.line(ks, te, { color: C.loss });
        b.vline(v.k, { color: C.idea, dash: [], width: 1.5 });
        b.dots([v.k, v.k], [train[v.k], test[v.k] + s2], { color: C.idea, r: 4 });
        b.legend([["test error", C.loss], ["training error", C.spot]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["training error", fmt(o.train, 3)], ["test error", fmt(o.test, 3)], ["noise variance", fmt(o.s2, 3)],
          ["best k for this training set", String(o.best)], ["test error at the best k", fmt(o.bestErr, 3)]];
      },
      note: "Simulated data: x uniform on [0, 1], Gaussian noise. Test error is the noise variance plus the squared distance between the fit and the truth, averaged over a fine grid of new x. It is noise + bias² + variance: small k has high variance, large k high bias, and training error is no guide to either.",
    });
  };

  // ---- Part 20: one day's recall against usual intake (attenuation) -----------------------------------------------
  W.saltrecall = function (el) {
    var BETA = 1.5, MEAN = 3.4, SL = 0.22, VX = MEAN * MEAN * (Math.exp(SL * SL) - 1), EX2 = VX + MEAN * MEAN;
    var lambda = function (cv, k) { return VX / (VX + EX2 * (Math.exp(cv * cv) - 1) / k); };
    QB.widget(el, {
      title: "Salt and blood pressure: what a noisy diet record does to a slope",
      sub: "In this simulated population each gram of usual sodium raises systolic pressure by 1.5 mm Hg. The survey does not see usual intake: it records what people ate on k days. Raise the day-to-day variation and the fitted slope sinks toward zero; average more days and it climbs back.",
      panels: 2, height: 300,
      controls: [
        { k: "cv", label: "Day-to-day variation of one recall", min: 0, max: 0.8, step: 0.05, value: 0.4, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "k", label: "Recall days averaged", min: 1, max: 14, step: 1, value: 1, fmt: function (x) { return String(x); } },
        { k: "n", label: "People surveyed", min: 100, max: 3000, step: 100, value: 500, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New survey", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, r = QB.rng(739 + 19 * s.seed), i, j, ws = [], ys = [];
        for (i = 0; i < n; i++) {
          var x = MEAN * Math.exp(-SL * SL / 2 + SL * r.normal()), y = 120 + BETA * (x - MEAN) + 12 * r.normal(), w = 0;
          for (j = 0; j < v.k; j++) w += x * Math.exp(-v.cv * v.cv / 2 + v.cv * r.normal());
          ws.push(w / v.k); ys.push(y);
        }
        var mw = QB.mean(ws), my = QB.mean(ys), sxx = 0, sxy = 0, rss = 0;
        for (i = 0; i < n; i++) { sxx += (ws[i] - mw) * (ws[i] - mw); sxy += (ws[i] - mw) * (ys[i] - my); }
        var b = sxx > 0 ? sxy / sxx : 0, a0 = my - b * mw;
        for (i = 0; i < n; i++) { var e = ys[i] - a0 - b * ws[i]; rss += e * e; }
        var se = sxx > 0 ? Math.sqrt(rss / (n - 2) / sxx) : 0, lam = lambda(v.cv, v.k);
        s.out = { b: b, se: se, lam: lam };
        var show = Math.min(n, 600), A = g[0].axes({ x: [0, 10], y: [80, 165], title: "Pressure against recorded sodium", xlabel: "recorded sodium, mean of " + v.k + (v.k > 1 ? " days" : " day") + " (g)" });
        A.dots(ws.slice(0, show), ys.slice(0, show), { color: C.spot, r: 2, alpha: 0.55 });
        A.line([0, 10], [120 + BETA * (0 - MEAN), 120 + BETA * (10 - MEAN)], { color: C.gain, dash: [5, 4], width: 1.6 });
        A.line([0, 10], [a0, a0 + 10 * b], { color: C.idea, width: 2.2 });
        A.legend([["fitted line", C.idea], ["true effect: 1.5 per g", C.gain]], { pos: "tl" });
        A.text(0, 80, "mm Hg", { color: C.muted, dx: 4, dy: -9 });
        var days = [], exp = []; for (j = 1; j <= 14; j++) { days.push(j); exp.push(BETA * lambda(v.cv, j)); }
        var B = g[1].axes({ x: [0, 15], y: [-1, 2.6], title: "Slope against recall days", xlabel: "recall days averaged, k" });
        B.hline(0, { color: C.muted, dash: [] });
        B.hline(BETA, { color: C.gain, dash: [5, 4], width: 1.6 });
        B.line(days, exp, { color: C.loss });
        B.dots(days, exp, { color: C.loss, r: 2.5 });
        B.line([v.k, v.k], [b - 1.96 * se, b + 1.96 * se], { color: C.idea, width: 2 });
        B.dots([v.k], [b], { color: C.idea, r: 5 });
        B.legend([["true effect", C.gain], ["expected slope λ × 1.5", C.loss], ["this survey, with its 95% interval", C.idea]], { pos: "br" });
      },
      readout: function (v, s) {
        var o = s.out, lo = o.b - 1.96 * o.se, hi = o.b + 1.96 * o.se;
        return [["share of the slope kept, λ", fmt(o.lam, 2)], ["expected slope", fmt(BETA * o.lam, 2)], ["fitted slope", fmt(o.b, 2)],
          ["95% interval", "[" + fmt(lo, 2) + ", " + fmt(hi, 2) + "]"], ["interval contains 1.5", lo <= BETA && BETA <= hi ? "yes" : "no"]];
      },
      note: "Simulated data: usual intake averages 3.4 g; each recall is usual intake times an independent day-to-day factor with mean one; pressure has person-level noise of sd 12 mm Hg. The slope on a noisy exposure tends to λ × 1.5, with λ = Var(usual) / (Var(usual) + Var(day error)/k). Surveying more people narrows the interval around the wrong number; only better measurement moves it.",
    });
  };
})();
