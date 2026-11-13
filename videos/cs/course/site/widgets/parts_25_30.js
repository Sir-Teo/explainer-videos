// Interactives for Act V, Limits and Secrets (Parts 25-30).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 25: Post's dominoes, searched with a budget ------------------------------------------------------
  W.pcpoverhang = function (el) {
    var SETS = [
      { name: "Sipser's four", d: [["b", "ca"], ["a", "ab"], ["ca", "a"], ["abc", "c"]] },
      { name: "three dominoes", d: [["10", "0"], ["00", "1"], ["0", "010"]] },
      { name: "no match", d: [["10", "1"], ["01", "1"], ["011", "00"]] },
      { name: "never settled", d: [["1", "11"], ["00", "0"]] },
      { name: "the film's four", d: [["1000", "0"], ["01", "0"], ["1", "101"], ["00", "001"]] },
    ];
    var MAXD = 240, cache = {};
    function search(k) { // breadth-first over overhangs, as explainer/cs/algo/computability.pcp_search does
      if (cache[k]) return cache[k];
      var d = SETS[k].d, q = [{ side: "", s: "", par: -1, dom: -1, depth: 0 }], seen = {}, head = 0;
      var fresh = [], total = 0, match = null, dead = 0, i, t, b, key, node;
      for (i = 0; i <= MAXD; i++) fresh.push(0);
      while (head < q.length && !match && q.length < 150000) {
        node = q[head]; head++;
        if (node.depth >= MAXD) continue;
        for (i = 0; i < d.length && !match; i++) {
          t = d[i][0]; b = d[i][1];
          if (node.side === "t") t = node.s + t; else if (node.side === "b") b = node.s + b;
          if (t === b) { match = { par: head - 1, dom: i }; break; }
          if (t.length > b.length && t.substring(0, b.length) === b) key = "t" + t.substring(b.length);
          else if (b.length > t.length && b.substring(0, t.length) === t) key = "b" + b.substring(t.length);
          else continue;
          if (!seen[key]) { seen[key] = 1; fresh[node.depth + 1]++; total++; q.push({ side: key.charAt(0), s: key.substring(1), par: head - 1, dom: i, depth: node.depth + 1 }); }
        }
      }
      var seq = [], over = [], p, tt = 0, bb = 0;
      if (match) {
        seq.push(match.dom);
        for (p = match.par; p > 0; p = q[p].par) seq.push(q[p].dom);
        seq.reverse();
        for (i = 0; i < seq.length; i++) { tt += d[seq[i]][0].length; bb += d[seq[i]][1].length; over.push(tt - bb); }
      } else if (head >= q.length) { for (i = 1; i <= MAXD; i++) if (fresh[i] > 0) dead = i; dead += 1; }
      cache[k] = { fresh: fresh, seq: seq, over: over, len: seq.length, dead: dead, total: total };
      return cache[k];
    }
    function label(k) { return SETS[k].d.map(function (x) { return x[0] + "/" + x[1]; }).join("  "); }
    QB.widget(el, {
      title: "A budget is not a verdict: searching Post's dominoes",
      sub: "Each domino is top/bottom; a match is a row of dominoes whose tops and bottoms spell the same string. The search keeps only the overhang, the part of one row that sticks out past the other. Pick a set, then raise the budget (the longest row tried): some sets match, one is exhausted, one never settles, and the film's four dominoes say nothing until 206.",
      panels: 2, height: 300,
      controls: [
        { k: "set", label: "Domino set", min: 1, max: 5, step: 1, value: 5, fmt: function (x) { return x + ": " + SETS[x - 1].name; } },
        { k: "budget", label: "Budget: dominoes in a row", min: 1, max: 230, step: 1, value: 120 },
      ],
      draw: function (g, v, s) {
        var r = search(v.set - 1), L = v.budget, xs = [], ys = [], i, top = 1, seen = 0;
        for (i = 1; i <= 230; i++) { xs.push(i); ys.push(r.fresh[i]); if (r.fresh[i] > top) top = r.fresh[i]; if (i <= L) seen += r.fresh[i]; }
        var verdict = r.len && r.len <= L ? "match" : (r.dead && r.dead <= L ? "none" : "open");
        s.out = { verdict: verdict, len: r.len, seen: seen, dead: r.dead };
        var a = g[0].axes({ x: [0, 230], y: [0, top * 1.15], title: "New overhangs found at each row length", xlabel: "dominoes in the row", xticks: [0, 50, 100, 150, 200] });
        a.bars(xs, ys, 1, { color: function (j) { return xs[j] <= L ? C.spot : C.line; }, gap: 0 });
        a.vline(L, { color: C.idea });
        if (r.len) a.vline(r.len, { color: C.gain, dash: [2, 3] });
        if (r.dead) a.vline(r.dead, { color: C.loss, dash: [2, 3] });
        a.text(115, top * 1.07, label(v.set - 1), { align: "center", color: C.muted, bg: true });
        var m = 4;
        for (i = 0; i < r.over.length; i++) m = Math.max(m, Math.abs(r.over[i]));
        var b = g[1].axes({ x: [0, 230], y: [-m * 1.2, m * 1.2], title: "Overhang along the shortest match", xlabel: "dominoes placed", xticks: [0, 50, 100, 150, 200] });
        b.hline(0, { color: C.muted });
        b.vline(L, { color: C.idea });
        if (r.len) {
          var kx = [0], ky = [0], cut = Math.min(L, r.len);
          for (i = 0; i < r.len; i++) { kx.push(i + 1); ky.push(r.over[i]); }
          b.line(kx, ky, { color: C.muted, width: 1.2 });
          b.line(kx.slice(0, cut + 1), ky.slice(0, cut + 1), { color: verdict === "match" ? C.gain : C.spot, width: 2 });
          b.text(8, m * 1.02, "top row ahead", { color: C.muted });
          b.text(8, -m * 1.02, "bottom row ahead", { color: C.muted });
        } else {
          b.text(115, m * 0.25, r.dead ? "No match exists:" : "No match is ever found,", { align: "center", color: r.dead ? C.loss : C.muted });
          b.text(115, -m * 0.2, r.dead ? "every overhang dies by row " + r.dead + "." : "and the overhangs never run out.", { align: "center", color: r.dead ? C.loss : C.muted });
        }
      },
      readout: function (v, s) {
        var o = s.out;
        return [["verdict at this budget", o.verdict === "match" ? "match of " + o.len + " dominoes" : o.verdict === "none" ? "no match exists (search exhausted)" : "none: the search was cut off"],
          ["overhangs explored", String(o.seen)],
          ["a budget that settles it", o.len ? String(o.len) : o.dead ? String(o.dead) : "does not exist"]];
      },
      note: "Exact breadth-first search in your browser, no simulation. Gold line: your budget. Green dashes: the shortest match. Red dashes: the row length at which the overhangs run out. Blue bars are within the budget, grey bars beyond it. No computable function of the dominoes bounds the budget that suffices: that is Post's theorem.",
    });
  };

  // ---- Part 26: random 3-SAT, decided by DPLL in the browser ---------------------------------------------------
  W.satthreshold = function (el) {
    var GRID = [2, 3, 3.5, 4, 4.25, 4.5, 5, 6, 7], cache = {};
    function formula(r, n, m) { // m clauses on three distinct variables with fair signs
      var cl = [], i, a, b, c;
      for (i = 0; i < m; i++) {
        a = 1 + Math.floor(r() * n);
        do { b = 1 + Math.floor(r() * n); } while (b === a);
        do { c = 1 + Math.floor(r() * n); } while (c === a || c === b);
        cl.push([r() < 0.5 ? a : -a, r() < 0.5 ? b : -b, r() < 0.5 ? c : -c]);
      }
      return cl;
    }
    function dpll(n, cl) { // unit propagation, then branch on the first open variable; returns [satisfiable, nodes]
      var val = new Int8Array(n + 1), nodes = 0;
      function rec() {
        nodes++;
        if (nodes > 4000) return false;
        var trail = [], changed = true, i, j, c, open, last, sat, l, v, pick = 0, ok = true;
        while (changed && ok) {
          changed = false; pick = 0;
          for (i = 0; i < cl.length && ok; i++) {
            c = cl[i]; open = 0; sat = false;
            for (j = 0; j < 3; j++) { l = c[j]; v = val[l > 0 ? l : -l]; if (v === 0) { open++; last = l; } else if ((v > 0) === (l > 0)) { sat = true; break; } }
            if (sat) continue;
            if (open === 0) ok = false;
            else if (open === 1) { val[last > 0 ? last : -last] = last > 0 ? 1 : -1; trail.push(last > 0 ? last : -last); changed = true; }
            else if (!pick) pick = last > 0 ? last : -last;
          }
        }
        if (ok && !pick) return true;
        if (ok) {
          val[pick] = 1; if (rec()) return true;
          val[pick] = -1; if (rec()) return true;
          val[pick] = 0;
        }
        for (i = 0; i < trail.length; i++) val[trail[i]] = 0;
        return false;
      }
      var res = rec();
      return [res && nodes <= 4000, nodes];
    }
    function point(r, n, ratio, trials) {
      var sat = 0, nodes = [], k, out;
      for (k = 0; k < trials; k++) { out = dpll(n, formula(r, n, Math.round(ratio * n))); if (out[0]) sat++; nodes.push(out[1]); }
      return [sat / trials, QB.quantile(nodes, 0.5)];
    }
    function curves(n, trials, seed) {
      var key = n + "|" + trials + "|" + seed;
      if (!cache[key]) {
        var r = QB.rng(seed * 7919 + n), f = [], w = [], i, p;
        for (i = 0; i < GRID.length; i++) { p = point(r, n, GRID[i], trials); f.push(p[0]); w.push(p[1]); }
        cache = {}; cache[key] = { f: f, w: w };
      }
      return cache[key];
    }
    QB.widget(el, {
      title: "Easy, hard, easy: random 3-SAT across the threshold",
      sub: "Each point is a batch of random formulas with n variables and m clauses, decided exactly by a small DPLL solver. Left: the fraction that are satisfiable. Right: the median number of search nodes. Slide the ratio m / n through 4.27, then raise n and watch the drop sharpen and the peak of work grow.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Variables n", min: 8, max: 24, step: 2, value: 20 },
        { k: "ratio", label: "Clauses per variable m / n", min: 2, max: 7, step: 0.05, value: 4.25, fmt: function (x) { return x.toFixed(2); } },
        { k: "trials", label: "Formulas per point", min: 10, max: 30, step: 5, value: 20 },
      ],
      buttons: [{ label: "New formulas", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var cv = curves(v.n, v.trials, s.seed), here = point(QB.rng(s.seed * 31 + v.n * 1000 + Math.round(v.ratio * 100)), v.n, v.ratio, v.trials);
        var top = Math.max(4, here[1]), i;
        for (i = 0; i < cv.w.length; i++) top = Math.max(top, cv.w[i]);
        s.out = [here[0], here[1], Math.round(v.ratio * v.n)];
        var a = g[0].axes({ x: [2, 7], y: [0, 1.05], title: "Fraction satisfiable, n = " + v.n, xlabel: "clauses per variable m / n", yfmt: function (y) { return Math.round(100 * y) + "%"; }, yticks: [0, 0.25, 0.5, 0.75, 1] });
        a.vline(4.27, { color: C.muted });
        a.line(GRID, cv.f, { color: C.spot }).dots(GRID, cv.f, { color: C.spot, r: 3 });
        a.vline(v.ratio, { color: C.idea }).dots([v.ratio], [here[0]], { color: C.idea, r: 5 });
        a.text(4.27, 1.0, "4.27", { color: C.muted, dx: 5 });
        var b = g[1].axes({ x: [2, 7], y: [0, top * 1.15], title: "Median DPLL nodes per formula", xlabel: "clauses per variable m / n" });
        b.vline(4.27, { color: C.muted });
        b.line(GRID, cv.w, { color: C.loss }).dots(GRID, cv.w, { color: C.loss, r: 3 });
        b.vline(v.ratio, { color: C.idea }).dots([v.ratio], [here[1]], { color: C.idea, r: 5 });
      },
      readout: function (v, s) {
        return [["clauses m", String(s.out[2])], ["satisfiable at this ratio", QB.pct(s.out[0], 0)], ["median nodes", fmt(s.out[1], 0)], ["assignments a truth table would try", String(Math.pow(2, v.n))]];
      },
      note: "Simulated data: uniform random 3-clauses, three distinct variables, fair signs. Blue: fraction satisfiable. Red: search nodes. Gold: your ratio, with its own batch of formulas. The grey line at 4.27 is the predicted limiting threshold; at these small n the drop is gradual and sits a little to its right.",
    });
  };

  // ---- Part 27: a cheating sum-check prover against the field size ---------------------------------------------
  W.sumcheckcheat = function (el) {
    var PR = [7, 11, 13, 17, 23, 31, 47, 61, 97, 127, 193, 257, 509, 1021, 2053, 4099, 8191];
    QB.widget(el, {
      title: "Sum-check: how often a false claim survives",
      sub: "A prover defends a false sum. Each round its polynomial must differ from the true one, and two different polynomials of degree d agree at no more than d of the p field points; if the verifier's random challenge lands on one of them the lie is repaired and the verifier accepts. Shrink the field until cheating usually works, then grow it until it almost never does.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Variables n (rounds)", min: 1, max: 16, step: 1, value: 4 },
        { k: "d", label: "Degree bound d", min: 1, max: 6, step: 1, value: 5 },
        { k: "pi", label: "Field size p", min: 0, max: 16, step: 1, value: 8, fmt: function (x) { return String(PR[x]); } },
      ],
      buttons: [{ label: "New runs", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var p = PR[v.pi], n = v.n, d = Math.min(v.d, p), r = QB.rng(s.seed * 97 + n * 7 + d * 131 + p), runs = 2000, i, k;
        var hit = [], caught = 0;
        for (k = 0; k <= n; k++) hit.push(0);
        for (i = 0; i < runs; i++) {
          for (k = 1; k <= n; k++) if (Math.floor(r() * p) < d) break; // the challenge is one of the d agreement points
          if (k > n) caught++; else hit[k]++;
        }
        var exact = 1 - Math.pow(1 - d / p, n), union = Math.min(1, n * d / p), meas = 1 - caught / runs;
        s.out = [meas, exact, union, p];
        var xs = [], ex = [], un = [];
        for (i = 0; i < PR.length; i++) { xs.push(PR[i]); ex.push(1 - Math.pow(1 - Math.min(d, PR[i]) / PR[i], n)); un.push(Math.min(1, n * d / PR[i])); }
        var a = g[0].axes({ x: [6, 10000], y: [0, 1.05], logx: true, title: "Chance the verifier accepts a false claim", xlabel: "field size p (log scale)", yfmt: function (y) { return Math.round(100 * y) + "%"; }, yticks: [0, 0.25, 0.5, 0.75, 1] });
        a.line(xs, un, { color: C.muted, dash: [4, 4], width: 1.2 }).line(xs, ex, { color: C.idea, width: 2 });
        a.vline(p, { color: C.idea, width: 1 });
        a.dots([p], [meas], { color: C.loss, r: 5 });
        a.legend([["1 − (1 − d/p)ⁿ", C.idea], ["union bound nd/p", C.muted], ["2,000 simulated runs", C.loss]], { pos: "tr" });
        var ks = [], hs = [], top = 0.02;
        for (k = 1; k <= n; k++) { ks.push(k); hs.push(hit[k] / runs); top = Math.max(top, hit[k] / runs); }
        top = Math.max(top, caught / runs);
        var b = g[1].axes({ x: [0.3, n + 1.7], y: [0, top * 1.2], title: "Where the 2,000 runs end", xlabel: "round in which the lie is repaired; last bar: caught", xticks: n <= 8 ? ks : [1, Math.round(n / 2), n], yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.bars(ks, hs, 0.8, { color: C.loss });
        b.bars([n + 1], [caught / runs], 0.8, { color: C.gain });
      },
      readout: function (v, s) {
        return [["false claim accepted", QB.pct(s.out[0])], ["theory", QB.pct(s.out[1])], ["union bound", QB.pct(s.out[2])], ["bits per field element", String(Math.ceil(Math.log(s.out[3]) / Math.LN2))]];
      },
      note: "Simulated data: the cheater of the film's experiment, whose error polynomial has exactly d roots in the field, against independent uniform challenges. Right panel: red bars are runs where a challenge repaired the lie (the verifier is fooled), the green bar the runs caught at the final check. The film's run is n = 4, d = 5, p = 97. Soundness costs only bits: each doubling of p adds one bit per message and halves the bound.",
    });
  };

  // ---- Part 28: one picture through a noisy channel, three ways ------------------------------------------------
  W.noisypicture = function (el) {
    var GLYPH = { C: ["01110", "10001", "10000", "10000", "10000", "10001", "01110"], S: ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
      "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"], "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"] };
    var COLS = 56, ROWS = 18, PIC = [], AW = [0, 0, 0, 0, 0, 0, 0, 0];
    (function () {
      var text = "CS28", x, y, k, gx, gy;
      for (y = 0; y < ROWS; y++) for (x = 0; x < COLS; x++) {
        k = Math.floor((x - 2) / 13); gx = Math.floor(((x - 2) % 13) / 2); gy = Math.floor((y - 2) / 2);
        PIC.push(x >= 2 && k >= 0 && k < 4 && gx < 5 && gy >= 0 && gy < 7 && GLYPH[text.charAt(k)][gy].charAt(gx) === "1" ? 1 : 0);
      }
      for (var e = 0; e < 128; e++) { var c = bits7(e), w = 0; for (k = 0; k < 7; k++) w += c[k]; var d = decode(c); AW[w] += (d[0] + d[1] + d[2] + d[3]) / 4; }
    })();
    function bits7(e) { var c = []; for (var i = 0; i < 7; i++) c.push((e >> i) & 1); return c; }
    function encode(d) { return [d[0] ^ d[1] ^ d[3], d[0] ^ d[2] ^ d[3], d[0], d[1] ^ d[2] ^ d[3], d[1], d[2], d[3]]; }
    function decode(c) { // the syndrome is the XOR of the positions holding a 1: the position of a single flip
      var s = 0, i; c = c.slice();
      for (i = 0; i < 7; i++) if (c[i]) s ^= i + 1;
      if (s) c[s - 1] ^= 1;
      return [c[2], c[4], c[5], c[6]];
    }
    function choose(n, k) { var r = 1; for (var i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }
    function repErr(n, p) { var s = 0; for (var j = (n + 1) / 2; j <= n; j++) s += choose(n, j) * Math.pow(p, j) * Math.pow(1 - p, n - j); return s; }
    function hamErr(p) { var s = 0; for (var w = 0; w <= 7; w++) s += AW[w] * Math.pow(p, w) * Math.pow(1 - p, 7 - w); return s; }
    function H2(p) { return p <= 0 || p >= 1 ? 0 : -(p * Math.log(p) + (1 - p) * Math.log(1 - p)) / Math.LN2; }
    QB.widget(el, {
      title: "One picture, one noisy channel, three ways to send it",
      sub: "A 56 by 18 picture goes through a channel that flips each bit with probability p: as it is, with every pixel repeated and voted on, and in blocks of Hamming(7,4). Raise p and watch each picture decay; raise the copies and the repetition picture cleans up while its rate falls. Past about p = 0.2 Hamming's code makes things worse than sending nothing extra.",
      panels: 2, height: 320,
      controls: [
        { k: "p", label: "Flip probability p", min: 0, max: 0.3, step: 0.005, value: 0.05, fmt: function (x) { return x.toFixed(3); } },
        { k: "n", label: "Copies in the repetition code", min: 1, max: 15, step: 2, value: 3 },
      ],
      buttons: [{ label: "New noise", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed * 13 + 5), p = v.p, n = v.n, N = COLS * ROWS, raw = [], rep = [], ham = [], i, j, votes, d, cw, out, e = [0, 0, 0];
        for (i = 0; i < N; i++) { raw.push(r() < p ? 1 - PIC[i] : PIC[i]); if (raw[i] !== PIC[i]) e[0]++; }
        for (i = 0; i < N; i++) { votes = 0; for (j = 0; j < n; j++) if (r() < p) votes++; rep.push(2 * votes > n ? 1 - PIC[i] : PIC[i]); if (rep[i] !== PIC[i]) e[1]++; }
        for (i = 0; i < N; i += 4) {
          d = [PIC[i], PIC[i + 1], PIC[i + 2], PIC[i + 3]]; cw = encode(d);
          for (j = 0; j < 7; j++) if (r() < p) cw[j] ^= 1;
          out = decode(cw);
          for (j = 0; j < 4; j++) { ham.push(out[j]); if (out[j] !== d[j]) e[2]++; }
        }
        s.out = { e: e, N: N, cap: 1 - H2(p) };
        var c = g.ctx, box = g[0].box, names = ["raw, rate 1", n + (n === 1 ? " copy" : " copies") + ", rate 1/" + n, "Hamming(7,4), rate 4/7"], cols = [C.cash, C.gain, C.idea];
        var slot = box.h / 3, cell = Math.max(2, Math.min(Math.floor((box.w - 24) / COLS), Math.floor((slot - 22) / ROWS))), x0 = box.x + Math.round((box.w - cell * COLS) / 2);
        [raw, rep, ham].forEach(function (im, k) {
          var y0 = Math.round(box.y + k * slot + 18), x, y;
          c.font = "600 12px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "bottom"; c.fillStyle = cols[k];
          c.fillText(names[k] + ": " + e[k] + " wrong", x0, y0 - 3);
          c.fillStyle = C.bg; c.fillRect(x0, y0, cell * COLS, cell * ROWS);
          for (y = 0; y < ROWS; y++) for (x = 0; x < COLS; x++) {
            var t = y * COLS + x;
            if (im[t] !== PIC[t]) c.fillStyle = C.loss; else if (im[t]) c.fillStyle = C.ink; else continue;
            c.fillRect(x0 + x * cell, y0 + y * cell, cell, cell);
          }
        });
        var ps = QB.linspace(0.001, 0.3, 80), a = g[1].axes({ x: [0, 0.3], y: [0.0001, 1], logy: true, title: "Bit error after decoding (exact)", xlabel: "flip probability p", yticks: [0.0001, 0.001, 0.01, 0.1, 1] });
        a.line(ps, ps, { color: C.cash, dash: [4, 4], width: 1.3 });
        a.line(ps, ps.map(function (q) { return repErr(n, q); }), { color: C.gain });
        a.line(ps, ps.map(hamErr), { color: C.idea });
        if (p > 0) a.vline(p, { color: C.ink, width: 1 });
        a.legend([["no code", C.cash], [n + " copies", C.gain], ["Hamming(7,4)", C.idea]], { pos: "br" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["pixels wrong: raw", o.e[0] + " of " + o.N], [v.n + " copies", String(o.e[1])], ["Hamming(7,4)", String(o.e[2])], ["capacity 1 − H(p)", fmt(o.cap, 2)]];
      },
      note: "Simulated data: independent flips, a fresh channel for each scheme. White pixels arrive right, red pixels arrive wrong. The curves are exact: the binomial tail for the vote, and all 128 error patterns for Hamming(7,4). Shannon's capacity is the rate that some long code could reach with almost no errors at this p; neither of these short codes comes close.",
    });
  };

  // ---- Part 29: AES-128 in the browser, and one flipped bit ------------------------------------------------------
  W.aesavalanche = function (el) {
    var SBOX = [], i;
    (function () { // the S-box: inversion in GF(2^8) mod x^8 + x^4 + x^3 + x + 1, then the affine map
      var exp = [], log = [], x = 1, k, b, v;
      for (k = 0; k < 255; k++) { exp[k] = x; log[x] = k; x ^= (x << 1) ^ (x & 0x80 ? 0x11b : 0); x &= 0x1ff; if (x & 0x100) x ^= 0x11b; } // powers of 3
      for (k = 0; k < 256; k++) {
        b = k ? exp[(255 - log[k]) % 255] : 0; v = b;
        for (var j = 1; j <= 4; j++) v ^= ((b << j) | (b >> (8 - j))) & 0xff;
        SBOX[k] = v ^ 0x63;
      }
    })();
    function xt(a) { return ((a << 1) ^ (a & 0x80 ? 0x1b : 0)) & 0xff; }
    function expand(key) { // 11 round keys of 16 bytes
      var w = key.slice(), rc = 1, k, t;
      for (k = 16; k < 176; k += 4) {
        t = w.slice(k - 4, k);
        if (k % 16 === 0) { t = [SBOX[t[1]] ^ rc, SBOX[t[2]], SBOX[t[3]], SBOX[t[0]]]; rc = xt(rc); }
        for (var j = 0; j < 4; j++) w.push(w[k - 16 + j] ^ t[j]);
      }
      return w;
    }
    function states(block, w) { // the state after AddRoundKey of rounds 0..10
      var s = [], out = [], r, c, j, t, a;
      for (j = 0; j < 16; j++) s.push(block[j] ^ w[j]);
      out.push(s.slice());
      for (r = 1; r <= 10; r++) {
        t = [];
        for (j = 0; j < 16; j++) t[j] = SBOX[s[(j + 4 * (j % 4)) % 16]]; // SubBytes and ShiftRows (column-major state)
        if (r < 10) for (c = 0; c < 16; c += 4) {
          a = t.slice(c, c + 4);
          for (j = 0; j < 4; j++) t[c + j] = xt(a[j]) ^ xt(a[(j + 1) % 4]) ^ a[(j + 1) % 4] ^ a[(j + 2) % 4] ^ a[(j + 3) % 4];
        }
        for (j = 0; j < 16; j++) s[j] = t[j] ^ w[16 * r + j];
        out.push(s.slice());
      }
      return out;
    }
    var FIPS = (function () { var k = [], p = []; for (i = 0; i < 16; i++) { k.push(i); p.push(17 * i); } return states(p, expand(k))[10]; })();
    var okVector = FIPS[0] === 0x69 && FIPS[1] === 0xc4 && FIPS[15] === 0x5a;
    QB.widget(el, {
      title: "The avalanche: one flipped bit through the rounds of AES",
      sub: "Two blocks that differ in a single bit are encrypted with the same random key. The grid shows the 128 bits of the state as 16 bytes: red where the two encryptions differ. Step through the rounds: one byte, then one column, then everything. Move the flipped bit and draw a new key; after two rounds the count always sits near 64.",
      panels: 2, height: 300,
      controls: [
        { k: "r", label: "Rounds completed", min: 0, max: 10, step: 1, value: 1 },
        { k: "bit", label: "Flipped input bit", min: 0, max: 127, step: 1, value: 0 },
      ],
      buttons: [{ label: "New key and block", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed * 101 + 7), key = [], p = [], q, j, k, n;
        for (j = 0; j < 16; j++) { key.push(Math.floor(r() * 256)); p.push(Math.floor(r() * 256)); }
        q = p.slice(); q[v.bit >> 3] ^= 1 << (v.bit & 7);
        var w = expand(key), A = states(p, w), B = states(q, w), counts = [], bytes = 0;
        for (k = 0; k <= 10; k++) { n = 0; for (j = 0; j < 16; j++) { var d = A[k][j] ^ B[k][j]; while (d) { n += d & 1; d >>= 1; } } counts.push(n); }
        for (j = 0; j < 16; j++) if (A[v.r][j] !== B[v.r][j]) bytes++;
        s.out = [counts[v.r], bytes, okVector];
        var c = g.ctx, box = g[0].box, size = Math.min(box.w - 40, box.h - 52), cell = Math.floor(size / 4), x0 = box.x + Math.round((box.w - 4 * cell) / 2), y0 = box.y + 34;
        c.font = "600 12.5px system-ui, sans-serif"; c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("State after round " + v.r + ": " + counts[v.r] + " of 128 bits differ", box.x + 14, box.y + 8);
        var bw = Math.floor((cell - 8) / 4), bh = Math.floor((cell - 8) / 2);
        for (j = 0; j < 16; j++) { // byte j sits in row j % 4, column j / 4, as in the standard
          var bx = x0 + Math.floor(j / 4) * cell, by = y0 + (j % 4) * cell, df = A[v.r][j] ^ B[v.r][j];
          c.fillStyle = df ? "rgba(248,113,113,0.13)" : C.bg; c.fillRect(bx + 1, by + 1, cell - 2, cell - 2);
          c.strokeStyle = C.line; c.strokeRect(bx + 0.5, by + 0.5, cell - 1, cell - 1);
          for (k = 0; k < 8; k++) {
            c.fillStyle = (df >> (7 - k)) & 1 ? C.loss : C.line;
            c.fillRect(bx + 4 + (k % 4) * bw + 1, by + 4 + Math.floor(k / 4) * bh + 1, bw - 2, bh - 2);
          }
        }
        var rs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        var a = g[1].axes({ x: [-0.6, 10.6], y: [0, 100], title: "Bits that differ after each round", xlabel: "rounds completed", xticks: rs });
        a.area([-0.6, 10.6], [64 + 11.3, 64 + 11.3], 64 - 11.3, { color: C.idea, alpha: 0.12 });
        a.hline(64, { color: C.idea });
        a.bars(rs, counts, 0.7, { color: function (m) { return m === v.r ? C.loss : C.spot; } });
        a.text(10.4, 92, "64 ± 2 s.d. of Binomial(128, ½)", { align: "right", color: C.idea });
      },
      readout: function (v, s) {
        return [["bits differing", s.out[0] + " of 128"], ["bytes touched", s.out[1] + " of 16"], ["unrelated blocks would differ in", "64 ± 5.7"], ["FIPS-197 check", s.out[2] ? "passes" : "FAILS"]];
      },
      note: "Real AES-128, computed in your browser and checked on load against the FIPS-197 example; the key and block are random. SubBytes confines a change to its byte, ShiftRows and MixColumns spread it over a column in round 1 and over all four columns in round 2. A teaching implementation: never use it to protect anything.",
    });
  };

  // ---- Part 30: an elliptic curve over GF(97), and the multiples of a point ------------------------------------
  W.curvemultiples = function (el) {
    var PR = 97, INV = [0], cache = {}, i;
    for (i = 1; i < PR; i++) { var x = 1; for (var e = 0; e < PR - 2; e++) x = x * i % PR; INV.push(x); } // Fermat inverses
    function mod(v) { return ((v % PR) + PR) % PR; }
    function add(P, Q, a) { // chord and tangent; null is the point at infinity
      if (!P) return Q; if (!Q) return P;
      if (P[0] === Q[0] && mod(P[1] + Q[1]) === 0) return null;
      var lam = P[0] === Q[0] ? mod((3 * P[0] * P[0] + a) * INV[mod(2 * P[1])]) : mod((Q[1] - P[1]) * INV[mod(Q[0] - P[0])]);
      var x3 = mod(lam * lam - P[0] - Q[0]);
      return [x3, mod(lam * (P[0] - x3) - P[1])];
    }
    function curve(a, b) {
      var key = a + "," + b;
      if (cache[key]) return cache[key];
      var sq = {}, pts = [], y, xx, k, best = null, c = { a: a, b: b, singular: mod(4 * a * a * a + 27 * b * b) === 0 };
      for (y = 0; y < PR; y++) { k = y * y % PR; (sq[k] = sq[k] || []).push(y); }
      for (xx = 0; xx < PR; xx++) { var ys = sq[mod(xx * xx * xx + a * xx + b)] || []; for (k = 0; k < ys.length; k++) pts.push([xx, ys[k]]); }
      c.pts = pts; c.mult = [];
      if (!c.singular) {
        for (k = 0; k < pts.length; k++) { // the point of largest order becomes G
          var n = 1, Q = pts[k];
          while (Q && n < 400) { Q = add(Q, pts[k], a); n++; }
          if (!best || n > best[1]) best = [pts[k], n];
        }
        var R = best[0];
        for (k = 1; k <= best[1]; k++) { c.mult.push(R); R = add(R, best[0], a); } // G, 2G, ..., (order)G = infinity (null)
        c.order = best[1];
      } else c.order = 1;
      cache = {}; cache[key] = c;
      return c;
    }
    QB.widget(el, {
      title: "Points on a curve mod 97, and the multiples of one of them",
      sub: "Left: every solution of y² = x³ + ax + b modulo 97, with the base point G (green) and its multiple kG (gold); the last few hops are drawn. Right: the x-coordinate of jG against j. Slide k: the multiples jump with no visible order, which is why recovering k from kG is hard. Change a and b: the group changes size, and at a = 0, b = 0 the curve is singular and there is no group at all.",
      panels: 2, height: 320,
      controls: [
        { k: "k", label: "Scalar k", min: 1, max: 120, step: 1, value: 7 },
        { k: "a", label: "Coefficient a", min: 0, max: 12, step: 1, value: 2 },
        { k: "b", label: "Coefficient b", min: 0, max: 12, step: 1, value: 3 },
      ],
      draw: function (g, v, s) {
        var c = curve(v.a, v.b), n = c.order, k = c.singular ? 0 : ((v.k - 1) % n) + 1, P = c.singular ? null : c.mult[k - 1], j;
        s.out = { N: c.pts.length + 1, n: n, k: k, P: P, singular: c.singular };
        var a = g[0].axes({ x: [-3, 99], y: [-3, 99], title: "y² = x³ + " + v.a + "x + " + v.b + "  (mod 97)", xlabel: "x", xticks: [0, 24, 48, 72, 96], yticks: [0, 24, 48, 72, 96] });
        a.hline(48.5, { color: C.line });
        a.dots(c.pts.map(function (p) { return p[0]; }), c.pts.map(function (p) { return p[1]; }), { color: c.singular ? C.loss : C.spot, r: 2.2, alpha: 0.8 });
        var b = g[1].axes({ x: [0, 121], y: [-3, 99], title: "x-coordinate of jG", xlabel: "j", xticks: [1, 30, 60, 90, 120] });
        if (c.singular) {
          a.text(48, 50, "singular: 4a³ + 27b² = 0", { align: "center", color: C.loss, bg: true });
          b.text(60, 50, "no group, no multiples", { align: "center", color: C.loss });
          return;
        }
        for (j = Math.max(1, k - 5); j < k; j++) { // the last hops, fading
          var A = c.mult[j - 1], B = c.mult[j];
          if (A && B) a.line([A[0], B[0]], [A[1], B[1]], { color: C.idea, width: 1.2, alpha: 0.25 + 0.15 * (j - (k - 6)) });
        }
        a.dots([c.mult[0][0]], [c.mult[0][1]], { color: C.gain, r: 5 });
        a.text(c.mult[0][0], c.mult[0][1], "G", { color: C.gain, dx: 8, dy: -8, bold: true });
        if (P) { a.dots([P[0]], [P[1]], { color: C.idea, r: 5 }); a.text(P[0], P[1], k + "G", { color: C.idea, dx: 8, dy: 8, bold: true }); }
        else a.text(48, 92, k + "G is the point at infinity", { align: "center", color: C.idea, bg: true });
        var js = [], xs = [];
        for (j = 1; j < n; j++) { js.push(j); xs.push(c.mult[j - 1][0]); }
        b.dots(js, xs, { color: C.spot, r: 2.2, alpha: 0.85 });
        b.vline(n, { color: C.muted });
        b.text(n, 94, "order " + n, { color: C.muted, dx: n > 85 ? -6 : 6, align: n > 85 ? "right" : "left" });
        if (P) b.dots([k], [P[0]], { color: C.idea, r: 5 });
      },
      readout: function (v, s) {
        var o = s.out;
        if (o.singular) return [["curve", "singular"], ["points", String(o.N - 1)], ["group", "none"]];
        return [["group size (with infinity)", String(o.N)], ["Hasse's range", "79 to 117"], ["order of G", String(o.n)], ["k mod order", String(o.k % o.n)], [o.k + "G", o.P ? "(" + o.P[0] + ", " + o.P[1] + ")" : "infinity"]];
      },
      note: "Exact arithmetic modulo 97, no simulation. The film's toy curve is a = 2, b = 3: 99 points and the point at infinity, with a point of order 50. Blue: the points; green: G, the point of largest order; gold: kG. A brute-force search for k takes at most the order of G here; on P-256 the order has 78 digits and the best known attack takes about its square root.",
    });
  };
})();
