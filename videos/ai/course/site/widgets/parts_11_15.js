// Interactives for AI, Built, Parts 11-15: optimizers, scale, attention, the lineage, memory.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var clamp = function (x, lo, hi) { return x < lo ? lo : x > hi ? hi : x; };

  // ---- Part 11: gradient descent and the heavy ball in a quadratic valley -----------------------------------
  W.valleyrace = function (el) {
    var X0 = -1, Y0 = 0.8, NSIM = 3000, NPLOT = 200;
    var radius = function (eta, beta, lam) { // the larger root modulus of z^2 - (1 + beta - eta lam) z + beta = 0
      var b = 1 + beta - eta * lam, disc = b * b - 4 * beta;
      if (disc < 0) return Math.sqrt(beta);
      return (Math.abs(b) + Math.sqrt(disc)) / 2;
    };
    var simulate = function (kap, eta, beta) { // f = (x^2 / kappa + y^2) / 2: curvature 1 across the valley, 1/kappa along it
      var x = X0, y = Y0, px = X0, py = Y0, f0 = (X0 * X0 / kap + Y0 * Y0) / 2, xs = [], ys = [], gap = [], hit = -1, k, nx, ny, f;
      for (k = 0; k < NSIM; k++) {
        f = (x * x / kap + y * y) / 2 / f0;
        if (k < NPLOT) { xs.push(clamp(x, -9, 9)); ys.push(clamp(y, -9, 9)); gap.push(clamp(f, 1e-12, 1e6)); }
        if (hit < 0 && f < 1e-6) hit = k;
        if (!(Math.abs(x) < 1e30 && Math.abs(y) < 1e30)) { x = clamp(x, -1e30, 1e30); y = clamp(y, -1e30, 1e30); px = x; py = y; continue; }
        nx = x - eta * x / kap + beta * (x - px); ny = y - eta * y + beta * (y - py);
        px = x; py = y; x = nx; y = ny;
      }
      return { xs: xs, ys: ys, gap: gap, hit: hit };
    };
    QB.widget(el, {
      title: "Two walkers in a valley: gradient descent and the heavy ball",
      sub: "The loss is a bowl with curvature L = 1 across the valley and L / κ along it. Blue is gradient descent, gold adds momentum β with the same step. Raise κ and blue crawls along the floor while gold keeps moving; then push the step past 2 / L and watch blue leave the valley, while gold survives until 2(1 + β) / L.",
      panels: 2, height: 300,
      controls: [
        { k: "lk", label: "Condition number κ", min: 0.3, max: 2.5, step: 0.05, value: 1.5, fmt: function (x) { return String(Math.round(Math.pow(10, x))); } },
        { k: "s", label: "Step size η, in units of 1 / L", min: 0.1, max: 2.4, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "beta", label: "Momentum β of the heavy ball", min: 0, max: 0.98, step: 0.02, value: 0.7, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var kap = Math.round(Math.pow(10, v.lk)), gd = simulate(kap, v.s, 0), hb = simulate(kap, v.s, v.beta), i;
        var rg = Math.max(radius(v.s, 0, 1), radius(v.s, 0, 1 / kap)), rh = Math.max(radius(v.s, v.beta, 1), radius(v.s, v.beta, 1 / kap));
        s.out = [rg, rh, gd.hit, hb.hit, kap];
        var a = g[0].axes({ x: [-1.25, 0.45], y: [-1, 1], title: "The first 60 steps, seen from above", xlabel: "along the valley (curvature L / κ)" });
        a.clip(function (c) {
          var f0 = (X0 * X0 / kap + Y0 * Y0) / 2, lev = [1, 0.6, 0.3, 0.12, 0.04, 0.01], ux = Math.abs(a.px(1) - a.px(0)), uy = Math.abs(a.py(1) - a.py(0));
          c.strokeStyle = C.line; c.lineWidth = 1;
          for (i = 0; i < lev.length; i++) {
            var r = Math.sqrt(2 * f0 * lev[i]);
            c.beginPath(); c.ellipse(a.px(0), a.py(0), Math.min(r * Math.sqrt(kap) * ux, 20000), r * uy, 0, 0, 6.2832); c.stroke();
          }
        });
        a.line(gd.xs.slice(0, 61), gd.ys.slice(0, 61), { color: C.spot, width: 1.4 }).dots(gd.xs.slice(0, 61), gd.ys.slice(0, 61), { color: C.spot, r: 2.2 });
        a.line(hb.xs.slice(0, 61), hb.ys.slice(0, 61), { color: C.idea, width: 1.4 }).dots(hb.xs.slice(0, 61), hb.ys.slice(0, 61), { color: C.idea, r: 2.2 });
        a.dots([0], [0], { color: C.ink, r: 4 });
        a.legend([["gradient descent", C.spot], ["heavy ball", C.idea], ["minimum", C.ink]], { pos: "br" });
        var ks = []; for (i = 0; i < NPLOT; i++) ks.push(i);
        var b = g[1].axes({ x: [0, NPLOT - 1], y: [1e-12, 1e6], logy: true, title: "The gap f − f*, relative to the start", xlabel: "step", yticks: [1e-12, 1e-9, 1e-6, 1e-3, 1, 1e3, 1e6], yfmt: function (y) { return y === 1 ? "1" : "1e" + Math.round(Math.log(y) / Math.LN10); } });
        b.hline(1e-6, { color: C.muted });
        b.line(ks, gd.gap, { color: C.spot, width: 1.7 }).line(ks, hb.gap, { color: C.idea, width: 1.7 });
        b.text(NPLOT - 4, 1e-6, "a millionth", { align: "right", color: C.muted, dy: -9 });
      },
      readout: function (v, s) {
        var o = s.out, rate = function (r) { return r >= 1 ? (r > 1 + 1e-9 ? "diverges (×" + fmt(r, 3) + ")" : "stalls (×1.000)") : "×" + fmt(r, 4); };
        var steps = function (h, r) { return h >= 0 ? String(h) : r >= 1 ? "never" : "over " + NSIM; };
        return [["κ", String(o[4])], ["gradient descent, per step", rate(o[0])], ["heavy ball, per step", rate(o[1])],
          ["steps to a millionth: gradient descent", steps(o[2], o[0])], ["heavy ball", steps(o[3], o[1])]];
      },
      note: "Exact iterations on f = (x²/κ + y²)/2 from the same start; no noise. The per-step factors are the largest root moduli of each method's recurrence over the two curvatures (for gradient descent, max |1 − ηλ|). The tuned heavy ball has η = 4 / (√L + √μ)² and √β = (√κ − 1) / (√κ + 1).",
    });
  };
  var human = function (x, digits) { // 74,500 -> "74.5k"
    var u = [[1e15, "Q"], [1e12, "T"], [1e9, "B"], [1e6, "M"], [1e3, "k"]], i;
    for (i = 0; i < u.length; i++) if (x >= u[i][0]) return String(parseFloat((x / u[i][0]).toPrecision(typeof digits === "number" ? digits : 3))) + u[i][1];
    return String(Math.round(x));
  };
  var sci = function (x) { // 3.14e23 -> "3.14 × 10^23"
    if (!(x > 0)) return "0";
    var e = Math.floor(Math.log(x) / Math.LN10 + 1e-9), m = x / Math.pow(10, e);
    if (m >= 9.995) { m = 1; e += 1; }
    return m.toFixed(2) + " × 10^" + e;
  };

  // ---- Part 12: Chinchilla's valley: one budget, split between size and data ---------------------------------
  W.isoflopvalley = function (el) {
    var E = 1.76, A = 0.1915 * Math.pow(74500, 0.58), B = 0.2584 * Math.pow(2.2e6, 0.43); // see the note
    var loss = function (N, D, al, be) { return E + A * Math.pow(N, -al) + B * Math.pow(D, -be); };
    var best = function (Cb, al, be) { return Math.pow(al * A / (be * B), 1 / (al + be)) * Math.pow(Cb / 6, be / (al + be)); };
    QB.widget(el, {
      title: "Chinchilla's valley: how to split a compute budget",
      sub: "The loss is a floor plus a term that falls with parameters N and one that falls with data D, and training costs C = 6ND. Left: the loss along three budgets as the model grows; each curve has one lowest point. Right: where that point sits as the budget grows. Change the exponents α and β and watch the best size bend toward the model or toward the data; then slide the model off the optimum and read what it costs.",
      panels: 2, height: 300,
      controls: [
        { k: "al", label: "α: how fast loss falls with size", min: 0.2, max: 0.9, step: 0.01, value: 0.58, fmt: function (x) { return x.toFixed(2); } },
        { k: "be", label: "β: how fast loss falls with data", min: 0.2, max: 0.9, step: 0.01, value: 0.43, fmt: function (x) { return x.toFixed(2); } },
        { k: "lc", label: "Budget C, in operations", min: 9, max: 15, step: 0.1, value: 12, fmt: function (x) { return "10^" + x.toFixed(1); } },
        { k: "rel", label: "Model size, relative to the best one", min: -1.5, max: 1.5, step: 0.05, value: 0, fmt: function (x) { return "× " + Math.pow(10, x).toPrecision(2); } },
      ],
      draw: function (g, v, s) {
        var Cb = Math.pow(10, v.lc), a = v.be / (v.al + v.be), Ns = best(Cb, v.al, v.be), Ds = Cb / (6 * Ns), N = Ns * Math.pow(10, v.rel), D = Cb / (6 * N), i, j;
        s.out = [a, Ns, Ds, Ds / Ns, loss(Ns, Ds, v.al, v.be), loss(N, D, v.al, v.be), N];
        var xs = QB.linspace(2, 10, 161).map(function (e) { return Math.pow(10, e); }), cols = [C.cash, C.spot, C.realized], mult = [0.01, 1, 100];
        var p = g[0].axes({ x: [1e2, 1e10], y: [E - 0.1, E + 2.1], logx: true, title: "Loss along three budgets", xlabel: "parameters N", xticks: [1e2, 1e4, 1e6, 1e8, 1e10], xfmt: human });
        p.hline(E, { color: C.muted });
        p.text(1.4e2, E, "floor E", { color: C.muted, dy: -9 });
        var fx = [], fy = [];
        for (j = 0; j <= 60; j++) { var cb = Math.pow(10, 7 + j * 0.2), n0 = best(cb, v.al, v.be); fx.push(n0); fy.push(loss(n0, cb / (6 * n0), v.al, v.be)); }
        p.line(fx, fy, { color: C.idea, width: 1.3, dash: [5, 4] });
        for (i = 0; i < 3; i++) {
          var cc = Cb * mult[i], ys = xs.map(function (n) { return Math.min(99, loss(n, cc / (6 * n), v.al, v.be)); }), nb = best(cc, v.al, v.be);
          p.line(xs, ys, { color: cols[i], width: i === 1 ? 2.2 : 1.4 });
          p.dots([nb], [loss(nb, cc / (6 * nb), v.al, v.be)], { color: cols[i], r: 3.5 });
        }
        p.dots([clamp(N, 1e2, 1e10)], [Math.min(E + 2.1, s.out[5])], { color: C.idea, r: 5.5 });
        p.legend([["C / 100", C.cash], ["budget C", C.spot], ["100 C", C.realized], ["valley floor", C.idea]], { pos: "tr" });
        var cs = QB.linspace(9, 15, 61).map(function (e) { return Math.pow(10, e); });
        var q = g[1].axes({ x: [1e9, 1e15], y: [1e2, 1e12], logx: true, logy: true, title: "The best split against the budget", xlabel: "budget C = 6ND (operations)",
          xticks: [1e9, 1e11, 1e13, 1e15], xfmt: function (x) { return "1e" + Math.round(Math.log(x) / Math.LN10); }, yticks: [1e2, 1e4, 1e6, 1e8, 1e10, 1e12], yfmt: human });
        q.line(cs, cs.map(function (c0) { return best(c0, v.al, v.be); }), { color: C.spot, width: 2 });
        q.line(cs, cs.map(function (c0) { return c0 / (6 * best(c0, v.al, v.be)); }), { color: C.gain, width: 2 });
        q.vline(Cb, { color: C.idea });
        q.dots([Cb, Cb], [clamp(Ns, 1e2, 1e12), clamp(Ds, 1e2, 1e12)], { color: C.idea, r: 4 });
        q.legend([["best size N*, slope " + a.toFixed(2), C.spot], ["best data D*, slope " + (1 - a).toFixed(2), C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["N* grows like C to the", fmt(o[0], 3)], ["best size N*", human(o[1])], ["best data D*", human(o[2])], ["data per parameter", o[3] >= 100 ? human(o[3]) : fmt(o[3], 1)],
          ["loss at the best split", fmt(o[4], 3)], ["loss at your size (" + human(o[6]) + ")", fmt(Math.min(o[5], 99), 3)]];
      },
      note: "An illustration of L(N, D) = E + A/N^α + B/D^β with C = 6ND. The starting exponents and the floor E = 1.76 bits are the film's fit to its own character models (α = 0.58, β = 0.43, so β/(α + β) = 0.42); A and B are chosen here so that the best split at 10^12 operations is the film's 74,500 parameters and 2.2 million characters, and do not come from the film. Chinchilla's own fits gave an exponent near 0.5: grow size and data together.",
    });
  };
  var arrow = function (c, x0, y0, x1, y1, color, width, alpha) { // a line with a head, in canvas pixels
    var ang = Math.atan2(y1 - y0, x1 - x0), len = Math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)), h = Math.min(9 + width, len);
    c.save(); c.globalAlpha = alpha; c.strokeStyle = color; c.fillStyle = color; c.lineWidth = width; c.lineCap = "round";
    c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1 - 0.6 * h * Math.cos(ang), y1 - 0.6 * h * Math.sin(ang)); c.stroke();
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x1 - h * Math.cos(ang - 0.42), y1 - h * Math.sin(ang - 0.42)); c.lineTo(x1 - h * Math.cos(ang + 0.42), y1 - h * Math.sin(ang + 0.42)); c.closePath(); c.fill();
    c.restore();
  };

  // ---- Part 13: a query among keys: scores, softmax weights, and the blend a head returns --------------------
  W.querycompass = function (el) {
    QB.widget(el, {
      title: "A query among keys: from an average to a recall",
      sub: "Every blue arrow is a key, and the gold arrow is the query. A key's score is β times its dot product with the query; the softmax turns scores into weights (the bars, and each arrow's thickness); the teal arrow is the weighted average the head returns. Turn the query and the weight flows from key to key. At β = 0 every key gets 1/n, the plain average; raise β and one key takes all the weight, a memory recalling a stored pattern.",
      panels: 2, height: 310,
      controls: [
        { k: "th", label: "Direction of the query", min: 0, max: 360, step: 2, value: 40, fmt: function (x) { return x + "°"; } },
        { k: "beta", label: "Sharpness β (in a transformer, 1/√d)", min: 0, max: 30, step: 0.5, value: 4, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Number of keys n", min: 2, max: 12, step: 1, value: 7 },
      ],
      buttons: [{ label: "New keys", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1300), n = v.n, kx = [], ky = [], sc = [], p = [], i, top = -Infinity, tot = 0, best = 0;
        for (i = 0; i < 12; i++) { var ang = 6.2832 * r(), len = 0.75 + 0.3 * r(); if (i < n) { kx.push(len * Math.cos(ang)); ky.push(len * Math.sin(ang)); } }
        var qx = Math.cos(v.th * Math.PI / 180), qy = Math.sin(v.th * Math.PI / 180);
        for (i = 0; i < n; i++) { sc.push(v.beta * (qx * kx[i] + qy * ky[i])); if (sc[i] > top) { top = sc[i]; best = i; } }
        for (i = 0; i < n; i++) { p.push(Math.exp(sc[i] - top)); tot += p[i]; }
        var ox = 0, oy = 0, H = 0;
        for (i = 0; i < n; i++) { p[i] /= tot; ox += p[i] * kx[i]; oy += p[i] * ky[i]; if (p[i] > 1e-12) H -= p[i] * Math.log(p[i]) / Math.LN2; }
        var on = Math.sqrt(ox * ox + oy * oy), bn = Math.sqrt(kx[best] * kx[best] + ky[best] * ky[best]);
        s.out = [p[best], Math.max(0, H), Math.log(n) / Math.LN2, on > 1e-9 ? (ox * kx[best] + oy * ky[best]) / (on * bn) : 0, best + 1];
        var c = g.ctx, bx = g[0].box, cx = bx.x + bx.w / 2, cy = bx.y + bx.h / 2 + 12, R = Math.min(bx.w / 2 - 24, bx.h / 2 - 34) / 1.12;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Keys, the query and what the head returns", bx.x + 12, bx.y + 6);
        c.strokeStyle = C.line; c.lineWidth = 1; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        c.restore();
        for (i = 0; i < n; i++) arrow(c, cx, cy, cx + R * kx[i], cy - R * ky[i], C.spot, 1.2 + 7 * p[i], 0.4 + 0.6 * Math.sqrt(p[i]));
        c.save(); c.font = "11.5px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = C.ink;
        for (i = 0; i < n; i++) { var kl = Math.sqrt(kx[i] * kx[i] + ky[i] * ky[i]); c.fillText(String(i + 1), cx + (R * kl + 11) * kx[i] / kl, cy - (R * kl + 11) * ky[i] / kl); }
        c.restore();
        arrow(c, cx, cy, cx + R * qx, cy - R * qy, C.idea, 2.2, 1);
        if (on > 0.02) arrow(c, cx, cy, cx + R * ox, cy - R * oy, C.realized, 3, 1);
        else { c.save(); c.fillStyle = C.realized; c.beginPath(); c.arc(cx, cy, 4, 0, 6.2832); c.fill(); c.restore(); }
        var xs = []; for (i = 0; i < n; i++) xs.push(i + 1);
        var b = g[1].axes({ x: [0.4, n + 0.6], y: [0, 1.02], title: "The attention weights", xlabel: "key", xticks: xs, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.bars(xs, p, 0.7, { color: function (j) { return j === best ? C.idea : C.spot; } });
        b.hline(1 / n, { color: C.muted });
        b.legend([["query", C.idea], ["keys (thicker = more weight)", C.spot], ["returned blend", C.realized], ["even share 1/n", C.muted]], { pos: p[best] > 0.55 && best >= n / 2 ? "tl" : "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["largest weight", QB.pct(o[0]) + " (key " + o[4] + ")"], ["entropy of the weights", fmt(o[1], 2) + " of " + fmt(o[2], 2) + " bits"],
          ["keys sharing the weight", fmt(Math.pow(2, o[1]), 1)], ["blend's cosine with the top key", fmt(o[3], 2)]];
      },
      note: "Random keys in the plane; the values are the keys themselves, as in a modern Hopfield read ξ ← Xᵀ softmax(βXξ). In a trained head the queries, keys and values are computed from the tokens by learned matrices, and the scores are divided by √d so that they start with a spread of about one.",
    });
  };
  var commas = function (x) { return String(Math.round(x)).replace(/\B(?=(\d{3})+(?!\d))/g, ","); };

  // ---- Part 14: a model's shape, its parameters, and the compute to train it ---------------------------------
  W.sixnd = function (el) {
    var VOCAB = 50257, CTX = 2048; // GPT-3's vocabulary and context
    var MODELS = [ // parameters N and training tokens D as the film gives them (tokens per parameter in brackets there)
      ["GPT-3", 174.6e9, 300e9, "right", -7, 0], ["Gopher", 280e9, 300e9, "left", 7, 0], ["Chinchilla", 70e9, 1.4e12, "right", -7, -11],
      ["LLaMA-7B", 6.7e9, 1.0e12, "right", -7, 0], ["Llama 3.1 405B", 405.8e9, 15.6e12, "right", -7, 0],
    ];
    var RUNS = [["the 2017 Transformer (big)", 2.3e19], ["GPT-3", 3.14e23], ["DeepSeek-V3", 3.3e24], ["Llama 3.1 405B", 3.8e25]];
    QB.widget(el, {
      title: "From a shape to a bill: parameters, tokens and 6ND",
      sub: "A decoder with L layers of width d has about 12Ld² weights, plus its embeddings; reading D tokens costs about 6ND operations. The sliders start at GPT-3's shape: 96 layers, 12,288 wide, 300 billion tokens. Left: your model (gold) among published ones (blue), with lines of equal tokens per parameter; the green one, 20, is Chinchilla's optimum. Right: its training compute on the film's ladder. Halve the width and see what a square does; then move the gold dot to Chinchilla's line.",
      panels: 2, height: 300,
      controls: [
        { k: "L", label: "Layers L", min: 2, max: 128, step: 1, value: 96 },
        { k: "d", label: "Width d", min: 128, max: 16384, step: 128, value: 12288, fmt: commas },
        { k: "lD", label: "Training tokens D", min: -3.5, max: 2.5, step: 0.01, value: 0, fmt: function (x) { return human(3e11 * Math.pow(10, x)); } },
      ],
      draw: function (g, v, s) {
        var N = 12 * v.L * v.d * v.d + (VOCAB + CTX) * v.d, D = 3e11 * Math.pow(10, v.lD), Cc = 6 * N * D, i;
        s.out = [N, Cc, D / N, 12 * v.L * v.d * v.d / N];
        var a = g[0].axes({ x: [1e6, 1e13], y: [1e8, 1e14], logx: true, logy: true, title: "Size against data", xlabel: "parameters N",
          xticks: [1e6, 1e8, 1e10, 1e12], xfmt: human, yticks: [1e8, 1e10, 1e12, 1e14], yfmt: human });
        var rat = [[1, C.cash], [20, C.gain], [1000, C.cash]];
        for (i = 0; i < rat.length; i++) a.line([1e6, 1e13], [1e6 * rat[i][0], 1e13 * rat[i][0]], { color: rat[i][1], width: i === 1 ? 1.6 : 1, dash: i === 1 ? null : [4, 4] });
        a.text(3e6, 3e9, "1,000 per parameter", { color: C.muted, size: 11, bg: true, dx: 4 });
        a.text(3e7, 6e8, "20 per parameter", { color: C.gain, size: 11, bg: true, dx: 4 });
        a.text(3e10, 3e10, "1 per parameter", { color: C.muted, size: 11, bg: true, dx: 4 });
        for (i = 0; i < MODELS.length; i++) {
          a.dots([MODELS[i][1]], [MODELS[i][2]], { color: C.spot, r: 3.5 });
          a.text(MODELS[i][1], MODELS[i][2], MODELS[i][0], { align: MODELS[i][3], dx: MODELS[i][4], dy: MODELS[i][5], size: 11 });
        }
        a.dots([clamp(N, 1e6, 1e13)], [clamp(D, 1e8, 1e14)], { color: C.idea, r: 6 });
        var b = g[1].axes({ x: [1e17, 1e28], y: [0, 5.6], logx: true, noY: true, title: "Training compute, in operations", xlabel: "operations (each step right is ×100)",
          xticks: [1e18, 1e20, 1e22, 1e24, 1e26, 1e28], xfmt: function (x) { return "1e" + Math.round(Math.log(x) / Math.LN10); } });
        for (i = 0; i < RUNS.length; i++) {
          b.line([1e17, RUNS[i][1]], [4.8 - i, 4.8 - i], { color: C.spot, width: 5, alpha: 0.55 });
          b.dots([RUNS[i][1]], [4.8 - i], { color: C.spot, r: 4 });
          b.text(1e17, 4.8 - i, RUNS[i][0] + ": " + sci(RUNS[i][1]), { dx: 6, dy: -11, size: 11 });
        }
        var cc = clamp(Cc, 1e17, 1e28);
        b.line([1e17, cc], [0.8, 0.8], { color: C.idea, width: 5, alpha: 0.8 });
        b.dots([cc], [0.8], { color: C.idea, r: 5 });
        b.text(1e17, 0.8, "your model, 6ND: " + sci(Cc), { dx: 6, dy: -11, size: 11, color: C.idea });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["parameters N", human(o[0], 4)], ["share in the layers (12Ld²)", QB.pct(o[3])], ["tokens per parameter", o[2] >= 100 ? commas(o[2]) : fmt(o[2], 2)],
          ["training compute 6ND", sci(o[1])], ["in petaflop/s-days", o[1] / 8.64e19 >= 10 ? commas(o[1] / 8.64e19) : fmt(o[1] / 8.64e19, 2)]];
      },
      note: "N = 12Ld² + (V + n_ctx)d with GPT-3's vocabulary of 50,257 and 2,048 positions; norms and biases are left out, and a feed-forward width of 4d is assumed. Published sizes, token counts and compute are the ones the film cites; the Transformer's figure is its paper's own estimate (time × GPUs × 9.5 TFLOP/s), DeepSeek-V3's is 6ND, and Llama 3.1's is its makers' figure. One petaflop/s-day is 8.64 × 10^19 operations.",
    });
  };
  // ---- Part 15: one matrix as a memory, written three ways ---------------------------------------------------
  W.deltamemory = function (el) {
    var DV = 8, NMAX = 96, RULES = ["add", "decay", "delta"];
    QB.widget(el, {
      title: "A matrix that remembers, and how it forgets",
      sub: "N key-value pairs are written, one after another, into a single 8 × d matrix and then read back with their keys. Blue adds an outer product each time (linear attention); purple shrinks the memory by α before each write; gold is the delta rule, which writes only the difference from what the memory already answers. Raise N toward d and watch adding fill with crosstalk along the dashed line (N − 1)/d; then set β to 2, where the delta rule's correction becomes a reflection.",
      panels: 2, height: 300,
      controls: [
        { k: "d", label: "Numbers in a key, d", min: 8, max: 64, step: 4, value: 32 },
        { k: "n", label: "Pairs stored, N", min: 1, max: NMAX, step: 1, value: 24 },
        { k: "alpha", label: "Decay α (purple)", min: 0.5, max: 1, step: 0.01, value: 0.95, fmt: function (x) { return x.toFixed(2); } },
        { k: "beta", label: "Delta rule's rate β (gold)", min: 0, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New keys", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1500), d = v.d, N = v.n, K = [], V = [], i, j, a, t, m, vv = 0;
        for (i = 0; i < NMAX; i++) {
          var k = new Float64Array(d), val = new Float64Array(DV), nn = 0;
          for (j = 0; j < d; j++) { k[j] = r.normal(); nn += k[j] * k[j]; }
          nn = Math.sqrt(nn) || 1; for (j = 0; j < d; j++) k[j] /= nn;
          for (a = 0; a < DV; a++) { val[a] = r.normal(); vv += val[a] * val[a]; }
          K.push(k); V.push(val);
        }
        vv /= NMAX; // the mean squared size of a value
        var S = [new Float64Array(DV * d), new Float64Array(DV * d), new Float64Array(DV * d)], rd = new Float64Array(DV);
        var read = function (M, k) { for (var p = 0; p < DV; p++) { var acc = 0, o = p * d; for (var q = 0; q < d; q++) acc += M[o + q] * k[q]; rd[p] = acc; } };
        var errOf = function (M, i0) { read(M, K[i0]); var e = 0; for (var p = 0; p < DV; p++) e += (rd[p] - V[i0][p]) * (rd[p] - V[i0][p]); return Math.min(e / vv, 1e6); };
        var cx = [], curve = [[], [], []], per = [[], [], []], mean = [0, 0, 0];
        for (t = 0; t < NMAX; t++) { // write pair t under each rule
          for (m = 0; m < 3; m++) {
            var M = S[m], kt = K[t], vt = V[t], o, p, q, coef;
            if (m === 1) for (j = 0; j < DV * d; j++) M[j] *= v.alpha;
            if (m === 2) read(M, kt);
            for (p = 0; p < DV; p++) { coef = m === 2 ? v.beta * (vt[p] - rd[p]) : vt[p]; o = p * d; for (q = 0; q < d; q++) M[o + q] += coef * kt[q]; }
          }
          var cnt = t + 1;
          if (cnt === N) for (m = 0; m < 3; m++) { for (i = 0; i < N; i++) { var e1 = errOf(S[m], i); per[m].push(e1); mean[m] += e1 / N; } }
          if (cnt === 1 || cnt % 4 === 0) { cx.push(cnt); for (m = 0; m < 3; m++) { var tot = 0; for (i = 0; i < cnt; i++) tot += errOf(S[m], i); curve[m].push(tot / cnt); } }
        }
        s.out = [mean[0], (N - 1) / d, mean[1], mean[2], DV * d, N * (d + DV)];
        var cols = [C.spot, C.q, C.idea], idx = [], top = 1.2;
        for (i = 0; i < N; i++) idx.push(i + 1);
        for (m = 0; m < 3; m++) for (i = 0; i < N; i++) top = Math.max(top, Math.min(per[m][i], 4));
        var a0 = g[0].axes({ x: [0.5, Math.max(N, 2) + 0.5], y: [0, top * 1.25], title: "Each pair's read error, oldest to newest", xlabel: "order written (1 = oldest)", nx: 6 });
        for (m = 0; m < 3; m++) { a0.line(idx, per[m], { color: cols[m], width: 1.3, alpha: 0.8 }); a0.dots(idx, per[m], { color: cols[m], r: N > 48 ? 1.8 : 2.6 }); }
        a0.legend([["adding", C.spot], ["decaying", C.q], ["delta rule", C.idea]], { pos: "tl" });
        var b0 = g[1].axes({ x: [0, NMAX], y: [0, 2.4], title: "Mean read error as the memory fills", xlabel: "pairs stored", xticks: [0, 24, 48, 72, 96] });
        b0.line([1, NMAX], [0, (NMAX - 1) / d], { color: C.muted, width: 1.2, dash: [5, 4] });
        for (m = 0; m < 3; m++) b0.line(cx, curve[m], { color: cols[m], width: m === 0 ? 2 : 1.6 });
        b0.vline(N, { color: C.ink });
        b0.text(N, 0.14, "N", { color: C.ink, dx: 5, size: 11 });
        b0.vline(d, { color: C.loss, dash: [2, 3] });
        b0.text(d, 2.25, "N = d", { color: C.loss, dx: 5, size: 11 });
        b0.legend([["theory (N − 1)/d", C.muted]], { pos: "br" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["mean error: adding", fmt(o[0], 2)], ["theory (N − 1)/d", fmt(o[1], 2)], ["decaying", fmt(o[2], 2)], ["delta rule", fmt(o[3], 2)],
          ["memory holds", o[4] + " numbers"], ["a cache of these pairs", o[5] + " numbers"]];
      },
      note: "Simulated data: random unit keys and random values of 8 numbers; an error of 1 means the read is as wrong as the value is large. The rules are S + vkᵀ, αS + vkᵀ and S + β(v − Sk)kᵀ. The matrix stays the same size however many pairs are written, which is what the cache of softmax attention gives up to recall exactly.",
    });
  };
})();
