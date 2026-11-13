// Interactives for Stage IV, PhD core (Parts 49-55).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var f1 = function (x) { return x.toFixed(1); }, f2 = function (x) { return x.toFixed(2); }, f0 = function (x) { return String(Math.round(x)); };

  // ---- Part 49: the gain from a model's tangent space, and its price when the model is wrong -----------------
  W.tangentgain = function (el) {
    QB.widget(el, {
      title: "What a model buys: two estimators of one cell of a 2 × 2 table",
      sub: "The target is P(X1 = 1, X2 = 1). The blue estimator is the cell's frequency and assumes nothing. The gold one multiplies the two margins, which is efficient if X1 and X2 are independent. At dependence 0 gold is tighter, by exactly the projection onto the tangent space; move the dependence away from 0 and its bias takes over.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "P(X1 = 1)", min: 0.1, max: 0.9, step: 0.05, value: 0.3, fmt: f2 },
        { k: "q", label: "P(X2 = 1)", min: 0.1, max: 0.9, step: 0.05, value: 0.6, fmt: f2 },
        { k: "dep", label: "Dependence (share of the largest possible covariance)", min: -0.5, max: 0.5, step: 0.05, value: 0, fmt: function (x) { return fmt(x, 2); } },
        { k: "n", label: "Sample size n", min: 50, max: 800, step: 50, value: 400, fmt: f0 },
      ],
      buttons: [{ label: "New samples", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 490), p = v.p, q = v.q, n = v.n, reps = 300, i, k;
        var hi = Math.min(p * (1 - q), (1 - p) * q), lo = Math.min(p * q, (1 - p) * (1 - q));
        var cov = v.dep >= 0 ? v.dep * hi : v.dep * lo, p11 = p * q + cov, p10 = p - p11, p01 = q - p11;
        var A = [], B = [], mseA = 0, mseB = 0;
        for (k = 0; k < reps; k++) {
          var c11 = 0, c10 = 0, c01 = 0;
          for (i = 0; i < n; i++) { var u = r(); if (u < p11) c11++; else if (u < p11 + p10) c10++; else if (u < p11 + p10 + p01) c01++; }
          var a = c11 / n, b = (c11 + c10) / n * (c11 + c01) / n;
          A.push(a); B.push(b); mseA += (a - p11) * (a - p11); mseB += (b - p11) * (b - p11);
        }
        mseA *= n / reps; mseB *= n / reps;
        var normA = p11 * (1 - p11), normB = q * q * p * (1 - p) + p * p * q * (1 - q);
        s.out = [p11, mseA, mseB, normA, normB, p * q - p11];
        var w = Math.max(4 * Math.sqrt(normA / n), Math.abs(cov) + 3 * Math.sqrt(normB / n)), x0 = p11 - w, x1 = p11 + w, nb = 30, bw = (x1 - x0) / nb;
        var hA = QB.hist(A, x0, x1, nb), hB = QB.hist(B, x0, x1, nb), top = 1, xs = [];
        for (i = 0; i < nb; i++) { xs.push(x0 + (i + 0.5) * bw); top = Math.max(top, hA[i], hB[i]); }
        var ax = g[0].axes({ x: [x0, x1], y: [0, top * 1.3], title: "300 samples: the two estimates", xlabel: "estimate of P(X1 = 1, X2 = 1)", nx: 4 });
        ax.bars(xs, hA, bw, { color: C.spot, alpha: 0.6 });
        ax.bars(xs, hB, bw, { color: C.idea, alpha: 0.6 });
        ax.vline(p11, { color: C.ink });
        ax.legend([["cell frequency", C.spot], ["product of margins", C.idea], ["truth", C.ink]], { pos: "tl" });
        var ymax = Math.max(0.3, 1.25 * Math.max(mseA, mseB, normA));
        var bx = g[1].axes({ x: [0.3, 2.7], y: [0, ymax], title: "n × mean squared error", xticks: [1, 2], xfmt: function (x) { return x === 1 ? "cell frequency" : "product of margins"; } });
        bx.bars([1, 2], [mseA, mseB], 0.6, { color: function (j) { return j ? C.idea : C.spot; } });
        bx.line([0.6, 1.4], [normA, normA], { color: C.ink, width: 2 });
        bx.line([1.6, 2.4], [normB, normB], { color: C.gain, width: 2 });
        bx.legend([["‖φ‖², no model", C.ink], ["‖φ*‖², under independence", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["truth", fmt(s.out[0], 3)], ["n·MSE, cell frequency", fmt(s.out[1], 3)], ["n·MSE, product", fmt(s.out[2], 3)],
          ["‖φ‖²", fmt(s.out[3], 3)], ["‖φ*‖²", fmt(s.out[4], 3)], ["bias of the product", fmt(s.out[5], 3)]];
      },
      note: "Simulated data. ‖φ‖² = p₁₁(1 − p₁₁) is the variance of the nonparametric influence function; ‖φ*‖² = q²p(1 − p) + p²q(1 − q) is the variance of its projection onto the tangent space {a(x1) + b(x2)} of the independence model, and is a bound only when that model holds.",
    });
  };

  // ---- Part 50: Pinsker's taper against a hard cut-off ----------------------------------------------------------
  W.pinskertaper = function (el) {
    QB.widget(el, {
      title: "Where to stop: a cut-off against Pinsker's taper",
      sub: "In the sequence model y_k = θ_k + ε z_k over the ellipsoid Σ k^(2α) θ_k² ≤ 1, a projection estimator keeps the first N coordinates. Slide N: too few and the worst case is bias, too many and it is noise. The gold line is the linear minimax risk, reached by the taper (1 − k^α/μ)₊ and by no cut-off.",
      panels: 2, height: 300,
      controls: [
        { k: "alpha", label: "Smoothness α", min: 0.5, max: 3, step: 0.25, value: 1, fmt: f2 },
        { k: "le", label: "Noise level ε", min: -2, max: -0.7, step: 0.05, value: -1.5, fmt: function (x) { return Math.pow(10, x).toFixed(3); } },
        { k: "N", label: "Cut-off N", min: 1, max: 200, step: 1, value: 8, fmt: f0 },
      ],
      draw: function (g, v, s) {
        var K = 600, eps = Math.pow(10, v.le), e2 = eps * eps, al = v.alpha, a = [], k, i;
        for (k = 1; k <= K; k++) a.push(Math.pow(k, al));
        var gmu = function (mu) { var t = 0; for (var j = 0; j < K; j++) { if (a[j] >= mu) break; t += a[j] * (mu - a[j]); } return e2 * t - 1; };
        var lo = 1, hi = 2; while (gmu(hi) < 0 && hi < 1e9) hi *= 2;
        for (i = 0; i < 60; i++) { var mid = 0.5 * (lo + hi); if (gmu(mid) < 0) lo = mid; else hi = mid; }
        var mu = 0.5 * (lo + hi), risk = 0, active = 0, taper = [], ks = [], cut = [];
        for (k = 0; k < K; k++) { var c = Math.max(0, 1 - a[k] / mu); risk += e2 * c; if (c > 0) active++; }
        var Ns = [], rs = [], best = Infinity, bestN = 1;
        for (k = 1; k <= 200; k++) { var rr = 1 / (a[k] * a[k]) + e2 * k; Ns.push(k); rs.push(rr); if (rr < best) { best = rr; bestN = k; } }
        var mine = rs[v.N - 1], bias = 1 / (a[v.N] * a[v.N]), noise = e2 * v.N;
        s.out = [mine, risk, mine / risk, best / risk, bestN, active, bias, noise];
        var kmax = Math.max(20, Math.min(200, Math.ceil(1.3 * Math.max(active, v.N))));
        for (k = 1; k <= kmax; k++) { ks.push(k); taper.push(Math.max(0, 1 - a[k - 1] / mu)); cut.push(k <= v.N ? 1 : 0); }
        var ax = g[0].axes({ x: [0, kmax], y: [0, 1.3], title: "Weight on coordinate k", xlabel: "k", yticks: [0, 0.5, 1] });
        ax.bars(ks, cut, 1, { color: C.spot, alpha: 0.45, gap: 0 });
        ax.line(ks, taper, { color: C.idea, width: 2.2 });
        ax.legend([["cut-off: keep k ≤ N", C.spot], ["Pinsker's taper", C.idea]], { pos: "tr" });
        var yl = Math.min(risk, best) / 3, yh = Math.max(rs[0], rs[199], risk) * 30;
        var bx = g[1].axes({ x: [1, 200], y: [yl, yh], logx: true, logy: true, title: "Worst-case risk of the cut-off", xlabel: "cut-off N" });
        bx.line(Ns, Ns.map(function (n) { return 1 / (a[n] * a[n]); }), { color: C.loss, width: 1.2, dash: [4, 3] });
        bx.line(Ns, Ns.map(function (n) { return e2 * n; }), { color: C.gain, width: 1.2, dash: [4, 3] });
        bx.line(Ns, rs, { color: C.spot, width: 2.2 });
        bx.hline(risk, { color: C.idea, width: 2, dash: [] });
        bx.dots([v.N], [mine], { color: C.ink, r: 5 });
        bx.legend([["cut-off's risk", C.spot], ["worst bias²", C.loss], ["noise ε²N", C.gain], ["linear minimax", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["cut-off's worst risk", s.out[0].toExponential(2)], ["linear minimax risk", s.out[1].toExponential(2)], ["ratio", fmt(s.out[2], 2)],
          ["best cut-off N", String(s.out[4])], ["its ratio", fmt(s.out[3], 2)], ["taper's support", String(s.out[5])]];
      },
      note: "Exact arithmetic, C = 1, a_k = k^α. The cut-off's worst-case risk is 1/a_(N+1)² + ε²N; the taper's is ε² Σ (1 − a_k/μ)₊ with ε² Σ a_k(μ − a_k)₊ = 1. For α = 1 the best cut-off's ratio tends to 3^(2/3) ≈ 2.08 as ε falls.",
    });
  };

  // ---- Part 51: the sphere's equator ----------------------------------------------------------------------------
  W.equatorband = function (el) {
    QB.widget(el, {
      title: "Almost all of a high-dimensional sphere lies near its equator",
      sub: "Points are drawn uniformly on the unit sphere in n dimensions and shown by their first two coordinates. The gold band is |x1| ≤ t. Raise the dimension: the cloud collapses toward the centre of the picture, and a band of fixed width, around any equator chosen in advance, swallows the sphere.",
      panels: 2, height: 310,
      controls: [
        { k: "ln", label: "Dimension n", min: 0.5, max: 4, step: 0.05, value: 1, fmt: function (x) { return String(Math.max(3, Math.round(Math.pow(10, x)))); } },
        { k: "t", label: "Band half-width t", min: 0.01, max: 1, step: 0.01, value: 0.1, fmt: f2 },
      ],
      buttons: [{ label: "New points", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = Math.max(3, Math.round(Math.pow(10, v.ln))), t = v.t, r = QB.rng(s.seed + 510), i, j;
        // the exact density of x1, c (1 - x^2)^((n-3)/2), on a grid fine enough for its width
        var R = Math.min(1, 8 / Math.sqrt(n)), M = 1200, dx = 2 * R / M, xs = [], fs = [], tot = 0, peak = 0;
        for (i = 0; i <= M; i++) { var x = -R + i * dx, f = Math.exp(0.5 * (n - 3) * Math.log(Math.max(1 - x * x, 1e-12))); xs.push(x); fs.push(f); tot += f * dx; }
        var mass = 0, cum = 0, half = R, found = false;
        for (i = 0; i <= M; i++) { fs[i] /= tot; peak = Math.max(peak, fs[i]); if (Math.abs(xs[i]) <= t) mass += fs[i] * dx; }
        for (i = 0; i <= M / 2 && !found; i++) { cum += (i === 0 ? fs[M / 2] : fs[M / 2 + i] + fs[M / 2 - i]) * dx; if (cum >= 0.95) { half = i * dx; found = true; } }
        mass = Math.min(1, mass);
        // 400 points: (x1, x2) = (g1, g2) / |g|, the other n - 2 squared coordinates by a chi-square draw
        var px = [], py = [], inside = 0, k = n - 2, N = 400;
        for (i = 0; i < N; i++) {
          var a = r.normal(), b = r.normal(), c2 = 0;
          if (k <= 40) { for (j = 0; j < k; j++) { var e = r.normal(); c2 += e * e; } }
          else { var wh = 1 - 2 / (9 * k) + r.normal() * Math.sqrt(2 / (9 * k)); c2 = k * wh * wh * wh; }
          var nr = Math.sqrt(a * a + b * b + Math.max(c2, 0));
          px.push(a / nr); py.push(b / nr); if (Math.abs(a / nr) <= t) inside++;
        }
        s.out = [n, mass, half, 1.96 / Math.sqrt(n), inside / N];
        var c = g.ctx, bx = g[0].box, cx = bx.x + bx.w / 2, cy = bx.y + bx.h / 2 + 10, rad = Math.min(bx.w, bx.h - 30) / 2 - 12;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("400 random points, first two coordinates", bx.x + 12, bx.y + 6);
        c.beginPath(); c.arc(cx, cy, rad, 0, 6.2832); c.clip();
        c.fillStyle = C.idea; c.globalAlpha = 0.22; c.fillRect(cx - t * rad, cy - rad, 2 * t * rad, 2 * rad); c.globalAlpha = 1;
        c.restore();
        c.save();
        c.strokeStyle = C.muted; c.lineWidth = 1.2; c.beginPath(); c.arc(cx, cy, rad, 0, 6.2832); c.stroke();
        c.fillStyle = C.spot; c.globalAlpha = 0.8;
        for (i = 0; i < N; i++) { c.beginPath(); c.arc(cx + px[i] * rad, cy - py[i] * rad, 1.8, 0, 6.2832); c.fill(); }
        c.globalAlpha = 1; c.fillStyle = C.muted; c.font = "11px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "top";
        c.fillText("x1 →", cx, cy + rad + 3);
        c.restore();
        var ax = g[1].axes({ x: [-1, 1], y: [0, peak * 1.25], title: "Exact density of one coordinate", xlabel: "x1" });
        var bxs = [], bfs = [];
        for (i = 0; i <= M; i++) { if (Math.abs(xs[i]) <= t) { bxs.push(xs[i]); bfs.push(fs[i]); } }
        if (bxs.length > 1) ax.area(bxs, bfs, 0, { color: C.idea, alpha: 0.3 });
        ax.line([-1].concat(xs, [1]), [0].concat(fs, [0]), { color: C.spot, width: 2 });
        ax.vline(-t, { color: C.idea }); ax.vline(t, { color: C.idea });
        ax.legend([["density of x1", C.spot], ["the band |x1| ≤ t", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["n", String(s.out[0])], ["mass of the sphere in the band", QB.pct(s.out[1])], ["of these 400 points", QB.pct(s.out[4])],
          ["half-width holding 95%", fmt(s.out[2], 3)], ["1.96/√n", fmt(s.out[3], 3)]];
      },
      note: "Simulated points; the density c(1 − x²)^((n−3)/2) and the band's mass are exact (numerical integration). The statement is for one direction fixed before the point is drawn, not for all equators at once.",
    });
  };

  // ---- Part 52: a spike against the Marchenko-Pastur bulk ---------------------------------------------------------
  W.bbpspike = function (el) {
    var P = 40;
    function jacobi(S) { // eigenvalues of a symmetric matrix (array of rows), by cyclic Jacobi rotations
      var p = S.length, A = S.map(function (row) { return row.slice(); }), sweep, i, j, k;
      for (sweep = 0; sweep < 8; sweep++) {
        var off = 0;
        for (i = 0; i < p; i++) for (j = i + 1; j < p; j++) off += A[i][j] * A[i][j];
        if (off < 1e-10) break;
        for (i = 0; i < p - 1; i++) for (j = i + 1; j < p; j++) {
          if (Math.abs(A[i][j]) < 1e-14) continue;
          var th = (A[j][j] - A[i][i]) / (2 * A[i][j]), t = (th >= 0 ? 1 : -1) / (Math.abs(th) + Math.sqrt(th * th + 1)), c = 1 / Math.sqrt(t * t + 1), sn = t * c;
          for (k = 0; k < p; k++) { var aik = A[i][k], ajk = A[j][k]; A[i][k] = c * aik - sn * ajk; A[j][k] = sn * aik + c * ajk; }
          for (k = 0; k < p; k++) { var aki = A[k][i], akj = A[k][j]; A[k][i] = c * aki - sn * akj; A[k][j] = sn * aki + c * akj; }
        }
      }
      var ev = []; for (i = 0; i < p; i++) ev.push(A[i][i]);
      return ev.sort(function (a, b) { return a - b; });
    }
    QB.widget(el, {
      title: "Can PCA see the spike? The BBP transition",
      sub: "Forty variables, all with variance 1 except the first, whose variance is 1 + ℓ. The blue bars are the sample covariance's eigenvalues, the grey curve is the Marchenko–Pastur law of pure noise. Raise ℓ past √(p/n): the top eigenvalue leaves the bulk and its eigenvector starts to point at the truth. Below it, PCA sees nothing.",
      panels: 2, height: 300,
      controls: [
        { k: "gam", label: "p / n", min: 0.1, max: 1, step: 0.05, value: 0.5, fmt: f2 },
        { k: "ell", label: "Spike ℓ", min: 0, max: 4, step: 0.05, value: 1.5, fmt: f2 },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 520), p = P, n = Math.round(p / v.gam), gam = p / n, ell = v.ell, sc = Math.sqrt(1 + ell), i, j, k;
        var S = []; for (i = 0; i < p; i++) { S.push([]); for (j = 0; j < p; j++) S[i].push(0); }
        var row = new Array(p);
        for (k = 0; k < n; k++) {
          for (i = 0; i < p; i++) row[i] = r.normal();
          row[0] *= sc;
          for (i = 0; i < p; i++) { var ri = row[i] / n, Si = S[i]; for (j = i; j < p; j++) Si[j] += ri * row[j]; }
        }
        for (i = 0; i < p; i++) for (j = 0; j < i; j++) S[i][j] = S[j][i];
        var ev = jacobi(S), top = ev[p - 1];
        var u = []; for (i = 0; i < p; i++) u.push(r.normal());
        for (k = 0; k < 120; k++) { // power iteration for the top eigenvector
          var w = [], nr = 0;
          for (i = 0; i < p; i++) { var t = 0; for (j = 0; j < p; j++) t += S[i][j] * u[j]; w.push(t); nr += t * t; }
          nr = Math.sqrt(nr) || 1; for (i = 0; i < p; i++) u[i] = w[i] / nr;
        }
        var over = u[0] * u[0], thr = Math.sqrt(gam), a = (1 - thr) * (1 - thr), b = (1 + thr) * (1 + thr);
        var limTop = ell > thr ? (1 + ell) * (1 + gam / ell) : b, limOver = ell > thr ? (1 - gam / (ell * ell)) / (1 + gam / ell) : 0;
        s.out = [n, thr, top, limTop, over, limOver];
        var xmax = Math.max(b + 0.6, top * 1.08, limTop * 1.05), nb = 36, bw = xmax / nb, h = QB.hist(ev, 0, xmax, nb), xs = [], hs = [], ymax = 0.9;
        for (i = 0; i < nb; i++) { xs.push((i + 0.5) * bw); hs.push(h[i] / (p * bw)); if (i > 0) ymax = Math.max(ymax, hs[i]); }
        var ax = g[0].axes({ x: [0, xmax], y: [0, ymax * 1.35], title: "Sample eigenvalues, n = " + n + ", p = " + p, xlabel: "eigenvalue" });
        ax.bars(xs, hs, bw, { color: C.spot, alpha: 0.6 });
        var mx = QB.linspace(a + 1e-4, b - 1e-4, 160), my = mx.map(function (x) { return Math.sqrt((b - x) * (x - a)) / (2 * Math.PI * gam * x); });
        ax.line(mx, my, { color: C.cash, width: 2 });
        ax.vline(b, { color: C.loss });
        ax.vline(limTop, { color: C.gain });
        ax.dots([top], [0.035 * ymax * 1.35], { color: C.idea, r: 5.5 });
        ax.legend([["top sample eigenvalue", C.idea], ["its BBP limit", C.gain], ["edge of the noise bulk", C.loss], ["Marchenko–Pastur", C.cash]], { pos: "tr" });
        var ls = QB.linspace(0.01, 4, 200), lo = ls.map(function (l) { return l > thr ? (1 - gam / (l * l)) / (1 + gam / l) : 0; });
        var bx = g[1].axes({ x: [0, 4], y: [0, 1], title: "Squared overlap of the top eigenvector", xlabel: "spike ℓ" });
        bx.line(ls, lo, { color: C.gain, width: 2 });
        bx.vline(thr, { color: C.loss });
        bx.text(thr, 0.93, "√(p/n)", { color: C.loss, dx: 5 });
        bx.dots([ell], [over], { color: C.idea, r: 5.5 });
        bx.legend([["this sample", C.idea], ["limit (Paul 2007)", C.gain]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["n", String(s.out[0])], ["threshold √(p/n)", fmt(s.out[1], 2)], ["top eigenvalue", fmt(s.out[2], 2)], ["BBP limit", fmt(s.out[3], 2)],
          ["overlap²", fmt(s.out[4], 2)], ["its limit", fmt(s.out[5], 2)]];
      },
      note: "Simulated Gaussian data with p = 40; the limits are for n and p growing together, so a sample this small scatters around them. Above the threshold the top eigenvalue tends to (1 + ℓ)(1 + γ/ℓ), which overstates 1 + ℓ, and the overlap to (1 − γ/ℓ²)/(1 + γ/ℓ), with γ = p/n.",
    });
  };

  // ---- Part 53: does the credible ball contain the truth? ------------------------------------------------------
  W.credibleball = function (el) {
    QB.widget(el, {
      title: "A credible ball that covers, and one that cannot",
      sub: "Sequence model Y_k = θ_k + Z_k/√n with the prior θ_k ~ N(0, k^(−1−2α)) and a truth of smoothness β. Left: the posterior mean's error and the posterior's own spread, against α. Right: 200 datasets' distances from the posterior mean to the truth, and the 95% credible radius. Push α above β: the ball shrinks faster than the error and stops covering.",
      panels: 2, height: 300,
      controls: [
        { k: "alpha", label: "Prior smoothness α", min: 0.5, max: 3, step: 0.125, value: 1.5, fmt: f2 },
        { k: "beta", label: "Truth's smoothness β", min: 0.5, max: 2, step: 0.25, value: 1, fmt: f2 },
        { k: "ln", label: "Sample size n", min: 2, max: 4, step: 0.25, value: 4, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
      ],
      buttons: [{ label: "New data", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var K = 400, n = Math.round(Math.pow(10, v.ln)), r = QB.rng(s.seed + 530), k, i, th = [];
        for (k = 1; k <= K; k++) th.push(Math.pow(k, -0.5 - v.beta) * Math.sin(k));
        var exact = function (al) {
          var b2 = 0, vr = 0, sp = 0;
          for (var q = 1; q <= K; q++) { var lam = Math.pow(q, -1 - 2 * al), w = n * lam / (1 + n * lam); b2 += (1 - w) * (1 - w) * th[q - 1] * th[q - 1]; vr += w * w / n; sp += lam / (1 + n * lam); }
          return [Math.sqrt(b2 + vr), Math.sqrt(sp)];
        };
        var as = QB.linspace(0.5, 3, 26), er = [], sp = [], lo = Infinity, hi = 0;
        for (i = 0; i < as.length; i++) { var e = exact(as[i]); er.push(e[0]); sp.push(e[1]); lo = Math.min(lo, e[0], e[1]); hi = Math.max(hi, e[0], e[1]); }
        var w = [], pv = [], reps = 200, d = [], rad = [], sq = Math.sqrt(n);
        for (k = 1; k <= K; k++) { var lam = Math.pow(k, -1 - 2 * v.alpha); w.push(n * lam / (1 + n * lam)); pv.push(lam / (1 + n * lam)); }
        for (i = 0; i < reps; i++) {
          var d2 = 0, r2 = 0;
          for (k = 0; k < K; k++) { var z = r.normal(), z2 = r.normal(), err = -(1 - w[k]) * th[k] + w[k] * z / sq; d2 += err * err; r2 += pv[k] * z2 * z2; }
          d.push(Math.sqrt(d2)); rad.push(Math.sqrt(r2));
        }
        rad.sort(function (a, b) { return a - b; });
        var R = rad[Math.floor(0.95 * reps) - 1], cover = 0;
        for (i = 0; i < reps; i++) if (d[i] <= R) cover++;
        var here = exact(v.alpha);
        s.out = [n, here[0], R, cover / reps, Math.min(v.alpha, v.beta) / (1 + 2 * v.alpha), v.beta / (1 + 2 * v.beta)];
        var ax = g[0].axes({ x: [0.5, 3], y: [lo / 6, hi * 1.5], logy: true, title: "Error and posterior spread, exact", xlabel: "prior smoothness α" });
        ax.line(as, er, { color: C.spot, width: 2.2 });
        ax.line(as, sp, { color: C.idea, width: 2.2 });
        ax.vline(v.beta, { color: C.gain });
        ax.vline(v.alpha, { color: C.ink });
        ax.legend([["root risk of the posterior mean", C.spot], ["posterior's root-mean-square radius", C.idea], ["α = β", C.gain], ["this prior", C.ink]], { pos: "bl" });
        var xmax = Math.max(QB.quantile(d, 1), R) * 1.2, nb = 30, bw = xmax / nb, h = QB.hist(d, 0, xmax, nb), xs = [], top = 1;
        for (i = 0; i < nb; i++) { xs.push((i + 0.5) * bw); top = Math.max(top, h[i]); }
        var bx = g[1].axes({ x: [0, xmax], y: [0, top * 1.3], title: "Distance from the posterior mean to the truth", xlabel: "‖posterior mean − truth‖", nx: 4 });
        bx.bars(xs, h, bw, { color: function (j) { return xs[j] <= R ? C.spot : C.loss; }, alpha: 0.7 });
        bx.vline(R, { color: C.idea, width: 2, dash: [] });
        bx.legend([["inside the ball", C.spot], ["outside", C.loss], ["95% credible radius", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["n", String(s.out[0])], ["root risk", fmt(s.out[1], 4)], ["credible radius", fmt(s.out[2], 4)], ["coverage of the 95% ball", QB.pct(s.out[3], 0)],
          ["rate exponent", fmt(s.out[4], 3)], ["minimax exponent", fmt(s.out[5], 3)]];
      },
      note: "Simulated data in the first 400 coordinates, truth θ_k = k^(−1/2−β) sin k. The posterior contracts like n^(−min(α, β)/(1 + 2α)), which is the minimax rate n^(−β/(1 + 2β)) only at α = β. A rougher prior (α < β) gives a slower rate and a conservative ball; a smoother one gives a ball too small for its bias.",
    });
  };

  // ---- Part 54: the best of K classifiers ---------------------------------------------------------------------
  W.bestofk = function (el) {
    QB.widget(el, {
      title: "Pick the best of K classifiers, then ask how good it is",
      sub: "Each dot is a classifier: its true error across, its training error on n points up. The gold one has the lowest training error. The red bar is the usual 95% interval around its training error, the green bar the Hoeffding plus union-bound interval over all K. Raise K: the gold dot sinks below the diagonal and the red bar stops reaching its true error.",
      panels: 2, height: 310,
      controls: [
        { k: "lk", label: "Classifiers K", min: 0, max: 4, step: 0.25, value: 3, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
        { k: "n", label: "Training points n", min: 50, max: 2000, step: 50, value: 200, fmt: f0 },
        { k: "spread", label: "True errors range from 0.5 − this to 0.5", min: 0, max: 0.3, step: 0.01, value: 0.01, fmt: f2 },
      ],
      buttons: [{ label: "New training set", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 540), K = Math.round(Math.pow(10, v.lk)), n = v.n, KM = 10000, tr = [], te = [], j, best = 0;
        var ks = [], opt = [], uni = [], run = 0;
        for (j = 0; j < KM; j++) {
          var t = 0.5 - v.spread * r(), e = Math.round(n * t + Math.sqrt(n * t * (1 - t)) * r.normal()) / n;
          e = Math.max(0, Math.min(1, e)); tr.push(t); te.push(e);
          if (e < te[run]) run = j;
          if (j < K && e < te[best]) best = j;
          if (j < 30 || j % 20 === 0 || j === KM - 1) { ks.push(j + 1); opt.push(tr[run] - te[run]); uni.push(Math.sqrt(Math.log(2 * (j + 1) / 0.05) / (2 * n))); }
        }
        var eb = te[best], tb = tr[best], wald = 1.96 * Math.sqrt(Math.max(eb * (1 - eb), 0) / n), un = Math.sqrt(Math.log(2 * K / 0.05) / (2 * n));
        s.out = [K, eb, tb, tb - eb, wald, un, Math.abs(tb - eb) <= wald, Math.abs(tb - eb) <= un];
        var lo = Math.max(0, 0.5 - v.spread - 1.15 * un - 0.03), hi = Math.min(1, 0.5 + 1.15 * un + 0.03);
        var ax = g[0].axes({ x: [lo, hi], y: [lo, hi], title: "Training error against true error", xlabel: "true error", nx: 4, ny: 4 });
        ax.line([lo, hi], [lo, hi], { color: C.muted, width: 1, dash: [4, 4] });
        var step = Math.max(1, Math.ceil(K / 1200)), dx = [], dy = [];
        for (j = 0; j < K; j += step) { dx.push(tr[j]); dy.push(te[j]); }
        ax.dots(dx, dy, { color: C.spot, r: 1.8, alpha: 0.55 });
        var off = (hi - lo) * 0.035;
        ax.line([eb - un, eb + un], [eb - off, eb - off], { color: C.gain, width: 3 });
        ax.line([eb - wald, eb + wald], [eb, eb], { color: C.loss, width: 3 });
        ax.dots([tb], [eb], { color: C.idea, r: 5.5 });
        ax.legend([["the selected classifier", C.idea], ["Wald interval for its true error", C.loss], ["union-bound interval", C.gain]], { pos: "tl" });
        var ymax = Math.max(uni[uni.length - 1] * 1.15, 0.05);
        var bx = g[1].axes({ x: [1, KM], y: [-0.15 * ymax, ymax], logx: true, title: "Optimism of the selected classifier", xlabel: "classifiers searched", xfmt: function (x) { return x >= 10000 ? "10k" : String(x); } });
        bx.hline(0, { color: C.muted });
        bx.line(ks, uni, { color: C.gain, width: 2 });
        bx.line([1, KM], [wald, wald], { color: C.loss, width: 2 });
        bx.line(ks, opt, { color: C.idea, width: 2 });
        bx.vline(K, { color: C.ink });
        bx.legend([["true error − training error", C.idea], ["union-bound half-width", C.gain], ["Wald half-width", C.loss]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["K", String(s.out[0])], ["selected: training error", fmt(s.out[1], 3)], ["its true error", fmt(s.out[2], 3)], ["optimism", fmt(s.out[3], 3)],
          ["Wald interval covers", s.out[6] ? "yes" : "no"], ["union bound covers", s.out[7] ? "yes" : "no"]];
      },
      note: "Simulated data: the classifiers' training errors are independent, with a normal approximation to the binomial. The union-bound half-width is √(log(2K/0.05)/(2n)); it grows like √(log K), the price of a guarantee over the whole class. A fresh holdout would need no such price.",
    });
  };

  // ---- Part 55: Problem 2, the walk stopped at +1 --------------------------------------------------------------
  W.stoppedwalk = function (el) {
    QB.widget(el, {
      title: "Exam Problem 2: stop the walk when it first reaches +1",
      sub: "A fair ±1 walk stops at +1, or at a floor −a if there is one. Right: the mean of the stopped walk split into its parts, computed exactly. With a floor the parts settle and the mean stays 0. Remove the floor: every walk ends at +1, so the limit's mean is 1, yet at every finite time the few walks still far below carry exactly −1 of it.",
      panels: 2, height: 300,
      controls: [
        { k: "a", label: "Floor at −a", min: 1, max: 40, step: 1, value: 5, fmt: f0 },
        { k: "lm", label: "Time horizon m", min: 1, max: 3, step: 0.1, value: 2.5, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
      ],
      buttons: [{ label: "New walks", act: function (s) { s.seed++; } }, { label: "Floor on / off", act: function (s) { s.nofloor = !s.nofloor; } }],
      draw: function (g, v, s) {
        var m = Math.round(Math.pow(10, v.lm)), a = v.a, nof = !!s.nofloor, L = nof ? m : a - 1, i, t;
        var p = new Float64Array(L + 3), q = new Float64Array(L + 3), top = 0, fl = 0, et = 0, ts = [], gT = [], gF = [], gA = [], gS = [];
        p[0] = 1; // p[i]: probability of still walking at position -i
        for (t = 1; t <= m; t++) {
          var lim = Math.min(L, t), alive = 0, mean = 0;
          for (i = 0; i <= Math.min(L, t - 1); i++) alive += p[i];
          et += alive;
          top += 0.5 * p[0];
          if (!nof) fl += 0.5 * p[L];
          for (i = 0; i <= lim; i++) { q[i] = 0.5 * (i > 0 ? p[i - 1] : 0) + 0.5 * (i < L ? p[i + 1] : 0); mean -= i * q[i]; }
          var sw = p; p = q; q = sw;
          ts.push(t); gT.push(top); gF.push(-a * fl); gA.push(mean); gS.push(top - a * fl + mean);
        }
        s.out = [top, fl, top - a * fl + gA[m - 1], et, nof, a, m];
        var r = QB.rng(s.seed + 550), ylo = nof ? -Math.max(8, Math.round(2.2 * Math.sqrt(m))) : -(a + 1);
        var paths = [], last = 1;
        for (var w = 0; w < 12; w++) {
          var xs = [0], ys = [0], pos = 0, stride = Math.max(1, Math.floor(m / 400));
          for (t = 1; t <= m; t++) {
            pos += r() < 0.5 ? 1 : -1;
            var stop = pos === 1 || (!nof && pos === -a);
            if (stop || t % stride === 0 || t === m) { xs.push(t); ys.push(pos); }
            if (stop) break;
          }
          paths.push([xs, ys, pos]); last = Math.max(last, xs[xs.length - 1]);
        }
        var xmax = nof ? m : Math.min(m, Math.max(20, Math.ceil(1.15 * last)));
        var ax = g[0].axes({ x: [0, xmax], y: [ylo, 4.5], title: "Twelve walks, stopped", xlabel: "time", nx: 4 });
        ax.hline(1, { color: C.idea }); if (!nof) ax.hline(-a, { color: C.loss });
        paths.forEach(function (pa) {
          ax.line(pa[0], pa[1], { color: C.spot, width: 1.1, alpha: 0.75 });
          if (pa[2] === 1 || (!nof && pa[2] === -a)) ax.dots([pa[0][pa[0].length - 1]], [pa[2]], { color: pa[2] === 1 ? C.idea : C.loss, r: 3 });
        });
        ax.legend(nof ? [["stopped at +1", C.idea]] : [["stopped at +1", C.idea], ["stopped at the floor", C.loss]], { pos: "tr" });
        var bx = g[1].axes({ x: [1, m], y: [-1.25, 2.4], logx: true, title: "Where the mean of the stopped walk sits", xlabel: "time m" });
        bx.line(ts, gT, { color: C.idea, width: 2.2 });
        if (!nof) bx.line(ts, gF, { color: C.loss, width: 2.2 });
        bx.line(ts, gA, { color: C.spot, width: 2.2 });
        bx.line(ts, gS, { color: C.ink, width: 1.5, dash: [5, 4] });
        bx.legend((nof ? [] : [["−a × P(at the floor)", C.loss]]).concat([["+1 × P(stopped at +1)", C.idea], ["E[S; still walking]", C.spot], ["their sum: 0 at every m", C.ink]]), { pos: "tl" });
      },
      readout: function (v, s) {
        var z = Math.abs(s.out[2]) < 5e-4 ? 0 : s.out[2];
        return [["P(stopped at +1 by m)", fmt(s.out[0], 3)], ["P(stopped at the floor)", s.out[4] ? "no floor" : fmt(s.out[1], 3)], ["mean at time T ∧ m", fmt(z, 3)],
          ["E[T ∧ m]", fmt(s.out[3], 1)], ["E S_T in the limit", s.out[4] ? "1" : "0"], ["E T", s.out[4] ? "infinite" : String(s.out[5])]];
      },
      note: "Exact dynamic programming for the right panel and the readout; the twelve paths are simulated. With the floor, T is bounded in mean (E T = a) and optional stopping gives E S_T = 0, so P(reach +1) = a/(a + 1). Without it the stopped walk is not uniformly integrable, and E S_T = 1.",
    });
  };
})();
