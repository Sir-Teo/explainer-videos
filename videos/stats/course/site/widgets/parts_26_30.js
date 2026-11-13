// Interactives for Stage III, Master's: Bayes, computation, model choice, smoothing and robustness (Parts 26-30).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 26: the eight schools' tau explorer -----------------------------------------------------------------
  W.schoolstau = function (el) {
    var Y = [28, 8, -3, 7, -1, 1, 18, 12], S = [15, 10, 16, 11, 9, 11, 10, 18], NAMES = "ABCDEFGH";
    var COL = [C.idea, C.spot, C.loss, C.gain, C.q, C.implied, C.realized, C.option];
    var pooled = function (y, s, tau) { // the precision-weighted mean of the schools given tau, and its variance
      var sw = 0, swy = 0, j, w;
      for (j = 0; j < 8; j++) { w = 1 / (s[j] * s[j] + tau * tau); sw += w; swy += w * y[j]; }
      return { mu: swy / sw, v: 1 / sw };
    };
    QB.widget(el, {
      title: "The tau explorer: how much the eight schools pool",
      sub: "Left: each school's estimate given the between-school spread tau, from one pooled number at tau = 0 out to the schools' own estimates. Right: what the data say about tau under a flat prior. Slide the cursor, then shrink the standard errors and watch the posterior leave zero.",
      panels: 2, height: 310,
      controls: [
        { k: "tau", label: "Cursor: tau", min: 0, max: 30, step: 0.5, value: 5, fmt: function (x) { return x.toFixed(1); } },
        { k: "se", label: "Standard errors, times", min: 0.3, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "ya", label: "School A's estimate", min: -10, max: 60, step: 1, value: 28, fmt: function (x) { return fmt(x, 0); } },
      ],
      draw: function (g, v, s) {
        var y = Y.slice(), sg = S.map(function (x) { return x * v.se; }), i, j;
        y[0] = v.ya;
        var n = 601, top = 150, taus = QB.linspace(0, top, n), lp = [], m = -1e300;
        for (i = 0; i < n; i++) { // log p(tau | y) with mu integrated out, flat priors
          var p = pooled(y, sg, taus[i]), l = 0.5 * Math.log(p.v);
          for (j = 0; j < 8; j++) { var V = sg[j] * sg[j] + taus[i] * taus[i]; l += -0.5 * Math.log(V) - 0.5 * (y[j] - p.mu) * (y[j] - p.mu) / V; }
          lp.push(l); if (l > m) m = l;
        }
        var dens = lp.map(function (l) { return Math.exp(l - m); }), h = top / (n - 1), cum = [0], tot;
        for (i = 1; i < n; i++) cum.push(cum[i - 1] + 0.5 * h * (dens[i] + dens[i - 1]));
        tot = cum[n - 1];
        var med = 0, below = 0;
        for (i = 1; i < n; i++) {
          if (cum[i - 1] <= 0.5 * tot && cum[i] > 0.5 * tot) med = taus[i - 1] + h * (0.5 * tot - cum[i - 1]) / (cum[i] - cum[i - 1]);
          if (taus[i] <= v.tau + 1e-9) below = cum[i] / tot;
        }
        var pc = pooled(y, sg, v.tau), wa = v.tau * v.tau / (sg[0] * sg[0] + v.tau * v.tau);
        s.out = [pc.mu, wa * y[0] + (1 - wa) * pc.mu, wa, med, below];

        var lo = Math.min(-12, v.ya - 4), hi = Math.max(32, v.ya + 4), xs = QB.linspace(0, 30, 91);
        var a = g[0].axes({ x: [0, 30], y: [lo, hi], title: "Each school's estimate given tau", xlabel: "tau" });
        var ends = [];
        for (j = 0; j < 8; j++) {
          var ys = xs.map(function (t) { var q = pooled(y, sg, t), w = t * t / (sg[j] * sg[j] + t * t); return w * y[j] + (1 - w) * q.mu; });
          a.line(xs, ys, { color: COL[j], width: j === 0 ? 2.4 : 1.5 });
          ends.push([ys[90], j]);
        }
        ends.sort(function (p, q) { return p[0] - q[0]; }); // letters at the right edge, spread so they do not overlap
        var gap = 13 * (hi - lo) / a.h, at = lo + 0.3 * gap;
        for (j = 0; j < 8; j++) { at = Math.max(at + (j ? gap : 0), ends[j][0]); at = Math.min(at, hi - (8 - j) * gap); a.text(30, at, NAMES.charAt(ends[j][1]), { color: COL[ends[j][1]], dx: -9, dy: -7, size: 11 }); }
        a.vline(v.tau, { color: C.ink });
        for (j = 0; j < 8; j++) { var wj = v.tau * v.tau / (sg[j] * sg[j] + v.tau * v.tau); a.dots([v.tau], [wj * y[j] + (1 - wj) * pc.mu], { color: COL[j], r: 3.5 }); }
        a.text(v.tau, lo, "cursor", { color: C.ink, dx: v.tau > 24 ? -6 : 6, dy: -9, align: v.tau > 24 ? "right" : "left" });

        var k = 121, tx = taus.slice(0, k), dn = dens.slice(0, k).map(function (d) { return d / tot; }), dmax = 0;
        for (i = 0; i < k; i++) dmax = Math.max(dmax, dn[i]);
        var b = g[1].axes({ x: [0, 30], y: [0, dmax * 1.25], title: "The posterior of tau", xlabel: "tau" });
        var kc = Math.max(1, Math.round(v.tau / h));
        b.area(tx.slice(0, kc + 1), dn.slice(0, kc + 1), 0, { color: C.spot, alpha: 0.3 });
        b.line(tx, dn, { color: C.spot, width: 2 });
        b.vline(v.tau, { color: C.ink });
        b.vline(med, { color: C.idea });
        b.legend([["p(tau | y)", C.spot], ["its median", C.idea], ["cursor", C.ink]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["pooled mean at the cursor", fmt(s.out[0], 1)], ["school A given tau", fmt(s.out[1], 1)], ["weight on A's own estimate", QB.pct(s.out[2], 0)],
          ["median of tau", fmt(s.out[3], 1)], ["P(tau below the cursor)", QB.pct(s.out[4], 0)]];
      },
      note: "Rubin's (1981) eight schools: effects 28, 8, −3, 7, −1, 1, 18, 12 with standard errors 15, 10, 16, 11, 9, 11, 10, 18. Flat priors on mu and tau; the grid for tau stops at 150, so with large standard errors the median shown is a little low. School A is the thick gold line.",
    });
  };

  // ---- Part 27: Neal's funnel, centred and non-centred, by HMC ---------------------------------------------------
  W.funnelneck = function (el) {
    QB.widget(el, {
      title: "Neal's funnel: the neck a fixed step cannot enter",
      sub: "The target is v ~ N(0, 3²) and x ~ N(0, e^v): wide at the top, a needle at the bottom. HMC runs 1,500 trajectories with one step size. Centred, steps that suit the mouth are far too long for the neck, so the chain rarely goes there; switch to non-centred (sample z, set x = z e^(v/2)) and the same step works everywhere.",
      panels: 2, height: 310,
      controls: [
        { k: "form", label: "Parametrization", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "non-centred" : "centred"; } },
        { k: "eps", label: "Leapfrog step size", min: 0.02, max: 0.6, step: 0.02, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "L", label: "Leapfrog steps per trajectory", min: 4, max: 40, step: 1, value: 16, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New chain", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 270), n = 1500, nc = v.form === 1, eps = v.eps, L = v.L, i, k;
        // U(v, u) = v²/18 + u² e^(−v)/2 + v/2 (centred, u = x) or v²/18 + u²/2 (non-centred, u = z)
        var U = function (q) { return q[0] * q[0] / 18 + (nc ? 0.5 * q[1] * q[1] : 0.5 * q[1] * q[1] * Math.exp(-q[0]) + 0.5 * q[0]); };
        var grad = function (q) {
          if (nc) return [q[0] / 9, q[1]];
          var e = Math.exp(-q[0]);
          return [q[0] / 9 - 0.5 * q[1] * q[1] * e + 0.5, q[1] * e];
        };
        var q = [0, 1], vs = [], xs = [], acc = 0, div = 0, dv = [], dx = [];
        for (i = 0; i < n; i++) {
          var p = [r.normal(), r.normal()], h0 = U(q) + 0.5 * (p[0] * p[0] + p[1] * p[1]);
          var qn = [q[0], q[1]], gr = grad(qn), ok = true;
          for (k = 0; k < L && ok; k++) {
            p[0] -= 0.5 * eps * gr[0]; p[1] -= 0.5 * eps * gr[1];
            qn[0] += eps * p[0]; qn[1] += eps * p[1];
            gr = grad(qn);
            p[0] -= 0.5 * eps * gr[0]; p[1] -= 0.5 * eps * gr[1];
            ok = isFinite(qn[0]) && isFinite(qn[1]) && isFinite(p[0]) && isFinite(p[1]) && Math.abs(qn[0]) < 60;
          }
          var h1 = ok ? U(qn) + 0.5 * (p[0] * p[0] + p[1] * p[1]) : Infinity;
          if (!(h1 - h0 < 1000)) { div++; dv.push(q[0]); dx.push(nc ? q[1] * Math.exp(q[0] / 2) : q[1]); }
          else if (Math.log(r() + 1e-300) < h0 - h1) { q = qn; acc++; }
          vs.push(q[0]); xs.push(nc ? q[1] * Math.exp(q[0] / 2) : q[1]);
        }
        var sorted = vs.slice().sort(function (a, b) { return a - b; });
        s.out = [acc / n, sorted[Math.floor(0.05 * n)], sorted[0], div];

        var clip = function (x) { return Math.max(-11.6, Math.min(11.6, x)); };
        var a = g[0].axes({ x: [-12, 12], y: [-10, 10], title: "The draws (x across, v up)", xlabel: "x" });
        var vv = QB.linspace(-10, 10, 81), env = vv.map(function (t) { return 2 * Math.exp(t / 2); });
        a.line(env, vv, { color: C.muted, width: 1.2 });
        a.line(env.map(function (e) { return -e; }), vv, { color: C.muted, width: 1.2 });
        a.dots(xs.map(clip), vs, { color: C.spot, r: 1.6, alpha: 0.55 });
        if (dv.length) a.dots(dx.map(clip), dv, { color: C.loss, r: 3 });
        a.hline(-4.93, { color: C.idea });
        a.text(-12, -4.93, "true 5% point of v", { color: C.idea, dx: 6, dy: 9, size: 11 });
        a.legend([["draws", C.spot], ["divergent starts", C.loss], ["x = ±2 e^(v/2)", C.muted]], { pos: "tl" });

        var nb = 30, hh = QB.hist(vs, -10, 10, nb), w = 20 / nb, mids = [], dens = [];
        for (i = 0; i < nb; i++) { mids.push(-10 + (i + 0.5) * w); dens.push(hh[i] / (n * w)); }
        var tx = QB.linspace(-10, 10, 101), ty = tx.map(function (t) { return QB.pdf(t / 3) / 3; });
        var b = g[1].axes({ x: [-10, 10], y: [0, 0.3], title: "v: sampled against N(0, 3²)", xlabel: "v" });
        b.bars(mids, dens, w, { color: C.spot, alpha: 0.6 });
        b.line(tx, ty, { color: C.idea, width: 2 });
        b.vline(-4.93, { color: C.idea });
        b.vline(s.out[1], { color: C.spot });
        b.legend([["sampled v, and its 5% point", C.spot], ["truth, and its 5% point", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["accepted", QB.pct(s.out[0], 0)], ["5% point of v (truth −4.93)", fmt(s.out[1], 2)], ["lowest v reached", fmt(s.out[2], 1)], ["divergent trajectories", String(s.out[3])]];
      },
      note: "Simulated in your browser: static HMC with unit masses on the two-dimensional funnel, 1,500 trajectories from (v, x) = (0, 1), no warmup or adaptation. A trajectory counts as divergent when its energy error exceeds 1,000. Points beyond |x| = 12 are drawn at the edge.",
    });
  };

  // ---- Part 28: the model-selection bench, with a penalty you can set -----------------------------------------------
  W.penaltybench = function (el) {
    var truth = function (x) { return Math.sin(2.5 * x) + 0.5 * x; };
    QB.widget(el, {
      title: "The bench: misfit plus a price per parameter",
      sub: "Polynomials of degree 0 to 10 are fitted to simulated points from a smooth curve. On the bench each degree's misfit (blue) carries a penalty (gold) of so much per coefficient; the criterion chooses the lowest total. Set the price to 0 and the largest model always wins; 2 is AIC, log n is BIC.",
      panels: 2, height: 310,
      controls: [
        { k: "pen", label: "Price per coefficient", min: 0, max: 8, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Sample size n", min: 20, max: 200, step: 10, value: 30, fmt: function (x) { return String(x); } },
        { k: "sd", label: "Noise sd", min: 0.1, max: 1.5, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 280), n = v.n, D = 10, i, d, k;
        var x = QB.linspace(-1.5, 1.5, n), f = x.map(truth), y = f.map(function (m) { return m + v.sd * r.normal(); });
        // Gram-Schmidt on the Legendre polynomials at the design points: nested fits for every degree at once
        var Q = [], P0 = x.map(function () { return 1; }), P1 = x.map(function (t) { return t / 1.5; }), cols = [P0, P1];
        for (d = 2; d <= D; d++) { var a = cols[d - 1], b = cols[d - 2]; cols.push(x.map(function (t, j) { return ((2 * d - 1) * (t / 1.5) * a[j] - (d - 1) * b[j]) / d; })); }
        for (d = 0; d <= D; d++) {
          var c = cols[d].slice(), pass;
          for (pass = 0; pass < 2; pass++) for (k = 0; k < d; k++) { var dot = 0; for (i = 0; i < n; i++) dot += Q[k][i] * c[i]; for (i = 0; i < n; i++) c[i] -= dot * Q[k][i]; }
          var nr = 0; for (i = 0; i < n; i++) nr += c[i] * c[i];
          nr = Math.sqrt(nr) || 1; Q.push(c.map(function (t) { return t / nr; }));
        }
        var fit = x.map(function () { return 0; }), fits = [], rss = [], err = [];
        for (d = 0; d <= D; d++) {
          var cy = 0; for (i = 0; i < n; i++) cy += Q[d][i] * y[i];
          var e = 0, t = 0;
          for (i = 0; i < n; i++) { fit[i] += cy * Q[d][i]; e += (y[i] - fit[i]) * (y[i] - fit[i]); t += (fit[i] - f[i]) * (fit[i] - f[i]); }
          rss.push(Math.max(e, 1e-12)); err.push(v.sd * v.sd + t / n); fits.push(fit.slice());
        }
        var dev = rss.map(function (q) { return n * Math.log(q / n); }), dmin = Math.min.apply(null, dev);
        var mis = dev.map(function (q) { return q - dmin; });
        var pick = function (price) { var best = 0, bv = Infinity; for (var j = 0; j <= D; j++) { var tv = mis[j] + price * (j + 1); if (tv < bv) { bv = tv; best = j; } } return best; };
        var ch = pick(v.pen), ea = 0; for (d = 1; d <= D; d++) if (err[d] < err[ea]) ea = d;
        s.out = [ch, pick(2), pick(Math.log(n)), ea, Math.log(n), err[ch], err[ea]];

        var a0 = g[0].axes({ x: [-1.5, 1.5], y: [-3, 3], title: "The data and the chosen fit (degree " + ch + ")", xlabel: "x" });
        a0.dots(x, y, { color: C.spot, r: n > 100 ? 1.8 : 2.6, alpha: 0.8 });
        a0.line(x, f, { color: C.muted, dash: [4, 4], width: 1.3 });
        a0.line(x, fits[ch], { color: C.idea, width: 2.2 });
        a0.legend([["chosen polynomial", C.idea], ["the true curve", C.muted]], { pos: "tl" });

        var degs = [], tot = [], pens = [];
        for (d = 0; d <= D; d++) { degs.push(d); pens.push(v.pen * (d + 1)); tot.push(mis[d] + pens[d]); }
        var ymax = Math.max(12, 1.3 * tot[D], 1.6 * tot[ch]);
        var b0 = g[1].axes({ x: [-0.7, 10.7], y: [0, ymax], title: "The bench: n log(RSS/n) + price × coefficients", xlabel: "polynomial degree", xticks: degs });
        b0.bars(degs, tot, 0.7, { color: function (j) { return j === ch ? C.idea : C.house; }, alpha: 0.9 });
        b0.bars(degs, mis, 0.7, { color: C.spot, alpha: 1 });
        b0.text(ch, Math.min(tot[ch], ymax * 0.9), "chosen", { color: C.idea, align: "center", dy: -9, bold: true, bg: true });
        b0.legend([["misfit", C.spot], ["penalty", C.house], ["lowest total", C.idea]], { pos: ch > 5 ? "tl" : "tr" });
      },
      readout: function (v, s) {
        return [["chosen at this price", "degree " + s.out[0]], ["AIC (price 2)", "degree " + s.out[1]], ["BIC (price log n = " + fmt(s.out[4], 2) + ")", "degree " + s.out[2]],
          ["lowest true error", "degree " + s.out[3]], ["true error of the choice / of the best", fmt(s.out[5], 3) + " / " + fmt(s.out[6], 3)]];
      },
      note: "Simulated data: y = sin(2.5x) + 0.5x + normal noise at n equally spaced x in [−1.5, 1.5]. Misfit is n log(RSS/n) above its minimum; true error is the mean squared error on new responses at the same x, which a real analyst never sees. Bars taller than the panel are cut off.",
    });
  };

  // ---- Part 29: a kernel density estimate and its exact MISE ---------------------------------------------------------
  W.humpsbandwidth = function (el) {
    var WT = [0.35, 0.65], MU = [2.0, 4.3], SG = [0.27, 0.42];
    var npdf = function (d, sd) { return Math.exp(-0.5 * d * d / (sd * sd)) / (sd * 2.5066282746310002); };
    var truth = function (x) { return WT[0] * npdf(x - MU[0], SG[0]) + WT[1] * npdf(x - MU[1], SG[1]); };
    var omega = function (a, h) { // w' Omega_a(h) w of Marron & Wand (1992)
      var t = 0, l, m;
      for (l = 0; l < 2; l++) for (m = 0; m < 2; m++) t += WT[l] * WT[m] * npdf(MU[l] - MU[m], Math.sqrt(a * h * h + SG[l] * SG[l] + SG[m] * SG[m]));
      return t;
    };
    var parts = function (h, n) { // integrated variance and integrated squared bias of the Gaussian-kernel estimate
      return { v: 1 / (2 * Math.sqrt(Math.PI) * n * h) - omega(2, h) / n, b: omega(2, h) - 2 * omega(1, h) + omega(0, h) };
    };
    QB.widget(el, {
      title: "Two humps, one bandwidth",
      sub: "A sample from a two-humped stand-in for Old Faithful's eruption lengths, and its kernel density estimate. Slide the bandwidth: small, and the curve chases every point (variance); large, and the humps merge (bias). The right panel is the exact mean integrated squared error and its two parts.",
      panels: 2, height: 310,
      controls: [
        { k: "lh", label: "Bandwidth h", min: -1.5, max: 0, step: 0.01, value: -0.8, fmt: function (x) { return Math.pow(10, x).toFixed(3); } },
        { k: "ln", label: "Sample size n", min: 1.7, max: 3, step: 0.05, value: 2.3, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 290), n = Math.round(Math.pow(10, v.ln)), h = Math.pow(10, v.lh), i, j;
        var xs = [];
        for (i = 0; i < n; i++) { var c = r() < WT[0] ? 0 : 1; xs.push(MU[c] + SG[c] * r.normal()); }
        var m = 181, grid = QB.linspace(0.8, 6.2, m), est = [], tr = grid.map(truth), dx = grid[1] - grid[0], ise = 0, modes = 0, top = 0;
        for (j = 0; j < m; j++) {
          var t = 0; for (i = 0; i < n; i++) { var u = (grid[j] - xs[i]) / h; if (u > -6 && u < 6) t += Math.exp(-0.5 * u * u); }
          est.push(t / (n * h * 2.5066282746310002)); ise += (est[j] - tr[j]) * (est[j] - tr[j]) * dx; top = Math.max(top, est[j]);
        }
        for (j = 1; j < m - 1; j++) if (est[j] > est[j - 1] && est[j] >= est[j + 1] && est[j] > 0.02 * top) modes++;
        var hs = [], mv = [], mb = [], mt = [], best = 0;
        for (j = 0; j <= 60; j++) { var hh = Math.pow(10, -1.5 + 1.5 * j / 60), p = parts(hh, n); hs.push(hh); mv.push(Math.max(p.v, 1e-9)); mb.push(Math.max(p.b, 1e-9)); mt.push(Math.max(p.v + p.b, 1e-9)); if (mt[j] < mt[best]) best = j; }
        var ph = parts(h, n);
        s.out = [modes, ise, ph.v + ph.b, hs[best], mt[best]];

        var a = g[0].axes({ x: [0.8, 6.2], y: [0, 1.3], title: "The estimate (n = " + n + ")", xlabel: "eruption length (minutes)" });
        a.area(grid, tr, 0, { color: C.muted, alpha: 0.18 });
        a.line(grid, tr, { color: C.muted, dash: [4, 4], width: 1.3 });
        a.line(grid, est, { color: C.idea, width: 2.2 });
        a.dots(xs.slice(0, 400), xs.slice(0, 400).map(function () { return 0.02; }), { color: C.spot, r: 1.5, alpha: 0.45 });
        a.legend([["kernel estimate", C.idea], ["the true density", C.muted], ["the sample", C.spot]], { pos: "tr" });

        var b = g[1].axes({ x: [0.0316, 1], y: [1e-4, 10], logx: true, logy: true, title: "Exact MISE against the bandwidth", xlabel: "bandwidth h", xticks: [0.05, 0.1, 0.2, 0.5, 1] });
        b.line(hs, mv, { color: C.spot, width: 1.5 });
        b.line(hs, mb, { color: C.loss, width: 1.5 });
        b.line(hs, mt, { color: C.idea, width: 2.2 });
        b.vline(h, { color: C.ink });
        b.dots([h], [Math.min(10, Math.max(1e-4, ise))], { color: C.ink, r: 4 });
        b.legend([["MISE", C.idea], ["variance", C.spot], ["squared bias", C.loss], ["this sample's error", C.ink]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["modes in the estimate", String(s.out[0])], ["this sample's squared error", fmt(s.out[1], 4)], ["exact MISE at this h", fmt(s.out[2], 4)],
          ["best h", fmt(s.out[3], 3)], ["best MISE", fmt(s.out[4], 4)]];
      },
      note: "Simulated data from 0.35 N(2, 0.27²) + 0.65 N(4.3, 0.42²), the film's stand-in for Old Faithful, with a Gaussian kernel. The MISE curves are Marron and Wand's (1992) exact formula, not a simulation. Up to 400 sample points are drawn.",
    });
  };

  // ---- Part 30: the estimator rail, with strays you can drag ---------------------------------------------------------
  W.strayrail = function (el) {
    var N = 25, NAMES = ["mean", "10% trimmed mean", "Hodges–Lehmann", "Huber (k = 1.345)", "median"];
    var COL = [C.loss, C.implied, C.gain, C.idea, C.spot];
    var num = function (a, b) { return a - b; };
    var med = function (x) { var t = x.slice().sort(num), m = t.length; return m % 2 ? t[(m - 1) / 2] : 0.5 * (t[m / 2 - 1] + t[m / 2]); };
    var estimates = function (x) {
      var n = x.length, t = x.slice().sort(num), i, j, gcut = Math.floor(0.1 * n), tr = 0, wa = [];
      for (i = gcut; i < n - gcut; i++) tr += t[i];
      for (i = 0; i < n; i++) for (j = i; j < n; j++) wa.push(0.5 * (x[i] + x[j]));
      var m0 = med(x), sc = 1.4826 * med(x.map(function (q) { return Math.abs(q - m0); })), mu = m0, it;
      if (sc > 1e-9) for (it = 0; it < 60; it++) { // Huber's M-estimate by IRLS, MAD scale held fixed
        var sw = 0, swx = 0;
        for (i = 0; i < n; i++) { var u = Math.abs(x[i] - mu) / sc, w = u <= 1.345 ? 1 : 1.345 / u; sw += w; swx += w * x[i]; }
        var nu = swx / sw; if (Math.abs(nu - mu) < 1e-7) { mu = nu; break; } mu = nu;
      }
      return [QB.mean(x), tr / (n - 2 * gcut), med(wa), mu, m0];
    };
    QB.widget(el, {
      title: "The estimator rail: drag the strays",
      sub: "Twenty-five simulated measurements of a quantity whose true value is 0. Replace some of them by strays at one position and drag it. One stray carries the mean as far as you like; add strays and the trimmed mean, then Hodges–Lehmann, then Huber and the median give way in turn.",
      panels: 2, height: 310,
      controls: [
        { k: "z", label: "Where the strays sit", min: -12, max: 12, step: 0.25, value: 9, fmt: function (x) { return fmt(x, 2); } },
        { k: "m", label: "How many of the 25 are strays", min: 0, max: 14, step: 1, value: 1, fmt: function (x) { return x + " (" + Math.round(4 * x) + "%)"; } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 300), base = [], i, k;
        for (i = 0; i < N; i++) base.push(r.normal());
        var make = function (z) { var x = base.slice(); for (var q = 0; q < v.m; q++) x[q] = z; return x; };
        var x = make(v.z), e = estimates(x);
        s.out = e;

        var a = g[0].axes({ x: [-13, 13], y: [0, 7], title: "The rail: the sample and five estimates of its centre", xlabel: "measurement", noY: true });
        a.vline(0, { color: C.muted });
        a.line([-13, 13], [0.6, 0.6], { color: C.muted, width: 1 });
        a.dots(base.slice(v.m), base.slice(v.m).map(function () { return 0.6; }), { color: C.ink, r: 2.6, alpha: 0.75 });
        if (v.m > 0) {
          a.dots([v.z], [0.6], { color: C.option, r: 6 });
          a.text(v.z, 0.6, v.m + (v.m === 1 ? " stray" : " strays"), { color: C.option, dy: -14, align: v.z > 8 ? "right" : v.z < -8 ? "left" : "center", size: 11 });
        }
        for (k = 0; k < 5; k++) {
          var yy = 6.2 - k * 1.05, ek = Math.max(-12.6, Math.min(12.6, e[k]));
          a.line([-13, 13], [yy, yy], { color: C.line, width: 1 });
          a.dots([ek], [yy], { color: COL[k], r: 5 });
          a.text(e[k] > 0 ? -13 : 13, yy, NAMES[k], { color: COL[k], dx: e[k] > 0 ? 5 : -5, dy: -9, align: e[k] > 0 ? "left" : "right", size: 11 });
        }

        var zs = QB.linspace(-12, 12, 49), curves = [[], [], [], [], []];
        for (i = 0; i < zs.length; i++) { var ez = estimates(make(zs[i])); for (k = 0; k < 5; k++) curves[k].push(ez[k]); }
        var b = g[1].axes({ x: [-12, 12], y: [-4, 4], title: "Each estimate as the strays move", xlabel: "position of the strays" });
        b.hline(0, { color: C.muted });
        for (k = 0; k < 5; k++) b.line(zs, curves[k], { color: COL[k], width: k === 0 ? 2.2 : 1.7 });
        b.vline(v.z, { color: C.option });
        for (k = 0; k < 5; k++) b.dots([v.z], [Math.max(-4, Math.min(4, e[k]))], { color: COL[k], r: 3.5 });
        b.legend([["mean", COL[0]], ["10% trimmed", COL[1]], ["Hodges–Lehmann", COL[2]], ["Huber", COL[3]], ["median", COL[4]]], { pos: "tl" });
      },
      readout: function (v, s) {
        return NAMES.map(function (nm, k) { return [nm, fmt(s.out[k], 2)]; });
      },
      note: "Simulated data: 25 draws from N(0, 1), the first few replaced by the strays. Huber's estimate uses the MAD as its scale. Breakdown comes at 1 stray for the mean, 3 for the 10% trimmed mean (it drops 2 from each end), 8 for Hodges–Lehmann (the limit for large samples is 29%) and 13 for Huber and the median.",
    });
  };
})();
