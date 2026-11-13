// Interactives for Act II, Learning from Data (Parts 6-10).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function solve(A, b) { // Gaussian elimination with partial pivoting on copies; a singular pivot is nudged, never divided by
    var n = b.length, M = [], i, j, k, t;
    for (i = 0; i < n; i++) { M.push(A[i].slice()); M[i].push(b[i]); }
    for (k = 0; k < n; k++) {
      var best = k;
      for (i = k + 1; i < n; i++) if (Math.abs(M[i][k]) > Math.abs(M[best][k])) best = i;
      t = M[k]; M[k] = M[best]; M[best] = t;
      if (Math.abs(M[k][k]) < 1e-12) M[k][k] = M[k][k] < 0 ? -1e-12 : 1e-12;
      for (i = k + 1; i < n; i++) {
        var f = M[i][k] / M[k][k];
        if (f !== 0) for (j = k; j <= n; j++) M[i][j] -= f * M[k][j];
      }
    }
    var x = new Array(n);
    for (i = n - 1; i >= 0; i--) { t = M[i][n]; for (j = i + 1; j < n; j++) t -= M[i][j] * x[j]; x[i] = t / M[i][i]; }
    return x;
  }

  // ---- Part 6: ridge shrinks, the lasso selects -------------------------------------------------------------
  W.ridgelassopath = function (el) {
    var P = 8, N = 60, TRUE = [3, -2, 1.5, 0, 0, 0, 0, 0], LO = -3, HI = 1.5, STEPS = 46;
    var soft = function (z, l) { return z > l ? z - l : z < -l ? z + l : 0; };
    var lasso = function (G, c, lam, w, sweeps) { // coordinate descent on (1/2n)|y - Zw|^2 + lam |w|_1, in place
      for (var s = 0; s < sweeps; s++) for (var j = 0; j < P; j++) {
        var r = c[j];
        for (var k = 0; k < P; k++) if (k !== j) r -= G[j][k] * w[k];
        w[j] = soft(r, lam) / G[j][j];
      }
      return w;
    };
    var ridge = function (G, c, lam) {
      var A = G.map(function (row, i) { var r = row.slice(); r[i] += lam; return r; });
      return solve(A, c);
    };
    var build = function (v, s) { // the data, its Gram matrix, and both paths; cached until a slider that changes the data moves
      var key = [s.seed, v.corr, v.noise].join("|");
      if (s.key === key) return s.d;
      var r = QB.rng(s.seed + 600), Z = [], y = [], i, j, k;
      for (i = 0; i < N; i++) {
        var common = r.normal(), row = [], t = 0;
        for (j = 0; j < P; j++) { row.push(Math.sqrt(1 - v.corr) * r.normal() + Math.sqrt(v.corr) * common); t += TRUE[j] * row[j]; }
        Z.push(row); y.push(t + v.noise * r.normal());
      }
      var my = QB.mean(y);
      for (j = 0; j < P; j++) {
        var col = Z.map(function (rw) { return rw[j]; }), m = QB.mean(col), sd = Math.max(1e-9, QB.sd(col) * Math.sqrt((N - 1) / N));
        for (i = 0; i < N; i++) Z[i][j] = (Z[i][j] - m) / sd;
      }
      var G = [], c = [];
      for (j = 0; j < P; j++) {
        G.push([]); t = 0;
        for (i = 0; i < N; i++) t += Z[i][j] * (y[i] - my);
        c.push(t / N);
        for (k = 0; k < P; k++) { t = 0; for (i = 0; i < N; i++) t += Z[i][j] * Z[i][k]; G[j].push(t / N); }
      }
      var ls = QB.linspace(LO, HI, STEPS), lp = [], rp = [], w = new Array(P).fill(0);
      for (j = 0; j < P; j++) { lp.push(new Array(STEPS)); rp.push(new Array(STEPS)); }
      for (i = STEPS - 1; i >= 0; i--) { // warm starts, from the largest penalty down
        lasso(G, c, Math.pow(10, ls[i]), w, 60);
        var rr = ridge(G, c, Math.pow(10, ls[i]));
        for (j = 0; j < P; j++) { lp[j][i] = w[j]; rp[j][i] = rr[j]; }
      }
      s.key = key; s.d = { G: G, c: c, ls: ls, lp: lp, rp: rp, lmax: Math.max.apply(null, c.map(Math.abs)) };
      return s.d;
    };
    QB.widget(el, {
      title: "Ridge shrinks, the lasso selects",
      sub: "Sixty simulated examples, eight standardized features; only three of them (gold) matter. Each curve is one weight as the penalty grows. Slide the penalty: the lasso's weights reach exactly zero one after another, ridge's only get small. Then raise the correlation and watch the lasso's choices become unstable.",
      panels: 2, height: 300,
      controls: [
        { k: "lam", label: "Penalty λ", min: LO, max: HI, step: 0.05, value: -0.7, fmt: function (x) { return Math.pow(10, x).toPrecision(2); } },
        { k: "corr", label: "Correlation between features", min: 0, max: 0.95, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "noise", label: "Noise sd", min: 0.2, max: 4, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var d = build(v, s), lam = Math.pow(10, v.lam), j, i;
        var wl = lasso(d.G, d.c, lam, new Array(P).fill(0), 400), wr = ridge(d.G, d.c, lam);
        var nz = 0, noiseNz = 0, eff = 0, minr = Infinity;
        for (j = 0; j < P; j++) {
          if (wl[j] !== 0) { nz++; if (TRUE[j] === 0) noiseNz++; }
          minr = Math.min(minr, Math.abs(wr[j]));
          var e = new Array(P).fill(0); e[j] = 1;
          var col = solve(d.G.map(function (row, a) { var q = row.slice(); q[a] += lam; return q; }), e);
          for (i = 0; i < P; i++) eff += d.G[j][i] * col[i]; // trace of G (G + lam I)^-1
        }
        s.out = [nz, noiseNz, eff, minr, d.lmax];
        var col2 = function (k) { return TRUE[k] !== 0 ? C.idea : C.spot; };
        var xf = function (x) { return x === Math.round(x) ? (x >= 0 ? String(Math.pow(10, x)) : "1e" + x).replace("-", "−") : ""; };
        var ylo = -3.4, yhi = 4.4; // the frame grows with the paths when noise and correlation make the weights large
        d.lp.concat(d.rp).forEach(function (path) { for (var q = 0; q < path.length; q++) { ylo = Math.min(ylo, 1.06 * path[q]); yhi = Math.max(yhi, 1.06 * path[q]); } });
        var opts = function (title) { return { x: [LO, HI], y: [ylo, yhi], title: title, xlabel: "penalty λ (log scale)", xticks: [-3, -2, -1, 0, 1], xfmt: xf }; };
        var a = g[0].axes(opts("Lasso: " + nz + " of 8 weights are not zero"));
        var b = g[1].axes(opts("Ridge: all 8 weights stay"));
        [[a, d.lp], [b, d.rp]].forEach(function (pair) {
          pair[0].hline(0, { color: C.muted });
          for (j = P - 1; j >= 0; j--) pair[0].line(d.ls, pair[1][j], { color: col2(j), width: TRUE[j] !== 0 ? 2 : 1.2, alpha: TRUE[j] !== 0 ? 1 : 0.8 });
          pair[0].vline(v.lam, { color: C.ink });
        });
        a.dots(new Array(P).fill(v.lam), wl, { color: col2, r: 3.2 });
        b.dots(new Array(P).fill(v.lam), wr, { color: col2, r: 3.2 });
        a.legend([["the 3 features that matter", C.idea], ["the 5 that do not", C.spot]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["lasso keeps", s.out[0] + " of 8"], ["of them useless", String(s.out[1])], ["lasso is all zero from λ =", fmt(s.out[4], 2)],
          ["ridge effective weights", fmt(s.out[2], 2)], ["ridge's smallest |weight|", fmt(s.out[3], 3)]];
      },
      note: "Simulated data: y = 3x₁ − 2x₂ + 1.5x₃ + noise. Lasso by coordinate descent on (1/2n)|y − Zw|² + λ|w|₁, ridge in closed form on (1/2n)|y − Zw|² + (λ/2)|w|². Ridge's effective number of weights is Σ d²/(d² + nλ) over the singular values d of Z.",
    });
  };

  // ---- Part 7: a Gaussian process, its length scale and the evidence ----------------------------------------
  W.gplengthscale = function (el) {
    var NMAX = 25, TRUE_NOISE = 0.25, GRID = QB.linspace(0, 10, 81), ELLS = QB.linspace(-1, 1, 41);
    var truth = function (x) { return Math.sin(1.1 * x) + 0.5 * Math.sin(2.7 * x + 1); };
    var kern = function (a, b, ell) { var d = (a - b) / ell; return Math.exp(-0.5 * d * d); };
    var chol = function (K) { // lower-triangular L with L L' = K; a non-positive pivot is floored
      var n = K.length, L = [], i, j, k, t;
      for (i = 0; i < n; i++) {
        L.push(new Array(n).fill(0));
        for (j = 0; j <= i; j++) {
          t = K[i][j];
          for (k = 0; k < j; k++) t -= L[i][k] * L[j][k];
          L[i][j] = i === j ? Math.sqrt(Math.max(t, 1e-10)) : t / L[j][j];
        }
      }
      return L;
    };
    var fsub = function (L, b) { var n = b.length, x = new Array(n), i, k, t; for (i = 0; i < n; i++) { t = b[i]; for (k = 0; k < i; k++) t -= L[i][k] * x[k]; x[i] = t / L[i][i]; } return x; };
    var bsub = function (L, b) { var n = b.length, x = new Array(n), i, k, t; for (i = n - 1; i >= 0; i--) { t = b[i]; for (k = i + 1; k < n; k++) t -= L[k][i] * x[k]; x[i] = t / L[i][i]; } return x; };
    var fitGP = function (xs, ys, ell, noise) {
      var n = xs.length, K = [], i, j;
      for (i = 0; i < n; i++) { K.push([]); for (j = 0; j < n; j++) K[i].push(kern(xs[i], xs[j], ell) + (i === j ? noise * noise : 0)); }
      var L = chol(K), z = fsub(L, ys), fit = 0, comp = 0;
      for (i = 0; i < n; i++) { fit -= 0.5 * z[i] * z[i]; comp -= Math.log(L[i][i]); }
      return { L: L, alpha: bsub(L, z), fit: fit, comp: comp, total: fit + comp - 0.5 * n * Math.log(2 * Math.PI) };
    };
    QB.widget(el, {
      title: "A Gaussian process: the length scale and Occam's razor",
      sub: "Noisy points (gold) from a hidden curve (dashed). The white line is the posterior mean and the band is ±2 posterior standard deviations of the function. Slide the length scale: too short and the band balloons between points, too long and the mean misses them. On the right the evidence adds a data-fit term and a complexity penalty, and peaks in between.",
      panels: 2, height: 300,
      controls: [
        { k: "ell", label: "Length scale ℓ", min: -1, max: 1, step: 0.05, value: -0.6, fmt: function (x) { return Math.pow(10, x).toFixed(2); } },
        { k: "n", label: "Points observed", min: 2, max: NMAX, step: 1, value: 12 },
        { k: "noise", label: "Noise sd the model assumes", min: 0.05, max: 1, step: 0.05, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New points", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 700), xs = [], ys = [], i, j;
        for (i = 0; i < NMAX; i++) { var x = 0.3 + 9.4 * r(), e = r.normal(); if (i < v.n) { xs.push(x); ys.push(truth(x) + TRUE_NOISE * e); } }
        var ell = Math.pow(10, v.ell), m = fitGP(xs, ys, ell, v.noise), mean = [], lo = [], hi = [];
        for (j = 0; j < GRID.length; j++) {
          var ks = xs.map(function (xi) { return kern(GRID[j], xi, ell); }), mu = 0, w = fsub(m.L, ks), q = 0;
          for (i = 0; i < xs.length; i++) { mu += ks[i] * m.alpha[i]; q += w[i] * w[i]; }
          var sd = Math.sqrt(Math.max(0, 1 - q));
          mean.push(mu); lo.push(mu - 2 * sd); hi.push(mu + 2 * sd);
        }
        var fit = [], comp = [], tot = [], best = 0, ymin = Infinity, ymax = -Infinity;
        for (j = 0; j < ELLS.length; j++) {
          var f = fitGP(xs, ys, Math.pow(10, ELLS[j]), v.noise);
          fit.push(f.fit); comp.push(f.comp); tot.push(f.total);
          if (f.total > tot[best]) best = j;
          ymin = Math.min(ymin, f.fit, f.comp, f.total); ymax = Math.max(ymax, f.fit, f.comp, f.total);
        }
        ymin = Math.max(ymin, -150); // a very long length scale can miss the points by hundreds of nats: keep the peak readable
        var pad = 0.08 * Math.max(1, ymax - ymin);
        s.out = [m.total, m.fit, m.comp, Math.pow(10, ELLS[best]), -0.5 * v.n * Math.log(2 * Math.PI)];
        var a = g[0].axes({ x: [0, 10], y: [-3.2, 3.2], title: "Posterior from " + v.n + " points, ℓ = " + ell.toFixed(2), xlabel: "x" });
        a.area(GRID, hi, lo, { color: C.spot, alpha: 0.22 });
        a.line(GRID, GRID.map(truth), { color: C.muted, dash: [4, 4], width: 1.2 });
        a.line(GRID, mean, { color: C.ink, width: 2 });
        a.dots(xs, ys, { color: C.idea, r: 3.5 });
        a.legend([["mean", C.ink], ["±2 sd", C.spot], ["hidden", C.muted]], { pos: "bl" });
        var xf = function (x) { return String(+Math.pow(10, x).toPrecision(2)); };
        var b = g[1].axes({ x: [-1, 1], y: [ymin - pad - 0.36 * Math.max(1, ymax - ymin), ymax + pad], title: "Log evidence against the length scale", xlabel: "length scale ℓ (log scale)", xticks: [-1, -0.5, 0, 0.5, 1], xfmt: xf });
        b.hline(0, { color: C.muted });
        b.line(ELLS, fit, { color: C.gain, width: 1.5 }).line(ELLS, comp, { color: C.implied, width: 1.5 }).line(ELLS, tot, { color: C.idea, width: 2.4 });
        b.vline(v.ell, { color: C.ink });
        b.dots([ELLS[best]], [tot[best]], { color: C.idea, r: 4.5 });
        b.legend([["data fit", C.gain], ["complexity penalty", C.implied], ["log evidence", C.idea]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["log evidence", fmt(s.out[0], 1)], ["= data fit", fmt(s.out[1], 1)], ["+ complexity penalty", fmt(s.out[2], 1)],
          ["+ constant", fmt(s.out[4], 1)], ["evidence is highest at ℓ =", fmt(s.out[3], 2)]];
      },
      note: "Simulated data: a sum of two sines plus noise of sd 0.25. Squared-exponential kernel with unit signal variance and zero mean. Data fit is −½ yᵀ(K + σ²I)⁻¹y, the complexity penalty is −½ log det(K + σ²I), the constant is −(n/2) log 2π. The band is for the hidden function, without observation noise.",
    });
  };

  // ---- Part 8: double descent, and the singular value behind it ---------------------------------------------
  W.descentpeak = function (el) {
    var PMAX = 120, NMAX = 24, D = 6, NT = 40, DRAWS = 6;
    var feats = function (x, S, p) { // p random ReLU features of one input, scaled by 1/sqrt(p)
      var f = new Array(p), sc = 1 / Math.sqrt(p);
      for (var j = 0; j < p; j++) { var z = S.B[j]; for (var k = 0; k < D; k++) z += S.A[j][k] * x[k]; f[j] = z > 0 ? z * sc : 0; }
      return f;
    };
    var gram = function (F, n, p) { // F'F when p <= n, FF' beyond: the smaller of the two, with the same nonzero spectrum
      var G = [], a, b, k, t, m = Math.min(n, p);
      for (a = 0; a < m; a++) {
        G.push(new Array(m));
        for (b = 0; b <= a; b++) {
          t = 0;
          if (p <= n) for (k = 0; k < n; k++) t += F[k][a] * F[k][b]; else for (k = 0; k < p; k++) t += F[a][k] * F[b][k];
          G[a][b] = t; G[b][a] = t;
        }
      }
      return G;
    };
    var testError = function (S, n, p, lam, keep) { // least squares on the features; beyond p = n, the fit of smallest norm
      var F = [], i, j, t, beta, G;
      for (i = 0; i < n; i++) F.push(feats(S.x[i], S, p));
      G = gram(F, n, p);
      if (keep) keep.G = G.map(function (row) { return row.slice(); });
      for (i = 0; i < G.length; i++) G[i][i] += lam;
      if (p <= n) {
        var c = [];
        for (j = 0; j < p; j++) { t = 0; for (i = 0; i < n; i++) t += F[i][j] * S.y[i]; c.push(t); }
        beta = solve(G, c);
      } else {
        var al = solve(G, S.y.slice(0, n));
        beta = new Array(p);
        for (j = 0; j < p; j++) { t = 0; for (i = 0; i < n; i++) t += F[i][j] * al[i]; beta[j] = t; }
      }
      var e = 0;
      for (i = 0; i < NT; i++) { var f = feats(S.xt[i], S, p), o = 0; for (j = 0; j < p; j++) o += f[j] * beta[j]; e += (o - S.ft[i]) * (o - S.ft[i]); }
      e /= NT;
      return e === e && e < 1e6 ? e : 1e6;
    };
    var eigs = function (G) { // eigenvalues of a small symmetric matrix by cyclic Jacobi rotations
      var m = G.length, A = G, sweep, a, b, k;
      for (sweep = 0; sweep < 10; sweep++) for (a = 0; a < m - 1; a++) for (b = a + 1; b < m; b++) {
        if (Math.abs(A[a][b]) < 1e-14) continue;
        var th = (A[b][b] - A[a][a]) / (2 * A[a][b]), tt = (th >= 0 ? 1 : -1) / (Math.abs(th) + Math.sqrt(th * th + 1)), cs = 1 / Math.sqrt(tt * tt + 1), sn = tt * cs;
        for (k = 0; k < m; k++) { var u = A[k][a], w = A[k][b]; A[k][a] = cs * u - sn * w; A[k][b] = sn * u + cs * w; }
        for (k = 0; k < m; k++) { u = A[a][k]; w = A[b][k]; A[a][k] = cs * u - sn * w; A[b][k] = sn * u + cs * w; }
      }
      var out = []; for (a = 0; a < m; a++) out.push(A[a][a]);
      return out.sort(function (x, y) { return y - x; });
    };
    var world = function (seed, noise) { // six draws: training inputs, a linear teacher, test inputs, random features
      var sets = [], d, i, j, k;
      for (d = 0; d < DRAWS; d++) {
        var r = QB.rng(seed * 97 + d * 13 + 800), S = { x: [], y: [], xt: [], ft: [], A: [], B: [] }, beta = [], row, t;
        for (k = 0; k < D; k++) beta.push(r.normal() / Math.sqrt(D));
        for (i = 0; i < NMAX; i++) { row = []; t = 0; for (k = 0; k < D; k++) { row.push(r.normal()); t += row[k] * beta[k]; } S.x.push(row); S.y.push(t + noise * r.normal()); }
        for (i = 0; i < NT; i++) { row = []; t = 0; for (k = 0; k < D; k++) { row.push(r.normal()); t += row[k] * beta[k]; } S.xt.push(row); S.ft.push(t); }
        for (j = 0; j < PMAX; j++) { row = []; for (k = 0; k < D; k++) row.push(r.normal()); S.A.push(row); S.B.push(r.normal()); }
        sets.push(S);
      }
      return sets;
    };
    QB.widget(el, {
      title: "Double descent: the peak where the model just fits",
      sub: "A noisy linear target in six inputs is fitted by least squares on p random ReLU features; beyond p = n the fit is the interpolant of smallest norm. Slide p up to n: the smallest singular value of the feature matrix (red) falls toward zero and the test error peaks. Keep going and both recover. Then add a little ridge penalty and the peak is gone.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Features p", min: 1, max: PMAX, step: 1, value: 16 },
        { k: "n", label: "Training points n", min: 8, max: NMAX, step: 1, value: 16 },
        { k: "noise", label: "Label noise sd", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "lam", label: "Ridge penalty", min: -8, max: 0, step: 0.25, value: -8, fmt: function (x) { return x <= -8 ? "0 (min norm)" : Math.pow(10, x).toPrecision(1); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var lam = Math.pow(10, v.lam), n = v.n, i, sets = world(s.seed, v.noise);
        var base = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 27, 30, 34, 38, 44, 50, 60, 75, 90, 105, 120], seen = {}, ps = [];
        base.concat([n - 2, n - 1, n, n + 1, n + 2]).forEach(function (q) { if (q >= 1 && q <= PMAX && !seen[q]) { seen[q] = 1; ps.push(q); } });
        ps.sort(function (a, b) { return a - b; });
        var med = ps.map(function (q) {
          var es = sets.map(function (S) { return testError(S, n, q, lam); }).sort(function (a, b) { return a - b; });
          return Math.sqrt(es[2] * es[3]); // the middle of six draws, on the log scale
        });
        var keep = {}, here = testError(sets[0], n, v.p, lam, keep), ev = eigs(keep.G), sv = ev.map(function (x) { return Math.sqrt(Math.max(x, 1e-16)); });
        var atN = med[ps.indexOf(n)], bottom = Infinity, m = sv.length;
        for (i = 0; i < ps.length; i++) if (ps[i] < n) bottom = Math.min(bottom, med[i]);
        s.out = [here, atN, bottom, med[med.length - 1], sv[m - 1]];
        var clS = function (y) { return Math.max(1.2e-4, Math.min(9, y)); }, idx = sv.map(function (_, k) { return k + 1; });
        var a = g[0].axes({ x: [0, NMAX + 1], y: [1e-4, 10], logy: true, title: "Singular values of the " + n + " × " + v.p + " feature matrix", xlabel: "singular value, largest first", xticks: [1, 6, 12, 18, 24] });
        a.line(idx, sv.map(clS), { color: C.spot, width: 1.2, alpha: 0.6 });
        a.dots(idx.slice(0, m - 1), sv.slice(0, m - 1).map(clS), { color: C.spot, r: 3 });
        a.dots([m], [clS(sv[m - 1])], { color: C.loss, r: 5 });
        a.legend([["singular values", C.spot], ["the smallest: the noise is divided by it", C.loss]], { pos: "bl" });
        var cl = function (y) { return Math.max(1.1e-2, Math.min(9e3, y)); };
        var b = g[1].axes({ x: [1, PMAX], y: [1e-2, 1e4], logy: true, title: "Test error against the number of features", xlabel: "features p", xticks: [1, 20, 40, 60, 80, 100, 120] });
        b.vline(n, { color: C.loss });
        b.text(n, 2.2e-2, "p = n", { color: C.loss, dx: 6, bg: true });
        b.line(ps, med.map(cl), { color: C.idea, width: 2 });
        b.dots([v.p], [cl(here)], { color: C.ink, r: 4.5 });
        b.legend([["test error, middle of 6 draws", C.idea], ["this draw, this p", C.ink]], { pos: "tr" });
      },
      readout: function (v, s) {
        var f = function (x) { return x >= 100 ? x.toFixed(0) : x >= 1 ? x.toFixed(1) : x.toFixed(3); };
        return [["smallest singular value", s.out[4] < 0.001 ? s.out[4].toExponential(1) : s.out[4].toFixed(3)], ["test error here", f(s.out[0])],
          ["typical at p = n", f(s.out[1])], ["lowest before p = n", f(s.out[2])], ["typical at p = 120", f(s.out[3])]];
      },
      note: "Simulated data: y = β·x + noise with x standard normal in six dimensions; features max(0, a·x + b)/√p with random a and b. Test error is the mean squared distance to β·x on 40 fresh inputs; values off the frame are drawn at its edge. With zero noise most of the peak goes: it is the noise that the small singular values amplify.",
    });
  };

  // ---- Part 9: a signal and its gradient through a deep random network --------------------------------------
  W.signaldepth = function (el) {
    var LMAX = 100, names = ["ReLU", "tanh"];
    var NMAX = 128;
    var pool = function (s, L) { // weights before scaling: unit-variance uniforms, made once per seed, layer by layer as depth asks
      if (s.key !== s.seed) {
        var r0 = QB.rng(s.seed * 31 + 900), x = new Float64Array(NMAX), gout = new Float64Array(NMAX), i;
        for (i = 0; i < NMAX; i++) { x[i] = r0.normal(); gout[i] = r0.normal(); }
        s.key = s.seed; s.net = { W: [], x: x, g: gout };
      }
      while (s.net.W.length < L) {
        var r = QB.rng(s.seed * 31 + 7 * s.net.W.length + 901), M = new Float32Array(NMAX * NMAX), k;
        for (k = 0; k < M.length; k++) M[k] = (r() - 0.5) * 3.4641016;
        s.net.W.push(M);
      }
      return s.net;
    };
    var rms = function (a) { var t = 0; for (var i = 0; i < a.length; i++) t += a[i] * a[i]; return Math.sqrt(t / a.length); };
    var gauss = function (f) { var t = 0, w = 0; for (var k = -40; k <= 40; k++) { var z = k * 0.15, q = Math.exp(-0.5 * z * z); t += q * f(z); w += q; } return t / w; }; // E f(z), z standard normal
    QB.widget(el, {
      title: "Fifty layers deep: does the signal survive, and does the gradient?",
      sub: "One input goes forward through a random network and one gradient comes back. With the weights' spread set as derived (He's 2/n for ReLU, 1/n for tanh) both keep their size. Slide the scale a little below 1 and they vanish layer by layer; a little above and ReLU explodes, while tanh saturates and its gradient still explodes. Dashed lines are the mean-field prediction.",
      panels: 2, height: 300,
      controls: [
        { k: "g", label: "Weight sd, × the derived one", min: 0.5, max: 1.5, step: 0.01, value: 0.9, fmt: function (x) { return x.toFixed(2); } },
        { k: "L", label: "Depth", min: 5, max: LMAX, step: 1, value: 50 },
        { k: "act", label: "Activation", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return names[x]; } },
        { k: "n", label: "Width", min: 16, max: 128, step: 16, value: 64 },
      ],
      buttons: [{ label: "New network", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, L = v.L, tanh = v.act === 1, net = pool(s, L), sc = v.g * Math.sqrt((tanh ? 1 : 2) / n), l, i, j, t;
        var h = net.x.subarray(0, n), zs = [], fw = [rms(h)], idx = [0];
        for (l = 0; l < L; l++) { // forward: z = W h, h = act(z)
          var Wl = net.W[l], z = new Float64Array(n), hn = new Float64Array(n);
          for (i = 0; i < n; i++) { t = 0; for (j = 0; j < n; j++) t += Wl[i * NMAX + j] * h[j]; z[i] = t * sc; hn[i] = tanh ? Math.tanh(z[i]) : (z[i] > 0 ? z[i] : 0); }
          zs.push(z); h = hn; fw.push(rms(h)); idx.push(l + 1);
        }
        var gr = net.g.subarray(0, n), bw = new Array(L + 1); bw[L] = rms(gr);
        for (l = L - 1; l >= 0; l--) { // backward: gradient at layer l = W' (gradient at l + 1, times act'(z))
          var Wb = net.W[l], zl = zs[l], d = new Float64Array(n), gp = new Float64Array(n);
          for (i = 0; i < n; i++) { var th = tanh ? Math.tanh(zl[i]) : 0; d[i] = gr[i] * (tanh ? 1 - th * th : (zl[i] > 0 ? 1 : 0)); }
          for (j = 0; j < n; j++) { t = 0; for (i = 0; i < n; i++) t += Wb[i * NMAX + j] * d[i]; gp[j] = t * sc; }
          gr = gp; bw[l] = rms(gr);
        }
        // mean field: q = variance of z, m = E act(z)^2, chi = c g^2 E act'(z)^2 per layer
        var c2 = (tanh ? 1 : 2) * v.g * v.g, m = fw[0] * fw[0], tf = [fw[0]], chi = [];
        for (l = 0; l < L; l++) {
          var q = c2 * m, sq = Math.sqrt(q);
          m = tanh ? gauss(function (z0) { var a = Math.tanh(sq * z0); return a * a; }) : q / 2;
          chi.push(tanh ? c2 * gauss(function (z0) { var a = Math.tanh(sq * z0), b0 = 1 - a * a; return b0 * b0; }) : c2 / 2);
          tf.push(Math.sqrt(m));
        }
        var tb = new Array(L + 1); tb[L] = bw[L];
        for (l = L - 1; l >= 0; l--) tb[l] = tb[l + 1] * Math.sqrt(chi[l]);
        var E = 2; // the frame: a whole number of decades either side of 1, wide enough for every curve, at most 20
        [fw, bw, tf, tb].forEach(function (arr) { for (var k = 0; k < arr.length; k++) if (arr[k] > 0 && isFinite(arr[k])) E = Math.max(E, Math.abs(Math.log(arr[k]) / Math.LN10) + 0.5); });
        E = Math.min(20, 2 * Math.ceil(E / 2));
        var lo = Math.pow(10, -E), hi = Math.pow(10, E);
        var cl = function (y) { return y === y ? Math.max(lo * 1.3, Math.min(hi / 1.3, y)) : lo * 1.3; };
        s.out = [fw[L] / Math.max(fw[0], 1e-300), bw[0] / Math.max(bw[L], 1e-300), Math.sqrt(chi[L - 1])];
        var yt = [lo, Math.pow(10, -E / 2), 1, Math.pow(10, E / 2), hi], yf = function (y) { var e = Math.round(Math.log(y) / Math.LN10); return e === 0 ? "1" : "1e" + String(e).replace("-", "−"); };
        var opt = function (title, xl) { return { x: [0, L], y: [lo, hi], logy: true, yticks: yt, yfmt: yf, title: title, xlabel: xl, nx: 5 }; };
        var a = g[0].axes(opt("Forward: size of the activations", "layer (input at 0)"));
        a.hline(1, { color: C.muted });
        a.line(idx, tf.map(cl), { color: C.ink, dash: [5, 4], width: 1.3 });
        a.line(idx, fw.map(cl), { color: C.spot, width: 2 });
        a.legend([["measured, width " + n, C.spot], ["mean-field prediction", C.ink]], { pos: "bl" });
        var b = g[1].axes(opt("Backward: size of the gradient", "layer (the gradient starts at layer " + L + ")"));
        b.hline(1, { color: C.muted });
        b.line(idx, tb.map(cl), { color: C.ink, dash: [5, 4], width: 1.3 });
        b.line(idx, bw.map(cl), { color: C.implied, width: 2 });
        b.legend([["measured", C.implied], ["mean-field prediction", C.ink]], { pos: "br" });
      },
      readout: function (v, s) {
        var f = function (x) { return x === 0 ? "0" : (x >= 0.01 && x < 1000) ? x.toFixed(2) : x.toExponential(1).replace("-", "−").replace("+", ""); };
        return [["signal after " + v.L + " layers", "× " + f(s.out[0])], ["gradient reaching layer 0", "× " + f(s.out[1])], ["gradient factor per layer, last layer", f(s.out[2])]];
      },
      note: "A random, untrained network: weights are independent with mean 0 and sd = scale × √(2/n) for ReLU and scale × √(1/n) for tanh, no biases; sizes are root mean squares over the units, on a log scale that widens with the curves, up to 1e±20. For ReLU the prediction is scale^layers both ways; at a finite width the measured curves wander around it and drift below. For tanh a factor per layer above 1 with a bounded signal is the chaotic phase; below 1 the ordered phase.",
    });
  };

  // ---- Part 10: the receptive field of a stack of convolutions ----------------------------------------------
  W.receptivecone = function (el) {
    var LMAX = 8, dil = ["none", "doubling"];
    var field = function (k, st, L, dbl) { // r_l = r_(l-1) + (k - 1) d_l j_(l-1), j_l = j_(l-1) s: r and j after each layer
      var r = [1], j = [1];
      for (var l = 1; l <= L; l++) { var d = dbl ? Math.pow(2, l - 1) : 1; r.push(r[l - 1] + (k - 1) * d * j[l - 1]); j.push(j[l - 1] * st); }
      return { r: r, j: j };
    };
    var big = function (x) { return x >= 1e9 ? x.toExponential(1).replace("+", "") : x >= 1e6 ? (x / 1e6).toFixed(1) + " million" : x >= 1e4 ? Math.round(x / 1000) + " thousand" : String(Math.round(x)); };
    QB.widget(el, {
      title: "The cone of one deep unit: its receptive field",
      sub: "A stack of one-dimensional convolutions. Left: the units in each layer that one top unit depends on, placed over the input pixels they are centred on. Right: the receptive field after each layer. With stride 1 it grows by k − 1 pixels a layer; raise the stride or let the dilation double and it grows geometrically.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Kernel size k", min: 2, max: 7, step: 1, value: 3 },
        { k: "L", label: "Layers", min: 1, max: LMAX, step: 1, value: 4 },
        { k: "st", label: "Stride of every layer", min: 1, max: 3, step: 1, value: 1 },
        { k: "dbl", label: "Dilation", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return dil[x]; } },
      ],
      draw: function (g, v, s) {
        var k = v.k, L = v.L, f = field(k, v.st, L, v.dbl), R = f.r[L], l, i, u;
        // the units each layer contributes, as positions in input pixels relative to the top unit's centre
        var half = [0], sets = [[0]];
        for (l = L; l >= 1; l--) {
          var step = (v.dbl ? Math.pow(2, l - 1) : 1) * f.j[l - 1], prev = sets[sets.length - 1], seen = {}, cur = [];
          half.push(half[half.length - 1] + (k - 1) / 2 * step);
          if (prev && prev.length * k <= 4000) {
            for (i = 0; i < prev.length; i++) for (u = 0; u < k; u++) { var pos = prev[i] + (u - (k - 1) / 2) * step, key = Math.round(pos * 2); if (!seen[key]) { seen[key] = 1; cur.push(pos); } }
            sets.push(cur.length <= 400 ? cur : null);
          } else sets.push(null);
        } // sets[m] and half[m] describe layer L - m
        var xr = half[L] * 1.08 + 0.6, left = [], right = [], ys = [];
        for (l = 0; l <= L; l++) { ys.push(l); left.push(-half[L - l]); right.push(half[L - l]); }
        var a = g[0].axes({ x: [-xr, xr], y: [-0.5, L + 0.45 + 0.32 * (L + 1)], title: "A layer-" + L + " unit sees " + big(R) + " input pixels", xlabel: "input pixel, from the unit's centre", yticks: ys, yfmt: function (y) { return y === 0 ? "input" : "layer " + y; }, nx: 4 });
        a.line(left, ys, { color: C.spot, width: 1.5 }).line(right, ys, { color: C.spot, width: 1.5 });
        for (l = 0; l <= L; l++) {
          var S = sets[L - l];
          a.line([-half[L - l], half[L - l]], [l, l], { color: l === 0 ? C.idea : C.spot, width: l === 0 ? 3 : 1, alpha: l === 0 ? 1 : 0.5 });
          if (S) a.dots(S, S.map(function () { return l; }), { color: l === L ? C.loss : l === 0 ? C.idea : C.ink, r: S.length > 120 ? 1.2 : S.length > 40 ? 1.8 : 3 });
        }
        a.legend([["the top unit", C.loss], ["units it depends on", C.ink], ["input pixels it sees", C.idea]], { pos: "tl" });
        var ls = [], cur2 = [], plain = [], full = field(k, v.st, LMAX, v.dbl), base = field(k, 1, LMAX, 0);
        for (l = 0; l <= LMAX; l++) { ls.push(l); cur2.push(Math.min(full.r[l], 9e6)); plain.push(base.r[l]); }
        var need = 0; for (l = 1; l <= LMAX; l++) if (!need && full.r[l] >= 224) need = l;
        s.out = [R, f.j[L], L * k * k, need];
        var yt = [1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7], yf = function (y) { return y >= 1e6 ? y / 1e6 + "M" : y >= 1e3 ? y / 1e3 + "k" : String(y); };
        var b = g[1].axes({ x: [0, LMAX], y: [1, 1e7], logy: true, yticks: yt, yfmt: yf, title: "Receptive field against depth", xlabel: "layers" });
        b.hline(224, { color: C.muted });
        b.text(LMAX, 224, "a 224-pixel image side", { color: C.muted, align: "right", dx: -4, dy: -9 });
        b.line(ls, plain, { color: C.spot, width: 1.5 });
        b.line(ls, cur2, { color: C.idea, width: 2.2 });
        b.dots([L], [Math.min(R, 9e6)], { color: C.loss, r: 4.5 });
        b.legend([["these settings", C.idea], ["stride 1, no dilation", C.spot]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["receptive field", big(s.out[0]) + " px"], ["spacing of the top layer's units", big(s.out[1]) + " px"], ["weights in 2-D, per pair of channels", s.out[2] + " (one layer with this field: " + big(s.out[0] * s.out[0]) + ")"],
          ["layers to cover 224 px", s.out[3] ? String(s.out[3]) : "more than 8"]];
      },
      note: "Exact arithmetic, no data: r grows by (k − 1) × dilation × the spacing of the layer below, and the spacing multiplies by the stride. Every layer here has the same kernel and stride; doubling dilation is 1, 2, 4, … as in WaveNet. Units are drawn where there are at most 400 of them in a layer; the outline is always exact.",
    });
  };
})();
