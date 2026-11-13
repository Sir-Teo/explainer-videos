// Interactives for Stage II, Bachelor's: Methods (Parts 11-15).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  var LF = [0]; // log factorials, for exact binomial probabilities
  (function () { for (var i = 1; i <= 200; i++) LF.push(LF[i - 1] + Math.log(i)); })();
  function binom(n, x, p) { return Math.exp(LF[n] - LF[x] - LF[n - x] + x * Math.log(p) + (n - x) * Math.log(1 - p)); }

  // ---- Part 11: the exact coverage of the Wald and Wilson intervals -----------------------------------------
  W.waldsawtooth = function (el) {
    var ends = function (n, z, wilson) { // the interval after each count x = 0..n
      var lo = [], hi = [], x, ph, c, h;
      for (x = 0; x <= n; x++) {
        ph = x / n;
        if (wilson) { c = (ph + z * z / (2 * n)) / (1 + z * z / n); h = z * Math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n); }
        else { c = ph; h = z * Math.sqrt(ph * (1 - ph) / n); }
        lo.push(Math.max(0, c - h)); hi.push(Math.min(1, c + h));
      }
      return [lo, hi];
    };
    var cover = function (n, p, e) { // the total probability of the counts whose interval contains p
      var s = 0, x;
      for (x = 0; x <= n; x++) if (e[0][x] <= p + 1e-12 && p <= e[1][x] + 1e-12) s += binom(n, x, p);
      return Math.min(1, s);
    };
    QB.widget(el, {
      title: "The sawtooth: exact coverage of two intervals for a proportion",
      sub: "Coverage is computed exactly, as a sum over the n + 1 possible counts: red is the textbook (Wald) interval, blue is Wilson's. Slide n one step at a time and watch the red curve jump; move p towards 0 and watch it collapse.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Sample size n", min: 5, max: 200, step: 1, value: 50 },
        { k: "p", label: "True proportion p", min: 0.01, max: 0.5, step: 0.005, value: 0.2, fmt: function (x) { return x.toFixed(3); } },
        { k: "lev", label: "Nominal level", min: 80, max: 99, step: 1, value: 95, fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, s) {
        var z = QB.inv(1 - (1 - v.lev / 100) / 2), nom = v.lev / 100, n = v.n, i, m;
        var eW = ends(n, z, false), eS = ends(n, z, true), ps = [], cW = [], cS = [], sum = 0;
        for (i = 0; i < 198; i++) { ps.push(0.005 + 0.0025 * i); cW.push(cover(n, ps[i], eW)); cS.push(cover(n, ps[i], eS)); sum += cW[i]; }
        var ns = [], dW = [], dS = [];
        for (m = 5; m <= 200; m++) { ns.push(m); dW.push(cover(m, v.p, ends(m, z, false))); dS.push(cover(m, v.p, ends(m, z, true))); }
        s.out = [cover(n, v.p, eW), cover(n, v.p, eS), sum / 198, nom];
        var ylo = Math.max(0, nom - 0.25), pc = function (y) { return Math.round(100 * y) + "%"; };
        var a = g[0].axes({ x: [0, 0.5], y: [ylo, 1], title: "Coverage against p, at n = " + n, xlabel: "true proportion p", yfmt: pc });
        a.hline(nom, { color: C.muted });
        a.line(ps, cS, { color: C.spot, width: 1.3 }).line(ps, cW, { color: C.loss, width: 1.3 });
        a.vline(v.p, { color: C.idea });
        a.legend([["Wald", C.loss], ["Wilson", C.spot], ["promised", C.muted]], { pos: "br" });
        var b = g[1].axes({ x: [5, 200], y: [ylo, 1], title: "Coverage against n, at p = " + v.p.toFixed(3), xlabel: "sample size n", yfmt: pc, xticks: [5, 50, 100, 150, 200] });
        b.hline(nom, { color: C.muted });
        b.line(ns, dS, { color: C.spot, width: 1.3 }).line(ns, dW, { color: C.loss, width: 1.3 });
        b.vline(n, { color: C.idea });
      },
      readout: function (v, s) {
        return [["Wald covers", QB.pct(s.out[0])], ["Wilson covers", QB.pct(s.out[1])], ["promised", QB.pct(s.out[3], 0)], ["Wald, mean over p", QB.pct(s.out[2])]];
      },
      note: "Exact binomial sums, no simulation. The gold line marks the chosen p (left) and n (right). The left panel shows p up to 0.5; the other half is its mirror image. Wilson's interval is near the promise on average but is not guaranteed at every p.",
    });
  };

  // ---- Part 12: least squares, one movable point ------------------------------------------------------------
  W.leastsquares = function (el) {
    QB.widget(el, {
      title: "One point against thirty: leverage and influence",
      sub: "Thirty simulated points follow y = 1 + 2x plus noise. Slide the gold point: far from the other x values it has leverage, and off the line it has a large residual. Only with both does it drag the fitted line.",
      panels: 2, height: 300,
      controls: [
        { k: "px", label: "The gold point's x", min: 0, max: 10, step: 0.1, value: 8, fmt: function (x) { return x.toFixed(1); } },
        { k: "off", label: "Its distance above the true line", min: -8, max: 8, step: 0.2, value: -6, fmt: function (x) { return fmt(x, 1); } },
        { k: "noise", label: "Noise sd of the other points", min: 0.2, max: 3, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 40), n = 30, xs = [], ys = [], i;
        for (i = 0; i < n; i++) { var x = 0.5 + 3.5 * r(); xs.push(x); ys.push(1 + 2 * x + v.noise * r.normal()); }
        var fit = function (X, Y) {
          var mx = QB.mean(X), my = QB.mean(Y), sxx = 0, sxy = 0, k;
          for (k = 0; k < X.length; k++) { sxx += (X[k] - mx) * (X[k] - mx); sxy += (X[k] - mx) * (Y[k] - my); }
          return { b: sxy / sxx, a: my - sxy / sxx * mx, mx: mx, sxx: sxx };
        };
        var f0 = fit(xs, ys), X1 = xs.concat([v.px]), Y1 = ys.concat([1 + 2 * v.px + v.off]), f1 = fit(X1, Y1);
        var h = 1 / (n + 1) + (v.px - f1.mx) * (v.px - f1.mx) / f1.sxx, res = [], rss = 0;
        for (i = 0; i <= n; i++) { res.push(Y1[i] - f1.a - f1.b * X1[i]); rss += res[i] * res[i]; }
        var s2 = rss / (n - 1), cook = res[n] * res[n] / (2 * s2) * h / ((1 - h) * (1 - h));
        s.out = [f0.b, f1.b, h, cook];
        var a = g[0].axes({ x: [0, 10], y: [-6, 28], title: "The fit without and with the gold point", xlabel: "x" });
        a.line([0, 10], [1, 21], { color: C.muted, dash: [4, 4], width: 1 });
        a.line([0, 10], [f0.a, f0.a + 10 * f0.b], { color: C.spot, width: 1.5, alpha: 0.7 });
        a.line([0, 10], [f1.a, f1.a + 10 * f1.b], { color: C.idea, width: 2.2 });
        a.dots(xs, ys, { color: C.spot, r: 2.6, alpha: 0.85 });
        a.dots([v.px], [1 + 2 * v.px + v.off], { color: C.idea, r: 6 });
        a.legend([["fit with the gold point", C.idea], ["fit without it", C.spot], ["truth", C.muted]], { pos: "tl" });
        var lev = X1.map(function (x) { return 1 / (n + 1) + (x - f1.mx) * (x - f1.mx) / f1.sxx; });
        var b = g[1].axes({ x: [0, 1], y: [-9, 9], title: "Residual against leverage", xlabel: "leverage h" });
        b.hline(0, { color: C.muted });
        b.dots(lev.slice(0, n), res.slice(0, n), { color: C.spot, r: 2.6, alpha: 0.85 });
        b.dots([h], [res[n]], { color: C.idea, r: 6 });
        b.vline(4 / (n + 1), { color: C.loss });
        b.text(4 / (n + 1), 8, "2p/n", { color: C.loss, dx: 5 });
      },
      readout: function (v, s) {
        return [["slope without", fmt(s.out[0], 2)], ["slope with", fmt(s.out[1], 2)], ["leverage of the gold point", fmt(s.out[2], 2)], ["Cook's distance", fmt(s.out[3], 2)]];
      },
      note: "Simulated data. Cook's distance is residual² × leverage / (1 − leverage)² in units of p·s²; a value near 1 means deleting the point moves the fit about as far as its own uncertainty.",
    });
  };

  // ---- Part 13: one field, three layouts --------------------------------------------------------------------
  W.fieldlayout = function (el) {
    var R = 6, K = 12, N = R * K, names = ["systematic", "randomized", "blocked"];
    var shuffle = function (a, r) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
    var layout = function (kind, r) { // 1 = new variety, 0 = standard; index = row * K + column
      var t = new Array(N), i, c, col;
      if (kind === 0) { for (i = 0; i < N; i++) t[i] = i % K >= K / 2 ? 1 : 0; return t; } // the east half
      if (kind === 1) { for (i = 0; i < N; i++) t[i] = i < N / 2 ? 1 : 0; return shuffle(t, r); }
      for (c = 0; c < K; c++) { col = shuffle([1, 1, 1, 0, 0, 0], r); for (i = 0; i < R; i++) t[i * K + c] = col[i]; } // each column is a block
      return t;
    };
    QB.widget(el, {
      title: "One field, three layouts",
      sub: "A field of 72 plots is more fertile towards the east. Half the plots get a new variety (gold dots). Choose a layout, then raise the gradient: the systematic layout credits the soil to the variety, randomization scatters around the truth, and blocking by column narrows the scatter.",
      panels: 2, height: 300,
      controls: [
        { k: "lay", label: "Layout shown", min: 0, max: 2, step: 1, value: 2, fmt: function (x) { return names[x]; } },
        { k: "grad", label: "Fertility gradient, west to east", min: 0, max: 8, step: 0.5, value: 6, fmt: function (x) { return x.toFixed(1); } },
        { k: "noise", label: "Plot-to-plot noise sd", min: 0.5, max: 4, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "gain", label: "True gain of the new variety", min: 0, max: 4, step: 0.25, value: 2, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New field", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 130), base = [], i, k, rep;
        for (i = 0; i < N; i++) base.push(v.grad * ((i % K) / (K - 1) - 0.5) + v.noise * r.normal());
        var est = function (t) { var a = 0, b = 0; for (var j = 0; j < N; j++) { if (t[j]) a += base[j] + v.gain; else b += base[j]; } return (a - b) / (N / 2); };
        var rr = QB.rng(s.seed + 131), shown = layout(v.lay, QB.rng(s.seed + 132)), sys = est(layout(0, rr)), eC = [], eB = [];
        for (rep = 0; rep < 300; rep++) { eC.push(est(layout(1, rr))); eB.push(est(layout(2, rr))); }
        s.out = [sys, QB.sd(eC), QB.sd(eB), est(shown)];
        // the field from above
        var c = g.ctx, bx = g[0].box, cw = Math.min(40, (bx.w - 36) / K), ch = Math.min(30, (bx.h - 84) / R), x0 = bx.x + (bx.w - cw * K) / 2, y0 = bx.y + 34;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The field, " + names[v.lay] + " layout", x0, bx.y + 8);
        for (i = 0; i < N; i++) {
          var u = Math.max(0, Math.min(1, (base[i] + 7) / 14)), px = x0 + (i % K) * cw, py = y0 + Math.floor(i / K) * ch;
          c.fillStyle = "rgb(" + Math.round(52 - 22 * u) + "," + Math.round(62 + 100 * u) + "," + Math.round(48 + 22 * u) + ")";
          c.fillRect(px + 1, py + 1, cw - 2, ch - 2);
          if (shown[i]) { c.fillStyle = C.idea; c.beginPath(); c.arc(px + cw / 2, py + ch / 2, Math.min(cw, ch) * 0.2, 0, 6.2832); c.fill(); }
        }
        if (v.lay === 2) { c.strokeStyle = C.ink; c.globalAlpha = 0.45; c.lineWidth = 1; for (k = 0; k < K; k++) c.strokeRect(x0 + k * cw + 0.5, y0 + 0.5, cw - 1, ch * R - 1); c.globalAlpha = 1; }
        c.fillStyle = C.muted; c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "top";
        c.textAlign = "left"; c.fillText("west", x0, y0 + ch * R + 6);
        c.textAlign = "right"; c.fillText("east", x0 + cw * K, y0 + ch * R + 6);
        c.textAlign = "center"; c.fillText("greener = more fertile", x0 + cw * K / 2, y0 + ch * R + 6);
        c.fillText("gold dot = new variety" + (v.lay === 2 ? "; a column is a block" : ""), x0 + cw * K / 2, y0 + ch * R + 23);
        c.restore();
        // the estimates over 300 fresh randomizations of the same field
        var lo = -4, hi = 10, nb = 56, w = (hi - lo) / nb, hC = QB.hist(eC, lo, hi, nb), hB = QB.hist(eB, lo, hi, nb), xs = [], top = 1;
        for (i = 0; i < nb; i++) { xs.push(lo + (i + 0.5) * w); top = Math.max(top, hC[i], hB[i]); }
        var a = g[1].axes({ x: [lo, hi], y: [0, top * 1.3], title: "Estimated gain over 300 randomizations", xlabel: "estimated gain", noY: true });
        a.bars(xs, hC, w, { color: C.spot, alpha: 0.7 }).bars(xs, hB, w, { color: C.idea, alpha: 0.7 });
        a.vline(v.gain, { color: C.ink }).vline(sys, { color: C.loss, dash: [] });
        a.legend([["randomized", C.spot], ["blocked", C.idea], ["systematic", C.loss], ["truth", C.ink]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["systematic estimate", fmt(s.out[0], 2)], ["sd, randomized", fmt(s.out[1], 2)], ["sd, blocked", fmt(s.out[2], 2)], ["this layout's estimate", fmt(s.out[3], 2)]];
      },
      note: "Simulated data. The histograms re-randomize the same field 300 times, so their spread is the randomization distribution; the systematic layout (new variety on the east half) has no spread to show, only its bias.",
    });
  };

  // ---- Part 14: the Challenger flights, a line and a logistic curve ------------------------------------------
  W.oringlogit = function (el) {
    var T = [66, 70, 69, 68, 67, 72, 73, 70, 57, 63, 70, 78, 67, 53, 67, 75, 70, 81, 76, 79, 75, 76, 58]; // launch order
    var Y = [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1]; // any O-ring distress
    var sig = function (e) { return 1 / (1 + Math.exp(-Math.max(-35, Math.min(35, e)))); };
    QB.widget(el, {
      title: "The Challenger flights: a line, and a logistic curve fitted step by step",
      sub: "The 23 flights before Challenger, by launch temperature: 1 means some O-ring distress. Take Newton steps from zero and watch the curve settle; move the probe to the forecast 31 °F and compare the curve with the least-squares line; then remove the flights without distress, as the chart that evening did.",
      panels: 2, height: 300,
      controls: [
        { k: "steps", label: "Newton steps taken", min: 0, max: 8, step: 1, value: 8 },
        { k: "probe", label: "Temperature probe (°F)", min: 31, max: 85, step: 1, value: 31 },
        { k: "zeros", label: "Flights without distress included", min: 0, max: 16, step: 1, value: 16, fmt: function (x) { return x + " of 16"; } },
      ],
      draw: function (g, v, s) {
        var xs = [], ys = [], out = [], i, k, seen = 0;
        for (i = 0; i < T.length; i++) {
          if (Y[i] === 1 || seen < v.zeros) { xs.push(T[i] - 70); ys.push(Y[i]); } else out.push(i);
          if (Y[i] === 0) seen++;
        }
        var n = xs.length, mx = QB.mean(xs), my = QB.mean(ys), sxx = 0, sxy = 0;
        for (i = 0; i < n; i++) { sxx += (xs[i] - mx) * (xs[i] - mx); sxy += (xs[i] - mx) * (ys[i] - my); }
        var lb = sxx > 0 ? sxy / sxx : 0, la = my - lb * mx; // the least-squares line
        var ll = function (b0, b1) { var t = 0; for (var j = 0; j < n; j++) { var e = Math.max(-35, Math.min(35, b0 + b1 * xs[j])); t += ys[j] * e - Math.log(1 + Math.exp(e)); } return t; };
        var b0 = 0, b1 = 0, path = [[0, 0, ll(0, 0)]];
        for (k = 0; k < 8; k++) { // Newton's method = iteratively reweighted least squares, with step-halving
          var s0 = 0, s1 = 0, h00 = 1e-9, h01 = 0, h11 = 1e-9;
          for (i = 0; i < n; i++) { var p = sig(b0 + b1 * xs[i]), w = Math.max(p * (1 - p), 1e-9); s0 += ys[i] - p; s1 += (ys[i] - p) * xs[i]; h00 += w; h01 += w * xs[i]; h11 += w * xs[i] * xs[i]; }
          var det = h00 * h11 - h01 * h01, d0 = 0, d1 = 0, cur = path[k][2], half;
          if (det > 1e-12) { d0 = (h11 * s0 - h01 * s1) / det; d1 = (h00 * s1 - h01 * s0) / det; }
          d0 = Math.max(-6, Math.min(6, d0)); d1 = Math.max(-2, Math.min(2, d1));
          for (half = 0; half < 20 && ll(b0 + d0, b1 + d1) < cur - 1e-10; half++) { d0 /= 2; d1 /= 2; }
          if (half === 20) { d0 = 0; d1 = 0; }
          b0 += d0; b1 += d1; path.push([b0, b1, ll(b0, b1)]);
        }
        var f = path[v.steps], px = v.probe - 70, orr = Math.exp(Math.max(-35, Math.min(35, -10 * f[1])));
        s.out = [sig(f[0] + f[1] * px), la + lb * px, f[2] > -0.005 ? 0 : f[2], orr];
        var a = g[0].axes({ x: [28, 86], y: [-0.5, 2], title: "Distress against launch temperature", xlabel: "launch temperature (°F)", yticks: [0, 0.5, 1, 1.5, 2] });
        a.hline(0, { color: C.muted, dash: [] }).hline(1, { color: C.muted, dash: [] });
        var grid = QB.linspace(28, 86, 117);
        a.line([28, 86], [la + lb * (28 - 70), la + lb * (86 - 70)], { color: C.loss, width: 1.6, dash: [5, 4] });
        a.line(grid, grid.map(function (t) { return sig(f[0] + f[1] * (t - 70)); }), { color: C.idea, width: 2.2 });
        var count = {}, jit = function (i) { var key = T[i] + "/" + Y[i]; count[key] = (count[key] || 0) + 1; return (Y[i] ? 1 : -1) * 0.075 * (count[key] - 1); };
        for (i = 0; i < T.length; i++) a.dots([T[i]], [Y[i] + jit(i)], { color: out.indexOf(i) >= 0 ? C.muted : C.spot, r: 3.4, alpha: out.indexOf(i) >= 0 ? 0.35 : 0.95 });
        a.vline(v.probe, { color: C.ink });
        a.legend([["logistic curve", C.idea], ["least-squares line", C.loss], ["flights (grey: left out)", C.spot]], { pos: "tr" });
        var b = g[1].axes({ x: [0, 8], y: [-17, 0], title: "Log-likelihood after each Newton step", xlabel: "step", xticks: [0, 1, 2, 3, 4, 5, 6, 7, 8] });
        var st = [0, 1, 2, 3, 4, 5, 6, 7, 8], lls = path.map(function (q) { return q[2]; });
        b.line(st, lls, { color: C.spot, width: 1.6 }).dots(st, lls, { color: C.spot, r: 3 });
        b.dots([v.steps], [f[2]], { color: C.idea, r: 6 });
        b.text(8, -15.2, n + " flights in the fit", { align: "right", color: C.muted });
      },
      readout: function (v, s) {
        return [["curve at " + v.probe + " °F", fmt(s.out[0], 4)], ["line at " + v.probe + " °F", fmt(s.out[1], 2)], ["log-likelihood", fmt(s.out[2], 2)],
          ["odds ratio per 10 °F colder", s.out[3] > 9999 ? "over 9,999" : fmt(s.out[3], 1)]];
      },
      note: "Launch temperatures and distress for the 23 flights from Dalal, Fowlkes and Hoadley (1989). Flights without distress are added in launch order. With none of them the outcome never varies, no finite maximum exists, and the steps run off towards certainty. A probe at 31 °F is 22 °F colder than any flight: an extrapolation.",
    });
  };

  // ---- Part 15: a beta prior, Bayes's table, and the credible interval's coverage --------------------------
  W.billiardbeta = function (el) {
    var M = 400, LT = [], L1 = [], j;
    for (j = 0; j < M; j++) { LT.push(Math.log((j + 0.5) / M)); L1.push(Math.log(1 - (j + 0.5) / M)); }
    var dens = function (a, b) { // the Beta(a, b) density at the M midpoints of (0, 1)
      var d = [], top = -Infinity, tot = 0, i, e;
      for (i = 0; i < M; i++) { e = (a - 1) * LT[i] + (b - 1) * L1[i]; d.push(e); if (e > top) top = e; }
      for (i = 0; i < M; i++) { d[i] = Math.exp(d[i] - top); tot += d[i]; }
      for (i = 0; i < M; i++) d[i] *= M / tot;
      return d;
    };
    var interval = function (d) { // the central 95% of a density on the grid
      var acc = 0, lo = 0, hi = 1, i, nx, gotLo = false;
      for (i = 0; i < M; i++) {
        nx = acc + d[i] / M;
        if (!gotLo && nx >= 0.025) { lo = (i + (0.025 - acc) / (nx - acc)) / M; gotLo = true; }
        if (nx >= 0.975) { hi = (i + (0.975 - acc) / (nx - acc)) / M; break; }
        acc = nx;
      }
      return [lo, hi];
    };
    QB.widget(el, {
      title: "Bayes's table: the posterior, and how often its interval is right",
      sub: "A hidden ball sits at p; each rolled ball stops to its left with probability p. Left: the prior, the posterior and its 95% interval. Right: how often that interval would contain each fixed truth. Give the prior weight in the wrong place (a = 18, b = 2, truth 0.05) and the coverage at the truth falls to zero, while the average over the prior stays at 95%.",
      panels: 2, height: 300,
      controls: [
        { k: "a", label: "Prior a: imaginary balls left", min: 1, max: 20, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "b", label: "Prior b: imaginary balls right", min: 1, max: 20, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Balls rolled", min: 0, max: 60, step: 1, value: 12 },
        { k: "p", label: "The hidden ball's position p", min: 0.02, max: 0.98, step: 0.01, value: 0.62, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "Roll again", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 151), n = v.n, x = 0, i, k;
        for (i = 0; i < n; i++) if (r() < v.p) x++;
        var prior = dens(v.a, v.b), post = dens(v.a + x, v.b + n - x), ci = interval(post), grid = [], mean = (v.a + x) / (v.a + v.b + n);
        for (i = 0; i < M; i++) grid.push((i + 0.5) / M);
        var ends = []; for (k = 0; k <= n; k++) ends.push(interval(dens(v.a + k, v.b + n - k)));
        var cover = function (p) { var t = 0; for (var q = 0; q <= n; q++) if (ends[q][0] <= p && p <= ends[q][1]) t += binom(n, q, p); return Math.min(1, t); };
        var cp = [], cv = [], avg = 0, wt = 0;
        for (i = 0; i < 200; i++) { cp.push((i + 0.5) / 200); cv.push(cover(cp[i])); avg += cv[i] * prior[2 * i] + cv[i] * prior[2 * i + 1]; wt += prior[2 * i] + prior[2 * i + 1]; }
        s.out = [x, n, v.a + x, v.b + n - x, mean, ci[0], ci[1], cover(v.p), wt > 0 ? avg / wt : 0];
        var top = 3; for (i = 0; i < M; i++) top = Math.max(top, post[i], Math.min(prior[i], 12));
        var a = g[0].axes({ x: [0, 1], y: [0, top * 1.45], title: "Prior and posterior of the position", xlabel: "position p", noY: true });
        var inx = [], iny = []; for (i = 0; i < M; i++) if (grid[i] >= ci[0] && grid[i] <= ci[1]) { inx.push(grid[i]); iny.push(post[i]); }
        if (inx.length > 1) a.area(inx, iny, 0, { color: C.idea, alpha: 0.28 });
        a.line(grid, prior, { color: C.cash, width: 1.5 }).line(grid, post, { color: C.idea, width: 2.2 });
        a.vline(v.p, { color: C.spot, dash: [] });
        a.legend([["prior", C.cash], ["posterior, 95% shaded", C.idea], ["the hidden ball", C.spot]], { pos: mean < 0.5 ? "tr" : "tl" });
        var b = g[1].axes({ x: [0, 1], y: [0, 1.04], title: "Coverage at each fixed truth", xlabel: "true p", yfmt: function (y) { return Math.round(100 * y) + "%"; }, yticks: [0, 0.25, 0.5, 0.75, 0.95] });
        var pm = 0; for (i = 0; i < M; i++) pm = Math.max(pm, prior[i]);
        b.area(grid, prior.map(function (d) { return 0.2 * d / pm; }), 0, { color: C.cash, alpha: 0.3 });
        b.hline(0.95, { color: C.muted });
        b.line(cp, cv, { color: C.realized, width: 1.6 });
        b.vline(v.p, { color: C.spot, dash: [] });
        b.dots([v.p], [s.out[7]], { color: C.spot, r: 4.5 });
        b.legend([["coverage", C.realized], ["prior (shape)", C.cash]], { pos: "bl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["stopped left", o[0] + " of " + o[1]], ["posterior", "Beta(" + (+o[2].toFixed(1)) + ", " + (+o[3].toFixed(1)) + ")"], ["mean", fmt(o[4], 3)],
          ["95% interval", fmt(o[5], 2) + " to " + fmt(o[6], 2)], ["coverage at this truth", QB.pct(o[7])], ["average over the prior", QB.pct(o[8])]];
      },
      note: "Simulated rolls. Posteriors and their equal-tailed intervals are computed on a grid of 400 points, so the prior-averaged coverage shows 95% only to within about a point. Coverage at a fixed truth is an exact binomial sum over the possible counts.",
    });
  };
})();
