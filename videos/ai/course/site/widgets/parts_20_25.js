// Interactives for Act IV, Generation and Perception (Parts 20-25).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 20: two players on V = xy - (gamma/2) y^2 --------------------------------------------------------
  W.ganspiral = function (el) {
    var names = ["simultaneous", "alternating", "extragradient", "optimistic"];
    var run = function (kind, eta, gam, T) { // x descends V, y ascends it
      var x = 1, y = 0, px = [x], py = [y], r = [1], t, gx, gy, ogx = 0, ogy = 1, hx, hy;
      for (t = 0; t < T; t++) {
        gx = y; gy = x - gam * y;
        if (kind === 0) { x -= eta * gx; y += eta * gy; }
        else if (kind === 1) { x -= eta * gx; y += eta * (x - gam * y); }
        else if (kind === 2) { hx = x - eta * gx; hy = y + eta * gy; x -= eta * hy; y += eta * (hx - gam * hy); }
        else { if (t === 0) { ogx = gx; ogy = gy; } x -= eta * (2 * gx - ogx); y += eta * (2 * gy - ogy); ogx = gx; ogy = gy; }
        px.push(x); py.push(y); r.push(Math.min(1e6, Math.max(1e-6, Math.sqrt(x * x + y * y))));
      }
      return { x: px, y: py, r: r };
    };
    QB.widget(el, {
      title: "Why GANs spiral: two players following their gradients",
      sub: "One player moves x to lower V = xy, the other moves y to raise it; the equilibrium is the gold dot. Choose how they step. Simultaneous steps spiral out, taking turns orbits, extragradient and optimistic steps spiral in. Then add the penalty on the y player and watch even simultaneous steps converge, until the step is too large.",
      panels: 2, height: 310,
      controls: [
        { k: "kind", label: "How the players step", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return names[x]; } },
        { k: "eta", label: "Step size η", min: 0.02, max: 0.6, step: 0.02, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "gam", label: "Penalty γ on the y player", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "T", label: "Steps", min: 10, max: 200, step: 10, value: 60 },
      ],
      draw: function (g, v, s) {
        var p = run(v.kind, v.eta, v.gam, v.T), i, m = 1.2, ts = [], all = [], cols = [C.loss, C.spot, C.gain, C.q];
        for (i = 0; i <= v.T; i++) { ts.push(i); m = Math.max(m, Math.abs(p.x[i]), Math.abs(p.y[i])); }
        m = Math.min(m * 1.08, 40);
        s.out = [p.r[v.T], Math.pow(p.r[v.T], 1 / v.T), Math.sqrt(1 + v.eta * v.eta)];
        var a = g[0].axes({ x: [-m, m], y: [-m, m], title: "The path of (x, y): " + names[v.kind], xlabel: "x (lowers V)", nx: 4, ny: 4 });
        a.hline(0).vline(0);
        a.line(p.x, p.y, { color: cols[v.kind], width: 1.5 });
        a.dots([1], [0], { color: C.ink, r: 3.5 }).dots([0], [0], { color: C.idea, r: 5 });
        a.dots([p.x[v.T]], [p.y[v.T]], { color: cols[v.kind], r: 4 });
        a.text(1, 0, "start", { dx: 6, dy: -9, color: C.muted });
        for (i = 0; i < 4; i++) all.push(run(i, v.eta, v.gam, v.T).r);
        var b = g[1].axes({ x: [0, v.T], y: [1e-3, 1e3], logy: true, title: "Distance from the equilibrium", xlabel: "step", nx: 4,
          yticks: [1e-3, 1e-2, 0.1, 1, 10, 100, 1000] });
        b.hline(1);
        for (i = 0; i < 4; i++) b.line(ts, all[i], { color: cols[i], width: i === v.kind ? 2.6 : 1.1, alpha: i === v.kind ? 1 : 0.55 });
        b.legend([["simultaneous", cols[0]], ["alternating", cols[1]], ["extragradient", cols[2]], ["optimistic", cols[3]]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["distance after " + v.T + " steps", s.out[0] >= 1e6 ? "over 1,000,000" : s.out[0] <= 1e-6 ? "under 0.000001" : fmt(s.out[0], s.out[0] < 0.1 ? 5 : 2)],
          ["mean factor per step", fmt(s.out[1], 4)], ["√(1 + η²)", fmt(s.out[2], 4)]];
      },
      note: "Exact iterations of the four update rules from (1, 0); nothing is simulated. With γ = 0 the simultaneous factor is exactly √(1 + η²). The penalty −(γ/2)y² plays the part of the R1 gradient penalty in the Dirac-GAN of chapter 6.",
    });
  };

  // ---- Part 21: sampling a two-bump mixture with the exact denoiser, in N steps --------------------------------
  W.ddimsteps = function (el) {
    var M = 1.2, SD = 0.25, NP = 500;
    var sched = function (t) { return [Math.cos(Math.PI * t / 2), Math.sin(Math.PI * t / 2)]; }; // alpha, sigma
    var xhat = function (x, a, b, w) { // the best guess of the clean point: E[x0 | x], exact for the mixture
      var v = a * a * SD * SD + b * b, l1 = -0.5 * (x + a * M) * (x + a * M) / v, l2 = -0.5 * (x - a * M) * (x - a * M) / v;
      var mx = Math.max(l1, l2), r1 = w * Math.exp(l1 - mx), r2 = (1 - w) * Math.exp(l2 - mx), k = a * SD * SD / v;
      return (r1 * (-M + k * (x + a * M)) + r2 * (M + k * (x - a * M))) / (r1 + r2);
    };
    var dens = function (x, w) { return (w * QB.pdf((x + M) / SD) + (1 - w) * QB.pdf((x - M) / SD)) / SD; };
    QB.widget(el, {
      title: "From noise to data in N steps, with the exact denoiser",
      sub: "The data are two bumps (gold). Each of 500 points starts as pure noise at the left and steps towards the denoiser's guess of its clean point. One step sends every point to the data's mean; a handful of deterministic (DDIM) steps already land on the bumps; with full noise (DDPM) the same few steps are not enough.",
      panels: 2, height: 310, weights: [1.25, 1],
      controls: [
        { k: "N", label: "Steps N", min: 1, max: 50, step: 1, value: 5 },
        { k: "eta", label: "Noise added back, η (0 DDIM, 1 DDPM)", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "w", label: "Weight of the left bump", min: 0.1, max: 0.9, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New noise", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 210), N = v.N, i, j, x = [], paths = [], ts = [];
        for (j = 0; j <= N; j++) ts.push(j / N);
        for (i = 0; i < NP; i++) { x.push(r.normal()); if (i < 40) paths.push([x[i]]); }
        for (j = 0; j < N; j++) {
          var A = sched(1 - j / N), B = sched(1 - (j + 1) / N), at = A[0], bt = Math.max(A[1], 1e-9), as = Math.max(B[0], 1e-9), bs = j === N - 1 ? 0 : B[1];
          var sg = v.eta * (bs / bt) * Math.sqrt(Math.max(0, 1 - at * at / (as * as))), keep = Math.sqrt(Math.max(0, bs * bs - sg * sg));
          for (i = 0; i < NP; i++) {
            var x0 = xhat(x[i], at, bt, v.w), e = (x[i] - at * x0) / bt;
            x[i] = as * x0 + keep * e + sg * r.normal();
            if (i < 40) paths[i].push(x[i]);
          }
        }
        var left = 0, near = 0;
        for (i = 0; i < NP; i++) { if (x[i] < 0) left++; if (Math.abs(Math.abs(x[i]) - M) < 2.5 * SD) near++; }
        s.out = [left / NP, near / NP];
        var a = g[0].axes({ x: [0, 1], y: [-3, 3], title: "40 of the paths: noise (left) to samples (right)", xlabel: "fraction of the way from noise to data", ny: 6 });
        for (i = 0; i < 40; i++) a.line(ts, paths[i], { color: paths[i][N] < 0 ? C.spot : C.q, width: 1, alpha: 0.55 });
        a.dots([1, 1], [-M, M], { color: C.idea, r: 5 });
        var lo = -2.5, hi = 2.5, nb = 50, h = QB.hist(x, lo, hi, nb), bw = (hi - lo) / nb, cx = [], hh = [], gx = QB.linspace(lo, hi, 201), gd = [];
        for (i = 0; i < nb; i++) { cx.push(lo + (i + 0.5) * bw); hh.push(Math.min(3.4, h[i] / (NP * bw))); }
        for (i = 0; i < gx.length; i++) gd.push(dens(gx[i], v.w));
        var b = g[1].axes({ x: [lo, hi], y: [0, 3.5], title: "Where the 500 samples land", xlabel: "x", ny: 4 });
        b.bars(cx, hh, bw, { color: C.spot, alpha: 0.7 });
        b.line(gx, gd, { color: C.idea, width: 2 });
        b.legend([["samples", C.spot], ["the data's density", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["samples in the left bump", QB.pct(s.out[0], 0)], ["should be", QB.pct(v.w, 0)], ["samples within 2.5 widths of a bump", QB.pct(s.out[1], 0)], ["denoiser evaluations", String(v.N)]];
      },
      note: "The denoiser is the exact posterior mean for this mixture, so every error is the sampler's. Noise schedule: α = cos(πt/2), σ = sin(πt/2), steps evenly spaced in t. Histogram bars are clipped at the top of the panel. Simulated noise.",
    });
  };

  // ---- Part 22: the same noise level at three resolutions, and SD3's shift ------------------------------------
  W.noiseshift = function (el) {
    var RES = [20, 40, 80];
    var ink = function (u, v) { // a capital A on the unit square: +1 on the strokes, -1 elsewhere
      var y = 1 - v, half = 0.34 * (1 - (y - 0.12) / 0.76), d = Math.abs(u - 0.5);
      if (y < 0.12 || y > 0.88) return -1;
      if (Math.abs(d - half) < 0.07) return 1;
      if (Math.abs(y - 0.4) < 0.055 && d < half) return 1;
      return -1;
    };
    var shift = function (sig, a) { return a * sig / (1 + (a - 1) * sig); };
    QB.widget(el, {
      title: "Bigger pictures need more noise",
      sub: "One letter at 20, 40 and 80 pixels a side, each pixel mixed with noise as z = (1 − σ)x + σε. At the same σ the large picture stays readable, because neighbouring pixels repeat each other and the noise averages out. Turn the shift on: each picture now gets the σ that leaves the same uncertainty about a flat patch, and the three are equally destroyed.",
      panels: 2, height: 300, weights: [1.6, 1],
      controls: [
        { k: "sig", label: "Noise level σ at 20 pixels", min: 0.05, max: 0.95, step: 0.01, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "on", label: "Resolution shift", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "on" : "off"; } },
      ],
      buttons: [{ label: "New noise", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var c = g.ctx, box = g[0].box, k, i, j, r = QB.rng(s.seed + 220), sg = [], sdv = [];
        var gap = 10, side = Math.max(40, Math.min((box.w - 4 * gap) / 3, box.h - 62)), top = box.y + 30 + Math.max(0, (box.h - 62 - side) / 2);
        c.save(); c.textBaseline = "top"; c.textAlign = "left"; c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif";
        c.fillText("The same letter, noised", box.x + gap, box.y + 6);
        for (k = 0; k < 3; k++) {
          var n = RES[k], a = n / RES[0], sig = v.on ? shift(v.sig, a) : v.sig, cell = side / n, x0 = box.x + gap + k * (side + gap);
          sg.push(sig); sdv.push(sig / ((1 - sig) * n));
          for (i = 0; i < n; i++) for (j = 0; j < n; j++) {
            var z = (1 - sig) * ink((j + 0.5) / n, (i + 0.5) / n) + sig * r.normal(), lum = Math.round(255 * Math.max(0, Math.min(1, (z + 1.6) / 3.2)));
            c.fillStyle = "rgb(" + lum + "," + lum + "," + lum + ")";
            c.fillRect(x0 + j * cell, top + i * cell, cell + 0.6, cell + 0.6);
          }
          c.fillStyle = C.muted; c.font = "11.5px system-ui, sans-serif"; c.textAlign = "center";
          c.fillText(n + " px, σ = " + sig.toFixed(2), x0 + side / 2, top + side + 7);
          c.textAlign = "left";
        }
        c.restore();
        s.out = [sg, sdv];
        var xs = QB.linspace(0, 1, 101), cols = [C.spot, C.gain, C.idea];
        var b = g[1].axes({ x: [0, 1], y: [0, 1], title: "The shifted noise level", xlabel: "σ at 20 pixels", nx: 4, ny: 4 });
        for (k = 0; k < 3; k++) b.line(xs, xs.map(function (x) { return shift(x, RES[k] / RES[0]); }), { color: cols[k], width: k ? 1.8 : 1.2 });
        b.vline(v.sig);
        for (k = 0; k < 3; k++) b.dots([v.sig], [shift(v.sig, RES[k] / RES[0])], { color: cols[k], r: v.on ? 4.5 : 2.5 });
        b.legend([["80 px (α = 4)", cols[2]], ["40 px (α = 2)", cols[1]], ["20 px", cols[0]]], { pos: "br" });
      },
      readout: function (v, s) {
        var o = s.out, f = function (x) { return x >= 100 ? "over 100" : fmt(x, 3); };
        return [["σ used at 20, 40, 80 px", o[0].map(function (x) { return x.toFixed(2); }).join(", ")],
          ["sd of a flat picture's colour estimate", o[1].map(f).join(", ")]];
      },
      note: "Simulated noise. The colour estimate of a flat picture with n pixels has standard deviation σ / ((1 − σ)√n); the shift σ′ = ασ / (1 + (α − 1)σ), α = √(m/n), makes it equal at every resolution and lowers the log signal-to-noise ratio by 2 log α.",
    });
  };

  // ---- Part 23: a tone, its samples, and the tone the samples describe --------------------------------------
  W.aliasfold = function (el) {
    var alias = function (f, fs) { return Math.abs(f - fs * Math.round(f / fs)); };
    QB.widget(el, {
      title: "Sampling folds what is too fast",
      sub: "The blue wave is the tone; the dots are its samples; the gold wave is the lowest tone that passes through the same dots, which is what a listener of the samples hears. Raise the tone past half the sampling rate and the gold wave parts from the blue: the tone folds back down. Raise the sampling rate to catch it again.",
      panels: 2, height: 300, weights: [1.4, 1],
      controls: [
        { k: "f", label: "Tone", min: 100, max: 12000, step: 50, value: 3000, fmt: function (x) { return (x / 1000).toFixed(2) + " kHz"; } },
        { k: "fs", label: "Sampling rate", min: 4000, max: 16000, step: 500, value: 8000, fmt: function (x) { return (x / 1000).toFixed(1) + " kHz"; } },
        { k: "ph", label: "Phase of the tone", min: 0, max: 350, step: 10, value: 0, fmt: function (x) { return x + "°"; } },
      ],
      draw: function (g, v, s) {
        var fa = alias(v.f, v.fs), ph = v.ph * Math.PI / 180, win = 2, i; // a window of 2 ms
        var k = Math.round(v.f / v.fs), sign = v.f - k * v.fs >= 0 ? 1 : -1; // cos(2 pi f n/fs + ph) = cos(2 pi fa n/fs + sign ph)
        var ts = QB.linspace(0, win, 600), tone = [], heard = [], nt = [], ns = [];
        for (i = 0; i < ts.length; i++) {
          tone.push(Math.cos(2 * Math.PI * v.f * ts[i] / 1000 + ph));
          heard.push(Math.cos(2 * Math.PI * fa * ts[i] / 1000 + sign * ph));
        }
        for (i = 0; i <= Math.floor(win * v.fs / 1000 + 1e-9); i++) { nt.push(i * 1000 / v.fs); ns.push(Math.cos(2 * Math.PI * v.f * i / v.fs + ph)); }
        s.out = [fa, v.fs / 2, v.fs / v.f];
        var folded = v.f > v.fs / 2 + 1e-9;
        var a = g[0].axes({ x: [0, win], y: [-1.45, 1.45], title: "Two milliseconds of the tone", xlabel: "time (ms)", ny: 4 });
        a.line(ts, tone, { color: C.spot, width: 1.3, alpha: folded ? 0.6 : 1 });
        a.line(ts, heard, { color: C.idea, width: 2, dash: folded ? null : [5, 4] });
        a.dots(nt, ns, { color: C.ink, r: 3.2 });
        a.legend([["the tone", C.spot], ["what the samples describe", C.idea]], { pos: "tl" });
        var fx = QB.linspace(0, 12, 241), fy = fx.map(function (x) { return alias(1000 * x, v.fs) / 1000; });
        var b = g[1].axes({ x: [0, 12], y: [0, 8.5], title: "The folding curve", xlabel: "tone (kHz)", nx: 6, ny: 4 });
        b.line([0, 8.5], [0, 8.5], { color: C.muted, width: 1, dash: [4, 4] });
        b.hline(v.fs / 2000, { color: C.loss });
        b.line(fx, fy, { color: C.idea, width: 2 });
        b.dots([v.f / 1000], [fa / 1000], { color: folded ? C.loss : C.gain, r: 5 });
        b.text(11.8, v.fs / 2000, "half the rate", { color: C.loss, align: "right", dy: -9 });
        b.text(0.3, 8, "heard (kHz)", { color: C.muted });
      },
      readout: function (v, s) {
        return [["heard as", (s.out[0] / 1000).toFixed(2) + " kHz"], ["Nyquist frequency", (s.out[1] / 1000).toFixed(2) + " kHz"],
          ["samples per period", fmt(s.out[2], 2)], ["verdict", v.f > v.fs / 2 + 1e-9 ? "aliased" : "faithful"]];
      },
      note: "Exact: cos(2π(f + k·fs)n/fs) = cos(2πfn/fs) for every whole k, and cosine is even, so a tone at f and a tone at fs − f give the same samples. A real converter filters out everything above half the rate before sampling.",
    });
  };

  // ---- Part 24: where the contrastive loss pushes, by temperature ---------------------------------------------
  W.temperaturepush = function (el) {
    QB.widget(el, {
      title: "Temperature decides which negatives get pushed",
      sub: "An anchor (gold) on the circle, its partner view (green) and the other points of the batch (red). The loss pulls the partner in and pushes each negative away with a force equal to its share of the softmax, shown by the size of each red dot. Lower the temperature and the push concentrates on the nearest few; raise it and every negative is pushed alike.",
      panels: 2, height: 310,
      controls: [
        { k: "tau", label: "Temperature τ", min: 0.05, max: 1, step: 0.01, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "M", label: "Negatives in the batch", min: 8, max: 256, step: 8, value: 64 },
        { k: "ang", label: "Angle between the two views", min: 0, max: 90, step: 1, value: 20, fmt: function (x) { return x + "°"; } },
      ],
      buttons: [{ label: "New batch", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 240), M = v.M, i, th = [], sim = [], w = [], sp = Math.cos(v.ang * Math.PI / 180), mx = sp / v.tau, tot = 0;
        for (i = 0; i < M; i++) { th.push(2 * Math.PI * r()); sim.push(Math.cos(th[i])); mx = Math.max(mx, sim[i] / v.tau); }
        for (i = 0; i < M; i++) { w.push(Math.exp(sim[i] / v.tau - mx)); tot += w[i]; }
        var wp = Math.exp(sp / v.tau - mx), pPartner = wp / (wp + tot), loss = -Math.log(Math.max(pPartner, 1e-300));
        var ord = [], top = 0, ess = 0, wmax = 0;
        for (i = 0; i < M; i++) { w[i] /= tot; ord.push(i); ess += w[i] * w[i]; wmax = Math.max(wmax, w[i]); }
        ord.sort(function (a, b) { return sim[b] - sim[a]; });
        for (i = 0; i < Math.max(1, Math.round(M / 10)); i++) top += w[ord[i]];
        s.out = [loss, Math.log(M + 1), top, 1 / ess, pPartner];
        var c = g.ctx, box = g[0].box, cx = box.x + box.w / 2, cy = box.y + box.h / 2 + 8, R = Math.max(30, Math.min(box.w, box.h - 40) / 2 - 22);
        c.save(); c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textBaseline = "top"; c.textAlign = "left";
        c.fillText("The batch on the circle", box.x + 12, box.y + 6);
        c.strokeStyle = C.line; c.lineWidth = 1.5; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        for (i = 0; i < M; i++) {
          c.globalAlpha = 0.75; c.fillStyle = C.loss; c.beginPath();
          c.arc(cx + R * Math.cos(th[i]), cy - R * Math.sin(th[i]), 1.5 + 13 * Math.sqrt(w[i] / wmax) * Math.sqrt(Math.min(1, wmax * 4)), 0, 6.2832); c.fill();
        }
        c.globalAlpha = 1;
        var pa = v.ang * Math.PI / 180;
        c.strokeStyle = C.gain; c.lineWidth = 2; c.beginPath(); c.arc(cx, cy, R, -pa, 0); c.stroke();
        c.fillStyle = C.gain; c.beginPath(); c.arc(cx + R * Math.cos(pa), cy - R * Math.sin(pa), 5.5, 0, 6.2832); c.fill();
        c.fillStyle = C.idea; c.beginPath(); c.arc(cx + R, cy, 6.5, 0, 6.2832); c.fill();
        c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "middle"; c.fillStyle = C.idea; c.textAlign = "right"; c.fillText("anchor", cx + R - 11, cy + 1);
        c.restore();
        var xs = [], ys = [], ymax = Math.max(0.05, Math.min(1, 1.25 * wmax));
        for (i = 0; i < M; i++) { xs.push(sim[ord[i]]); ys.push(w[ord[i]]); }
        var b = g[1].axes({ x: [-1, 1], y: [0, ymax], title: "Each negative's share of the push", xlabel: "cosine similarity to the anchor", nx: 4, ny: 4, yfmt: function (y) { return (100 * y).toFixed(ymax < 0.2 ? 1 : 0) + "%"; } });
        b.hline(1 / M, { color: C.muted });
        b.line(xs, ys, { color: C.loss, width: 1, alpha: 0.5 }).dots(xs, ys, { color: C.loss, r: 3 });
        b.vline(sp, { color: C.gain, dash: null, width: 1.5 });
        b.text(-0.95, 1 / M, "an equal share, 1/" + M, { color: C.muted, dy: -9 });
        b.legend([["negatives", C.loss], ["the partner's similarity", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["loss", fmt(o[0], 2)], ["at collapse, log(M + 1)", fmt(o[1], 2)], ["push on the nearest tenth", QB.pct(o[2], 0)],
          ["effective negatives", fmt(o[3], 1) + " of " + v.M], ["probability given to the partner", QB.pct(o[4], 1)]];
      },
      note: "Simulated batch: negatives uniform on the circle. The loss is −log of the partner's softmax share among the partner and the M negatives; its gradient on a negative's similarity is that negative's share divided by τ. Effective negatives is 1 / Σ share².",
    });
  };

  // ---- Part 25: repeated averaging on a graph of three communities -------------------------------------------
  W.oversmooth = function (el) {
    var K = 3, PER = 12, N = K * PER, KMAX = 64;
    var mix = function (t) { // feature -1 .. 1 as blue .. grey .. gold
      t = Math.max(-1, Math.min(1, t));
      var a = t < 0 ? [88, 166, 255] : [247, 209, 84], m = [120, 130, 145], u = Math.abs(t);
      return "rgb(" + Math.round(m[0] + (a[0] - m[0]) * u) + "," + Math.round(m[1] + (a[1] - m[1]) * u) + "," + Math.round(m[2] + (a[2] - m[2]) * u) + ")";
    };
    QB.widget(el, {
      title: "Over-smoothing: what repeated averaging forgets",
      sub: "Thirty-six nodes in three communities; each node starts with a noisy feature near −1, 0 or +1 (blue, grey, gold). One round replaces every feature by the normalized average over the node and its neighbours, as a graph convolution does. A few rounds remove the noise; many rounds remove the communities too, at a rate set by the second eigenvalue λ₂. Add edges between the communities and it happens sooner.",
      panels: 2, height: 320,
      controls: [
        { k: "k", label: "Rounds of averaging", min: 0, max: KMAX, step: 1, value: 2 },
        { k: "pout", label: "Chance of an edge between communities", min: 0, max: 0.3, step: 0.01, value: 0.03, fmt: function (x) { return x.toFixed(2); } },
        { k: "noise", label: "Noise in the starting features", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New graph", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 250), i, j, k, A = [], d = [], px = [], py = [], h = [], y = [];
        for (i = 0; i < N; i++) { A.push(new Array(N).fill(0)); y.push(Math.floor(i / PER)); }
        for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) { // the same random numbers decide every edge, so a slider only adds or removes edges
          var u = r();
          if (u < (y[i] === y[j] ? 0.4 : v.pout)) { A[i][j] = 1; A[j][i] = 1; }
        }
        for (i = 0; i < N; i++) {
          var ca = -Math.PI / 2 + 2 * Math.PI * y[i] / K, na = 2 * Math.PI * (i % PER) / PER, rr = 0.13 + 0.05 * r();
          px.push(0.5 + 0.31 * Math.cos(ca) + rr * Math.cos(na)); py.push(0.6 + 0.36 * Math.sin(ca) + 1.25 * rr * Math.sin(na));
        }
        for (i = 0; i < N; i++) h.push(y[i] - 1 + v.noise * r.normal());
        for (i = 0; i < N; i++) { d.push(1); for (j = 0; j < N; j++) d[i] += A[i][j]; }
        var step = function (x) { // x <- D^-1/2 (A + I) D^-1/2 x
          var o = new Array(N), a, b, t;
          for (a = 0; a < N; a++) { t = x[a] / d[a]; for (b = 0; b < N; b++) if (A[a][b]) t += x[b] / Math.sqrt(d[a] * d[b]); o[a] = t; }
          return o;
        };
        var energy = function (x) { var o = step(x), e = 0, a; for (a = 0; a < N; a++) e += x[a] * (x[a] - o[a]); return Math.max(e, 0); };
        // lambda_2: power iteration on (A_hat + I)/2 with the top eigenvector sqrt(d) projected out
        var dn = 0, q = [], lam = 0; for (i = 0; i < N; i++) dn += d[i];
        var rq = QB.rng(7); for (i = 0; i < N; i++) q.push(rq.normal());
        for (k = 0; k < 300; k++) {
          var dot = 0, nrm = 0, o = step(q);
          for (i = 0; i < N; i++) o[i] = 0.5 * (o[i] + q[i]);
          for (i = 0; i < N; i++) dot += o[i] * Math.sqrt(d[i]);
          for (i = 0; i < N; i++) { o[i] -= dot * Math.sqrt(d[i]) / dn; nrm += o[i] * o[i]; }
          nrm = Math.sqrt(nrm) || 1; lam = nrm; // |(A_hat + I)/2 q| for a unit q tends to (lambda_2 + 1)/2
          for (i = 0; i < N; i++) q[i] = o[i] / nrm;
          if (k === 0) lam = 0.5;
        }
        var l2 = Math.max(-1, Math.min(1, 2 * lam - 1));
        var ks = [], es = [], ref = [], cur = h.slice(), e0 = Math.max(energy(h), 1e-12), shown = h, means;
        for (k = 0; k <= KMAX; k++) {
          if (k === v.k) shown = cur.slice();
          ks.push(k); es.push(Math.max(1e-9, energy(cur) / e0)); ref.push(Math.max(1e-9, Math.pow(Math.abs(l2), 2 * k)));
          cur = step(cur);
        }
        means = [0, 0, 0]; for (i = 0; i < N; i++) means[y[i]] += shown[i] / PER;
        var within = 0; for (i = 0; i < N; i++) within += (shown[i] - means[y[i]]) * (shown[i] - means[y[i]]) / N;
        s.out = [l2, es[v.k], means[2] - means[0], Math.sqrt(within)];
        var c = g.ctx, box = g[0].box, X = function (a) { return box.x + 14 + (box.w - 28) * a; }, Y = function (a) { return box.y + 26 + (box.h - 40) * a; };
        c.save(); c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textBaseline = "top"; c.textAlign = "left";
        c.fillText("Node features after " + v.k + (v.k === 1 ? " round" : " rounds"), box.x + 12, box.y + 6);
        c.lineWidth = 1;
        for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) if (A[i][j]) {
          c.strokeStyle = y[i] === y[j] ? "rgba(139,152,169,0.22)" : "rgba(248,113,113,0.55)";
          c.beginPath(); c.moveTo(X(px[i]), Y(py[i])); c.lineTo(X(px[j]), Y(py[j])); c.stroke();
        }
        for (i = 0; i < N; i++) {
          c.fillStyle = mix(shown[i]); c.beginPath(); c.arc(X(px[i]), Y(py[i]), 6.5, 0, 6.2832); c.fill();
          c.strokeStyle = "#0e1117"; c.stroke();
        }
        c.restore();
        var b = g[1].axes({ x: [0, KMAX], y: [1e-6, 1], logy: true, title: "Dirichlet energy left", xlabel: "rounds of averaging", nx: 4, yticks: [1e-6, 1e-4, 1e-2, 1],
          yfmt: function (t) { return t >= 1 ? "1" : "1e" + Math.round(Math.log(t) / Math.LN10); } });
        b.line(ks, ref, { color: C.idea, width: 1.4, dash: [5, 4] }).line(ks, es, { color: C.spot, width: 2 });
        b.vline(v.k); b.dots([v.k], [es[v.k]], { color: C.spot, r: 4.5 });
        b.legend([["energy of the features", C.spot], ["λ₂ to the power 2k", C.idea]], { pos: "bl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["λ₂", fmt(o[0], 3)], ["energy left", o[1] < 1e-4 ? "under 0.01%" : QB.pct(o[1], 2)], ["gold mean − blue mean", fmt(o[2], 3)], ["spread within a community", fmt(o[3], 3)]];
      },
      note: "Simulated graph: edges inside a community with chance 0.4; edges between communities are drawn red. The averaging matrix is D^(−1/2)(A + I)D^(−1/2), a graph convolution without weights or nonlinearity. Dirichlet energy is xᵀ(I − Â)x, zero only when every feature is proportional to the square root of its node's degree.",
    });
  };
})();
