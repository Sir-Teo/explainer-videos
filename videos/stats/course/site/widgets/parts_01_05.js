// Interactives for Stage I, Bachelor's: Foundations (Parts 1-5).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  function lgamma(x) { // Lanczos; x > 0
    var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.001208650973866179, -0.000005395239384953];
    var y = x, t = x + 5.5, s = 1.000000000190015;
    t -= (x + 0.5) * Math.log(t);
    for (var j = 0; j < 6; j++) { y += 1; s += c[j] / y; }
    return -t + Math.log(2.5066282746310005 * s / x);
  }

  // ---- Part 1: the centre as the minimizer of a loss ----------------------------------------------------------
  W.lpcentre = function (el) {
    QB.widget(el, {
      title: "Which centre follows the outlier?",
      sub: "Fourteen simulated incomes (blue) and one gold income you can move. Every centre here minimizes the total of |x − c| raised to a power p: p = 1 gives the median, p = 2 the mean, and a large p approaches the midrange. Drag the gold income far to the right and see which centres follow it.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Power p in the loss |x − c|^p", min: 1, max: 8, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "out", label: "The gold income, thousands a year", min: 20, max: 400, step: 5, value: 150, fmt: function (x) { return x.toFixed(0); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 100), xs = [], i, k;
        for (i = 0; i < 14; i++) xs.push(Math.min(120, Math.max(8, 38 * Math.exp(0.5 * r.normal()))));
        var all = xs.concat([v.out]), sorted = all.slice().sort(function (a, b) { return a - b; });
        var med = sorted[7], mean = QB.mean(all), lo = sorted[0], hi = sorted[14], mid = (lo + hi) / 2;
        var loss = function (c, p) { var t = 0; for (k = 0; k < all.length; k++) t += Math.pow(Math.abs(all[k] - c), p); return t; };
        var centre = function (p) { // the loss is convex in c: ternary search between the smallest and largest value
          if (p <= 1.0001) return med;
          var a = lo, b = hi, m1, m2;
          for (var it = 0; it < 80; it++) { m1 = a + (b - a) / 3; m2 = b - (b - a) / 3; if (loss(m1, p) < loss(m2, p)) b = m2; else a = m1; }
          return (a + b) / 2;
        };
        var cp = centre(v.p), lmin = Math.max(loss(cp, v.p), 1e-9);
        s.out = [med, mean, cp, mid];
        var a0 = g[0].axes({ x: [0, 420], y: [0, 1], noY: true, title: "Fifteen incomes and four centres", xlabel: "income, thousands a year" });
        a0.vline(mid, { color: C.muted });
        a0.vline(med, { color: C.gain, dash: [], width: 1.6 });
        a0.vline(mean, { color: C.loss, dash: [], width: 1.6 });
        a0.vline(cp, { color: C.q, dash: [6, 3], width: 2.4 });
        a0.dots(xs, xs.map(function (x, j) { return 0.08 + 0.03 * j; }), { color: C.spot, r: 3.2 });
        a0.dots([v.out], [0.29], { color: C.idea, r: 6 });
        a0.legend([["median", C.gain], ["mean", C.loss], ["minimizer for this p", C.q], ["midrange", C.muted]], { pos: "tr" });
        var cs = QB.linspace(0, 420, 141), ls = cs.map(function (c) { return loss(c, v.p) / lmin; });
        var a1 = g[1].axes({ x: [0, 420], y: [1, 3], title: "Total loss relative to its minimum", xlabel: "candidate centre c, thousands a year" });
        a1.line(cs, ls, { color: C.q, width: 2 });
        a1.vline(cp, { color: C.q });
        a1.dots([cp], [1], { color: C.q, r: 5 });
        a1.text(cp, 2.8, "c = " + fmt(cp, 1), { color: C.q, dx: cp > 300 ? -8 : 8, align: cp > 300 ? "right" : "left", bg: true });
      },
      readout: function (v, s) {
        return [["median", fmt(s.out[0], 1)], ["mean", fmt(s.out[1], 1)], ["minimizer at p = " + v.p.toFixed(1), fmt(s.out[2], 1)], ["midrange", fmt(s.out[3], 1)]];
      },
      note: "Simulated data, in thousands a year. With fifteen values the median is the eighth in order, so moving the largest one cannot change it; the mean moves by one fifteenth of the change; for large p the minimizer is pulled toward the point halfway between the smallest and the largest value.",
    });
  };

  // ---- Part 2: a screening test in natural frequencies ---------------------------------------------------------
  W.screenposterior = function (el) {
    QB.widget(el, {
      title: "A positive test: how likely is the condition?",
      sub: "A thousand people are screened once. Gold squares have the condition and test positive; blue squares are healthy and test positive too. The chance of the condition given a positive test is the gold share of all the positives. Make the condition rare and watch that share fall far below the test's sensitivity.",
      panels: 2, height: 300,
      controls: [
        { k: "prev", label: "Prevalence of the condition", min: 0.1, max: 50, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "sens", label: "Sensitivity, P(positive | condition)", min: 50, max: 99.5, step: 0.5, value: 90, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "spec", label: "Specificity, P(negative | healthy)", min: 50, max: 99.5, step: 0.5, value: 95, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var prev = v.prev / 100, sens = v.sens / 100, spec = v.spec / 100, N = 1000, i;
        var nSick = Math.round(N * prev), tp = Math.round(nSick * sens), fn = nSick - tp;
        var fp = Math.round((N - nSick) * (1 - spec)), tn = N - nSick - fp;
        var post = function (q, times) { var o = q / (1 - q) * Math.pow(sens / (1 - spec), times); return o / (1 + o); };
        s.out = { pos: tp + fp, tp: tp, post: post(prev, 1), lr: sens / (1 - spec), post2: post(prev, 2) };
        // the icon array, drawn by hand
        var c = g[0].ctx, b = g[0].box, cols = 40, rows = 25, top = b.y + 30;
        var cell = Math.max(3, Math.floor(Math.min((b.w - 28) / cols, (b.h - 30 - 46) / rows)));
        var x0 = b.x + (b.w - cols * cell) / 2, dim = "#2b3546";
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("One thousand people, tested once", x0, b.y + 8);
        for (i = 0; i < N; i++) {
          c.fillStyle = i < tp ? C.idea : i < nSick ? C.loss : i < nSick + fp ? C.spot : dim;
          c.fillRect(x0 + (i % cols) * cell, top + Math.floor(i / cols) * cell, cell - 1, cell - 1);
        }
        var items = [["condition, positive: " + tp, C.idea], ["condition, missed: " + fn, C.loss], ["healthy, positive: " + fp, C.spot], ["healthy, negative: " + tn, dim]];
        var lw = Math.max(cols * cell, Math.min(b.w - 20, 330)), lx0 = b.x + (b.w - lw) / 2, ly = top + rows * cell + 12, half = lw / 2;
        c.font = "11px system-ui, sans-serif"; c.textBaseline = "middle";
        for (i = 0; i < 4; i++) {
          var lx = lx0 + (i % 2) * half, yy = ly + Math.floor(i / 2) * 16;
          c.fillStyle = items[i][1]; c.fillRect(lx, yy - 5, 10, 10);
          c.fillStyle = C.ink; c.fillText(items[i][0], lx + 15, yy);
        }
        c.restore();
        // the posterior against the prior
        var qs = [], one = [], two = [];
        for (i = 0; i <= 60; i++) { var q = 0.001 * Math.pow(500, i / 60); qs.push(q); one.push(post(q, 1)); two.push(post(q, 2)); }
        var a = g[1].axes({ x: [0.001, 0.5], y: [0, 1], logx: true, title: "P(condition | positive test)", xlabel: "prevalence (the prior probability)",
          xfmt: function (x) { return +(100 * x).toPrecision(2) + "%"; } });
        a.hline(sens, { color: C.muted });
        a.vline(prev, { color: C.muted });
        a.line(qs, two, { color: C.q, width: 1.8 });
        a.line(qs, one, { color: C.idea, width: 2.2 });
        a.dots([prev], [post(prev, 2)], { color: C.q, r: 4 });
        a.dots([prev], [post(prev, 1)], { color: C.idea, r: 5.5 });
        a.legend([["after one positive test", C.idea], ["after two positives", C.q], ["sensitivity", C.muted]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["positives per 1,000", String(s.out.pos)], ["of them with the condition", String(s.out.tp)], ["P(condition | positive)", pct(s.out.post)],
          ["likelihood ratio", fmt(s.out.lr, 1)], ["after two positives", pct(s.out.post2)]];
      },
      note: "Nothing is simulated: the squares are the expected counts, rounded to whole people, and the percentages are exact. Posterior odds = prior odds × likelihood ratio, sensitivity / (1 − specificity). The second test multiplies by the same ratio only if the two tests err independently, among people with the condition and among people without.",
    });
  };

  // ---- Part 3: the law of rare events and Le Cam's bound -------------------------------------------------------
  W.rareevents = function (el) {
    var NS = [4, 5, 6, 8, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100, 126, 158, 200, 251, 316, 398, 501, 631, 794, 1000];
    function countPmf(ps, K) { // the exact law of a sum of independent Bernoulli(p_i), truncated at K
      var a = new Array(K + 1).fill(0), i, k; a[0] = 1;
      for (i = 0; i < ps.length; i++) { var p = ps[i]; for (k = K; k >= 1; k--) a[k] = a[k] * (1 - p) + a[k - 1] * p; a[0] *= 1 - p; }
      return a;
    }
    function poisPmf(m, K) { var q = new Array(K + 1), k; q[0] = Math.exp(-m); for (k = 1; k <= K; k++) q[k] = q[k - 1] * m / k; return q; }
    function tv(a, q) {
      var d = 0, sa = 0, sq = 0, k;
      for (k = 0; k < a.length; k++) { d += Math.abs(a[k] - q[k]); sa += a[k]; sq += q[k]; }
      return 0.5 * (d + Math.max(0, 1 - sa) + Math.max(0, 1 - sq));
    }
    QB.widget(el, {
      title: "Many rare chances make a Poisson",
      sub: "A count is the number of successes in n independent trials whose chances add up to λ. Blue bars are its exact distribution, gold dots the Poisson with the same mean. Raise n and the two merge; then make the risks unequal, so that a few trials carry most of the chance, and watch the distance grow, always under Le Cam's bound.",
      panels: 2, height: 300,
      controls: [
        { k: "lam", label: "Expected count λ", min: 0.2, max: 4, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "ln", label: "Number of trials n", min: 0.6, max: 3, step: 0.05, value: 1, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
        { k: "spread", label: "Inequality of the risks", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New risks", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = Math.max(4, Math.round(Math.pow(10, v.ln))), r = QB.rng(s.seed + 300), w = [], ws = 0, ps = [], i, sum = 0, sq = 0, pmax = 0;
        for (i = 0; i < n; i++) { var wi = Math.exp(2 * v.spread * r.normal()); w.push(wi); ws += wi; }
        for (i = 0; i < n; i++) { var p = Math.min(1, v.lam * w[i] / ws); ps.push(p); sum += p; sq += p * p; pmax = Math.max(pmax, p); }
        var K = Math.min(n, 40), a = countPmf(ps, K), q = poisPmf(sum, K), d = tv(a, q), bound = Math.min(1, sq);
        s.out = [n, pmax, d, bound, sum];
        var ks = [], top = 0.3;
        for (i = 0; i <= 12; i++) { ks.push(i); top = Math.max(top, 1.15 * (i <= K ? a[i] : 0), 1.15 * (i <= K ? q[i] : 0)); }
        var a0 = g[0].axes({ x: [-0.7, 12.7], y: [0, top], title: "Exact count (bars) and Poisson (dots)", xlabel: "number of events", xticks: [0, 2, 4, 6, 8, 10, 12] });
        a0.bars(ks, ks.map(function (k) { return k <= K ? a[k] : 0; }), 0.8, { color: C.spot });
        a0.dots(ks, ks.map(function (k) { return k <= K ? q[k] : 0; }), { color: C.idea, r: 4 });
        a0.legend([["sum of n rare trials", C.spot], ["Poisson, same mean", C.idea]], { pos: "tr" });
        var tvs = [], bs = [], eq;
        for (i = 0; i < NS.length; i++) {
          eq = new Array(NS[i]).fill(Math.min(1, v.lam / NS[i]));
          var Ki = Math.min(NS[i], 40);
          tvs.push(Math.max(1e-7, tv(countPmf(eq, Ki), poisPmf(v.lam, Ki)))); bs.push(Math.min(1, v.lam * v.lam / NS[i]));
        }
        var a1 = g[1].axes({ x: [3.5, 1400], y: [1e-5, 2], logx: true, logy: true, xticks: [10, 100, 1000], title: "Distance to the Poisson, against n", xlabel: "number of trials n",
          yticks: [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1], yfmt: function (y) { return y >= 0.01 ? String(y) : "1e" + Math.round(Math.log10(y)); } });
        a1.line(NS, bs, { color: C.idea, width: 1.8 });
        a1.line(NS, tvs, { color: C.spot, width: 1.8 });
        a1.vline(n, { color: C.muted });
        a1.dots([n], [Math.max(1.2e-5, bound)], { color: C.idea, r: 5 });
        a1.dots([n], [Math.max(1.2e-5, d)], { color: C.spot, r: 5 });
        a1.legend([["Le Cam's bound, Σ pᵢ²", C.idea], ["exact total variation", C.spot]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["trials n", String(s.out[0])], ["largest single chance", fmt(s.out[1], 3)], ["total variation distance", fmt(s.out[2], 4)],
          ["Le Cam's bound", fmt(s.out[3], 4)]];
      },
      note: "Everything is computed exactly; only the unequal risks are drawn at random (seeded). The lines are for equal chances λ/n, where the bound is λ²/n; the two large dots are the trials as set. Total variation is the largest difference the two distributions can give to the probability of any event.",
    });
  };

  // ---- Part 4: the hat matrix's trace and degrees of freedom ---------------------------------------------------
  W.hatdof = function (el) {
    QB.widget(el, {
      title: "Why divide by n − p?",
      sub: "Each simulated data set is y = Xβ + noise with n rows and p columns, fitted by least squares. Its residual sum of squares, in units of σ², piles up around n − p, not n: the hat matrix has p eigenvalues equal to one, and the residuals live in the other n − p dimensions. Raise p toward n and watch RSS / n fall ever further below σ².",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Rows n", min: 10, max: 60, step: 1, value: 40, fmt: function (x) { return String(x); } },
        { k: "p", label: "Columns p (at most n − 2)", min: 1, max: 20, step: 1, value: 2, fmt: function (x) { return String(x); } },
        { k: "reps", label: "Simulated data sets", min: 100, max: 1000, step: 100, value: 400, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New design", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, p = Math.max(1, Math.min(v.p, n - 2)), reps = v.reps, r = QB.rng(s.seed + 400), Q = [], i, j, k, dot, tr = 0;
        for (j = 0; j < p; j++) { // the design's columns, orthonormalized by modified Gram-Schmidt: H = QQ'
          var col = new Array(n);
          for (i = 0; i < n; i++) col[i] = j === 0 ? 1 : r.normal();
          for (k = 0; k < j; k++) { dot = 0; for (i = 0; i < n; i++) dot += Q[k][i] * col[i]; for (i = 0; i < n; i++) col[i] -= dot * Q[k][i]; }
          var norm = 0; for (i = 0; i < n; i++) norm += col[i] * col[i];
          norm = Math.max(Math.sqrt(norm), 1e-9);
          for (i = 0; i < n; i++) { col[i] /= norm; tr += col[i] * col[i]; }
          Q.push(col);
        }
        var rss = [], z = new Array(n), tot;
        for (var rep = 0; rep < reps; rep++) { // RSS / sigma^2 = |z|^2 - |Q'z|^2 for standard normal noise z
          tot = 0;
          for (i = 0; i < n; i++) { z[i] = r.normal(); tot += z[i] * z[i]; }
          for (j = 0; j < p; j++) { dot = 0; for (i = 0; i < n; i++) dot += Q[j][i] * z[i]; tot -= dot * dot; }
          rss.push(Math.max(tot, 0));
        }
        var m = QB.mean(rss), df = n - p;
        s.out = [tr, df, m, m / n, m / df];
        var xmax = Math.ceil(n + 3 * Math.sqrt(2 * n)), nb = 30, bw = xmax / nb, h = QB.hist(rss, 0, xmax, nb), top = 0;
        var mids = [], dens = [], xs = QB.linspace(0.05, xmax, 160), lg = lgamma(df / 2);
        for (i = 0; i < nb; i++) { mids.push((i + 0.5) * bw); dens.push(h[i] / (reps * bw)); top = Math.max(top, dens[i]); }
        var chi = xs.map(function (x) { return Math.exp((df / 2 - 1) * Math.log(x) - x / 2 - (df / 2) * Math.LN2 - lg); });
        for (i = 0; i < chi.length; i++) top = Math.max(top, chi[i]);
        top *= 1.3;
        var a0 = g[0].axes({ x: [0, xmax], y: [0, top], title: "RSS / σ² in the simulated data sets", xlabel: "residual sum of squares / σ²" });
        a0.bars(mids, dens, bw, { color: C.spot, alpha: 0.6 });
        a0.line(xs, chi, { color: C.idea, width: 2.2 });
        a0.vline(df, { color: C.idea });
        a0.vline(n, { color: C.loss });
        a0.text(df, top * 0.62, "n − p", { color: C.idea, align: "right", dx: -5, bg: true });
        a0.text(n, top * 0.62, "n", { color: C.loss, dx: 6, bg: true });
        a0.legend([["simulated", C.spot], ["χ² with n − p df", C.idea]], { pos: "tr" });
        var pm = Math.min(20, n - 2), pg = [], naive = [];
        for (j = 1; j <= pm; j++) { pg.push(j); naive.push(1 - j / n); }
        var a1 = g[1].axes({ x: [0, pm + 1], y: [0, 1.25], title: "Two estimates of σ² as p grows", xlabel: "columns in the design, p" });
        a1.vline(p, { color: C.muted });
        a1.line([0, pm + 1], [1, 1], { color: C.gain, width: 1.8 });
        a1.line(pg, naive, { color: C.loss, width: 1.8 });
        a1.dots([p], [m / n], { color: C.loss, r: 5 });
        a1.dots([p], [m / df], { color: C.gain, r: 5 });
        a1.legend([["RSS / (n − p), in units of σ²", C.gain], ["RSS / n", C.loss]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["trace of H", fmt(s.out[0], 2)], ["n − p", String(s.out[1])], ["mean RSS / σ²", fmt(s.out[2], 2)], ["mean RSS / n", fmt(s.out[3], 3) + " σ²"],
          ["mean RSS / (n − p)", fmt(s.out[4], 3) + " σ²"]];
      },
      note: "Simulated data: an intercept and p − 1 random columns, independent normal noise with one variance σ². The lines are the theory (1 and 1 − p/n); the dots are the averages over the simulated data sets. The trace of H is computed from the orthonormalized columns and equals p.",
    });
  };

  // ---- Part 5: slicing a bivariate normal ----------------------------------------------------------------------
  W.galtonslice = function (el) {
    QB.widget(el, {
      title: "Slice the ellipse: regression to the mean",
      sub: "Three thousand simulated parent and child pairs, both in SD units, with correlation ρ. The gold band selects parents near one height; the right panel shows their children. Their average sits at ρ times the parent's height, closer to the mean than the parent, and their spread is the same in every slice. Slide ρ toward 1 and the regression disappears.",
      panels: 2, height: 300,
      controls: [
        { k: "rho", label: "Correlation ρ", min: -0.9, max: 0.95, step: 0.05, value: 0.45, fmt: function (x) { return fmt(x, 2); } },
        { k: "x0", label: "The parent's height x₀, SDs from the mean", min: -2.5, max: 2.5, step: 0.1, value: 1.5, fmt: function (x) { return fmt(x, 1); } },
        { k: "hw", label: "Half-width of the slice", min: 0.1, max: 0.5, step: 0.05, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 500), N = 3000, shown = 600, xs = [], ys = [], sy = [], i, c = Math.sqrt(Math.max(1e-6, 1 - v.rho * v.rho));
        for (i = 0; i < N; i++) {
          var z1 = r.normal(), z2 = r.normal(), y = v.rho * z1 + c * z2;
          if (i < shown) { xs.push(z1); ys.push(y); }
          if (Math.abs(z1 - v.x0) < v.hw) sy.push(y);
        }
        var m = sy.length, mu = v.rho * v.x0;
        s.out = [mu, m > 0 ? QB.mean(sy) : null, c, m > 1 ? QB.sd(sy) : null, m];
        var L = 3.5, a0 = g[0].axes({ x: [-L, L], y: [-L, L], title: "Parent and child, in SD units", xlabel: "parent" });
        a0.area([v.x0 - v.hw, v.x0 + v.hw], [L, L], -L, { color: C.idea, alpha: 0.16 });
        a0.dots(xs, ys, { r: 1.8, alpha: 0.8, color: function (j) { return Math.abs(xs[j] - v.x0) < v.hw ? C.idea : C.spot; } });
        a0.line([-L, L], [-L, L], { color: C.muted, dash: [4, 4], width: 1.2 });
        a0.line([-L, L], [-v.rho * L, v.rho * L], { color: C.gain, width: 2.2 });
        a0.dots([v.x0], [mu], { color: C.ink, r: 4.5 });
        a0.legend([["regression line, slope ρ", C.gain], ["child = parent", C.muted]], { pos: v.rho >= 0 ? "tl" : "bl" });
        var nb = 28, bw = 2 * L / nb, h = QB.hist(sy, -L, L, nb), mids = [], dens = [], grid = QB.linspace(-L, L, 141);
        for (i = 0; i < nb; i++) { mids.push(-L + (i + 0.5) * bw); dens.push(m > 0 ? h[i] / (m * bw) : 0); }
        var top = Math.max(0.5, 1.3 * 0.3989 / c);
        for (i = 0; i < nb; i++) top = Math.max(top, Math.min(1.08 * dens[i], 2.6 * 0.3989 / c));
        var a1 = g[1].axes({ x: [-L, L], y: [0, top], title: "The children of the slice", xlabel: "child" });
        a1.bars(mids, dens, bw, { color: C.idea, alpha: 0.45 });
        a1.line(grid, grid.map(function (t) { return QB.pdf(t); }), { color: C.muted, dash: [4, 4], width: 1.4 });
        a1.line(grid, grid.map(function (t) { return QB.pdf((t - mu) / c) / c; }), { color: C.gain, width: 2.2 });
        a1.vline(v.x0, { color: C.muted });
        a1.vline(mu, { color: C.gain });
        a1.legend([["children in the slice", C.idea], ["N(ρx₀, 1 − ρ²)", C.gain], ["all children", C.muted]], { pos: mu > 0 ? "tl" : "tr" });
      },
      readout: function (v, s) {
        return [["predicted child, ρx₀", fmt(s.out[0], 2)], ["mean of the slice", s.out[1] === null ? "no points" : fmt(s.out[1], 2)],
          ["conditional SD, √(1 − ρ²)", fmt(s.out[2], 2)], ["SD of the slice", s.out[3] === null ? "too few points" : fmt(s.out[3], 2)], ["points in the slice", String(s.out[4])]];
      },
      note: "Simulated data from a bivariate normal with unit variances. The green curve is the exact conditional law at x₀; a slice of positive width mixes nearby parents, so its histogram is slightly wider. The dashed vertical line marks a child as extreme as the parent.",
    });
  };
})();
