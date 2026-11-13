// Interactives for Act IV, Algorithms (Parts 19-24).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(c, str, x, y, o) { // one line of text on the canvas
    o = o || {}; c.save(); c.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    c.fillStyle = o.color || C.muted; c.textAlign = o.align || "left"; c.textBaseline = o.base || "middle";
    c.fillText(str, x, y); c.restore();
  }
  function heading(c, box, str) { label(c, str, box.x + 12, box.y + 14, { bold: true, size: 12.5, color: C.ink }); }
  function lg2(x) { return Math.log(x) / Math.LN2; }

  // ---- Part 19: squaring the evaluation points ---------------------------------------------------------------
  W.rootsquaring = function (el) {
    var names = ["roots of unity", "real ± pairs"];
    QB.widget(el, {
      title: "Why the FFT evaluates at roots of unity",
      sub: "Evaluating at x and −x shares the work, because both need the same two half-size polynomials at x². To recurse, the squared points must again come in opposite pairs. Square the n roots of unity and they land on n/2 roots of unity, pairs intact. Switch to real ± pairs and the trick works once, then stops.",
      panels: 2, height: 300,
      controls: [
        { k: "lg", label: "Points n", min: 1, max: 6, step: 1, value: 3, fmt: function (x) { return String(Math.pow(2, x)); } },
        { k: "sq", label: "Times squared", min: 0, max: 6, step: 1, value: 0 },
        { k: "kind", label: "Point set", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return names[x]; } },
      ],
      draw: function (g, v, s) {
        var n = Math.pow(2, v.lg), k = v.sq, real = v.kind === 1, c = g.ctx, b = g[0].box, j;
        var distinct = real ? (k === 0 ? n : n / 2) : Math.max(1, n / Math.pow(2, k));
        var pairs = real ? k === 0 : distinct >= 2;
        var direct = n * n, once = n * n / 2 + n / 2, fast = n / 2 * v.lg;
        s.out = [n, distinct, pairs, direct, real ? once : fast];
        heading(c, b, "The points after " + k + (k === 1 ? " squaring" : " squarings"));
        var cx = b.x + b.w / 2, cy = b.y + 28 + (b.h - 56) / 2, R = Math.min(b.w - 40, b.h - 70) / 2;
        c.save(); c.strokeStyle = C.line; c.lineWidth = 1;
        c.beginPath(); c.moveTo(cx - R - 12, cy); c.lineTo(cx + R + 12, cy); c.moveTo(cx, cy - R - 8); c.lineTo(cx, cy + R + 8); c.stroke();
        c.strokeStyle = "#3a475c"; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        var pts = [], seen = {}, key, x, y, a, r0, p = Math.pow(2, k);
        for (j = 0; j < n; j++) {
          if (real) {
            r0 = (Math.floor(j / 2) + 1) / (n / 2) * (j % 2 ? -1 : 1);
            c.fillStyle = C.muted; c.globalAlpha = 0.45; c.beginPath(); c.arc(cx + R * r0, cy, 2.5, 0, 6.2832); c.fill();
            x = Math.pow(r0, p); y = 0;
          } else {
            a = 2 * Math.PI * j / n;
            c.fillStyle = C.muted; c.globalAlpha = 0.45; c.beginPath(); c.arc(cx + R * Math.cos(a), cy - R * Math.sin(a), 2.5, 0, 6.2832); c.fill();
            a = 2 * Math.PI * ((j * p) % n) / n; x = Math.cos(a); y = Math.sin(a);
          }
          key = Math.round(x * 1e6) + "," + Math.round(y * 1e6);
          if (!seen[key]) { seen[key] = 1; pts.push([x, y]); }
        }
        c.globalAlpha = 1;
        if (pairs) { // join each point to its opposite
          c.strokeStyle = C.spot; c.lineWidth = 1; c.globalAlpha = 0.5;
          for (j = 0; j < pts.length; j++) { c.beginPath(); c.moveTo(cx + R * pts[j][0], cy - R * pts[j][1]); c.lineTo(cx - R * pts[j][0], cy + R * pts[j][1]); c.stroke(); }
          c.globalAlpha = 1;
        }
        c.fillStyle = C.idea;
        for (j = 0; j < pts.length; j++) { c.beginPath(); c.arc(cx + R * pts[j][0], cy - R * pts[j][1], 4.5, 0, 6.2832); c.fill(); }
        c.restore();
        label(c, n + " points (grey) land on " + distinct + " (gold)" + (pairs ? ", still in ± pairs" : ", no ± pairs left"), cx, b.y + b.h - 14, { align: "center", color: pairs ? C.gain : C.loss });
        var ns = [], d = [], o = [], f = [];
        for (j = 1; j <= 6; j++) { var m = Math.pow(2, j); ns.push(m); d.push(m * m); o.push(m * m / 2 + m / 2); f.push(Math.max(1, m / 2 * j)); }
        var ax = g[1].axes({ x: [2, 64], y: [1, 10000], logx: true, logy: true, title: "Multiplications to evaluate at n points", xlabel: "n (coefficients and points)", xticks: [2, 4, 8, 16, 32, 64], xfmt: function (t) { return String(t); } });
        ax.line(ns, d, { color: C.loss }).line(ns, o, { color: C.implied, alpha: real ? 1 : 0.45 }).line(ns, f, { color: C.spot, alpha: real ? 0.45 : 1 });
        ax.dots([n], [Math.max(1, real ? once : fast)], { color: C.idea, r: 5 });
        ax.legend([["one point at a time: n²", C.loss], ["one halving: n²/2 + n/2", C.implied], ["FFT: (n/2) lg n", C.spot]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["points", String(s.out[0])], ["distinct after squaring", String(s.out[1])], ["opposite pairs left", s.out[2] ? "yes" : "no"],
          ["one point at a time", String(s.out[3])], ["with this point set", String(s.out[4])]];
      },
      note: "Exact counts of multiplications, no simulation. The roots of unity are the n complex numbers with xⁿ = 1; a blue line joins each point to its opposite. Squares of real numbers are never negative, so a real point set cannot keep its pairs. The gold dot on the right marks the count for the chosen point set.",
    });
  };

  // ---- Part 20: a Bloom filter filling up --------------------------------------------------------------------
  W.bloombits = function (el) {
    var N = 150, Q = 3000;
    QB.widget(el, {
      title: "A Bloom filter: bits per word against hash functions",
      sub: "150 words are added to an array of m bits; each word sets k bits. A word that was never added is a false positive when all k of its bits are already set. Raise k from 1: the error falls, then rises again as the array fills past one half. Add bits per word and the whole curve drops.",
      panels: 2, height: 300,
      controls: [
        { k: "bpw", label: "Bits per word m/n", min: 2, max: 20, step: 1, value: 10 },
        { k: "k", label: "Hash functions k", min: 1, max: 16, step: 1, value: 7 },
      ],
      buttons: [{ label: "New hashes", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 200), m = v.bpw * N, bits = new Array(m).fill(0), i, j, set = 0, fp = 0, hit;
        for (i = 0; i < N; i++) for (j = 0; j < v.k; j++) bits[Math.floor(r() * m)] = 1;
        for (i = 0; i < m; i++) set += bits[i];
        for (i = 0; i < Q; i++) { hit = 1; for (j = 0; j < v.k && hit; j++) hit = bits[Math.floor(r() * m)]; fp += hit; }
        var th = function (k) { return Math.pow(1 - Math.exp(-k / v.bpw), k); };
        s.out = [set / m, fp / Q, th(v.k), v.bpw * Math.LN2];
        var c = g.ctx, b = g[0].box;
        heading(c, b, "The array: " + m + " bits, " + QB.pct(set / m, 0) + " set");
        var X = b.x + 14, Y = b.y + 30, Wd = b.w - 28, Ht = b.h - 44;
        var cell = Math.max(2, Math.floor(Math.sqrt(Wd * Ht / m))), cols = Math.floor(Wd / cell);
        while (Math.ceil(m / cols) * cell > Ht && cell > 2) { cell--; cols = Math.floor(Wd / cell); }
        c.save();
        for (i = 0; i < m; i++) {
          c.fillStyle = bits[i] ? C.idea : "#222b3a";
          c.fillRect(X + (i % cols) * cell, Y + Math.floor(i / cols) * cell, Math.max(1, cell - 1), Math.max(1, cell - 1));
        }
        c.restore();
        var ks = [], ys = [], top = 0;
        for (j = 1; j <= 16; j++) { ks.push(j); ys.push(Math.max(1e-6, th(j))); }
        var ax = g[1].axes({ x: [1, 16], y: [1e-5, 1], logy: true, title: "False positives against k", xlabel: "hash functions k", xticks: [1, 4, 8, 12, 16], yfmt: function (t) { return t >= 0.01 ? Math.round(100 * t) + "%" : (100 * t).toPrecision(1) + "%"; } });
        ax.line(ks, ys, { color: C.q });
        ax.vline(Math.min(16, Math.max(1, v.bpw * Math.LN2)), { color: C.muted });
        ax.dots([v.k], [Math.max(1.2e-5, fp / Q)], { color: C.gain, r: 5 });
        ax.legend([["formula (1 − e^(−kn/m))^k", C.q], ["measured on 3,000 non-words", C.gain], ["k = (m/n) ln 2", C.muted]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["bits set", QB.pct(s.out[0])], ["false positives, measured", QB.pct(s.out[1], 2)], ["formula", QB.pct(s.out[2], 2)], ["best k", fmt(s.out[3], 1)]];
      },
      note: "Simulated data: every hash is an independent uniform position, the ideal model behind the formula. Gold cells are set bits. A real filter's hash functions only approximate this, so the film measures its own. A measured rate of zero is drawn at the bottom of the axis.",
    });
  };

  // ---- Part 21: three matchers on one text -------------------------------------------------------------------
  W.skipahead = function (el) {
    var N = 3000, SHOW = 64, kinds = ["random letters", "aaa…, pattern aa…ab", "aaa…, pattern baa…a"];
    QB.widget(el, {
      title: "Naive, Knuth-Morris-Pratt and Horspool on the same text",
      sub: "Each strip is the start of a 3,000-letter text, shaded by how often each letter is compared: dark is never, blue once, gold twice, red three times or more. On random letters the naive scan is near one comparison per letter and Horspool (Boyer and Moore's bad-character skip) reads a fraction. Shrink the alphabet, or pick a text of one letter, and two of the three break. KMP never passes two.",
      panels: 2, height: 300,
      controls: [
        { k: "sig", label: "Alphabet size", min: 2, max: 26, step: 1, value: 20 },
        { k: "m", label: "Pattern length m", min: 2, max: 24, step: 1, value: 8 },
        { k: "kind", label: "Text", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return kinds[x]; } },
      ],
      buttons: [{ label: "New text", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 77), m = v.m, t = new Array(N), p = new Array(m), i, j, k;
        if (v.kind === 0) {
          for (i = 0; i < N; i++) t[i] = Math.floor(r() * v.sig);
          k = Math.floor(r() * (N - m)); for (j = 0; j < m; j++) p[j] = t[k + j];
        } else {
          for (i = 0; i < N; i++) t[i] = 0;
          for (j = 0; j < m; j++) p[j] = 0;
          p[v.kind === 1 ? m - 1 : 0] = 1;
        }
        var seen = [new Array(SHOW).fill(0), new Array(SHOW).fill(0), new Array(SHOW).fill(0)], cmp = [0, 0, 0], hits = [0, 0, 0];
        var touch = function (a, pos) { cmp[a]++; if (pos < SHOW) seen[a][pos]++; };
        for (i = 0; i + m <= N; i++) { // naive
          for (j = 0; j < m; j++) { touch(0, i + j); if (t[i + j] !== p[j]) break; }
          if (j === m) hits[0]++;
        }
        var fail = new Array(m).fill(0); k = 0; // Knuth-Morris-Pratt
        for (j = 1; j < m; j++) { while (k && p[j] !== p[k]) k = fail[k - 1]; if (p[j] === p[k]) k++; fail[j] = k; }
        for (i = 0, j = 0; i < N; i++) {
          for (;;) { touch(1, i); if (t[i] === p[j]) { j++; break; } if (j === 0) break; j = fail[j - 1]; }
          if (j === m) { hits[1]++; j = fail[j - 1]; }
        }
        var shift = {}; for (j = 0; j < m - 1; j++) shift[p[j]] = m - 1 - j; // Horspool
        for (i = 0; i + m <= N; i += (shift[t[i + m - 1]] || m)) {
          for (j = m - 1; j >= 0; j--) { touch(2, i + j); if (t[i + j] !== p[j]) break; }
          if (j < 0) hits[2]++;
        }
        s.out = [cmp[0] / N, cmp[1] / N, cmp[2] / N, hits[0], hits[0] === hits[1] && hits[1] === hits[2]];
        var c = g.ctx, b = g[0].box, names = ["naive", "KMP", "Horspool"], cols = [C.spot, C.idea, C.loss];
        heading(c, b, "The first " + SHOW + " letters: comparisons at each one");
        var X = b.x + 14, cw = (b.w - 28) / SHOW, rowH = Math.min(46, (b.h - 60) / 3), Y0 = b.y + 44;
        for (k = 0; k < 3; k++) {
          label(c, names[k] + ": " + fmt(cmp[k] / N, 2) + " per letter", X, Y0 + k * (rowH + 22) - 9, { color: C.ink });
          for (i = 0; i < SHOW; i++) {
            j = seen[k][i];
            c.fillStyle = j === 0 ? "#222b3a" : cols[Math.min(j, 3) - 1];
            c.fillRect(X + i * cw, Y0 + k * (rowH + 22), Math.max(1, cw - 1), rowH - 6);
          }
        }
        var top = Math.max(2.5, Math.ceil(Math.max(cmp[0], cmp[2]) / N * 1.1));
        var ax = g[1].axes({ x: [0, 3], y: [0, top], title: "Comparisons per letter of text", xticks: [0.5, 1.5, 2.5], xfmt: function (x) { return names[Math.floor(x)]; }, xlabel: "all " + N + " letters" });
        ax.bars([0.5, 1.5, 2.5], [cmp[0] / N, cmp[1] / N, cmp[2] / N], 0.6, { color: function (q) { return [C.loss, C.gain, C.implied][q]; } });
        ax.hline(2, { color: C.gain }).hline(1, { color: C.muted });
        ax.legend([["KMP's bound: 2", C.gain], ["one per letter", C.muted]], { pos: v.kind === 1 ? "tr" : "tl" });
      },
      readout: function (v, s) {
        return [["naive", fmt(s.out[0], 2)], ["KMP", fmt(s.out[1], 2)], ["Horspool", fmt(s.out[2], 2)], ["occurrences", String(s.out[3])], ["the three agree", s.out[4] ? "yes" : "no"]];
      },
      note: "Simulated text: independent uniform letters, with the pattern copied from a random place in it, or one repeated letter with the stated pattern. Counts are comparisons divided by the text length. Full Boyer-Moore adds the good-suffix rule, which rescues the third text; without Galil's refinement it still has its own n times m worst case, a pattern that matches everywhere.",
    });
  };

  // ---- Part 22: the orientation test on neighbouring doubles -------------------------------------------------
  W.orientgrid = function (el) {
    var G = 64, U = Math.pow(2, -53), pivots = ["p", "q", "r"];
    // the sign of the same determinant, written around each of the three points
    function det(k, px, py, qx, qy, rx, ry) {
      var d = k === 0 ? (qx - px) * (ry - py) - (qy - py) * (rx - px)
        : k === 1 ? (rx - qx) * (py - qy) - (ry - qy) * (px - qx)
          : (px - rx) * (qy - ry) - (py - ry) * (qx - rx);
      return d > 0 ? 1 : d < 0 ? -1 : 0;
    }
    QB.widget(el, {
      title: "Left, right, or on the line? The answer in double precision",
      sub: "Each cell is a point p whose coordinates are neighbouring doubles just above 1/2; the line runs through q = (a, a) and r = (b, b), so the true answer is left above the diagonal and right below it. The colour is what the floating determinant says; red cells are wrong. Change which point the differences are taken from, or move q and r, and the wrong cells move.",
      panels: 2, height: 320,
      controls: [
        { k: "piv", label: "Differences taken from", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return pivots[x]; } },
        { k: "a", label: "q = (a, a)", min: 1, max: 30, step: 1, value: 12 },
        { k: "b", label: "r = (b, b)", min: 2, max: 60, step: 1, value: 24 },
      ],
      draw: function (g, v, s) {
        var a = v.a, bq = v.b === v.a ? v.a + 1 : v.b, c = g.ctx, b = g[0].box, i, j, k, x, y, sg, ex, wrong = [0, 0, 0], zero = 0;
        var side = Math.max(60, Math.min(b.w - 28, b.h - 62)), cell = side / G, X = b.x + (b.w - side) / 2, Y = b.y + 30;
        heading(c, b, "Floating sign at 64 × 64 neighbouring doubles");
        c.save();
        for (j = 0; j < G; j++) {
          y = 0.5 + j * U;
          for (i = 0; i < G; i++) {
            x = 0.5 + i * U;
            ex = (j > i ? 1 : j < i ? -1 : 0) * (bq > a ? 1 : -1);
            for (k = 0; k < 3; k++) { sg = det(k, x, y, a, a, bq, bq); if (sg !== ex) wrong[k]++; if (k === v.piv) { s.sg = sg; } }
            sg = s.sg; if (sg === 0) zero++;
            c.fillStyle = sg !== ex ? C.loss : sg > 0 ? C.spot : sg < 0 ? C.gain : C.cash;
            c.fillRect(X + i * cell, Y + (G - 1 - j) * cell, cell + 0.5, cell + 0.5);
          }
        }
        c.restore();
        label(c, "blue left · green right · grey on the line · red wrong", b.x + b.w / 2, Y + side + 14, { align: "center", size: 11 });
        s.out = [wrong[v.piv], zero, wrong, bq];
        var ax = g[1].axes({ x: [0, 3], y: [0, G * G], title: "Wrong signs of " + G * G + ", by the point subtracted", xticks: [0.5, 1.5, 2.5], xfmt: function (t) { return "from " + pivots[Math.floor(t)]; }, yticks: [0, 1024, 2048, 3072, 4096] });
        ax.bars([0.5, 1.5, 2.5], wrong, 0.6, { color: function (q) { return q === v.piv ? C.loss : C.cash; } });
        for (k = 0; k < 3; k++) ax.text(k + 0.5, wrong[k], String(wrong[k]), { align: "center", dy: -9, color: C.ink });
      },
      readout: function (v, s) {
        return [["wrong signs", s.out[0] + " of " + G * G], ["reported on the line", String(s.out[1])], ["truly on the line", String(G)], ["line through", "(" + v.a + ", " + v.a + ") and (" + s.out[3] + ", " + s.out[3] + ")"]];
      },
      note: "Computed here in your browser's own double-precision arithmetic, not simulated; the exact sign is known because the line is the diagonal. Algebraically the three determinants are equal. When a = b the widget uses b = a + 1. The film's grid is 256 × 256 with q = (12, 12) and r = (24, 24).",
    });
  };

  // ---- Part 23: a dual solution as a proof -------------------------------------------------------------------
  W.dualbound = function (el) {
    var A = [[2, 1], [1, 2]], B = [8, 7], C2 = 2; // maximize c1 x1 + 2 x2 with 2 x1 + x2 <= 8, x1 + 2 x2 <= 7, x >= 0
    var V = [[0, 0], [4, 0], [3, 2], [0, 3.5]];
    QB.widget(el, {
      title: "Prices that prove the optimum",
      sub: "Left: maximize c₁x₁ + 2x₂ over the blue region; the gold dot is the best vertex. Right: multiply the two constraints by prices y₁, y₂ and add. If the sum covers both profit coefficients (the shaded region), then 8y₁ + 7y₂ is a ceiling on every plan's profit. Slide the prices down to the corner of the shaded region and the ceiling meets the optimum; leave the region and it proves nothing.",
      panels: 2, height: 310,
      controls: [
        { k: "c1", label: "Profit of product 1, c₁", min: 0, max: 6, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1); } },
        { k: "y1", label: "Price y₁ of constraint 1", min: 0, max: 3, step: 0.05, value: 1.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "y2", label: "Price y₂ of constraint 2", min: 0, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var c1 = v.c1, i, best = 0, bv = -1, val;
        for (i = 0; i < 4; i++) { val = c1 * V[i][0] + C2 * V[i][1]; if (val > bv + 1e-9) { bv = val; best = i; } }
        var cover1 = A[0][0] * v.y1 + A[1][0] * v.y2, cover2 = A[0][1] * v.y1 + A[1][1] * v.y2;
        var feas = cover1 >= c1 - 1e-9 && cover2 >= C2 - 1e-9, bound = B[0] * v.y1 + B[1] * v.y2;
        var cand = [[c1 / 2, 0], [C2, 0], [0, c1], [0, C2 / 2], [(2 * c1 - C2) / 3, (2 * C2 - c1) / 3]], dbest = null, dv = 1e9, d;
        for (i = 0; i < cand.length; i++) {
          d = cand[i];
          if (d[0] < -1e-9 || d[1] < -1e-9 || 2 * d[0] + d[1] < c1 - 1e-9 || d[0] + 2 * d[1] < C2 - 1e-9) continue;
          if (8 * d[0] + 7 * d[1] < dv - 1e-9) { dv = 8 * d[0] + 7 * d[1]; dbest = d; }
        }
        s.out = [bv, feas, bound, dv, V[best], dbest, cover1, cover2];
        var a = g[0].axes({ x: [0, 5], y: [0, 4.5], title: "Primal: plans (x₁, x₂)", xlabel: "x₁" });
        a.area([0, 3, 4], [3.5, 2, 0], 0, { color: C.spot, alpha: 0.28 });
        a.line([0, 4], [8, 0], { color: C.spot, width: 1.3 }).line([0, 5], [3.5, 1], { color: C.spot, width: 1.3 });
        a.text(0.25, 4.15, "2x₁ + x₂ ≤ 8", { color: C.spot, bg: true }).text(3.4, 1.55, "x₁ + 2x₂ ≤ 7", { color: C.spot, bg: true });
        a.line([0, 5], [bv / C2, (bv - 5 * c1) / C2], { color: C.idea, dash: [5, 4], width: 1.4 }); // the objective line through the optimum
        if (feas) a.line([0, 5], [bound / C2, (bound - 5 * c1) / C2], { color: C.gain, width: 1.4 });
        a.dots([V[best][0]], [V[best][1]], { color: C.idea, r: 6 });
        a.legend(feas ? [["profit = " + fmt(bv, 2) + " (best)", C.idea], ["ceiling = " + fmt(bound, 2), C.gain]] : [["profit = " + fmt(bv, 2) + " (best)", C.idea]], { pos: "tr" });
        var q = g[1].axes({ x: [0, 3.2], y: [0, 3.2], title: "Dual: prices (y₁, y₂)", xlabel: "y₁" });
        var ys = QB.linspace(0, 3.2, 65), lo = ys.map(function (t) { return Math.min(3.2, Math.max(0, c1 - 2 * t, (C2 - t) / 2)); });
        q.area(ys, ys.map(function () { return 3.2; }), lo, { color: C.gain, alpha: 0.2 });
        q.line([0, 3.2], [c1, c1 - 6.4], { color: C.gain, width: 1.2 }).line([0, 3.2], [C2 / 2, (C2 - 3.2) / 2], { color: C.gain, width: 1.2 });
        q.line([0, 3.2], [bound / 7, (bound - 8 * 3.2) / 7], { color: feas ? C.gain : C.loss, dash: [5, 4], width: 1.2 }); // prices with the same ceiling
        if (dbest) q.dots([dbest[0]], [dbest[1]], { color: C.idea, r: 5 });
        q.dots([v.y1], [v.y2], { color: feas ? C.gain : C.loss, r: 6 });
        q.legend([["your prices: " + (feas ? "a valid ceiling" : "prove nothing"), feas ? C.gain : C.loss], ["cheapest valid prices", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["best plan", "(" + fmt(o[4][0], 1) + ", " + fmt(o[4][1], 1) + "), profit " + fmt(o[0], 2)],
          ["your prices cover", fmt(o[6], 2) + " ≥ " + fmt(v.c1, 1) + " and " + fmt(o[7], 2) + " ≥ 2: " + (o[1] ? "yes" : "no")],
          ["ceiling 8y₁ + 7y₂", o[1] ? fmt(o[2], 2) : "not valid"], ["gap to the optimum", o[1] ? fmt(o[2] - o[0], 2) : "none proved"],
          ["cheapest valid ceiling", fmt(o[3], 2)]];
      },
      note: "Exact arithmetic on a fixed two-constraint linear program; nothing is simulated. Weak duality: every point of the shaded region gives a ceiling. Strong duality: the cheapest ceiling equals the best profit, so the gold dots on the two sides always carry the same value.",
    });
  };

  // ---- Part 24: a Fenwick tree's responsibility ranges -------------------------------------------------------
  W.lowbitladder = function (el) {
    var modes = ["prefix sum of a[1..i]", "add to a[i]"];
    function low(i) { return i & -i; }
    QB.widget(el, {
      title: "A Fenwick tree: which cells does one operation touch?",
      sub: "Cell j holds the sum of the lowbit(j) elements that end at j, drawn as a bar; taller rows hold longer ranges. A prefix sum strips the lowest set bit of i until it reaches 0, and its gold bars tile a[1..i] exactly. An update adds the lowest set bit until it passes n, and touches every bar that covers i. On the right, compare with a plain array (slow queries) and a prefix-sum array (slow updates).",
      panels: 2, height: 300,
      controls: [
        { k: "lg", label: "Cells n", min: 3, max: 6, step: 1, value: 5, fmt: function (x) { return String(Math.pow(2, x)); } },
        { k: "i", label: "Index i", min: 1, max: 64, step: 1, value: 13 },
        { k: "mode", label: "Operation", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return modes[x]; } },
      ],
      draw: function (g, v, s) {
        var n = Math.pow(2, v.lg), i = Math.min(v.i, n), j, k, path = {}, steps = [], lv = v.lg + 1;
        if (v.mode === 0) for (j = i; j > 0; j -= low(j)) { path[j] = 1; steps.push(j); }
        else for (j = i; j <= n; j += low(j)) { path[j] = 1; steps.push(j); }
        var plain = v.mode === 0 ? i : 1, pre = v.mode === 0 ? 1 : n - i + 1;
        s.out = [i, steps, plain, pre, lv, n];
        var a = g[0].axes({ x: [0, n], y: [0, lv], title: "Responsibility ranges, by lowest set bit", xlabel: "array position", xticks: [0, n / 4, n / 2, 3 * n / 4, n], yticks: [], noY: true });
        var c = g.ctx, rh = (a.py(0) - a.py(1));
        c.save();
        for (j = 1; j <= n; j++) {
          k = Math.round(lg2(low(j)));
          var x0 = a.px(j - low(j)), x1 = a.px(j), y0 = a.py(k + 1) + 3;
          c.fillStyle = path[j] ? C.idea : "#2b3850"; c.globalAlpha = path[j] ? 1 : 0.9;
          c.fillRect(x0 + 1, y0, Math.max(1.5, x1 - x0 - 2), Math.max(4, rh - 6));
        }
        c.globalAlpha = 1; c.restore();
        if (v.mode === 0) a.area([0, i], [0.12, 0.12], 0, { color: C.gain, alpha: 0.9 });
        a.vline(v.mode === 0 ? i : i - 0.5, { color: C.gain, dash: [3, 3] });
        var xs = [], f = [], pl = [], pp = [], t;
        for (j = 1; j <= n; j++) {
          xs.push(j);
          k = 0; if (v.mode === 0) for (t = j; t > 0; t -= low(t)) k++; else for (t = j; t <= n; t += low(t)) k++;
          f.push(k); pl.push(v.mode === 0 ? j : 1); pp.push(v.mode === 0 ? 1 : n - j + 1);
        }
        var b = g[1].axes({ x: [1, n], y: [0.8, 80], logy: true, title: "Cells touched by this operation at each index", xlabel: "index i", xticks: [1, n / 4, n / 2, 3 * n / 4, n], yticks: [1, 2, 4, 8, 16, 32, 64], yfmt: function (y) { return String(y); } });
        b.hline(lv, { color: C.muted });
        b.line(xs, pl, { color: C.loss, width: 1.4 }).line(xs, pp, { color: C.implied, width: 1.4 }).line(xs, f, { color: C.idea, width: 1.8 });
        b.vline(i, { color: C.gain, dash: [3, 3] });
        b.dots([i], [steps.length], { color: C.idea, r: 5 });
        b.legend([["Fenwick tree", C.idea], ["plain array", C.loss], ["prefix-sum array", C.implied], ["lg n + 1", C.muted]], { pos: v.mode === 0 ? "tl" : "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["i", String(o[0]) + " = " + o[0].toString(2) + "₂"], ["Fenwick cells", o[1].join(" → ") + " (" + o[1].length + ")"], ["plain array", String(o[2])], ["prefix-sum array", String(o[3])], ["bound lg n + 1", String(o[4])]];
      },
      note: "Exact counts of cells read or written, not times. Gold bars are the cells this operation touches; the green mark shows the prefix being summed or the element being changed. An index above n is clipped to n. A plain array answers a prefix sum by reading i cells; a prefix-sum array must rewrite n − i + 1 totals after one change.",
    });
  };
})();
