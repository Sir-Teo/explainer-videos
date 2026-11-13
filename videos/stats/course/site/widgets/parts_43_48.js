// Interactives for Stage IV, PhD core (Parts 43-48).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // Binomial(n, p) probabilities, k = 0..n, by the recurrence in logs.
  function binom(n, p) {
    var out = new Array(n + 1), lp = n * Math.log(1 - p), r = Math.log(p / (1 - p)), k;
    for (k = 0; k <= n; k++) { out[k] = Math.exp(lp); lp += Math.log((n - k) / (k + 1)) + r; }
    return out;
  }
  // The exact Kolmogorov distance of the standardized Binomial(n, p) from N(0, 1): attained at an atom.
  function kolm(n, p) {
    var pr = binom(n, p), s = Math.sqrt(n * p * (1 - p)), cum = 0, best = { d: 0, x: 0, lo: 0, hi: 0 }, k;
    for (k = 0; k <= n; k++) {
      var x = (k - n * p) / s, G = QB.cdf(x), left = cum; cum += pr[k];
      if (Math.abs(left - G) > best.d) best = { d: Math.abs(left - G), x: x, lo: Math.min(left, G), hi: Math.max(left, G) };
      if (Math.abs(cum - G) > best.d) best = { d: Math.abs(cum - G), x: x, lo: Math.min(cum, G), hi: Math.max(cum, G) };
    }
    return best;
  }

  // ---- Part 43: the central limit theorem's rate, exactly -----------------------------------------------------
  W.kolmogorovgap = function (el) {
    QB.widget(el, {
      title: "The Kolmogorov gap and the Berry-Esseen bound",
      sub: "Left: the CDF of a standardized sum of n coin tosses (blue staircase) against the normal CDF (gold), with the largest vertical gap in red. Right: that gap for n = 1 to 1,024 on log-log axes, under the dashed bound 0.4748 ρ/√n. Slide p away from one half: the bound loosens faster than the gap grows.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Number of tosses n", min: 1, max: 200, step: 1, value: 10 },
        { k: "p", label: "Probability of heads p", min: 0.02, max: 0.5, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var n = v.n, p = v.p, q = 1 - p, pr = binom(n, p), sd = Math.sqrt(n * p * q), k, cum = 0;
        var rho = (p * p + q * q) / Math.sqrt(p * q), best = kolm(n, p), bound = 0.4748 * rho / Math.sqrt(n);
        s.out = [best.d, bound, rho];
        var a = g[0].axes({ x: [-3.5, 3.5], y: [0, 1], title: "CDF of the standardized sum", xlabel: "z" });
        var xs = [-3.5], ys = [0];
        for (k = 0; k <= n; k++) { var x = (k - n * p) / sd; xs.push(x); ys.push(cum); cum += pr[k]; xs.push(x); ys.push(cum); }
        xs.push(3.5); ys.push(1);
        a.line(xs, ys, { color: C.spot, width: 1.8 });
        var zs = QB.linspace(-3.5, 3.5, 120);
        a.line(zs, zs.map(QB.cdf), { color: C.idea, width: 1.8 });
        a.line([best.x, best.x], [best.lo, best.hi], { color: C.loss, width: 4 });
        a.legend([["sum of n tosses", C.spot], ["normal", C.idea], ["largest gap", C.loss]], { pos: "tl" });
        var ns = [], ds = [], bs = [];
        for (k = 0; k <= 10; k++) { var m = Math.pow(2, k); ns.push(m); ds.push(kolm(m, p).d); bs.push(Math.min(1, 0.4748 * rho / Math.sqrt(m))); }
        var b = g[1].axes({ x: [1, 1024], y: [0.003, 1], logx: true, logy: true, title: "Gap against n (log-log)", xlabel: "n" });
        b.line(ns, bs, { color: C.muted, dash: [5, 4], width: 1.5 });
        b.line(ns, ds, { color: C.spot, width: 2 });
        b.dots(ns, ds, { color: C.spot, r: 2.5 });
        b.dots([n], [best.d], { color: C.loss, r: 5 });
        b.legend([["exact gap", C.spot], ["Berry-Esseen bound", C.muted], ["this n", C.loss]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["Kolmogorov gap", fmt(s.out[0], 4)], ["bound 0.4748 ρ/√n", fmt(s.out[1], 4)], ["gap / bound", QB.pct(s.out[0] / s.out[1], 0)], ["ρ = E|X−μ|³/σ³", fmt(s.out[2], 2)]];
      },
      note: "Exact binomial arithmetic, no simulation. The bound is Shevtsova's constant for i.i.d. summands with a finite third moment; a bound above 1 says nothing. For a fair coin the gap is about 0.399/√n, 84% of the bound.",
    });
  };

  // ---- Part 44: Ville's inequality on betting paths ------------------------------------------------------------
  W.villewealth = function (el) {
    QB.widget(el, {
      title: "Betting against a coin: Ville's line",
      sub: "A gambler tests whether a coin is fair by betting on heads at the odds a biased coin would deserve; her wealth is a likelihood ratio. Left: thirty wealth paths on a log scale, gold once they reach 1/α. Right: the share of 300 paths that have rejected by each toss, for the wealth test and for a one-sided z test of size α repeated every tenth toss. With a fair coin the first stays under α and the second does not; then bias the coin.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "The coin's true P(heads)", min: 0.5, max: 0.65, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "p1", label: "The gambler bets as if P(heads) were", min: 0.52, max: 0.8, step: 0.01, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "alpha", label: "Size α (reject at wealth 1/α)", min: 0.01, max: 0.25, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 440), R = 300, T = 400, up = Math.log(v.p1 / 0.5) / Math.LN10, dn = Math.log((1 - v.p1) / 0.5) / Math.LN10;
        var thr = -Math.log(v.alpha) / Math.LN10, zc = QB.inv(1 - v.alpha), ts = [], i, t;
        var crossW = new Array(T + 1).fill(0), crossZ = new Array(T + 1).fill(0), paths = [], hits = [], finals = [];
        for (t = 0; t <= T; t++) ts.push(t);
        for (i = 0; i < R; i++) {
          var w = 0, h = 0, tw = -1, tz = -1, keep = i < 30 ? [0] : null;
          for (t = 1; t <= T; t++) {
            var head = r() < v.p; w += head ? up : dn; h += head ? 1 : 0;
            if (tw < 0 && w >= thr) tw = t;
            if (tz < 0 && t % 10 === 0 && (h - t / 2) / Math.sqrt(t / 4) > zc) tz = t;
            if (keep) keep.push(w);
          }
          if (tw > 0) for (t = tw; t <= T; t++) crossW[t]++;
          if (tz > 0) for (t = tz; t <= T; t++) crossZ[t]++;
          if (keep) { paths.push(keep); hits.push(tw); }
          finals.push(w);
        }
        for (t = 0; t <= T; t++) { crossW[t] /= R; crossZ[t] /= R; }
        s.out = [crossW[T], crossZ[T], QB.quantile(finals, 0.5)];
        var a = g[0].axes({ x: [0, T], y: [-8, 4], title: "Wealth paths (log scale)", xlabel: "toss", yticks: [-8, -6, -4, -2, 0, 2, 4], yfmt: function (y) { return y === 0 ? "1" : "1e" + (y < 0 ? "−" : "") + Math.abs(y); } });
        for (i = 0; i < paths.length; i++) a.line(ts, paths[i], { color: hits[i] > 0 ? C.idea : C.spot, width: 1, alpha: hits[i] > 0 ? 0.9 : 0.55 });
        a.hline(thr, { color: C.loss, width: 1.5 });
        a.text(0, thr, "1/α", { color: C.loss, dx: 6, dy: -11, bg: true });
        a.legend([["reached 1/α", C.idea], ["never did", C.spot]], { pos: "bl" });
        var b = g[1].axes({ x: [0, T], y: [0, 1], title: "Share of paths that have rejected", xlabel: "toss" });
        b.hline(v.alpha, { color: C.muted });
        b.text(T, v.alpha, "α", { color: C.muted, align: "right", dx: -4, dy: -9 });
        b.line(ts, crossZ, { color: C.loss, width: 2 });
        b.line(ts, crossW, { color: C.idea, width: 2 });
        b.legend([["wealth test (Ville)", C.idea], ["z test, peeking", C.loss]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["wealth test rejected", QB.pct(s.out[0], 1)], ["Ville's bound under a fair coin", QB.pct(v.alpha, 0)], ["peeking z test rejected", QB.pct(s.out[1], 1)], ["median final wealth", "10^" + fmt(s.out[2], 1)]];
      },
      note: "Simulated data: 300 paths of 400 tosses. Under a fair coin the wealth is a nonnegative martingale started at 1, so Ville's inequality bounds the chance of ever reaching 1/α by α; a rejection when the coin is biased is power, not error.",
    });
  };

  // ---- Part 45: a whole decision problem as a risk set ---------------------------------------------------------
  W.riskhull = function (el) {
    QB.widget(el, {
      title: "Fair or biased? The risk set of a small decision problem",
      sub: "A coin is fair or biased; it is tossed three times and you must say which. Each of the sixteen rules is a point: its risk if the coin is fair (across) and if it is biased (up). Left: the points, the admissible lower edge, the Bayes rule for your prior (where its supporting line touches) and the minimax rule on the diagonal. Right: the Bayes risk against the prior; its peak is the least favourable prior and its height is the minimax risk.",
      panels: 2, height: 320,
      controls: [
        { k: "pi", label: "Prior probability that the coin is fair", min: 0, max: 1, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "pb", label: "The biased coin's P(heads)", min: 0.55, max: 0.95, step: 0.01, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
        { k: "cost", label: "Cost of missing a biased coin (a false alarm costs 1)", min: 0.5, max: 4, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var p0 = binom(3, 0.5), p1 = binom(3, v.pb), R1 = [], R2 = [], k, x;
        for (k = 0; k < 16; k++) { // bit x of k set: say "biased" when X = x
          var a = 0, b = 0;
          for (x = 0; x < 4; x++) { if ((k >> x) & 1) a += p0[x]; else b += v.cost * p1[x]; }
          R1.push(a); R2.push(b);
        }
        var bayes = function (pi) { var best = 0, r = Infinity, j; for (j = 0; j < 16; j++) { var q = pi * R1[j] + (1 - pi) * R2[j]; if (q < r - 1e-12) { r = q; best = j; } } return { r: r, j: best }; };
        var lo = 0, hi = 1, i; // the Bayes risk is concave in the prior: golden-section search for its peak
        for (i = 0; i < 60; i++) { var m1 = lo + 0.382 * (hi - lo), m2 = lo + 0.618 * (hi - lo); if (bayes(m1).r < bayes(m2).r) lo = m1; else hi = m2; }
        var lf = (lo + hi) / 2, mm = bayes(lf).r, B = bayes(v.pi);
        var thr = [[0, v.cost]], cum0 = 0, cum1 = 0; // threshold rules "biased if X >= c", c = 4..0
        for (x = 3; x >= 0; x--) { cum0 += p0[x]; cum1 += p1[x]; thr.push([cum0, v.cost * (1 - cum1)]); }
        var c = -1; for (x = 0; x <= 4; x++) { var bits = (15 << x) & 15; if (bits === B.j) c = x; }
        s.out = [B.r, mm, lf, c];
        var ymax = Math.max(1.05, v.cost * 1.05);
        var ax = g[0].axes({ x: [-0.04, 1.06], y: [-0.04 * ymax, ymax], title: "The sixteen rules as risk points", xlabel: "risk if the coin is fair" });
        ax.line([0, ymax], [0, ymax], { color: C.muted, dash: [3, 4], width: 1 });
        ax.area(thr.map(function (t) { return t[0]; }), thr.map(function (t) { return t[1]; }), thr.map(function (t, j) { return v.cost - thr[4 - j][1]; }), { color: C.spot, alpha: 0.1 }); // the hull: its upper edge is the lower edge of the opposite rules
        ax.line(thr.map(function (t) { return t[0]; }), thr.map(function (t) { return t[1]; }), { color: C.idea, width: 2 });
        ax.dots(R1, R2, { color: C.spot, r: 3 });
        if (v.pi < 0.999) ax.line([0, 1.05], [B.r / (1 - v.pi), (B.r - v.pi * 1.05) / (1 - v.pi)], { color: C.gain, width: 1.5 });
        else ax.vline(B.r, { color: C.gain, width: 1.5, dash: [] });
        ax.dots([R1[B.j]], [R2[B.j]], { color: C.gain, r: 6 });
        ax.dots([mm], [mm], { color: C.loss, r: 5 });
        ax.legend([["admissible edge", C.idea], ["Bayes rule and its line", C.gain], ["minimax rule", C.loss]], { pos: "tr" });
        var ps = QB.linspace(0, 1, 201), rs = ps.map(function (q) { return bayes(q).r; });
        var bx = g[1].axes({ x: [0, 1], y: [0, Math.max(0.2, mm * 1.35)], title: "Bayes risk against the prior", xlabel: "prior probability of a fair coin" });
        bx.line(ps, rs, { color: C.idea, width: 2 });
        bx.hline(mm, { color: C.loss });
        bx.vline(lf, { color: C.loss });
        bx.text(lf, mm, "least favourable", { color: C.loss, dx: lf > 0.6 ? -6 : 6, dy: -10, align: lf > 0.6 ? "right" : "left" });
        bx.dots([v.pi], [B.r], { color: C.gain, r: 6 });
      },
      readout: function (v, s) {
        var rule = s.out[3] < 0 ? "a non-threshold rule" : s.out[3] === 0 ? "always say biased" : s.out[3] === 4 ? "always say fair" : "biased if heads ≥ " + s.out[3];
        return [["Bayes rule", rule], ["its Bayes risk", fmt(s.out[0], 3)], ["minimax risk", fmt(s.out[1], 3)], ["least favourable prior", fmt(s.out[2], 3)]];
      },
      note: "Exact arithmetic. Randomizing between rules fills the shaded hull, so only its lower-left edge is admissible. The minimax rule usually mixes two neighbouring threshold rules; its risk equals the largest Bayes risk, which is the minimax theorem for this finite problem.",
    });
  };

  // ---- Part 46: Neyman structure, slice by slice --------------------------------------------------------------
  function choose(n, k) { if (k < 0 || k > n) return 0; var r = 1, i; for (i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }
  W.similarslices = function (el) {
    var M = 8, N = 10;
    QB.widget(el, {
      title: "Neyman structure: every slice spends exactly α",
      sub: "Two groups of 8 and 10 trials; is the first success probability larger? Given the total number of successes, the first group's count has a known (hypergeometric) law whatever the common probability is. Left: that law for one total, with the part the test rejects in red. Right: the test's size at every common probability. The randomized test spends α in every slice, so its size is flat; Fisher's exact test never randomizes and wastes some of it.",
      panels: 2, height: 300,
      controls: [
        { k: "t", label: "Total successes in both groups (the slice)", min: 1, max: 17, step: 1, value: 9 },
        { k: "alpha", label: "Level α", min: 0.01, max: 0.2, step: 0.01, value: 0.05, fmt: function (x) { return x.toFixed(2); } },
        { k: "p", label: "Common success probability (the nuisance)", min: 0.05, max: 0.95, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var phi = [], pmfs = [], t, x, j;
        for (t = 0; t <= M + N; t++) { // the level-alpha one-sided test of each slice: reject for large x
          var lo = Math.max(0, t - N), hi = Math.min(M, t), row = new Array(M + 1).fill(0), pm = new Array(M + 1).fill(0), tail = 0, den = choose(M + N, t), open = true;
          for (x = lo; x <= hi; x++) pm[x] = choose(M, x) * choose(N, t - x) / den;
          for (x = hi; x >= lo && open; x--) {
            if (tail + pm[x] <= v.alpha + 1e-12) { row[x] = 1; tail += pm[x]; } else { row[x] = (v.alpha - tail) / pm[x]; open = false; }
          }
          phi.push(row); pmfs.push(pm);
        }
        var size = function (p, rand) {
          var px = binom(M, p), py = binom(N, p), tot = 0, y;
          for (x = 0; x <= M; x++) for (y = 0; y <= N; y++) { var f = phi[x + y][x]; tot += px[x] * py[y] * (rand ? f : (f >= 1 - 1e-12 ? 1 : 0)); }
          return tot;
        };
        var pm0 = pmfs[v.t], ph = phi[v.t], xs = [], full = [], rej = [], spentF = 0, spentR = 0, c = -1;
        for (x = 0; x <= M; x++) { xs.push(x); full.push(pm0[x]); rej.push(pm0[x] * ph[x]); spentR += pm0[x] * ph[x]; if (ph[x] >= 1 - 1e-12) spentF += pm0[x]; if (ph[x] > 1e-12 && c < 0) c = x; }
        s.out = [spentR, spentF, size(v.p, true), size(v.p, false), c, c >= 0 ? ph[c] : 0];
        var a = g[0].axes({ x: [-0.6, M + 0.6], y: [0, Math.max.apply(null, full) * 1.25], title: "First group's successes, given the total", xlabel: "successes in the group of 8", xticks: xs });
        a.bars(xs, full, 0.8, { color: C.spot, alpha: 0.75 });
        a.bars(xs, rej, 0.8, { color: C.loss, alpha: 0.95 });
        a.legend([["conditional null law", C.spot], ["rejected (probability mass)", C.loss]], { pos: "tl" });
        var ps = QB.linspace(0.02, 0.98, 97), sr = [], sf = [];
        for (j = 0; j < ps.length; j++) { sr.push(size(ps[j], true)); sf.push(size(ps[j], false)); }
        var b = g[1].axes({ x: [0, 1], y: [0, Math.max(0.06, v.alpha * 1.4)], title: "Size against the nuisance parameter", xlabel: "common success probability" });
        b.hline(v.alpha, { color: C.muted });
        b.line(ps, sf, { color: C.spot, width: 2 });
        b.line(ps, sr, { color: C.idea, width: 2 });
        b.vline(v.p, { color: C.muted });
        b.dots([v.p, v.p], [s.out[2], s.out[3]], { color: function (i) { return i ? C.spot : C.idea; }, r: 4.5 });
        b.legend([["randomized: similar", C.idea], ["Fisher's exact test", C.spot]], { pos: "bl" });
      },
      readout: function (v, s) {
        var rule = s.out[4] < 0 ? "never rejects" : "reject from " + s.out[4] + " up (with probability " + fmt(s.out[5], 2) + " at " + s.out[4] + ")";
        return [["this slice", rule], ["slice spends: randomized", fmt(s.out[0], 3)], ["Fisher", fmt(s.out[1], 3)], ["size at this p: randomized", fmt(s.out[2], 3)], ["Fisher", fmt(s.out[3], 3)]];
      },
      note: "Exact arithmetic for X ~ Bin(8, p₁), Y ~ Bin(10, p₂) under p₁ = p₂. The total is sufficient for the common probability and complete, so a test is similar exactly when every slice has conditional level α.",
    });
  };

  // ---- Part 47: Hodges's risk bump ----------------------------------------------------------------------------
  W.hodgesbump = function (el) {
    // n E(T - theta)^2 for T = xbar 1(|xbar| >= n^-power), xbar ~ N(theta, 1/n), at theta = h / sqrt(n): exact.
    function risk(h, n, power) {
      var a = Math.pow(n, 0.5 - power), lo = -a - h, hi = a - h;
      var P = QB.cdf(hi) - QB.cdf(lo), z2 = P - (hi * QB.pdf(hi) - lo * QB.pdf(lo));
      return Math.max(1e-6, 1 - z2 + h * h * P);
    }
    QB.widget(el, {
      title: "Hodges's estimator: superefficient at zero, and the bump beside it",
      sub: "Report the sample mean, unless it is within n^(−power) of zero; then report zero. Left: the risk times n against the true mean θ. Right: the same risk at θ = h/√n, on a log scale, with the worst case over |h| ≤ c shaded. The sample mean's scaled risk is 1 everywhere. Keep c below 1 and Hodges wins; widen it, or raise n, and the bump takes over.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Sample size n", min: 1, max: 6, step: 0.25, value: 2, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
        { k: "c", label: "Neighbourhood radius c (in units of 1/√n)", min: 0.25, max: 40, step: 0.25, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "power", label: "Threshold exponent (Hodges: 0.25)", min: 0.1, max: 0.45, step: 0.01, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var n = Math.round(Math.pow(10, v.k)), rt = Math.sqrt(n), i, th = QB.linspace(-0.6, 0.6, 481);
        var r1 = th.map(function (t) { return risk(t * rt, n, v.power); });
        var edge = Math.pow(n, 0.5 - v.power), xmax = Math.min(60, Math.max(6, 1.7 * edge, 1.3 * v.c));
        var hs = QB.linspace(0, xmax, 801), r2 = hs.map(function (h) { return risk(h, n, v.power); });
        var peak = 0, at = 0, worst = 0;
        for (i = 0; i < hs.length; i++) { if (r2[i] > peak) { peak = r2[i]; at = hs[i]; } if (hs[i] <= v.c + 1e-9 && r2[i] > worst) worst = r2[i]; }
        s.out = [risk(0, n, v.power), peak, at, worst, xmax];
        var top = Math.max(4, Math.min(peak, 1e5) * 1.15);
        var a = g[0].axes({ x: [-0.6, 0.6], y: [0, top], title: "n × mean squared error against θ", xlabel: "true mean θ" });
        a.hline(1, { color: C.muted });
        a.line(th, r1, { color: C.idea, width: 2 });
        a.legend([["Hodges", C.idea], ["sample mean", C.muted]], { pos: "tr" });
        var b = g[1].axes({ x: [0, xmax], y: [0.01, 10000], logy: true, title: "The same risk at θ = h/√n (log scale)", xlabel: "local parameter h" });
        var inside = hs.filter(function (h) { return h <= v.c + 1e-9; });
        b.area(inside, inside.map(function () { return worst; }), 0.01, { color: C.loss, alpha: 0.2 });
        b.line([0, Math.min(v.c, xmax)], [worst, worst], { color: C.loss, width: 2.5 });
        b.hline(1, { color: C.muted });
        b.line(hs, hs.map(function (h) { return Math.max(1e-6, h * h); }), { color: C.spot, width: 1.2, dash: [5, 4] });
        b.line(hs, r2, { color: C.idea, width: 2 });
        b.vline(v.c, { color: C.loss });
        b.legend([["Hodges", C.idea], ["its limit h²", C.spot], ["worst case over |h| ≤ c", C.loss]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["scaled risk at θ = 0", fmt(s.out[0], 3)], ["peak of the bump in view", fmt(s.out[1], 1) + " at h = " + fmt(s.out[2], 1)], ["worst over |h| ≤ c", fmt(s.out[3], 2)], ["sample mean", "1.00"]];
      },
      note: "Exact arithmetic for normal data with variance 1. The peak sits near the edge of the zeroing zone, h = n^(1/2 − power), and grows without bound; the local asymptotic minimax theorem takes n to infinity first and c to infinity second, which is the order in which Hodges loses.",
    });
  };

  // ---- Part 48: the empirical process and Kolmogorov's law -----------------------------------------------------
  function kolmCdf(t) { // P(sup |Brownian bridge| <= t)
    if (t <= 0.05) return 0;
    var s = 0, k;
    if (t >= 0.6) { for (k = 1; k <= 30; k++) s += (k % 2 ? 1 : -1) * Math.exp(-2 * k * k * t * t); return Math.min(1, Math.max(0, 1 - 2 * s)); }
    for (k = 1; k <= 12; k++) s += Math.exp(-(2 * k - 1) * (2 * k - 1) * Math.PI * Math.PI / (8 * t * t));
    return Math.min(1, Math.max(0, Math.sqrt(2 * Math.PI) / t * s));
  }
  function kolmQuantile(p) { var lo = 0.2, hi = 4, i; for (i = 0; i < 50; i++) { var m = (lo + hi) / 2; if (kolmCdf(m) < p) lo = m; else hi = m; } return (lo + hi) / 2; }
  W.bridgesup = function (el) {
    QB.widget(el, {
      title: "Doob's heuristic, and what fitting the parameters does to it",
      sub: "Left: one sample's empirical process, √n (Fₙ − F), drawn on the probability scale, between the dashed lines ± the Kolmogorov critical value. Right: the largest absolute value of that path over 300 samples (bars) against the law of a Brownian bridge's largest absolute value (gold). With F known the bars follow the curve at any n above a handful. Switch to a fitted normal: the path is tied down and Kolmogorov's table almost never rejects.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Sample size n", min: 5, max: 300, step: 5, value: 50 },
        { k: "fit", label: "The normal's mean and SD are", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "estimated from the sample" : "known"; } },
        { k: "level", label: "Confidence level of the band", min: 0.8, max: 0.99, step: 0.01, value: 0.95, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New samples", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 480), n = v.n, R = 300, rt = Math.sqrt(n), crit = kolmQuantile(v.level), sups = [], first = null, i, j, over = 0;
        for (i = 0; i < R; i++) {
          var z = new Float64Array(n), m = 0, ss = 0;
          for (j = 0; j < n; j++) { z[j] = r.normal(); m += z[j]; }
          m /= n; for (j = 0; j < n; j++) ss += (z[j] - m) * (z[j] - m);
          var sd = Math.sqrt(ss / (n - 1)) || 1, u = new Float64Array(n), d = 0;
          for (j = 0; j < n; j++) u[j] = v.fit ? QB.cdf((z[j] - m) / sd) : QB.cdf(z[j]);
          u.sort();
          for (j = 0; j < n; j++) d = Math.max(d, (j + 1) / n - u[j], u[j] - j / n);
          sups.push(rt * d); if (rt * d > crit) over++;
          if (i === 0) first = u;
        }
        s.out = [sups[0], crit, over / R, QB.quantile(sups, v.level)];
        var xs = [0], ys = [0];
        for (j = 0; j < n; j++) { xs.push(first[j]); ys.push(rt * (j / n - first[j])); xs.push(first[j]); ys.push(rt * ((j + 1) / n - first[j])); }
        xs.push(1); ys.push(0);
        var a = g[0].axes({ x: [0, 1], y: [-2.6, 2], title: "One sample: √n (Fₙ − F)", xlabel: "F(x)", yticks: [-2, -1, 0, 1, 2] });
        a.hline(0, { color: C.muted, dash: [] });
        a.hline(crit, { color: C.loss }); a.hline(-crit, { color: C.loss });
        a.line(xs, ys, { color: C.spot, width: 1.6 });
        a.legend([["empirical process", C.spot], ["± Kolmogorov's critical value", C.loss]], { pos: "bl" });
        var nb = 30, lo = 0, hi = 2.1, w = (hi - lo) / nb, h = QB.hist(sups, lo, hi, nb), mids = [], dens = [], top = 1.9;
        for (i = 0; i < nb; i++) { mids.push(lo + (i + 0.5) * w); dens.push(h[i] / (R * w)); top = Math.max(top, dens[i] * 1.1); }
        var ts = QB.linspace(0.06, hi, 140), kd = ts.map(function (t) { return (kolmCdf(t + 0.01) - kolmCdf(t - 0.01)) / 0.02; });
        var b = g[1].axes({ x: [lo, hi], y: [0, top], title: "Largest |√n (Fₙ − F)| over 300 samples", xlabel: "√n sup |Fₙ − F|" });
        b.bars(mids, dens, w, { color: C.spot, alpha: 0.7 });
        b.line(ts, kd, { color: C.idea, width: 2 });
        b.vline(crit, { color: C.loss });
        b.legend([["300 samples", C.spot], ["sup |Brownian bridge|", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["this sample's largest gap × √n", fmt(s.out[0], 3)], ["Kolmogorov's critical value", fmt(s.out[1], 3)], ["samples beyond it", QB.pct(s.out[2], 1) + " (nominal " + QB.pct(1 - v.level, 0) + ")"], ["their own " + QB.pct(v.level, 0) + " point", fmt(s.out[3], 3)]];
      },
      note: "Simulated normal data, 300 samples per redraw. With known parameters the law of the largest gap does not depend on the distribution, and Kolmogorov's value is slightly conservative at small n. With the mean and SD estimated the limit is Durbin's process, not a Brownian bridge: its largest value is much smaller, so the test needs its own (Lilliefors or parametric bootstrap) critical value.",
    });
  };
})();
