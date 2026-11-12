// Interactives for the course page and Acts I-II (Parts 1-8).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- the course page: the same paths under P and under Q -----------------------------------------------------
  W.hero = function (el) {
    var N = 44, STEPS = 140;
    QB.widget(el, {
      height: 250, bg: C.panel,
      init: function (s) { s.t = 0; s.seed = 3; },
      animate: function (v, s, dt) { s.t += dt / 7; if (s.t > 1.25) { s.t = 0; s.seed++; } return true; },
      draw: function (g, v, s) {
        var a = g[0].axes({ x: [0, 1.16], y: [55, 190], noX: true, noY: true, noFrame: true, xticks: [], yticks: [] });
        var r = QB.rng(s.seed), shown = Math.min(1, s.t), k, i, xs = QB.linspace(0, 1, STEPS + 1), endsP = [], endsQ = [];
        for (k = 0; k < N; k++) {
          var yP = [100], yQ = [100], lp = 0, lq = 0;
          for (i = 1; i <= STEPS; i++) {
            var z = r.normal() * 0.26 / Math.sqrt(STEPS);
            lp += (0.14 - 0.0338) / STEPS + z; lq += (0.02 - 0.0338) / STEPS + z;
            yP.push(100 * Math.exp(lp)); yQ.push(100 * Math.exp(lq));
          }
          var n = Math.max(2, Math.round(shown * STEPS));
          a.line(xs.slice(0, n), yQ.slice(0, n), { color: C.q, width: 1, alpha: 0.38 });
          a.line(xs.slice(0, n), yP.slice(0, n), { color: C.p, width: 1, alpha: 0.38 });
          endsP.push(yP[STEPS]); endsQ.push(yQ[STEPS]);
        }
        if (s.t > 1) { // the two terminal densities, drawn sideways at the right edge
          var ys = QB.linspace(55, 190, 80), al = Math.min(1, (s.t - 1) * 6);
          [[0.14, C.p], [0.02, C.q]].forEach(function (m) {
            var mu = Math.log(100) + m[0] - 0.0338, d = ys.map(function (y) { return 1.01 + 3.4 * QB.pdf((Math.log(y) - mu) / 0.26) / y * 10; });
            a.line(d, ys, { color: m[1], width: 2, alpha: al });
          });
        }
        a.text(0.012, 182, "the same shocks, two measures  (simulated)", { color: C.muted, size: 11 });
        a.text(0.012, 66, "P: what happens", { color: C.p, bold: true, size: 12 });
        a.text(0.012, 59, "Q: what is priced", { color: C.q, bold: true, size: 12, dy: 8 });
      },
    });
  };

  // ---- Part 1: is it a random walk, and is it Gaussian? --------------------------------------------------------
  W.walk = function (el) {
    QB.widget(el, {
      title: "Returns: clusters and tails",
      sub: "A simulated market of 2,500 days. Turn up the persistence of volatility and the weight of the tails, and compare the histogram with the bell curve of the same variance.",
      panels: 2, weights: [1.25, 1], height: 300,
      controls: [
        { k: "pers", label: "Volatility persistence (α + β)", min: 0, max: 0.99, step: 0.01, value: 0.95, fmt: function (x) { return x.toFixed(2); } },
        { k: "nu", label: "Tail weight of each day's shock (Student t, degrees of freedom)", min: 3, max: 30, step: 1, value: 5, fmt: function (x) { return x >= 30 ? "30 (≈ normal)" : String(x); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 2500, r = QB.rng(s.seed + 10), ret = new Array(n), al = Math.min(0.12, v.pers * 0.12), be = Math.max(0, v.pers - al), h = 1, i;
        for (i = 0; i < n; i++) { var z = v.nu >= 30 ? r.normal() : r.student(v.nu); ret[i] = Math.sqrt(h) * z; h = (1 - al - be) + al * ret[i] * ret[i] + be * h; }
        var sdv = QB.sd(ret), zs = ret.map(function (x) { return x / sdv; }), k4 = QB.mean(zs.map(function (x) { return x * x * x * x; })) - 3;
        var big = zs.filter(function (x) { return Math.abs(x) > 4; }).length;
        s.out = [k4, big, n * 2 * (1 - QB.cdf(4))];
        var a = g[0].axes({ x: [0, n], y: [-8, 8], title: "Daily returns, in standard deviations", xlabel: "day" });
        a.line(ret.map(function (_, j) { return j; }), zs, { color: C.spot, width: 0.7 });
        a.hline(4, { color: C.loss }); a.hline(-4, { color: C.loss });
        var b = g[1].axes({ x: [-7, 7], y: [0.5, 600], logy: true, title: "How often each size occurs (log scale)", xlabel: "standard deviations" });
        var H = QB.hist(zs, -7, 7, 56), xs = QB.linspace(-7 + 0.125, 7 - 0.125, 56);
        b.bars(xs, H.map(function (c) { return Math.max(c, 0.5); }), 0.25, { color: C.spot, base: 0.5 });
        var gx = QB.linspace(-7, 7, 141);
        b.line(gx, gx.map(function (x) { var y = n * 0.25 * QB.pdf(x); return y > 0.5 ? y : null; }), { color: C.p, width: 2 });
        b.legend([["simulated market", C.spot], ["normal, same variance", C.p]], { pos: "tr" });
      },
      readout: function (v, s) { return [["excess kurtosis", fmt(s.out[0], 1)], ["days beyond 4σ", s.out[1] + " (a normal expects " + fmt(s.out[2], 2) + ")"]]; },
      note: "Simulated: GARCH(1,1) with Student-t shocks. Real daily equity returns look like persistence ≈ 0.98 and about 4-6 degrees of freedom.",
    });
  };

  // ---- Part 2: leverage and the liquidation price ---------------------------------------------------------------
  W.margin = function (el) {
    QB.widget(el, {
      title: "Leverage chooses the distance to the barrier",
      sub: "A long position on one simulated path of 60 days. The position is closed for you when equity falls to the maintenance margin.",
      panels: 2, height: 290,
      controls: [
        { k: "L", label: "Leverage", min: 1, max: 20, step: 0.5, value: 5, fmt: function (x) { return x + "×"; } },
        { k: "m", label: "Maintenance margin", min: 0.5, max: 10, step: 0.5, value: 2.5, fmt: function (x) { return x + "% of notional"; } },
        { k: "sig", label: "Daily volatility", min: 0.5, max: 6, step: 0.25, value: 3, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New path", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 60, r = QB.rng(s.seed + 40), p = [100], i, m = v.m / 100, sg = v.sig / 100;
        for (i = 1; i <= n; i++) p.push(p[i - 1] * Math.exp(-0.5 * sg * sg + sg * r.normal()));
        var liq = 100 * (1 - 1 / v.L) / (1 - m), eq = [], hit = -1;
        for (i = 0; i <= n; i++) { var e = 100 / v.L + (p[i] - 100); if (hit < 0 && e < m * p[i]) hit = i; eq.push(hit >= 0 && i > hit ? null : e / (100 / v.L)); }
        var d = -Math.log(Math.max(liq, 1e-9) / 100), prob = v.L <= 1 ? 0 : 2 * QB.cdf(-d / (sg * Math.sqrt(n)));
        s.out = [liq, hit, prob, eq];
        var xs = QB.linspace(0, n, n + 1), lo = Math.min(Math.min.apply(null, p), liq) - 4, hi = Math.max.apply(null, p) + 4;
        var a = g[0].axes({ x: [0, n], y: [Math.max(0, lo), hi], title: "Price and the liquidation price", xlabel: "day" });
        a.line(xs, p, { color: C.spot });
        if (v.L > 1) { a.hline(liq, { color: C.loss, width: 1.4 }); a.text(n * 0.02, liq, "liquidation price " + fmt(liq, 1), { color: C.loss, dy: 9 }); }
        if (hit >= 0) a.dots([hit], [p[hit]], { color: C.loss, r: 5 });
        var b = g[1].axes({ x: [0, n], y: [-0.2, 2.6], title: "Equity, as a multiple of the margin posted", xlabel: "day" });
        b.hline(0, { dash: null }); b.hline(1);
        b.line(xs, eq, { color: hit >= 0 ? C.loss : C.gain, width: 2 });
      },
      readout: function (v, s) {
        return [["liquidation price", v.L > 1 ? fmt(s.out[0], 2) : "none"], ["on this path", s.out[1] >= 0 ? "liquidated on day " + s.out[1] : "survives"],
          ["P(liquidated in 60 days)", pct(s.out[2], 1)]];
      },
      note: "P(liquidated) is the reflection-principle formula for a driftless Brownian log price: 2Φ(−d / σ√T), d the log distance to the liquidation price.",
    });
  };

  // ---- Part 3: where a share's value sits in time ----------------------------------------------------------------
  W.dcf = function (el) {
    QB.widget(el, {
      title: "A share is a very long bond",
      sub: "A cash flow of 100 next year, growing forever. Move the discount rate and the growth rate and watch the value and where it sits in time.",
      panels: 2, height: 290,
      controls: [
        { k: "r", label: "Discount rate r", min: 4, max: 14, step: 0.1, value: 8, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "g", label: "Growth g", min: 0, max: 6, step: 0.1, value: 3, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = v.r / 100, gr = Math.min(v.g / 100, r - 0.005), val = 100 / (r - gr), q = (1 + gr) / (1 + r), yrs = QB.linspace(1, 60, 60);
        var wts = yrs.map(function (t) { return 100 * (1 - q) * Math.pow(q, t - 1); }), dur = (1 + r) / (r - gr), first10 = 1 - Math.pow(q, 10);
        s.out = [val, 1 / (r - gr), first10, gr];
        var a = g[0].axes({ x: [0, 61], y: [0, Math.max(6, wts[0] * 1.15)], title: "Share of today's value paid in each year, %", xlabel: "year" });
        a.bars(yrs, wts, 1, { color: function (i) { return i < 10 ? C.spot : C.q; } });
        a.vline(Math.min(dur, 60), { color: C.p }); a.text(Math.min(dur, 60), Math.max(6, wts[0] * 1.15) * 0.9, " average date: year " + fmt(dur, 0), { color: C.p, align: dur > 40 ? "right" : "left" });
        var rs = QB.linspace(0.04, 0.14, 100), b = g[1].axes({ x: [4, 14], y: [0, 8000], title: "Value against the discount rate", xlabel: "discount rate, %" });
        b.line(rs.map(function (x) { return 100 * x; }), rs.map(function (x) { return x - gr > 0.004 ? 100 / (x - gr) : null; }), { color: C.p, width: 2 });
        b.dots([v.r], [Math.min(val, 8000)], { color: C.ink, r: 5 });
      },
      readout: function (v, s) {
        return [["value", fmt(s.out[0], 0)], ["duration 1/(r−g)", fmt(s.out[1], 1) + " years"], ["value from the first ten years", pct(s.out[2], 0)],
          ["a +1 point rise in r costs", pct(1 - (v.r / 100 - s.out[3]) / (v.r / 100 + 0.01 - s.out[3]), 0)]];
      },
      note: "Gordon growth: value = D₁/(r − g). Growth is capped just below the discount rate, where the formula stops making sense.",
    });
  };

  // ---- Part 4: a change of measure re-weights the same paths ------------------------------------------------------
  W.measure = function (el) {
    QB.widget(el, {
      title: "A change of measure: the same paths, re-weighted",
      sub: "Fair coin-flip walks of 40 steps (4,000 simulated, 200 drawn). Under Q the up-probability is q; each path keeps its shape and gets the weight dQ/dP = (2q)^ups · (2(1−q))^downs.",
      panels: 2, weights: [1.3, 1], height: 300,
      controls: [{ k: "q", label: "Up-probability under Q", min: 0.36, max: 0.64, step: 0.01, value: 0.58, fmt: function (x) { return x.toFixed(2); } }],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 40, K = 4000, SHOW = 200, r = QB.rng(s.seed + 70), paths = [], wts = [], ends = [], i, k, xs = QB.linspace(0, n, n + 1), wmax = 0;
        for (k = 0; k < K; k++) { var y = k < SHOW ? [0] : null, pos = 0, ups = 0; for (i = 1; i <= n; i++) { var u = r() < 0.5 ? 1 : -1; if (u > 0) ups++; pos += u; if (y) y.push(pos); }
          var w = Math.pow(2 * v.q, ups) * Math.pow(2 * (1 - v.q), n - ups); if (y) { paths.push(y); wmax = Math.max(wmax, w); } wts.push(w); ends.push(pos); }
        var a = g[0].axes({ x: [0, n], y: [-22, 22], title: "200 paths drawn under P; brightness is the weight under Q", xlabel: "step" });
        for (k = 0; k < SHOW; k++) a.line(xs, paths[k], { color: C.q, width: 1, alpha: 0.05 + 0.75 * Math.min(1, wts[k] / (0.35 * wmax)) });
        var sw = 0, sx = 0; for (k = 0; k < K; k++) { sw += wts[k]; sx += wts[k] * ends[k]; }
        s.out = [QB.mean(ends), sx / K, n * (2 * v.q - 1), sw / K];
        var b = g[1].axes({ x: [-22, 22], y: [0, 0.2], title: "Where the walk ends", xlabel: "final position" });
        var hp = new Array(45).fill(0), hq = new Array(45).fill(0);
        for (k = 0; k < K; k++) { hp[ends[k] + 22] += 1 / K; hq[ends[k] + 22] += wts[k] / K; }
        var ex = [], ep = [], eq = [], logc = 0; // exact binomial laws on even positions
        for (i = 0; i <= n; i++) { if (i > 0) logc += Math.log((n - i + 1) / i); ex.push(2 * i - n); ep.push(Math.exp(logc + n * Math.log(0.5))); eq.push(Math.exp(logc + i * Math.log(v.q) + (n - i) * Math.log(1 - v.q))); }
        b.bars(QB.linspace(-22, 22, 45), hp, 1.6, { color: C.cash, alpha: 0.55 });
        b.bars(QB.linspace(-22, 22, 45), hq, 0.9, { color: C.q, alpha: 0.9 });
        b.line(ex, ep, { color: C.cash, width: 1.5 }); b.line(ex, eq, { color: C.q, width: 2 });
        b.legend([["P: fair coin", C.cash], ["Q: re-weighted", C.q]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["mean under P", fmt(s.out[0], 2)], ["mean under Q, by weights", fmt(s.out[1], 2)], ["exact n(2q−1)", fmt(s.out[2], 2)], ["average weight", fmt(s.out[3], 2) + " (should be 1)"]];
      },
      note: "This is all Girsanov's theorem does in continuous time: no path is added or removed, only its weight changes.",
    });
  };

  // ---- Part 5: quadratic variation ---------------------------------------------------------------------------------
  W.ito = function (el) {
    QB.widget(el, {
      title: "Quadratic variation: why dW² = dt",
      sub: "One Brownian path on [0, 1], watched on finer and finer grids. The sum of squared increments settles on elapsed time; the sum of absolute increments runs away.",
      panels: 2, height: 290,
      controls: [{ k: "k", label: "Number of steps", min: 2, max: 12, step: 1, value: 5, fmt: function (x) { return String(Math.pow(2, x)); } }],
      buttons: [{ label: "New path", act: function (s) { s.seed++; s.fine = null; } }],
      draw: function (g, v, s) {
        var M = 4096, i;
        if (!s.fine) { var r = QB.rng(s.seed + 90); s.fine = [0]; for (i = 1; i <= M; i++) s.fine.push(s.fine[i - 1] + r.normal() / Math.sqrt(M)); }
        var n = Math.pow(2, v.k), step = M / n, xs = [], ys = [], qv = [0], fv = 0, lo = Math.min.apply(null, s.fine), hi = Math.max.apply(null, s.fine);
        for (i = 0; i <= n; i++) { xs.push(i / n); ys.push(s.fine[i * step]); if (i > 0) { var d = ys[i] - ys[i - 1]; qv.push(qv[i - 1] + d * d); fv += Math.abs(d); } }
        s.out = [qv[n], fv, Math.sqrt(2 / n)];
        var a = g[0].axes({ x: [0, 1], y: [lo - 0.1, hi + 0.1], title: "The path, sampled " + n + " times", xlabel: "time" });
        a.line(QB.linspace(0, 1, M + 1), s.fine, { color: C.line, width: 1 }); a.line(xs, ys, { color: C.spot, width: 1.6 });
        if (n <= 64) a.dots(xs, ys, { color: C.spot, r: 2.5 });
        var b = g[1].axes({ x: [0, 1], y: [0, 1.6], title: "Sum of squared increments so far", xlabel: "time" });
        b.line([0, 1], [0, 1], { color: C.p, width: 1.5, dash: [5, 4] }); b.line(xs, qv, { color: C.gain, width: 2 });
        b.legend([["Σ (ΔW)²", C.gain], ["elapsed time t", C.p]], { pos: "tl" });
      },
      readout: function (v, s) { return [["Σ (ΔW)² at T = 1", fmt(s.out[0], 3)], ["its standard deviation √(2/n)", fmt(s.out[2], 3)], ["Σ |ΔW|", fmt(s.out[1], 1) + " (grows like √n)"]]; },
      note: "A smooth path has zero quadratic variation. Brownian motion's is t, and that is the extra term in Itô's lemma.",
    });
  };

  // ---- Part 6: Stambaugh's bias -----------------------------------------------------------------------------------
  W.hac = function (el) {
    QB.widget(el, {
      title: "A predictor that predicts nothing",
      sub: "Returns are regressed on a persistent predictor whose true slope is zero, in 600 simulated samples. The estimates are biased, and a nominal 5% test rejects far more often than 5%.",
      panels: 2, height: 290,
      controls: [
        { k: "rho", label: "Persistence of the predictor ρ", min: 0, max: 0.99, step: 0.01, value: 0.97, fmt: function (x) { return x.toFixed(2); } },
        { k: "c", label: "Correlation of the two shocks", min: -0.99, max: 0, step: 0.01, value: -0.95, fmt: function (x) { return x.toFixed(2); } },
        { k: "T", label: "Sample length (months)", min: 30, max: 600, step: 10, value: 120, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var R = 600, r = QB.rng(11), slopes = [], ts = [], k, t;
        for (k = 0; k < R; k++) {
          var x = 0, sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0, T = v.T, xs = new Array(T), ys = new Array(T);
          for (t = 0; t < T; t++) { var e = r.normal(), u = v.c * e + Math.sqrt(1 - v.c * v.c) * r.normal(); xs[t] = x; ys[t] = u; x = v.rho * x + e; }
          for (t = 0; t < T; t++) { sx += xs[t]; sy += ys[t]; }
          var mx = sx / T, my = sy / T;
          for (t = 0; t < T; t++) { sxx += (xs[t] - mx) * (xs[t] - mx); sxy += (xs[t] - mx) * (ys[t] - my); syy += (ys[t] - my) * (ys[t] - my); }
          var b = sxy / sxx, se = Math.sqrt((syy - b * sxy) / (T - 2) / sxx); slopes.push(b); ts.push(b / se);
        }
        var bias = v.c * (-(1 + 3 * v.rho) / v.T), m = QB.mean(slopes), w = Math.max(0.05, 4 * QB.sd(slopes));
        s.out = [m, bias, ts.filter(function (z) { return Math.abs(z) > 1.96; }).length / R];
        var a = g[0].axes({ x: [-w, w], y: [0, R * 0.16], title: "Estimated slope (the truth is 0)", xlabel: "slope" });
        a.bars(QB.linspace(-w + w / 40, w - w / 40, 40), QB.hist(slopes, -w, w, 40), w / 20, { color: C.spot });
        a.vline(0, { color: C.ink, dash: null }); a.vline(m, { color: C.p }); a.vline(bias, { color: C.loss, dash: [2, 3] });
        a.legend([["mean estimate", C.p], ["Stambaugh's formula", C.loss]], { pos: "tl" });
        var bx = g[1].axes({ x: [-5, 5], y: [0, 0.5], title: "t-statistics against the standard normal", xlabel: "t" });
        bx.bars(QB.linspace(-4.875, 4.875, 40), QB.hist(ts, -5, 5, 40).map(function (c) { return c / R / 0.25; }), 0.25, { color: C.spot });
        var gx = QB.linspace(-5, 5, 101); bx.line(gx, gx.map(QB.pdf), { color: C.p, width: 2 });
        bx.vline(1.96, { color: C.loss }); bx.vline(-1.96, { color: C.loss });
      },
      readout: function (v, s) { return [["mean slope", fmt(s.out[0], 4)], ["formula −ρ_uv (1+3ρ)/T", fmt(s.out[1], 4)], ["rejected at 5%", pct(s.out[2], 1)]]; },
      note: "The dividend yield is a predictor of this kind: very persistent, with shocks strongly negatively correlated with returns.",
    });
  };

  // ---- Part 7: GARCH --------------------------------------------------------------------------------------------------
  W.garch = function (el) {
    QB.widget(el, {
      title: "GARCH(1,1): today's variance from yesterday's surprise",
      sub: "σ²ₜ = ω + α r²ₜ₋₁ + β σ²ₜ₋₁, with ω set so the long-run volatility stays at 1% a day. α is the reaction to news, β the memory.",
      panels: 2, weights: [1.3, 1], height: 290,
      controls: [
        { k: "a", label: "Reaction α", min: 0, max: 0.3, step: 0.01, value: 0.08, fmt: function (x) { return x.toFixed(2); } },
        { k: "b", label: "Memory β", min: 0, max: 0.98, step: 0.01, value: 0.9, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var be = Math.min(v.b, 0.995 - v.a), n = 2000, r = QB.rng(s.seed + 130), h = 1, ret = [], vol = [], i, k;
        for (i = 0; i < n; i++) { vol.push(Math.sqrt(h)); var x = Math.sqrt(h) * r.normal(); ret.push(x); h = (1 - v.a - be) + v.a * x * x + be * h; }
        var sq = ret.map(function (x) { return x * x; }), m = QB.mean(sq), den = 0, acf = [];
        for (i = 0; i < n; i++) den += (sq[i] - m) * (sq[i] - m);
        for (k = 1; k <= 30; k++) { var num = 0; for (i = k; i < n; i++) num += (sq[i] - m) * (sq[i - k] - m); acf.push(num / den); }
        var p = v.a + be; s.out = [p, p > 0 && p < 1 ? Math.log(0.5) / Math.log(p) : 0, be];
        var xs = QB.linspace(0, n - 1, n), a = g[0].axes({ x: [0, n], y: [-7, 7], title: "Returns and ±2 conditional volatilities, %", xlabel: "day" });
        a.line(xs, ret, { color: C.spot, width: 0.7 });
        a.line(xs, vol.map(function (x) { return 2 * x; }), { color: C.p, width: 1.4 }); a.line(xs, vol.map(function (x) { return -2 * x; }), { color: C.p, width: 1.4 });
        var b = g[1].axes({ x: [0, 31], y: [-0.1, 0.6], title: "Autocorrelation of squared returns", xlabel: "lag, days" });
        b.bars(QB.linspace(1, 30, 30), acf, 1, { color: C.spot }); b.hline(0, { dash: null });
        if (p > 0) b.line(QB.linspace(1, 30, 30), QB.linspace(1, 30, 30).map(function (k2) { return acf[0] > 0 ? acf[0] * Math.pow(p, k2 - 1) : 0; }), { color: C.p, width: 2 });
      },
      readout: function (v, s) { return [["persistence α + β", fmt(s.out[0], 2)], ["half-life of a volatility shock", s.out[1] > 0 ? fmt(s.out[1], 0) + " days" : "none"], ["β used", fmt(s.out[2], 2)]]; },
      note: "The line is the theoretical decay (α + β)ᵏ from the first lag. β is capped so that α + β stays below one.",
    });
  };

  // ---- Part 8: Kelly -----------------------------------------------------------------------------------------------------
  W.kelly = function (el) {
    QB.widget(el, {
      title: "How much to bet",
      sub: "An even-money bet won with probability p, repeated 500 times, staking a fixed fraction of wealth. The growth rate has one peak; past twice the peak the median path goes to zero.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Probability of winning", min: 0.5, max: 0.7, step: 0.005, value: 0.55, fmt: function (x) { return x.toFixed(3); } },
        { k: "k", label: "Stake, as a multiple of Kelly", min: 0, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2) + " × Kelly"; } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var fs = 2 * v.p - 1, f = Math.min(0.999, v.k * fs), gr = function (x) { return v.p * Math.log(1 + x) + (1 - v.p) * Math.log(1 - x); };
        var fx = QB.linspace(0, Math.min(0.999, Math.max(0.05, 3 * fs)), 120), a = g[0].axes({ x: [0, fx[119]], y: [-Math.max(0.004, gr(fs)) * 1.5, Math.max(0.004, gr(fs)) * 1.4], title: "Growth rate per bet", xlabel: "fraction of wealth staked", yfmt: function (y) { return (100 * y).toFixed(1) + "%"; } });
        a.line(fx, fx.map(gr), { color: C.p, width: 2 }); a.hline(0, { dash: null }); a.vline(fs, { color: C.gain }); a.dots([f], [gr(f)], { color: C.ink, r: 5 });
        a.text(fs, -Math.max(0.004, gr(fs)) * 1.3, " Kelly", { color: C.gain });
        var n = 500, r = QB.rng(s.seed + 160), xs = QB.linspace(0, n, n + 1), b = g[1].axes({ x: [0, n], y: [-4, 6], title: "Wealth on 30 paths (log₁₀)", xlabel: "bet" }), lost = 0, k, i;
        for (k = 0; k < 30; k++) { var y = [0]; for (i = 1; i <= n; i++) y.push(y[i - 1] + Math.log10(r() < v.p ? 1 + f : 1 - f)); if (y[n] < 0) lost++; b.line(xs, y, { color: y[n] < 0 ? C.loss : C.gain, width: 1, alpha: 0.6 }); }
        b.hline(0, { dash: null }); b.line([0, n], [0, n * gr(f) / Math.LN10], { color: C.ink, width: 1.5, dash: [5, 4] });
        s.out = [fs, gr(f), lost];
      },
      readout: function (v, s) { return [["Kelly fraction 2p − 1", pct(s.out[0], 1)], ["growth per bet at your stake", pct(s.out[1], 3)], ["paths below their start", s.out[2] + " of 30"]]; },
      note: "The dashed line is the growth rate times the number of bets: the median path. Half Kelly keeps three quarters of the growth.",
    });
  };
})();
