// Interactives for Stage III, Master's: many variables, many questions, prediction and causes (Parts 31-36).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  function lgamma(x) { // Lanczos, for the Beta density
    var g = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
    var y = x, t = x + 5.5, s = 1.000000000190015, j;
    t -= (x + 0.5) * Math.log(t);
    for (j = 0; j < 6; j++) { y += 1; s += g[j] / y; }
    return -t + Math.log(2.5066282746310005 * s / x);
  }
  function jacobi(A, n) { // eigenvalues and eigenvectors of a symmetric matrix (rows of arrays), cyclic Jacobi
    var V = [], i, j, k, sweep;
    for (i = 0; i < n; i++) { V.push([]); for (j = 0; j < n; j++) V[i].push(i === j ? 1 : 0); }
    for (sweep = 0; sweep < 12; sweep++) {
      var off = 0;
      for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) off += A[i][j] * A[i][j];
      if (off < 1e-18) break;
      for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) {
        if (Math.abs(A[i][j]) < 1e-300) continue;
        var th = (A[j][j] - A[i][i]) / (2 * A[i][j]);
        var t = (th >= 0 ? 1 : -1) / (Math.abs(th) + Math.sqrt(th * th + 1)), c = 1 / Math.sqrt(t * t + 1), s = t * c;
        for (k = 0; k < n; k++) { var aki = A[k][i], akj = A[k][j]; A[k][i] = c * aki - s * akj; A[k][j] = s * aki + c * akj; }
        for (k = 0; k < n; k++) { var aik = A[i][k], ajk = A[j][k]; A[i][k] = c * aik - s * ajk; A[j][k] = s * aik + c * ajk; }
        for (k = 0; k < n; k++) { var vki = V[k][i], vkj = V[k][j]; V[k][i] = c * vki - s * vkj; V[k][j] = s * vki + c * vkj; }
      }
    }
    var order = [];
    for (i = 0; i < n; i++) order.push(i);
    order.sort(function (a, b) { return A[b][b] - A[a][a]; });
    return { val: order.map(function (o) { return A[o][o]; }), vec: function (r, kk) { return V[r][order[kk]]; } };
  }

  // ---- Part 31: a map from a table of distances --------------------------------------------------------------
  W.roadmapmds = function (el) {
    QB.widget(el, {
      title: "A map from a table of distances",
      sub: "Only the distances between the towns go in; classical scaling returns the gold map, turned to lie over the true one (grey rings). Make the roads wind and the map bends a little. Then corrupt one entry of the table: the map barely moves, and the entry shows up as the worst-fitting pair.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Towns", min: 8, max: 40, step: 1, value: 25, fmt: function (x) { return String(x); } },
        { k: "wind", label: "How much roads wind (up to)", min: 0, max: 0.6, step: 0.02, value: 0.2, fmt: function (x) { return pct(x, 0); } },
        { k: "bad", label: "One table entry multiplied by", min: 1, max: 3, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New island", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 310), n = v.n, i, j, P = [], D = [], u = [];
        for (i = 0; i < 40; i++) { P.push([0.6 + 8.8 * r(), 0.6 + 8.8 * r()]); u.push([]); }
        for (i = 0; i < 40; i++) for (j = i + 1; j < 40; j++) { u[i][j] = r(); }
        for (i = 0; i < n; i++) { D.push([]); for (j = 0; j < n; j++) D[i].push(0); }
        for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) {
          var d = Math.sqrt(Math.pow(P[i][0] - P[j][0], 2) + Math.pow(P[i][1] - P[j][1], 2)) * (1 + v.wind * u[i][j]);
          if (i === 0 && j === 1) d *= v.bad;
          D[i][j] = d; D[j][i] = d;
        }
        // double-centre -D^2/2
        var rowm = [], tot = 0, B = [];
        for (i = 0; i < n; i++) { var sm = 0; for (j = 0; j < n; j++) sm += D[i][j] * D[i][j]; rowm.push(sm / n); tot += sm; }
        tot /= n * n;
        for (i = 0; i < n; i++) { B.push([]); for (j = 0; j < n; j++) B[i].push(-0.5 * (D[i][j] * D[i][j] - rowm[i] - rowm[j] + tot)); }
        var e = jacobi(B, n), pos = 0, neg = 0;
        for (i = 0; i < n; i++) { if (e.val[i] > 0) pos += e.val[i]; else neg -= e.val[i]; }
        pos = Math.max(pos, 1e-12);
        var X = [], l1 = Math.sqrt(Math.max(e.val[0], 0)), l2 = Math.sqrt(Math.max(e.val[1], 0));
        for (i = 0; i < n; i++) X.push([e.vec(i, 0) * l1, e.vec(i, 1) * l2]);
        // Procrustes: rotate or reflect, scale and shift the map onto the truth
        var ma = [0, 0], mb = [0, 0];
        for (i = 0; i < n; i++) { ma[0] += P[i][0] / n; ma[1] += P[i][1] / n; mb[0] += X[i][0] / n; mb[1] += X[i][1] / n; }
        var best = null;
        [1, -1].forEach(function (flip) {
          var cc = 0, ss = 0, bb = 0;
          for (var q = 0; q < n; q++) {
            var ax = P[q][0] - ma[0], ay = P[q][1] - ma[1], bx = X[q][0] - mb[0], by = flip * (X[q][1] - mb[1]);
            cc += ax * bx + ay * by; ss += ay * bx - ax * by; bb += bx * bx + by * by;
          }
          var val = Math.sqrt(cc * cc + ss * ss);
          if (!best || val > best.val) best = { val: val, th: Math.atan2(ss, cc), flip: flip, sc: val / Math.max(bb, 1e-12) };
        });
        var F = [], se = 0, co = Math.cos(best.th), si = Math.sin(best.th);
        for (i = 0; i < n; i++) {
          var bx = X[i][0] - mb[0], by = best.flip * (X[i][1] - mb[1]);
          F.push([ma[0] + best.sc * (bx * co - by * si), ma[1] + best.sc * (bx * si + by * co)]);
          se += Math.pow(F[i][0] - P[i][0], 2) + Math.pow(F[i][1] - P[i][1], 2);
        }
        var worst = { gap: -1, i: 0, j: 1, table: 0, map: 0 };
        for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) {
          var dm = Math.sqrt(Math.pow(X[i][0] - X[j][0], 2) + Math.pow(X[i][1] - X[j][1], 2));
          if (Math.abs(dm - D[i][j]) > worst.gap) worst = { gap: Math.abs(dm - D[i][j]), i: i, j: j, table: D[i][j], map: dm };
        }
        s.out = { rmse: Math.sqrt(se / n), two: (Math.max(e.val[0], 0) + Math.max(e.val[1], 0)) / pos, neg: neg / pos, worst: worst };
        var a = g[0].axes({ x: [-1, 11], y: [-1, 13.5], title: "The island: truth and the rebuilt map" });
        for (i = 0; i < n; i++) a.line([P[i][0], F[i][0]], [P[i][1], F[i][1]], { color: C.muted, width: 1 });
        a.line([F[worst.i][0], F[worst.j][0]], [F[worst.i][1], F[worst.j][1]], { color: C.loss, width: 2 });
        a.dots(P.slice(0, n).map(function (p) { return p[0]; }), P.slice(0, n).map(function (p) { return p[1]; }), { color: C.cash, r: 5, alpha: 0.45 });
        a.dots(F.map(function (p) { return p[0]; }), F.map(function (p) { return p[1]; }), { color: C.idea, r: 3 });
        a.legend([["true position", C.cash], ["rebuilt from distances", C.idea], ["worst-fitting pair", C.loss]], { pos: "tl" });
        var m = Math.min(n, 40), xs = [], hs = [], top = Math.max(e.val[0], 1e-9), low = Math.min(e.val[n - 1], 0);
        for (i = 0; i < m; i++) { xs.push(i + 1); hs.push(e.val[i]); }
        var b = g[1].axes({ x: [0, m + 1], y: [Math.min(-0.05 * top, 1.15 * low), 1.1 * top], title: "Eigenvalues of the double-centred table", xlabel: "rank" });
        b.bars(xs, hs, 0.8, { color: function (k) { return k < 2 ? C.idea : hs[k] >= 0 ? C.spot : C.loss; } });
        b.hline(0, { color: C.muted, dash: [] });
        b.legend([["the map's two dimensions", C.idea], ["further positive", C.spot], ["negative: not Euclidean", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out, w = o.worst;
        return [["map error (RMSE, island 10 across)", fmt(o.rmse, 2)], ["share of positive eigenvalues in two dimensions", pct(o.two, 1)],
          ["negative eigenvalues, share of positive", pct(o.neg, 1)],
          ["worst pair", "towns " + (w.i + 1) + " and " + (w.j + 1) + ": table " + fmt(w.table, 1) + ", map " + fmt(w.map, 1)]];
      },
      note: "Simulated island. Each distance is the straight line stretched by its own random factor (a stand-in for a road network); the corrupted entry is the distance between towns 1 and 2. With no winding and no corruption the table is Euclidean and the map is exact.",
    });
  };

  // ---- Part 32: an lq budget meets the least-squares contours ------------------------------------------------
  W.lqcorner = function (el) {
    var NB = 720;
    function solve(q, t, rho, b1, b2) { // minimize the quadratic loss over the lq ball of radius t
      var inside = Math.pow(Math.abs(b1), q) + Math.pow(Math.abs(b2), q) <= Math.pow(t, q);
      if (inside) return [b1, b2, 0];
      var best = Infinity, out = [0, 0, 0], k;
      for (k = 0; k < NB; k++) {
        var c = k % (NB / 4) === 0 && (k / (NB / 4)) % 2 === 1 ? 0 : Math.cos(2 * Math.PI * k / NB);
        var sn = k % (NB / 2) === 0 ? 0 : Math.sin(2 * Math.PI * k / NB);
        var rr = t / Math.pow(Math.pow(Math.abs(c), q) + Math.pow(Math.abs(sn), q), 1 / q);
        var x = rr * c, y = rr * sn, dx = x - b1, dy = y - b2, loss = dx * dx + 2 * rho * dx * dy + dy * dy;
        if (loss < best) { best = loss; out = [x, y, loss]; }
      }
      return out;
    }
    QB.widget(el, {
      title: "Why an l1 budget gives exact zeros",
      sub: "The gold dot is the least-squares estimate and the ellipses are its contours of equal fit. The solution (white) is the first point of the blue budget region the growing ellipse touches. At q = 1 it sits on a corner, with one coefficient exactly zero; slide q to 2 and the zero is gone.",
      panels: 2, height: 310,
      controls: [
        { k: "q", label: "Exponent q of the budget |b1|^q + |b2|^q", min: 0.5, max: 2, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "t", label: "Budget (radius of the ball)", min: 0.1, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "b2", label: "Least-squares b2 (b1 is 2)", min: 0, max: 2.5, step: 0.05, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "rho", label: "Correlation of the two predictors", min: -0.9, max: 0.9, step: 0.05, value: 0.3, fmt: function (x) { return fmt(x, 2); } },
      ],
      draw: function (g, v, s) {
        var q = v.q, sol = solve(q, v.t, v.rho, 2, v.b2), k, bx = [], by = [];
        for (k = 0; k <= 360; k++) {
          var c = Math.cos(2 * Math.PI * k / 360), sn = Math.sin(2 * Math.PI * k / 360);
          var rr = v.t / Math.pow(Math.pow(Math.abs(c), q) + Math.pow(Math.abs(sn), q), 1 / q);
          bx.push(rr * c); by.push(rr * sn);
        }
        var a = g[0].axes({ x: [-3.2, 3.2], y: [-3.2, 3.2], title: "The budget region and the contours of fit", xlabel: "b1" });
        a.hline(0, { color: C.line, dash: [] }); a.vline(0, { color: C.line, dash: [] });
        a.clip(function (ctx) {
          ctx.fillStyle = C.spot; ctx.globalAlpha = 0.22; ctx.beginPath();
          for (var i = 0; i < bx.length; i++) { if (i) ctx.lineTo(a.px(bx[i]), a.py(by[i])); else ctx.moveTo(a.px(bx[i]), a.py(by[i])); }
          ctx.closePath(); ctx.fill();
        });
        a.line(bx, by, { color: C.spot, width: 1.6 });
        var lev = Math.sqrt(Math.max(sol[2], 0)), levels = [lev, lev * 0.5, lev * 1.5 + 0.4];
        levels.forEach(function (cl, idx) {
          if (cl < 1e-6) return;
          var ex = [], ey = [];
          for (var i = 0; i <= 120; i++) {
            var th = 2 * Math.PI * i / 120, p = cl * Math.cos(th) / Math.sqrt(1 + v.rho), m = cl * Math.sin(th) / Math.sqrt(1 - v.rho);
            ex.push(2 + (p + m) / Math.SQRT2); ey.push(v.b2 + (p - m) / Math.SQRT2);
          }
          a.line(ex, ey, { color: C.idea, width: idx === 0 ? 1.8 : 1, alpha: idx === 0 ? 1 : 0.45 });
        });
        a.dots([2], [v.b2], { color: C.idea, r: 4.5 });
        a.dots([sol[0]], [sol[1]], { color: C.ink, r: 4.5 });
        a.text(-3.05, 2.85, "b2", { color: C.muted });
        a.legend([["budget region", C.spot], ["least squares and its contours", C.idea], ["constrained solution", C.ink]], { pos: "bl" });
        var ts = [], p1 = [], p2 = [], zeros = 0, nt = 40;
        for (k = 0; k <= nt; k++) {
          var tt = 0.02 + 2.98 * k / nt, so = solve(q, tt, v.rho, 2, v.b2);
          ts.push(tt); p1.push(so[0]); p2.push(so[1]);
          if (Math.abs(so[0]) < 1e-9 || Math.abs(so[1]) < 1e-9) zeros++;
        }
        var b = g[1].axes({ x: [0, 3], y: [-0.6, 2.6], title: "The path as the budget grows", xlabel: "budget" });
        b.hline(0, { color: C.muted });
        b.line(ts, p1, { color: C.realized, width: 2 }); b.line(ts, p2, { color: C.option, width: 2 });
        b.vline(v.t, { color: C.ink });
        b.legend([["b1", C.realized], ["b2", C.option], ["the budget now", C.ink]], { pos: "tl" });
        s.out = { sol: sol, z: (Math.abs(sol[0]) < 1e-9 ? 1 : 0) + (Math.abs(sol[1]) < 1e-9 ? 1 : 0), share: zeros / (nt + 1) };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["solution b1", fmt(o.sol[0], 2)], ["solution b2", fmt(o.sol[1], 2)], ["coefficients exactly zero", String(o.z)],
          ["share of budgets with an exact zero", pct(o.share, 0)]];
      },
      note: "The fit is (b − b̂)ᵀ Σ (b − b̂) with unit variances and the chosen correlation. q = 1 is the lasso, q = 2 ridge; below 1 the region is not convex, which is why best subset (q → 0) is hard. The solution is found by searching 720 points of the boundary.",
    });
  };

  // ---- Part 33: the p-value sea and the Benjamini-Hochberg line ---------------------------------------------
  W.bhsea = function (el) {
    var M = 200, STUDIES = 200;
    function study(r, m1, eff, rho, q) {
      var shared = Math.sqrt(rho) * r.normal(), sc = Math.sqrt(1 - rho), p = [], i;
      for (i = 0; i < M; i++) { var z = shared + sc * r.normal() + (i < m1 ? eff : 0); p.push({ p: 1 - QB.cdf(z), real: i < m1 }); }
      p.sort(function (a, b) { return a.p - b.p; });
      var k = 0, V = 0, bon = 0;
      for (i = 0; i < M; i++) { if (p[i].p <= q * (i + 1) / M) k = i + 1; if (p[i].p <= q / M) bon++; }
      for (i = 0; i < k; i++) if (!p[i].real) V++;
      return { p: p, k: k, V: V, bon: bon, fdp: k ? V / k : 0 };
    }
    var buf = new Float64Array(M), raw = new Float64Array(M);
    function quick(r, m1, eff, rho, q) { // the same study, keeping only its count of discoveries and false ones
      var shared = Math.sqrt(rho) * r.normal(), sc = Math.sqrt(1 - rho), i, k = 0, V = 0;
      for (i = 0; i < M; i++) { raw[i] = 1 - QB.cdf(shared + sc * r.normal() + (i < m1 ? eff : 0)); buf[i] = raw[i]; }
      buf.sort();
      for (i = 0; i < M; i++) if (buf[i] <= q * (i + 1) / M) k = i + 1;
      if (k) { for (i = m1; i < M; i++) if (raw[i] <= buf[k - 1]) V++; }
      return { k: k, fdp: k ? V / k : 0 };
    }
    QB.widget(el, {
      title: "Two hundred questions and the Benjamini-Hochberg line",
      sub: "Left: one study's smallest p-values in order, real effects blue and true nulls red. Everything up to the last point under the gold line is a discovery. Right: the share of false discoveries in 200 such studies. Add a shared factor and the average stays under q while single studies scatter.",
      panels: 2, height: 310,
      controls: [
        { k: "m1", label: "Real effects among 200 tests", min: 0, max: 60, step: 5, value: 20, fmt: function (x) { return String(x); } },
        { k: "eff", label: "Size of a real effect (in standard errors)", min: 0, max: 5, step: 0.1, value: 3, fmt: function (x) { return x.toFixed(1); } },
        { k: "q", label: "Target false discovery rate q", min: 0.01, max: 0.3, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "rho", label: "Correlation between tests (one shared factor)", min: 0, max: 0.8, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New study", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var one = study(QB.rng(s.seed + 330), v.m1, v.eff, v.rho, v.q), show = 80, i;
        var ymax = Math.max(0.02, 2 * v.q * show / M), xr = [], yr = [], xn = [], yn = [];
        for (i = 0; i < show; i++) { if (one.p[i].real) { xr.push(i + 1); yr.push(one.p[i].p); } else { xn.push(i + 1); yn.push(one.p[i].p); } }
        var a = g[0].axes({ x: [0, show + 1], y: [0, ymax], title: "This study: the 80 smallest p-values", xlabel: "rank" });
        a.line([0, show], [0, v.q * show / M], { color: C.idea, width: 2 });
        a.hline(v.q / M, { color: C.cash });
        if (one.k) a.vline(one.k + 0.5, { color: C.ink });
        a.dots(xr, yr, { color: C.spot, r: 2.8 }); a.dots(xn, yn, { color: C.loss, r: 2.8 });
        a.legend([["real effect", C.spot], ["true null", C.loss], ["BH line: q × rank / 200", C.idea], ["Bonferroni: q / 200", C.cash]], { pos: "tl" });
        var r = QB.rng(977), fd = [], mean = 0, big = 0, none = 0;
        for (i = 0; i < STUDIES; i++) { var st = quick(r, v.m1, v.eff, v.rho, v.q); fd.push(st.fdp); mean += st.fdp / STUDIES; if (st.fdp > 2 * v.q) big++; if (!st.k) none++; }
        var nb = 25, h = QB.hist(fd.map(function (x) { return Math.min(x, 0.9999); }), 0, 1, nb), top = 1, xs = [];
        for (i = 0; i < nb; i++) { xs.push((i + 0.5) / nb); top = Math.max(top, h[i]); }
        var b = g[1].axes({ x: [0, 1], y: [0, top * 1.15], title: "False discovery proportion in 200 studies", xlabel: "share of a study's discoveries that are false" });
        b.bars(xs, h, 1 / nb, { color: C.spot });
        b.vline(v.q, { color: C.idea }); b.vline(mean, { color: C.ink, dash: [] });
        b.legend([["target q", C.idea], ["average over the studies", C.ink]], { pos: "tr" });
        s.out = { one: one, mean: mean, big: big / STUDIES, none: none / STUDIES };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["BH discoveries", String(o.one.k)], ["of them false", String(o.one.V)], ["Bonferroni discoveries", String(o.one.bon)],
          ["average FDP over 200 studies", fmt(o.mean, 3) + " (π0·q = " + fmt((1 - v.m1 / M) * v.q, 3) + ")"],
          ["studies with FDP above 2q", pct(o.big, 0)], ["studies with no discovery", pct(o.none, 0)]];
      },
      note: "Simulated data: one-sided z-tests, nulls N(0, 1), real effects shifted, every pair of tests equally correlated. A study with no discoveries counts as FDP 0. Benjamini-Hochberg's rate is π0·q for independent tests and at most that under this kind of positive dependence.",
    });
  };

  // ---- Part 34: the score ladder -------------------------------------------------------------------------------
  W.scoreladder = function (el) {
    var SETS = 300;
    QB.widget(el, {
      title: "The score ladder: what a conformal 90% promises",
      sub: "Left: one calibration set's scores, sorted; the gold bar at rank ⌈(n+1)(1−α)⌉ is the threshold. Right: the coverage that threshold gives new cases, over 300 calibration sets, against its Beta law. Grow n and the spread narrows. Then make test cases noisier than calibration cases and the promise fails.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Calibration cases n", min: 19, max: 199, step: 10, value: 19, fmt: function (x) { return String(x); } },
        { k: "alpha", label: "Miscoverage α", min: 0.05, max: 0.5, step: 0.05, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "shift", label: "Test noise ÷ calibration noise", min: 0.5, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New calibration set", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, k = Math.min(n, Math.ceil((n + 1) * (1 - v.alpha) - 1e-9)), i, j;
        var scores = function (r) { var o = []; for (var t = 0; t < n; t++) o.push(Math.abs(r.normal())); o.sort(function (a, b) { return a - b; }); return o; };
        var cover = function (q) { return 2 * QB.cdf(q / v.shift) - 1; };
        var sc = scores(QB.rng(s.seed + 340)), q = sc[k - 1], xs = [];
        for (i = 0; i < n; i++) xs.push(i + 1);
        var a = g[0].axes({ x: [0, n + 1], y: [0, Math.max(3, sc[n - 1] * 1.08)], title: "Calibration scores, sorted", xlabel: "rank" });
        a.bars(xs, sc, 0.82, { color: function (t) { return t === k - 1 ? C.idea : C.spot; }, gap: n > 80 ? 0 : 1 });
        a.hline(q, { color: C.idea });
        a.text(1, q, "threshold: rank " + k + " of " + n, { color: C.idea, dy: -10, bg: true });
        var r = QB.rng(4711), cov = [], mean = 0;
        for (j = 0; j < SETS; j++) { var c = cover(scores(r)[k - 1]); cov.push(c); mean += c / SETS; }
        var nb = 40, h = QB.hist(cov.map(function (x) { return Math.min(x, 0.99999); }), 0, 1, nb), dens = [], top = 0, bx = [];
        for (i = 0; i < nb; i++) { dens.push(h[i] * nb / SETS); bx.push((i + 0.5) / nb); top = Math.max(top, dens[i]); }
        var gx = QB.linspace(0.002, 0.998, 250), lc = lgamma(n + 1) - lgamma(k) - lgamma(n + 1 - k);
        var gy = gx.map(function (x) { return Math.exp(lc + (k - 1) * Math.log(x) + (n - k) * Math.log(1 - x)); });
        for (i = 0; i < gy.length; i++) top = Math.max(top, gy[i]);
        var b = g[1].axes({ x: [0, 1], y: [0, top * 1.12], title: "Coverage given the calibration set", xlabel: "coverage" });
        b.bars(bx, dens, 1 / nb, { color: C.spot, alpha: 0.7 });
        b.line(gx, gy, { color: C.idea, width: 2 });
        b.vline(1 - v.alpha, { color: C.cash }); b.vline(cover(q), { color: C.ink, dash: [] });
        b.legend([["300 calibration sets", C.spot], ["Beta(k, n+1−k): exchangeable", C.idea], ["nominal 1 − α", C.cash], ["the set on the left", C.ink]], { pos: "tl" });
        s.out = { k: k, q: q, c: cover(q), mean: mean };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["rank k", o.k + " of " + v.n], ["threshold", fmt(o.q, 2)], ["coverage with this calibration set", pct(o.c, 1)],
          ["average over calibration sets", pct(o.mean, 1)], ["promised if exchangeable", pct(o.k / (v.n + 1), 1) + " (at least " + pct(1 - v.alpha, 0) + ")"]];
      },
      note: "Simulated data: scores are absolute standard normal errors, so the coverage a threshold gives is known exactly. The guarantee is an average over calibration sets and needs calibration and test cases to be exchangeable; the Beta curve is the law of coverage when they are.",
    });
  };

  // ---- Part 35: a science table and who assigns the treatment ------------------------------------------------
  W.sciencecoin = function (el) {
    var REPS = 400;
    function table(n, sdTau) { // fixed potential outcomes: the science
      var r = QB.rng(3507), base = [], y0 = [], y1 = [], i;
      for (i = 0; i < 200; i++) {
        var b = r.normal(), e0 = r.normal(), et = r.normal();
        base.push(b); y0.push(148 + 8.4 * b + 8 * e0); y1.push(y0[i] - 8 + sdTau * (-0.6 * b + 0.8 * et));
      }
      return { base: base.slice(0, n), y0: y0.slice(0, n), y1: y1.slice(0, n) };
    }
    function assign(r, T, n, sel) { // treat the half with the highest score: baseline (doctor) mixed with noise (coin)
      var sc = [], i, z = new Array(n).fill(0);
      for (i = 0; i < n; i++) sc.push([sel * T.base[i] + (1 - sel) * r.normal(), i]);
      sc.sort(function (a, b) { return b[0] - a[0]; });
      for (i = 0; i < n / 2; i++) z[sc[i][1]] = 1;
      return z;
    }
    function estimate(T, z, n) { var a = 0, b = 0; for (var i = 0; i < n; i++) { if (z[i]) a += T.y1[i]; else b += T.y0[i]; } return (a - b) / (n / 2); }
    function variance(x) { var m = QB.mean(x), s = 0; for (var i = 0; i < x.length; i++) s += (x[i] - m) * (x[i] - m); return s / (x.length - 1); }
    QB.widget(el, {
      title: "Both outcomes of every patient, and who chooses",
      sub: "Each patient has a blood pressure without the drug (blue) and with it (gold); an assignment shows one and hides the other (faint). Press New assignment a few times with a coin: the estimates scatter around the true average effect. Then let the doctor treat the patients with the highest baseline and watch the whole histogram move.",
      panels: 2, height: 310,
      controls: [
        { k: "sel", label: "Who assigns: coin (0) to doctor (1)", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "sd", label: "SD of the individual effects (mm Hg)", min: 0, max: 12, step: 0.5, value: 5, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Patients", min: 20, max: 200, step: 20, value: 40, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New assignment", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, T = table(n, v.sd), i, tau = [];
        for (i = 0; i < n; i++) tau.push(T.y1[i] - T.y0[i]);
        var sate = QB.mean(tau), z = assign(QB.rng(s.seed + 350), T, n, v.sel), est = estimate(T, z, n);
        var order = []; for (i = 0; i < n; i++) order.push(i);
        order.sort(function (p, q) { return T.base[p] - T.base[q]; });
        var a = g[0].axes({ x: [0, n + 1], y: [108, 196], title: "The science table, ordered by baseline", xlabel: "patient (lowest baseline to highest)" });
        var sx = [], sy = [], hx = [], hy = [], scol = [], hcol = [];
        for (i = 0; i < n; i++) {
          var u = order[i];
          a.line([i + 1, i + 1], [T.y0[u], T.y1[u]], { color: C.muted, width: 1, alpha: 0.5 });
          sx.push(i + 1); sy.push(z[u] ? T.y1[u] : T.y0[u]); scol.push(z[u] ? C.idea : C.spot);
          hx.push(i + 1); hy.push(z[u] ? T.y0[u] : T.y1[u]); hcol.push(z[u] ? C.spot : C.idea);
        }
        var rad = n > 100 ? 2 : 3;
        a.dots(hx, hy, { color: function (k) { return hcol[k]; }, r: rad, alpha: 0.22 });
        a.dots(sx, sy, { color: function (k) { return scol[k]; }, r: rad });
        a.legend([["Y(0): without the drug", C.spot], ["Y(1): with the drug", C.idea]], { pos: "tl" });
        var r = QB.rng(8123), ests = [];
        for (i = 0; i < REPS; i++) ests.push(estimate(T, assign(r, T, n, v.sel), n));
        var lo = -26, hi = 14, nb = 40, h = QB.hist(ests.map(function (x) { return Math.max(lo, Math.min(hi - 1e-6, x)); }), lo, hi, nb), xs = [], top = 1;
        for (i = 0; i < nb; i++) { xs.push(lo + (i + 0.5) * (hi - lo) / nb); top = Math.max(top, h[i]); }
        var b = g[1].axes({ x: [lo, hi], y: [0, top * 1.2], title: "Difference in means over 400 assignments", xlabel: "estimated effect (mm Hg)" });
        b.bars(xs, h, (hi - lo) / nb, { color: C.spot, alpha: 0.75 });
        b.vline(sate, { color: C.idea, dash: [], width: 2 }); b.vline(Math.max(lo, Math.min(hi, est)), { color: C.ink });
        b.legend([["true average effect", C.idea], ["this assignment", C.ink]], { pos: "tr" });
        var s1 = variance(T.y1), s0 = variance(T.y0), st = variance(tau), half = n / 2;
        s.out = { sate: sate, est: est, mean: QB.mean(ests), sd: Math.sqrt(variance(ests)), exact: Math.sqrt(Math.max(0, s1 / half + s0 / half - st / n)), cons: Math.sqrt(s1 / half + s0 / half) };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["true average effect", fmt(o.sate, 2)], ["this assignment's estimate", fmt(o.est, 2)],
          ["average estimate over 400 assignments", fmt(o.mean, 2)], ["SD of the estimates", fmt(o.sd, 2)],
          ["Neyman's SD under a coin: exact, conservative", fmt(o.exact, 2) + ", " + fmt(o.cons, 2)]];
      },
      note: "Simulated patients; no real trial shows both outcomes. Half the patients are treated: those with the highest score, a mix of baseline pressure (the doctor) and noise (the coin). Neyman's exact variance is S1²/n1 + S0²/n0 − Sτ²/n; the conservative one drops the last term, which grows with the SD of the effects.",
    });
  };

  // ---- Part 36: double robustness --------------------------------------------------------------------------------
  W.twochances = function (el) {
    var REPS = 120, TAU = 2;
    function fitArm(x, y, quad) { // least squares of y on (1, x) or (1, x, x^2); returns a predictor
      var p = quad ? 3 : 2, A = [], bv = [], i, j, k;
      for (i = 0; i < p; i++) { A.push(new Array(p).fill(0)); bv.push(0); }
      for (k = 0; k < x.length; k++) {
        var f = [1, x[k], x[k] * x[k]];
        for (i = 0; i < p; i++) { bv[i] += f[i] * y[k]; for (j = 0; j < p; j++) A[i][j] += f[i] * f[j]; }
      }
      for (i = 0; i < p; i++) A[i][i] += 1e-6;
      for (i = 0; i < p; i++) { // Gaussian elimination (the matrix is positive definite)
        for (j = i + 1; j < p; j++) { var m = A[j][i] / A[i][i]; for (k = i; k < p; k++) A[j][k] -= m * A[i][k]; bv[j] -= m * bv[i]; }
      }
      var c = new Array(p).fill(0);
      for (i = p - 1; i >= 0; i--) { var sm = bv[i]; for (j = i + 1; j < p; j++) sm -= A[i][j] * c[j]; c[i] = sm / A[i][i]; }
      return function (xx) { return c[0] + c[1] * xx + (quad ? c[2] * xx * xx : 0); };
    }
    function sample(r, n, conf) {
      var x = [], t = [], y = [], e = [], n1 = 0, i;
      for (i = 0; i < n; i++) {
        var xi = -2 + 4 * r(), ei = Math.min(0.995, Math.max(0.005, 1 / (1 + Math.exp(-conf * (xi * xi - 1.3))))), ti = r() < ei ? 1 : 0;
        x.push(xi); e.push(ei); t.push(ti); n1 += ti; y.push(TAU * ti + 3 * xi * xi + r.normal());
      }
      if (n1 < 3) { for (i = 0; i < 3; i++) { if (!t[i]) { t[i] = 1; y[i] += TAU; } } }       // keep both arms fittable
      if (n - n1 < 3) { for (i = 0; i < 3; i++) { if (t[i]) { t[i] = 0; y[i] -= TAU; } } }
      return { x: x, t: t, y: y, e: e };
    }
    function analyse(d, outRight, psRight) {
      var n = d.x.length, x1 = [], y1 = [], x0 = [], y0 = [], i, share = 0;
      for (i = 0; i < n; i++) { if (d.t[i]) { x1.push(d.x[i]); y1.push(d.y[i]); } else { x0.push(d.x[i]); y0.push(d.y[i]); } share += d.t[i] / n; }
      share = Math.min(0.99, Math.max(0.01, share));
      var m1 = fitArm(x1, y1, outRight), m0 = fitArm(x0, y0, outRight), gc = 0, w1 = 0, w0 = 0, a1 = 0, a0 = 0, dr = 0;
      for (i = 0; i < n; i++) {
        var e = psRight ? d.e[i] : share, mu1 = m1(d.x[i]), mu0 = m0(d.x[i]);
        gc += (mu1 - mu0) / n;
        if (d.t[i]) { w1 += 1 / e; a1 += d.y[i] / e; dr += (d.y[i] - mu1) / e / n; } else { w0 += 1 / (1 - e); a0 += d.y[i] / (1 - e); dr -= (d.y[i] - mu0) / (1 - e) / n; }
      }
      return { gc: gc, ipw: a1 / w1 - a0 / w0, aipw: gc + dr, m1: m1, m0: m0 };
    }
    var word = function (x) { return x ? "right" : "wrong"; };
    QB.widget(el, {
      title: "Two chances to be right",
      sub: "Doctors treat patients at the extremes of x more often, and the outcome rises with x². Each estimator is run on 120 simulated studies; the truth is 2. Set one model wrong and the method that relies on it drifts off while the doubly robust estimate stays. Set both wrong and nothing is left.",
      panels: 2, height: 310,
      controls: [
        { k: "out", label: "Outcome model (wrong: straight line in x; right: with x²)", min: 0, max: 1, step: 1, value: 0, fmt: word },
        { k: "ps", label: "Propensity model (wrong: constant; right: the true one)", min: 0, max: 1, step: 1, value: 1, fmt: word },
        { k: "conf", label: "Strength of confounding", min: 0, max: 2, step: 0.1, value: 0.8, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Patients per study", min: 100, max: 600, step: 100, value: 300, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New studies", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 360), d = sample(r, v.n, v.conf), one = analyse(d, v.out, v.ps), i;
        var a = g[0].axes({ x: [-2, 2], y: [-3, 18], title: "One study, with the fitted outcome curves", xlabel: "x" });
        var x0 = [], y0 = [], x1 = [], y1 = [];
        for (i = 0; i < v.n; i++) { if (d.t[i]) { x1.push(d.x[i]); y1.push(d.y[i]); } else { x0.push(d.x[i]); y0.push(d.y[i]); } }
        a.dots(x0, y0, { color: C.spot, r: 2, alpha: 0.6 }); a.dots(x1, y1, { color: C.idea, r: 2, alpha: 0.6 });
        var gx = QB.linspace(-2, 2, 60);
        a.line(gx, gx.map(one.m0), { color: C.spot, width: 2 }); a.line(gx, gx.map(one.m1), { color: C.idea, width: 2 });
        a.legend([["untreated", C.spot], ["treated", C.idea]], { pos: "tl" });
        var rows = [["gc", C.realized, 3], ["ipw", C.implied, 2], ["aipw", C.gain, 1]], est = { gc: [], ipw: [], aipw: [] }, naive = 0;
        for (i = 0; i < REPS; i++) {
          var dd = sample(r, v.n, v.conf), o = analyse(dd, v.out, v.ps), n1 = 0, s1 = 0, s0 = 0, k;
          est.gc.push(o.gc); est.ipw.push(o.ipw); est.aipw.push(o.aipw);
          for (k = 0; k < v.n; k++) { if (dd.t[k]) { n1++; s1 += dd.y[k]; } else s0 += dd.y[k]; }
          naive += (s1 / n1 - s0 / (v.n - n1)) / REPS;
        }
        var b = g[1].axes({ x: [-1, 8], y: [0.4, 5.7], title: "Estimates in 120 studies", xlabel: "estimated average effect", noY: true });
        b.vline(TAU, { color: C.ink, dash: [], width: 1.5 }); b.vline(Math.max(-1, Math.min(8, naive)), { color: C.loss });
        var jr = QB.rng(55);
        rows.forEach(function (row) {
          var xs = est[row[0]].map(function (x) { return Math.max(-0.95, Math.min(7.95, x)); }), ys = xs.map(function () { return row[2] + 0.5 * (jr() - 0.5); });
          b.dots(xs, ys, { color: row[1], r: 2.2, alpha: 0.7 });
        });
        b.legend([["outcome model", C.realized], ["weighting", C.implied], ["doubly robust (AIPW)", C.gain], ["truth", C.ink], ["no adjustment", C.loss]], { pos: "tr" });
        s.out = { gc: QB.mean(est.gc), ipw: QB.mean(est.ipw), aipw: QB.mean(est.aipw), naive: naive };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["truth", fmt(TAU, 2)], ["no adjustment", fmt(o.naive, 2)], ["outcome model", fmt(o.gc, 2)], ["weighting", fmt(o.ipw, 2)], ["doubly robust", fmt(o.aipw, 2)]];
      },
      note: "Simulated data: x uniform on (−2, 2), treatment probability logistic in x², outcome 2·treatment + 3x² + noise. Readout values are averages over the 120 studies. The right propensity model here is the true one; with strong confounding its weights are large and the weighted estimates scatter, the price of thin overlap.",
    });
  };
})();
