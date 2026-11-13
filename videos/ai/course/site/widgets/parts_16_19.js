// Interactives for Act III, the Transformer Era: sparsity, silicon, pretraining at scale, inference (Parts 16-19).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 16: a router that plays favourites, a balancing bias, and a capacity factor -------------------------
  W.expertload = function (el) {
    var E = 8, K = 2, N = 256, GAMMA = 0.02;
    var shares = function (S, b) { // each expert's share of the token slots when the top two of score + bias are chosen
      var f = new Array(E).fill(0), t, i, a, c, va, vc, x;
      for (t = 0; t < N; t++) {
        a = -1; c = -1; va = -1e9; vc = -1e9;
        for (i = 0; i < E; i++) {
          x = S[t * E + i] + b[i];
          if (x > va) { c = a; vc = va; a = i; va = x; } else if (x > vc) { c = i; vc = x; }
        }
        f[a] += 1 / (K * N); f[c] += 1 / (K * N);
      }
      return f;
    };
    var dropped = function (f, c) { var s = 0, i; for (i = 0; i < E; i++) s += Math.max(0, f[i] - c / E); return s; };
    QB.widget(el, {
      title: "Favourite experts, a balancing bias, and what a capacity factor drops",
      sub: "256 simulated tokens each choose 2 of 8 experts by router score. Raise the favouritism and a few experts take most of the work; whatever exceeds an expert's buffer (the gold line, c fair shares) is dropped, shown in red. Then run the loss-free bias: each step lowers a busy expert's bias and raises an idle one's, and the bars level out.",
      panels: 2, height: 300,
      controls: [
        { k: "fav", label: "How strongly the router plays favourites", min: 0, max: 2, step: 0.1, value: 1.2, fmt: function (x) { return x.toFixed(1); } },
        { k: "steps", label: "Steps of the loss-free bias", min: 0, max: 300, step: 5, value: 0 },
        { k: "c", label: "Capacity factor c", min: 0.5, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New tokens", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 160), S = new Array(N * E), b = new Array(E).fill(0), zero = new Array(E).fill(0), t, i, n, f;
        for (t = 0; t < N; t++) for (i = 0; i < E; i++) S[t * E + i] = v.fav * (1.2 - 2.4 * i / (E - 1)) + r.normal();
        var f0 = shares(S, zero);
        for (n = 0; n < v.steps; n++) { f = shares(S, b); for (i = 0; i < E; i++) b[i] -= GAMMA * (f[i] > 1 / E ? 1 : f[i] < 1 / E ? -1 : 0); }
        f = shares(S, b);
        var xs = [], load = [], kept = [], top = 0, sq = 0;
        for (i = 0; i < E; i++) { xs.push(i + 1); load.push(E * f[i]); kept.push(Math.min(E * f[i], v.c)); top = Math.max(top, E * f[i]); sq += f[i] * f[i]; }
        s.out = [top, top - 1, dropped(f, v.c), E * sq];
        var a = g[0].axes({ x: [0.4, 8.6], y: [0, 4.2], title: "Each expert's load, in fair shares", xlabel: "expert", xticks: xs });
        a.bars(xs, load, 0.7, { color: C.loss });
        a.bars(xs, kept, 0.7, { color: C.spot, alpha: 1 });
        a.hline(1, { color: C.muted });
        a.hline(v.c, { color: C.idea, dash: [], width: 1.6 });
        a.legend([["processed", C.spot], ["dropped", C.loss], ["buffer: c fair shares", C.idea]], { pos: "tr" });
        var cs = QB.linspace(0.5, 2, 31), d0 = cs.map(function (c) { return dropped(f0, c); }), d1 = cs.map(function (c) { return dropped(f, c); });
        var bx = g[1].axes({ x: [0.5, 2], y: [0, 0.6], title: "Token slots dropped against capacity", xlabel: "capacity factor c", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        bx.line(cs, d1, { color: C.gain, width: 3 }).line(cs, d0, { color: C.loss, width: 1.5, dash: [5, 4] });
        bx.vline(v.c, { color: C.idea });
        bx.legend([["no balancing", C.loss], ["with the bias, after " + v.steps + " steps", C.gain]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["busiest expert", fmt(s.out[0], 2) + " × fair"], ["MaxVio", fmt(s.out[1], 2)], ["slots dropped at c", QB.pct(s.out[2])], ["E Σ fᵢ² (Switch's penalty at P = f)", fmt(s.out[3], 3)]];
      },
      note: "Simulated data: scores are a fixed preference per expert plus unit normal noise, and the bias moves by 0.02 a step on the same 256 tokens. The dropped share is the sum over experts of max(0, fᵢ − c/E); the bias changes which experts are chosen, never the gates.",
    });
  };

  // ---- Part 17: the roofline, and where a matrix product sits on it ---------------------------------------------
  W.rooflineridge = function (el) {
    var BYTES = [4, 2, 1, 0.5], NAMES = ["FP32", "BF16", "FP8", "FP4"];
    var unit = function (x, what) { // 3.35e12 -> "3.35 T" + what
      var e = Math.max(0, Math.min(6, Math.floor(Math.log10(Math.max(x, 1)) / 3 + 1e-9))), m = x / Math.pow(1000, e);
      return (m >= 100 ? m.toFixed(0) : m >= 10 ? m.toFixed(1) : m.toFixed(2)) + " " + ["", "k", "M", "G", "T", "P", "E"][e] + what;
    };
    var decade = function (v) { var e = Math.round(Math.log10(v)); return ["1 G", "1 T", "1 P", "1 E"][(e - 9) / 3] || ""; };
    QB.widget(el, {
      title: "The roofline: bound by arithmetic, or by bytes?",
      sub: "A program that does I operations per byte it moves runs at most at min(P, β·I): the blue roofline. The gold dot is an n × n matrix product with each matrix moved once (I = 2n / 3s for s-byte numbers); the pink dot is a matrix times one vector (I = 2/s), which never leaves the slope. Grow n until the product reaches the roof, then raise the peak and watch the ridge move away.",
      panels: 2, height: 300,
      controls: [
        { k: "P", label: "Peak arithmetic P", min: 10, max: 17, step: 0.005, value: 14.995, fmt: function (x) { return unit(Math.pow(10, x), "FLOP/s"); } },
        { k: "B", label: "Memory bandwidth β", min: 10, max: 14, step: 0.005, value: 12.525, fmt: function (x) { return unit(Math.pow(10, x), "B/s"); } },
        { k: "n", label: "Matrix size n", min: 2, max: 14, step: 0.25, value: 8, fmt: function (x) { return String(Math.round(Math.pow(2, x))); } },
        { k: "s", label: "Number format", min: 0, max: 3, step: 1, value: 1, fmt: function (x) { return NAMES[x] + ", " + BYTES[x] + " bytes"; } },
      ],
      draw: function (g, v, s) {
        var P = Math.pow(10, v.P), B = Math.pow(10, v.B), by = BYTES[v.s], n = Math.round(Math.pow(2, v.n));
        var roof = function (I) { return Math.min(P, B * I); };
        var Imm = 2 * n / (3 * by), Imv = 2 / by, ridge = P / B;
        s.out = [ridge, Imm, roof(Imm), roof(Imv), roof(Imm) >= P, 1.5 * by * ridge];
        var Is = [], ys = [], i, lo = 0.1, hi = 1e5;
        for (i = 0; i <= 120; i++) { Is.push(lo * Math.pow(hi / lo, i / 120)); ys.push(roof(Is[i])); }
        var yt = [1e9, 1e12, 1e15, 1e18];
        var a = g[0].axes({ x: [lo, hi], y: [1e8, 1e18], logx: true, logy: true, title: "Speed bound (FLOP/s) against intensity", xlabel: "arithmetic intensity I (FLOP per byte)", yticks: yt, yfmt: decade, xticks: [0.1, 1, 10, 100, 1000, 1e4, 1e5], xfmt: function (x) { return x >= 1000 ? x / 1000 + "k" : String(x); } });
        a.line(Is, ys, { color: C.spot, width: 2.4 });
        if (ridge > lo && ridge < hi) a.vline(ridge, { color: C.muted });
        a.dots([Math.max(lo, Math.min(hi, Imv))], [roof(Imv)], { color: C.option, r: 5 });
        a.dots([Math.max(lo, Math.min(hi, Imm))], [roof(Imm)], { color: C.idea, r: 6 });
        a.legend([["roofline min(P, β·I)", C.spot], ["n × n product", C.idea], ["matrix × vector", C.option], ["ridge P/β", C.muted]], { pos: "br" });
        var ns = [], sp = [];
        for (i = 0; i <= 96; i++) { ns.push(Math.pow(2, 2 + 12 * i / 96)); sp.push(roof(2 * ns[i] / (3 * by))); }
        var b = g[1].axes({ x: [4, 16384], y: [1e8, 1e18], logx: true, logy: true, title: "The n × n product's bound against n", xlabel: "matrix size n", yticks: yt, yfmt: decade, xticks: [4, 16, 64, 256, 1024, 4096, 16384], xfmt: function (x) { return x >= 1024 ? x / 1024 + "k" : String(x); } });
        b.hline(roof(Imv), { color: C.option });
        b.line(ns, sp, { color: C.spot, width: 2.4 });
        b.vline(n, { color: C.idea });
        b.dots([n], [roof(Imm)], { color: C.idea, r: 6 });
        b.legend([["n × n product", C.spot], ["matrix × vector", C.option]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["ridge P/β", fmt(s.out[0], s.out[0] < 10 ? 2 : 0) + " FLOP/byte"], ["product's intensity", fmt(s.out[1], s.out[1] < 10 ? 2 : 0)],
          ["product's bound", unit(s.out[2], "FLOP/s") + (s.out[4] ? " (arithmetic-bound)" : " (memory-bound)")],
          ["matrix × vector", unit(s.out[3], "FLOP/s")], ["n to reach the roof", String(Math.ceil(s.out[5]))]];
      },
      note: "No simulation: the bound is min(P, β·I). The sliders start near an H100 in BF16 (989 TFLOP/s, 3.35 TB/s), where a square product needs n of about 886 to reach the roof. On real chips the peak P itself depends on the format; here P and the format move separately.",
    });
  };

  // ---- Part 18: a pipeline's schedule and its bubble --------------------------------------------------------------
  W.pipelinebubble = function (el) {
    var orders = function (p, m, oneF) { // each GPU's list of [kind, micro-batch]: kind 0 forward, 1 backward
      var out = [], s, i, w, ops;
      for (s = 0; s < p; s++) {
        ops = [];
        if (!oneF) { for (i = 0; i < m; i++) ops.push([0, i]); for (i = 0; i < m; i++) ops.push([1, i]); }
        else {
          w = Math.min(p - s - 1, m);
          for (i = 0; i < w; i++) ops.push([0, i]);
          for (i = 0; i < m - w; i++) { ops.push([0, w + i]); ops.push([1, i]); }
          for (i = m - w; i < m; i++) ops.push([1, i]);
        }
        out.push(ops);
      }
      return out;
    };
    var simulate = function (ord, p, m, tb) { // an operation starts when its GPU is free and its input has arrived
      var end = [[], []], cells = [], free = [], idx = [], s, done = 0, total = 2 * p * m, moved = true, op, dep, t, d;
      for (s = 0; s < p; s++) { end[0].push(new Array(m)); end[1].push(new Array(m)); free.push(0); idx.push(0); }
      while (done < total && moved) {
        moved = false;
        for (s = 0; s < p; s++) {
          if (idx[s] >= ord[s].length) continue;
          op = ord[s][idx[s]];
          dep = op[0] === 0 ? (s > 0 ? end[0][s - 1][op[1]] : 0) : (s < p - 1 ? end[1][s + 1][op[1]] : end[0][s][op[1]]);
          if (dep === undefined) continue;
          t = Math.max(free[s], dep); d = op[0] === 0 ? 1 : tb;
          end[op[0]][s][op[1]] = t + d; free[s] = t + d; idx[s]++; done++; moved = true;
          cells.push([s, op[0], op[1], t, t + d]);
        }
      }
      var T = 0, busy = 0, ev = [], cur = 0, peak = 0, i;
      for (i = 0; i < cells.length; i++) {
        T = Math.max(T, cells[i][4]); busy += cells[i][4] - cells[i][3];
        if (cells[i][0] === 0) ev.push(cells[i][1] === 0 ? [cells[i][3], 1] : [cells[i][4], -1]);
      }
      ev.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      for (i = 0; i < ev.length; i++) { cur += ev[i][1]; peak = Math.max(peak, cur); }
      return { cells: cells, T: T, bubble: T > 0 ? 1 - busy / (p * T) : 0, peak: peak };
    };
    QB.widget(el, {
      title: "The pipeline bubble: GPUs waiting for each other",
      sub: "A model is cut into p stages, one per GPU, and a batch into m micro-batches. Blue cells are forward passes, gold cells backward passes, grey is a GPU waiting. Add micro-batches and the grey corners shrink to (p − 1)/(m + p − 1) of the time; switch to 1F1B and the bubble stays the same while the first GPU holds far fewer micro-batches at once.",
      panels: 2, weights: [1.45, 1], height: 310,
      controls: [
        { k: "p", label: "Stages p (GPUs)", min: 2, max: 8, step: 1, value: 4 },
        { k: "m", label: "Micro-batches m", min: 1, max: 24, step: 1, value: 8 },
        { k: "sch", label: "Schedule", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "1F1B" : "GPipe"; } },
        { k: "tb", label: "Backward time, in forward passes", min: 1, max: 3, step: 0.5, value: 2, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var r = simulate(orders(v.p, v.m, v.sch === 1), v.p, v.m, v.tb), c = g.ctx, bx = g[0].box, i, cell;
        s.out = [r.bubble, (v.p - 1) / (v.m + v.p - 1), r.T, r.peak];
        var x0 = bx.x + 50, y0 = bx.y + 30, w = bx.w - 62, h = bx.h - 30 - 34, rh = h / v.p;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Each GPU's time", x0, bx.y + 8);
        c.font = "11px system-ui, sans-serif"; c.textBaseline = "middle";
        var lx = x0 + w, items = [["waiting", "#3a475c"], ["backward", C.idea], ["forward", C.spot]];
        for (i = 0; i < items.length; i++) { // a legend on the title line, right to left
          c.textAlign = "right"; c.fillStyle = C.muted; c.fillText(items[i][0], lx, bx.y + 15); lx -= c.measureText(items[i][0]).width + 5;
          c.fillStyle = items[i][1]; c.fillRect(lx - 10, bx.y + 10, 10, 10); lx -= 20;
        }
        for (i = 0; i < v.p; i++) {
          c.fillStyle = "#3a475c"; c.fillRect(x0, y0 + i * rh + 1, w, rh - 2);
          c.fillStyle = C.muted; c.textAlign = "right"; c.fillText("GPU " + (i + 1), x0 - 6, y0 + (i + 0.5) * rh);
        }
        var sx = w / r.T, wide = sx >= 15 && rh >= 14;
        for (i = 0; i < r.cells.length; i++) {
          cell = r.cells[i];
          c.fillStyle = cell[1] === 0 ? C.spot : C.idea;
          c.fillRect(x0 + cell[3] * sx, y0 + cell[0] * rh + 1, Math.max(1, (cell[4] - cell[3]) * sx - (sx > 4 ? 1 : 0)), rh - 2);
          if (wide) { c.fillStyle = C.bg; c.textAlign = "center"; c.fillText(String(cell[2] + 1), x0 + (cell[3] + cell[4]) / 2 * sx, y0 + (cell[0] + 0.5) * rh); }
        }
        c.fillStyle = C.muted; c.textAlign = "left"; c.textBaseline = "top"; c.fillText("0", x0, y0 + h + 5);
        c.textAlign = "right"; c.fillText(fmt(r.T, r.T % 1 ? 1 : 0), x0 + w, y0 + h + 5);
        c.textAlign = "center"; c.fillText("time, in forward passes", x0 + w / 2, y0 + h + 17);
        c.restore();
        var ms = [], bs = [], k;
        for (k = 1; k <= 24; k++) { ms.push(k); bs.push((v.p - 1) / (k + v.p - 1)); }
        var a = g[1].axes({ x: [1, 24], y: [0, 1], title: "Idle share of the GPUs' time", xlabel: "micro-batches m", xticks: [1, 4, 8, 12, 16, 20, 24], yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.line(ms, bs, { color: C.spot });
        a.vline(v.m, { color: C.muted });
        a.dots([v.m], [r.bubble], { color: C.loss, r: 5.5 });
        a.legend([["(p − 1)/(m + p − 1)", C.spot], ["this schedule, simulated", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["bubble, simulated", QB.pct(s.out[0])], ["(p − 1)/(m + p − 1)", QB.pct(s.out[1])], ["total time", fmt(s.out[2], 1) + " forward passes"], ["micro-batches held on GPU 1", String(s.out[3])]];
      },
      note: "An exact simulation with fixed durations: an operation starts when its GPU is free and its input has arrived. Numbers in the cells are micro-batches (shown when they fit). A micro-batch is held from its forward pass until its backward pass ends; communication is free here.",
    });
  };

  // ---- Part 19: rounding error, the step an outlier sets, and scales per block ------------------------------------
  W.roundingstep = function (el) {
    var N = 2048, GROUPS = [N, 256, 32], GNAMES = ["whole tensor", "256 weights", "32 weights"];
    var round = function (w, bits, grp) { // symmetric rounding with one scale per group: [mean squared error, predicted]
      var q = Math.pow(2, bits - 1) - 1, se = 0, pred = 0, i, j, A, d, e;
      for (i = 0; i < N; i += grp) {
        A = 1e-9; for (j = i; j < i + grp; j++) A = Math.max(A, Math.abs(w[j]));
        d = A / q; pred += grp * d * d / 12;
        for (j = i; j < i + grp; j++) { e = w[j] - d * Math.max(-q, Math.min(q, Math.round(w[j] / d))); se += e * e; }
      }
      return [se / N, pred / N];
    };
    QB.widget(el, {
      title: "Rounding error: Δ²/12, until one large weight sets the step",
      sub: "2,048 simulated weights (unit normal) are rounded to b bits with a step Δ = max|w| / (2^(b−1) − 1). With smooth weights and many levels the error is Δ²/12. Now make eight of the weights large: one scale for the whole tensor stretches the step and the bulk falls onto a few levels, while a scale per block keeps the levels where the weights are.",
      panels: 2, height: 300,
      controls: [
        { k: "bits", label: "Bits per weight b", min: 2, max: 8, step: 1, value: 4 },
        { k: "out", label: "Size of the 8 outliers (in standard deviations)", min: 1, max: 30, step: 1, value: 12 },
        { k: "grp", label: "One scale per", min: 0, max: 2, step: 1, value: 2, fmt: function (x) { return GNAMES[x]; } },
      ],
      buttons: [{ label: "New weights", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 190), w = new Array(N), i, b;
        for (i = 0; i < N; i++) w[i] = r.normal();
        for (i = 0; i < 8; i++) w[i * 256 + 17] = (i % 2 ? -1 : 1) * Math.max(v.out, Math.abs(w[i * 256 + 17]));
        var grp = GROUPS[v.grp], bs = [], mT = [], pT = [], mG = [], pG = [], t, u;
        for (b = 2; b <= 8; b++) { t = round(w, b, N); u = round(w, b, grp); bs.push(b); mT.push(Math.sqrt(t[0])); pT.push(Math.sqrt(t[1])); mG.push(Math.sqrt(u[0])); pG.push(Math.sqrt(u[1])); }
        var k = v.bits - 2, A = 0; for (i = 0; i < N; i++) A = Math.max(A, Math.abs(w[i]));
        var step = A / (Math.pow(2, v.bits - 1) - 1), inview = 0, lv;
        s.out = [step, mT[k], pT[k], mG[k], pG[k]];
        var h = QB.hist(w, -4, 4, 40), xs = [], hs = [];
        for (i = 0; i < 40; i++) { xs.push(-3.9 + 0.2 * i); hs.push(h[i] / (N * 0.2)); }
        var a = g[0].axes({ x: [-4, 4], y: [0, 0.5], title: "The bulk of the weights, and the tensor's levels", xlabel: "weight (standard deviations)" });
        a.bars(xs, hs, 0.2, { color: C.spot, alpha: 0.7 });
        for (lv = -Math.floor(4 / step); lv <= Math.floor(4 / step); lv++) inview++;
        if (inview <= 80) for (lv = -Math.floor(4 / step); lv <= Math.floor(4 / step); lv++) a.vline(lv * step, { color: C.idea, dash: [], width: inview > 30 ? 0.6 : 1.2 });
        a.text(-3.8, 0.47, inview + (inview === 1 ? " level" : " levels") + " between −4 and 4", { color: C.idea, bg: true });
        var e = g[1].axes({ x: [2, 8], y: [0.001, 20], logy: true, title: "Rounding error (rms) against bits", xlabel: "bits per weight b", xticks: bs });
        e.line(bs, pT, { color: C.loss, dash: [5, 4], width: 1.3 }).line(bs, mT, { color: C.loss, width: 2.2 });
        e.line(bs, pG, { color: C.gain, dash: [5, 4], width: 1.3 }).line(bs, mG, { color: C.gain, width: 2.2 });
        e.vline(v.bits, { color: C.muted });
        e.dots([v.bits, v.bits], [mT[k], mG[k]], { color: function (j) { return j ? C.gain : C.loss; }, r: 4.5 });
        e.legend([["one scale for the tensor", C.loss], ["one scale per " + GNAMES[v.grp], C.gain], ["dashed: Δ/√12 predicted", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["tensor's step Δ", fmt(s.out[0], 3)], ["tensor scale: rms error", fmt(s.out[1], 3) + " (Δ/√12 = " + fmt(s.out[2], 3) + ")"],
          ["chosen scale: rms error", fmt(s.out[3], 3) + " (predicted " + fmt(s.out[4], 3) + ")"]];
      },
      note: "Simulated data. Gold lines on the left are the levels of the single tensor-wide scale. The prediction Δ²/12 assumes the error is spread evenly inside a step: it fails when the step is wider than the bulk of the weights (few bits, large outliers), where the error is capped by the size of the weights themselves. Extra scales cost storage, which is not counted here.",
    });
  };
})();
