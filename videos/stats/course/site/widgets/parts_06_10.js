// Interactives for Stage I, Bachelor's: Foundations (Parts 6-10).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- shared numbers ----------------------------------------------------------------------------------------
  var T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131,
    2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045];
  function t975(df) { // the 97.5% point of Student's t: the table to 29 df, Cornish-Fisher beyond
    if (df <= 29) return T975[Math.max(1, Math.round(df)) - 1];
    var z = 1.959964;
    return z + (z * z * z + z) / (4 * df) + (5 * Math.pow(z, 5) + 16 * z * z * z + 3 * z) / (96 * df * df);
  }
  function lgamma(x) { // Lanczos, x > 0
    var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
    var y = x, t = x + 5.5, s = 1.000000000190015;
    t -= (x + 0.5) * Math.log(t);
    for (var j = 0; j < 6; j++) { y += 1; s += c[j] / y; }
    return -t + Math.log(2.5066282746310005 * s / x);
  }
  function tpdf(x, df) {
    return Math.exp(lgamma((df + 1) / 2) - lgamma(df / 2) - 0.5 * Math.log(df * Math.PI) - (df + 1) / 2 * Math.log(1 + x * x / df));
  }

  // ---- Part 6: is thirty enough? -----------------------------------------------------------------------------
  W.thirtyenough = function (el) {
    QB.widget(el, {
      title: "Is thirty enough? The bell's speed depends on the skew",
      sub: "Samples of n are drawn from the population on the left, and each mean is standardized by its own standard error. With no skew the histogram sits on Student's t curve and the 95% interval keeps its promise at every n. Raise the skew and see how large n must be before it does again, and on which side the misses fall.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Sample size n", min: 2, max: 200, step: 1, value: 30 },
        { k: "s", label: "Skew of the population (σ of its log)", min: 0, max: 1.5, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New samples", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 600), n = v.n, sg = v.s, flat = sg < 0.01, i, k;
        var mu = flat ? 0 : (Math.exp(sg * sg / 2) - 1) / sg;
        var e2 = Math.exp(sg * sg), skew = flat ? 0 : (e2 + 2) * Math.sqrt(e2 - 1);
        var R = Math.max(500, Math.min(2000, Math.floor(100000 / n))), mult = t975(n - 1);
        var T = [], cover = 0, low = 0, high = 0;
        for (i = 0; i < R; i++) {
          var sum = 0, sq = 0;
          for (k = 0; k < n; k++) { var z = r.normal(), x = flat ? z : (Math.exp(sg * z) - 1) / sg; sum += x; sq += x * x; }
          var m = sum / n, se = Math.sqrt(Math.max(1e-12, (sq - n * m * m) / (n - 1)) / n), t = (m - mu) / se;
          T.push(t);
          if (t < -mult) low++; else if (t > mult) high++; else cover++;
        }
        s.out = [skew, skew / Math.sqrt(n), cover / R, low / R, high / R];
        // the population
        var xs = QB.linspace(-2.5, 6, 240), ys = xs.map(function (x) {
          if (flat) return QB.pdf(x);
          var u = 1 + sg * x; if (u <= 0) return 0;
          return QB.pdf(Math.log(u) / sg) / u;
        });
        var top = 0; for (i = 0; i < ys.length; i++) top = Math.max(top, ys[i]);
        var a = g[0].axes({ x: [-2.5, 6], y: [0, top * 1.25], title: "The population", xlabel: "one observation" });
        a.area(xs, ys, 0, { color: C.spot, alpha: 0.22 }).line(xs, ys, { color: C.spot });
        a.vline(mu, { color: C.idea, dash: [] });
        a.legend([["density", C.spot], ["its mean", C.idea]], { pos: "tr" });
        // the standardized means
        var nb = 40, h = QB.hist(T, -5, 5, nb), w = 10 / nb, mids = [], dens = [];
        for (i = 0; i < nb; i++) { mids.push(-5 + (i + 0.5) * w); dens.push(h[i] / (R * w)); }
        var b = g[1].axes({ x: [-5, 5], y: [0, 0.6], title: "Standardized means of n", xlabel: "(mean − true mean) / standard error" });
        b.bars(mids, dens, w, { color: function (j) { return Math.abs(mids[j]) > mult ? C.loss : C.spot; }, alpha: 0.75 });
        var zs = QB.linspace(-5, 5, 160);
        b.line(zs, zs.map(function (x) { return tpdf(x, n - 1); }), { color: C.idea, width: 2 });
        b.vline(-mult, { color: C.muted }).vline(mult, { color: C.muted });
        b.legend([["simulated", C.spot], ["outside the 95% interval", C.loss], ["Student's t, n − 1 df", C.idea]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["population skewness", fmt(s.out[0], 2)], ["skewness / √n", fmt(s.out[1], 2)], ["95% interval covers", pct(s.out[2])],
          ["true mean above the interval", pct(s.out[3])], ["below it", pct(s.out[4])]];
      },
      note: "Simulated data: the population is (exp(σZ) − 1)/σ with Z standard normal, a shifted lognormal that becomes the normal at σ = 0. The interval is mean ± t × s/√n with Student's multiplier. A bar left of the grey lines is a sample whose interval lies wholly below the true mean.",
    });
  };

  // ---- Part 7: RANDU's fifteen planes ------------------------------------------------------------------------
  W.randuplanes = function (el) {
    QB.widget(el, {
      title: "Random numbers fall mainly in the planes",
      sub: "Each dot is three consecutive numbers (x, y, z) from a generator, drawn inside the unit cube. Turn the cube: from most angles RANDU's dots (red) look like a uniform cloud, but near 56° with no tilt they line up on fifteen planes. Switch to a modern generator (green) and no angle does that.",
      panels: 2, height: 320,
      controls: [
        { k: "az", label: "Turn the cube (degrees)", min: 0, max: 180, step: 0.5, value: 20, fmt: function (x) { return x.toFixed(1); } },
        { k: "el", label: "Tilt (degrees)", min: -30, max: 30, step: 0.5, value: 0, fmt: function (x) { return fmt(x, 1); } },
        { k: "n", label: "Triples", min: 300, max: 4000, step: 100, value: 2000 },
      ],
      buttons: [{ label: "Switch generator", act: function (s) { s.gen = 1 - s.gen; } }, { label: "New seed", act: function (s) { s.seed++; } }],
      init: function (s) { s.gen = 0; },
      draw: function (g, v, s) {
        var n = v.n, P = [], i, j, M = 2147483648, bins = new Array(10).fill(0);
        var next;
        if (s.gen === 0) { var x = 2 * s.seed + 1; next = function () { x = (65539 * x) % M; return x / M; }; }
        else { next = QB.rng(s.seed + 700); }
        for (i = 0; i < n; i++) {
          var t = [next(), next(), next()]; P.push(t);
          for (j = 0; j < 3; j++) bins[Math.min(9, Math.floor(10 * t[j]))]++;
        }
        var chi = 0, e = 3 * n / 10; for (i = 0; i < 10; i++) chi += (bins[i] - e) * (bins[i] - e) / e;
        var th = v.az * Math.PI / 180, ph = v.el * Math.PI / 180, ct = Math.cos(th), st = Math.sin(th), cp = Math.cos(ph), sp = Math.sin(ph);
        var proj = function (p) { // orthographic: right = (-sin t, cos t, 0), up = (-cos t sin p, -sin t sin p, cos p)
          var a = p[0] - 0.5, b = p[1] - 0.5, c = p[2] - 0.5;
          return [-a * st + b * ct, -(a * ct + b * st) * sp + c * cp];
        };
        var col = s.gen === 0 ? C.loss : C.gain;
        var bw = Math.max(40, g[0].box.w - 22), bh = Math.max(40, g[0].box.h - 32), half = 0.92; // equal scales on both axes
        var ax = g[0].axes({ x: [-half * Math.max(1, bw / bh), half * Math.max(1, bw / bh)], y: [-half * Math.max(1, bh / bw), half * Math.max(1, bh / bw)], noX: true, noY: true, noFrame: true, xticks: [], yticks: [],
          title: (s.gen === 0 ? "RANDU" : "A modern generator") + ": " + n + " triples in the cube" });
        var edges = [[0, 1], [0, 2], [0, 4], [1, 3], [1, 5], [2, 3], [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]];
        for (i = 0; i < 12; i++) {
          var p0 = proj([edges[i][0] & 1, (edges[i][0] >> 1) & 1, (edges[i][0] >> 2) & 1]), p1 = proj([edges[i][1] & 1, (edges[i][1] >> 1) & 1, (edges[i][1] >> 2) & 1]);
          ax.line([p0[0], p1[0]], [p0[1], p1[1]], { color: C.muted, width: 1, alpha: 0.6 });
        }
        var X = [], Y = [], K = [], seen = {}, distinct = 0;
        for (i = 0; i < n; i++) {
          var q = proj(P[i]); X.push(q[0]); Y.push(q[1]);
          var k = 9 * P[i][0] - 6 * P[i][1] + P[i][2]; K.push(k);
          var key = Math.round(k * 1e6); if (!seen[key]) { seen[key] = 1; distinct++; }
        }
        ax.dots(X, Y, { color: col, r: 1.3, alpha: 0.85 });
        var off = Math.asin(Math.min(1, Math.abs(9 * ct * cp - 6 * st * cp + sp) / Math.sqrt(118))) * 180 / Math.PI;
        s.out = [s.gen === 0 ? "RANDU" : "modern (mulberry32)", distinct, off, chi];
        var nb = 64, w = 0.25, h = QB.hist(K, -6.125, 9.875, nb), mids = [], fr = [], top = 0; // integers at bin centres
        for (i = 0; i < nb; i++) { mids.push(-6 + i * w); fr.push(h[i] / n); top = Math.max(top, fr[i]); }
        var b = g[1].axes({ x: [-6, 10], y: [0, Math.max(0.05, top * 1.2)], title: "9x − 6y + z for every triple", xlabel: "9x − 6y + z", yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.bars(mids, fr, w, { color: col, alpha: 0.85 });
        b.legend([["RANDU: integers only", C.loss], ["modern: any value", C.gain]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["generator", s.out[0]], ["distinct values of 9x − 6y + z", String(s.out[1])], ["line of sight off the planes by", fmt(s.out[2], 1) + "°"],
          ["1-D χ² of the numbers (9 df; 5% point 16.9)", fmt(s.out[3], 1)]];
      },
      note: "RANDU is x ← 65539·x mod 2³¹ (IBM, 1960s), computed exactly here. Since 65539 = 2¹⁶ + 3, each number is 6 times the last minus 9 times the one before, modulo 2³¹, so 9x − 6y + z is an integer. The one-dimensional χ² test sees nothing wrong. A cloud without planes is not a proof of randomness.",
    });
  };

  // ---- Part 8: Student's cards -------------------------------------------------------------------------------
  W.studentcards = function (el) {
    QB.widget(el, {
      title: "Student's cards: which multiplier keeps the promise?",
      sub: "Fifty samples of n are dealt from a population, and each gives the interval mean ± 1.96 s/√n (thick) and the wider Student's interval (thin). With n = 4 the thick one misses far more often than 1 time in 20. Raise n and the two agree; raise the skew and even Student's promise, which was made for normal data, starts to slip.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Sample size n", min: 2, max: 30, step: 1, value: 4 },
        { k: "s", label: "Skew of the population (0 is normal)", min: 0, max: 1.2, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "Deal again", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 800), n = v.n, sg = v.s, flat = sg < 0.01, i, k, R = 3000, show = 50;
        var mu = flat ? 0 : (Math.exp(sg * sg / 2) - 1) / sg, mult = t975(n - 1);
        var M = [], SE = [], cz = 0, ct = 0, shownMiss = 0;
        for (i = 0; i < R; i++) {
          var sum = 0, sq = 0;
          for (k = 0; k < n; k++) { var z = r.normal(), x = flat ? z : (Math.exp(sg * z) - 1) / sg; sum += x; sq += x * x; }
          var m = sum / n, se = Math.sqrt(Math.max(0, (sq - n * m * m) / (n - 1)) / n), e = Math.abs(m - mu);
          if (e <= 1.96 * se) cz++;
          if (e <= mult * se) ct++;
          if (i < show) { M.push(m); SE.push(se); if (e > 1.96 * se) shownMiss++; }
        }
        // what normal theory says 1.96 achieves at every n: P(|t| <= 1.96) with n - 1 df, by Simpson's rule
        var ns = [], th = [];
        for (k = 2; k <= 30; k++) {
          var acc = 0, J = 120, hh = 3.92 / J;
          for (i = 0; i <= J; i++) acc += (i === 0 || i === J ? 1 : i % 2 ? 4 : 2) * tpdf(-1.96 + i * hh, k - 1);
          ns.push(k); th.push(acc * hh / 3);
        }
        s.out = [mult, cz / R, th[n - 2], ct / R, shownMiss];
        var sdPop = flat ? 1 : Math.sqrt(Math.exp(sg * sg) * (Math.exp(sg * sg) - 1)) / sg, span = 4.2 * sdPop / Math.sqrt(n) + 0.4;
        var a = g[0].axes({ x: [0, show + 1], y: [mu - span, mu + 1.75 * span], title: "Fifty samples, fifty intervals", xlabel: "sample", xticks: [10, 20, 30, 40, 50] });
        a.hline(mu, { color: C.idea, dash: [], width: 1.5 });
        for (i = 0; i < show; i++) {
          var missZ = Math.abs(M[i] - mu) > 1.96 * SE[i], missT = Math.abs(M[i] - mu) > mult * SE[i];
          a.line([i + 1, i + 1], [M[i] - mult * SE[i], M[i] + mult * SE[i]], { color: missT ? C.loss : C.muted, width: 1 });
          a.line([i + 1, i + 1], [M[i] - 1.96 * SE[i], M[i] + 1.96 * SE[i]], { color: missZ ? C.loss : C.spot, width: 3 });
        }
        a.legend([["± 1.96 s/√n, covers", C.spot], ["misses the true mean", C.loss], ["Student's interval", C.muted], ["true mean", C.idea]], { pos: "tl" });
        var b = g[1].axes({ x: [1, 31], y: [0.6, 1], title: "Coverage against n", xlabel: "sample size n", xticks: [2, 5, 10, 15, 20, 25, 30], yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.hline(0.95, { color: C.muted });
        b.line(ns, th, { color: C.spot, width: 1.6 });
        b.dots([n], [cz / R], { color: C.spot, r: 5 });
        b.dots([n], [ct / R], { color: C.gain, r: 5 });
        b.legend([["1.96: normal theory", C.spot], ["Student's t, simulated", C.gain], ["the 95% promise", C.muted]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["Student's multiplier", fmt(s.out[0], 2)], ["1.96 covers", pct(s.out[1])], ["normal theory says", pct(s.out[2])],
          ["Student's covers", pct(s.out[3])], ["thick intervals missing, of the 50 shown", String(s.out[4])]];
      },
      note: "Simulated data: 3,000 samples per setting from (exp(σZ) − 1)/σ, which is the normal at skew 0. The blue curve is exact for normal data, P(|t| ≤ 1.96) with n − 1 degrees of freedom; the dots are the simulated coverage at the chosen n (blue for 1.96, green for Student's).",
    });
  };

  // ---- Part 9: the German tank problem -----------------------------------------------------------------------
  W.tankserials = function (el) {
    var COL = [C.spot, C.loss, C.idea, C.gain], NAME = ["2x̄ − 1", "max", "max + gap", "range"];
    function recipes(x, k) { // x: the captured serials
      var sum = 0, mx = -Infinity, mn = Infinity;
      for (var i = 0; i < k; i++) { sum += x[i]; if (x[i] > mx) mx = x[i]; if (x[i] < mn) mn = x[i]; }
      return [2 * sum / k - 1, mx, mx * (1 + 1 / k) - 1, (mx - mn) * (k + 1) / (k - 1) - 1];
    }
    function capture(r, N, k, first) { // k distinct serials from first .. first + N - 1
      var seen = {}, out = [];
      while (out.length < k) { var j = Math.floor(r() * N); if (!seen[j]) { seen[j] = 1; out.push(first + j); } }
      return out;
    }
    QB.widget(el, {
      title: "The tank factory game: four recipes for N",
      sub: "A factory has built N tanks, numbered in sequence, and k are captured at random (white ticks). Four recipes turn the serials into an estimate of N. With numbering from 1, the maximum plus the average gap wins. Now move the first serial away from 1: every recipe that assumed it is thrown off, and only the range recipe still works.",
      panels: 2, height: 300,
      controls: [
        { k: "N", label: "Tanks built N", min: 100, max: 1000, step: 10, value: 300 },
        { k: "k", label: "Tanks captured k", min: 2, max: 20, step: 1, value: 6 },
        { k: "first", label: "First serial number", min: 1, max: 201, step: 10, value: 1 },
      ],
      buttons: [{ label: "Capture again", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = v.N, k = v.k, first = v.first, r = QB.rng(s.seed + 900), i, j, R = 1500;
        var x = capture(r, N, k, first), e = recipes(x, k), sq = [0, 0, 0, 0];
        for (i = 0; i < R; i++) { var q = recipes(capture(r, N, k, first), k); for (j = 0; j < 4; j++) sq[j] += (q[j] - N) * (q[j] - N); }
        var rmse = sq.map(function (t) { return Math.sqrt(t / R); });
        var exact = Math.sqrt((N - k) * (N + 1) / (k * (k + 2)));
        s.out = [e, rmse, exact];
        var xmax = 1.7 * N + 2.2 * first;
        var a = g[0].axes({ x: [0, xmax], y: [-0.8, 5.7], yticks: [], noY: true, title: "One capture and the four estimates", xlabel: "serial number, or estimate of N" });
        a.vline(N, { color: C.ink, dash: [], width: 1.5 });
        a.text(N, -0.42, "N = " + N, { color: C.ink, dx: 5, size: 11.5 });
        for (i = 0; i < k; i++) a.line([x[i], x[i]], [4.05, 4.75], { color: C.ink, width: 2 });
        a.text(0, 5.2, "captured serials", { color: C.muted, dx: 5, size: 11 });
        for (j = 0; j < 4; j++) {
          var ex = Math.max(0, Math.min(xmax, e[j]));
          a.line([0, ex], [3 - j, 3 - j], { color: COL[j], width: 1, alpha: 0.5 });
          a.dots([ex], [3 - j], { color: COL[j], r: 5 });
          a.text(0, 3 - j, NAME[j] + ": " + Math.round(e[j]), { color: COL[j], dx: 5, dy: -10, size: 11.5 });
        }
        var top = Math.max(rmse[0], rmse[1], rmse[2], rmse[3], 1) * 1.45;
        var b = g[1].axes({ x: [0.3, 4.7], y: [0, top], title: "RMSE over " + R + " captures", xticks: [1, 2, 3, 4], xfmt: function (t) { return NAME[t - 1]; }, xlabel: "recipe" });
        b.bars([1, 2, 3, 4], rmse, 0.62, { color: function (t) { return COL[t]; } });
        for (j = 0; j < 4; j++) b.text(j + 1, rmse[j], Math.round(rmse[j]) + "", { align: "center", dy: -9, size: 11.5 });
        b.hline(exact, { color: C.muted });
        b.legend([["exact SD of max + gap, start at 1", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["2x̄ − 1", String(Math.round(s.out[0][0]))], ["max (MLE)", String(Math.round(s.out[0][1]))], ["max + average gap", String(Math.round(s.out[0][2]))],
          ["range recipe", String(Math.round(s.out[0][3]))], ["RMSE of max + gap", fmt(s.out[1][2], 1)], ["exact SD when serials start at 1", fmt(s.out[2], 1)]];
      },
      note: "Simulated captures, uniform without replacement. The recipes: 2x̄ − 1 (moments), the maximum m (maximum likelihood), m(1 + 1/k) − 1 (the best unbiased estimator when numbering starts at 1) and (m − smallest)(k + 1)/(k − 1) − 1, which never assumes where numbering starts. The dashed line is √((N − k)(N + 1)/(k(k + 2))).",
    });
  };

  // ---- Part 10: the peeking problem --------------------------------------------------------------------------
  W.peekpaths = function (el) {
    QB.widget(el, {
      title: "Peeking: a 5% test, checked again and again",
      sub: "Each line is the t statistic of one experiment as its data arrive; the white curves are the 5% critical values. With no true effect every crossing is a false alarm. An experimenter who tests from the 10th observation on and stops at the first crossing is wrong far more often than 1 time in 20. Give her more patience, or let her look less often, and watch the rate.",
      panels: 2, height: 300,
      controls: [
        { k: "nmax", label: "Patience: the largest sample size", min: 20, max: 500, step: 10, value: 100 },
        { k: "every", label: "Look after every … observations", min: 1, max: 50, step: 1, value: 1 },
        { k: "delta", label: "True effect (in standard deviations)", min: 0, max: 0.5, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New experiments", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1000), N = v.nmax, R = 400, show = 24, i, n, first = 10;
        var crit = [0, 0]; for (n = 2; n <= N; n++) crit.push(t975(n - 1));
        var stopAt = new Array(N + 1).fill(0), endHits = 0, paths = [], stops = [];
        for (i = 0; i < R; i++) {
          var sum = 0, sq = 0, stop = 0, path = i < show ? [] : null, t = 0;
          for (n = 1; n <= N; n++) {
            var x = v.delta + r.normal(); sum += x; sq += x * x;
            if (n >= 2) { var va = Math.max(1e-12, (sq - sum * sum / n) / (n - 1)); t = (sum / n) / Math.sqrt(va / n); }
            if (path) path.push(n >= 5 ? t : null);
            if (!stop && n >= first && (n - first) % v.every === 0 && Math.abs(t) > crit[n]) stop = n;
          }
          if (Math.abs(t) > crit[N]) endHits++;
          if (stop) stopAt[stop]++;
          if (path) { paths.push(path); stops.push(stop); }
        }
        var ns = [], ever = [], acc = 0, looks = Math.floor((N - first) / v.every) + 1;
        for (n = first; n <= N; n++) { acc += stopAt[n]; ns.push(n); ever.push(acc / R); }
        s.out = [acc / R, endHits / R, looks];
        var xs = []; for (n = 1; n <= N; n++) xs.push(n);
        var a = g[0].axes({ x: [0, N], y: [-5, 5], title: show + " of the " + R + " experiments", xlabel: "observations so far" });
        for (i = 0; i < paths.length; i++) a.line(xs, paths[i], { color: stops[i] ? C.loss : C.spot, width: stops[i] ? 1.3 : 1, alpha: stops[i] ? 0.9 : 0.45 });
        var cx = xs.slice(first - 1), cu = cx.map(function (k) { return crit[k]; }), cl = cu.map(function (c) { return -c; });
        a.line(cx, cu, { color: C.ink, width: 1.4 }).line(cx, cl, { color: C.ink, width: 1.4 });
        for (i = 0; i < paths.length; i++) if (stops[i]) a.dots([stops[i]], [paths[i][stops[i] - 1]], { color: C.idea, r: 3.5 });
        a.legend([["stopped at a crossing", C.loss], ["never significant at a look", C.spot], ["first crossing", C.idea]], { pos: "bl" });
        var top = Math.max(0.3, Math.min(1, ever[ever.length - 1] * 1.3 + 0.05));
        var b = g[1].axes({ x: [0, 1.04 * N], y: [0, top], title: "Declared significant by n", xlabel: "largest sample size n", yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.hline(0.05, { color: C.muted });
        b.line(ns, ever, { color: C.loss, width: 2 });
        b.dots([N], [endHits / R], { color: C.spot, r: 5 });
        b.legend([["stopping at the first p < 0.05", C.loss], ["one test at the end", C.spot], ["the 5% promise", C.muted]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["looks at the data", String(s.out[2])], ["significant at some look", pct(s.out[0])], ["significant in one test at the end", pct(s.out[1])],
          [v.delta === 0 ? "every rejection here is" : "rejections here are", v.delta === 0 ? "a false alarm" : "power, not error"]];
      },
      note: "Simulated data: 400 experiments of normal observations with unit standard deviation, a two-sided one-sample t-test of mean 0 at the 5% level, first look at the 10th observation. With 400 experiments each rate has a Monte Carlo error of about 2 points. With a true effect the same habit inflates the reported effect sizes instead.",
    });
  };
})();
