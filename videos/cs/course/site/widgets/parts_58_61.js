// Interactives for Act XI, The Research Frontier, concluded (Parts 58-61).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(c, str, x, y, o) { // one line of canvas text
    o = o || {};
    c.save(); c.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    c.fillStyle = o.color || C.ink; c.textAlign = o.align || "left"; c.textBaseline = o.base || "middle";
    c.fillText(str, x, y); c.restore();
  }

  // ---- Part 58: the Kleene chain of factorial, and the run of fact n by small steps -------------------------
  W.kleenefactorial = function (el) {
    var FACT = ["fix", "fact", "n", ["if", ["op", "=", ["var", "n"], ["int", 0]], ["int", 1],
      ["op", "*", ["var", "n"], ["app", ["var", "fact"], ["op", "-", ["var", "n"], ["int", 1]]]]]];
    var isValue = function (t) { return t[0] === "int" || t[0] === "bool" || t[0] === "fix"; };
    var subst = function (t, x, v) { // v is closed, so no capture can happen
      var k = t[0];
      if (k === "int" || k === "bool") return t;
      if (k === "var") return t[1] === x ? v : t;
      if (k === "fix") return (t[1] === x || t[2] === x) ? t : ["fix", t[1], t[2], subst(t[3], x, v)];
      if (k === "app") return ["app", subst(t[1], x, v), subst(t[2], x, v)];
      if (k === "if") return ["if", subst(t[1], x, v), subst(t[2], x, v), subst(t[3], x, v)];
      return ["op", t[1], subst(t[2], x, v), subst(t[3], x, v)];
    };
    var step = function (t) { // one small step, call by value, left to right
      var k = t[0], s;
      if (k === "app") {
        if (!isValue(t[1])) { s = step(t[1]); return s ? ["app", s, t[2]] : null; }
        if (!isValue(t[2])) { s = step(t[2]); return s ? ["app", t[1], s] : null; }
        if (t[1][0] === "fix") return subst(subst(t[1][3], t[1][1], t[1]), t[1][2], t[2]);
        return null;
      }
      if (k === "if") {
        if (!isValue(t[1])) { s = step(t[1]); return s ? ["if", s, t[2], t[3]] : null; }
        return t[1][1] ? t[2] : t[3];
      }
      if (k === "op") {
        if (!isValue(t[2])) { s = step(t[2]); return s ? ["op", t[1], s, t[3]] : null; }
        if (!isValue(t[3])) { s = step(t[3]); return s ? ["op", t[1], t[2], s] : null; }
        var a = t[2][1], b = t[3][1];
        if (t[1] === "=") return ["bool", a === b];
        return ["int", t[1] === "*" ? a * b : t[1] === "-" ? a - b : a + b];
      }
      return null;
    };
    var pending = function (t) { // the multiplications waiting in the term: Part 11's call stack, written out
      if (t[0] === "op") return (t[1] === "*" && t[3][0] !== "int" ? 1 : 0) + pending(t[2]) + pending(t[3]);
      if (t[0] === "app") return pending(t[2]);
      return 0;
    };
    var size = function (t) {
      var k = t[0];
      if (k === "int" || k === "bool" || k === "var") return 1;
      if (k === "fix") return 1 + size(t[3]);
      if (k === "app") return 1 + size(t[1]) + size(t[2]);
      if (k === "if") return 1 + size(t[1]) + size(t[2]) + size(t[3]);
      return 1 + size(t[2]) + size(t[3]);
    };
    var CAP = 48, N0 = -2, N1 = 6, KMAX = 8;
    var fact = function (n) { var f = 1; for (var i = 2; i <= n; i++) f *= i; return f; };
    QB.widget(el, {
      title: "Factorial twice: as a limit of partial functions, and as a run of steps",
      sub: "Left: the Kleene chain. Row k is F applied k times to the function that is defined nowhere; it knows factorial on 0 to k − 1 and nothing else. Right: fact n rewritten by the small-step rules. Raise n and the run needs a higher row of the chain; make n negative and the run never ends, which is why the meaning is the least fixed point.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Iterate k of the chain", min: 0, max: KMAX, step: 1, value: 3 },
        { k: "n", label: "Input n", min: N0, max: N1, step: 1, value: 3, fmt: function (x) { return fmt(x, 0); } },
      ],
      draw: function (g, v, s) {
        var c = g.ctx, bx = g[0].box, n = v.n, k = v.k, i, j;
        // the run of fact n
        var t = ["app", FACT, ["int", n]], sizes = [size(t)], stack = [pending(t)], steps = 0, done = false;
        while (steps < CAP) {
          if (isValue(t)) { done = true; break; }
          t = step(t); steps++; sizes.push(size(t)); stack.push(pending(t));
        }
        if (isValue(t)) done = true;
        var defined = n >= 0 && n < k;
        s.out = { defined: defined, value: defined ? fact(n) : 0, steps: steps, done: done, result: done ? t[1] : 0, peak: Math.max.apply(null, stack), need: n + 1 };
        // the chain as a table
        var cols = N1 - N0 + 1, left = bx.x + 46, top = bx.y + 46, cw = (bx.w - 46 - 10) / cols, rh = Math.min(22, (bx.h - 46 - 26) / (KMAX + 1));
        label(c, "The chain F^k(⊥): defined cells hold n!", bx.x + 10, bx.y + 13, { bold: true, size: 12.5 });
        label(c, "n =", bx.x + 10, bx.y + 34, { color: C.muted, size: 11 });
        for (j = 0; j < cols; j++) label(c, fmt(N0 + j, 0), left + (j + 0.5) * cw, bx.y + 34, { color: N0 + j === n ? C.idea : C.muted, align: "center", size: 11, bold: N0 + j === n });
        for (i = 0; i <= KMAX; i++) {
          var y = top + i * rh, on = i <= k;
          label(c, "k = " + i, bx.x + 10, y + rh / 2, { color: i === k ? C.idea : C.muted, size: 11, bold: i === k });
          for (j = 0; j < cols; j++) {
            var m = N0 + j, def = m >= 0 && m < i;
            c.globalAlpha = on ? 1 : 0.28;
            c.fillStyle = def ? "rgba(74,222,128,0.22)" : "rgba(139,152,169,0.10)";
            c.fillRect(left + j * cw + 1, y + 1, cw - 2, rh - 2);
            label(c, def ? String(fact(m)) : "⊥", left + (j + 0.5) * cw, y + rh / 2, { color: def ? C.gain : C.muted, align: "center", size: 11 });
            c.globalAlpha = 1;
          }
        }
        c.strokeStyle = C.idea; c.lineWidth = 2;
        c.strokeRect(left + (n - N0) * cw + 1, top + k * rh + 1, cw - 2, rh - 2);
        label(c, "green: defined   ⊥: no answer yet   gold: row k, input n", bx.x + 10, bx.y + bx.h - 12, { color: C.muted, size: 11 });
        // the run
        var xs = [], ymax = Math.max(4, s.out.peak + 1);
        for (i = 0; i < stack.length; i++) xs.push(i);
        var a = g[1].axes({ x: [0, Math.max(10, steps)], y: [0, ymax], title: "fact " + fmt(n, 0) + " by small steps: multiplications waiting", xlabel: "small steps taken", ny: 4 });
        a.area(xs, stack, 0, { color: done ? C.spot : C.loss, alpha: 0.18 });
        a.line(xs, stack, { color: done ? C.spot : C.loss, width: 2 });
        if (done) {
          a.dots([steps], [0], { color: C.gain, r: 5 });
          a.text(Math.max(10, steps), ymax, "value " + s.out.result + " after " + steps + " steps", { align: "right", dx: -8, dy: 14, color: C.gain, bg: true });
        } else {
          a.text(0, ymax, "no value: the stack grows for ever", { dx: 8, dy: 14, color: C.loss, bg: true });
        }
      },
      readout: function (v, s) {
        var o = s.out;
        return [["F^k(⊥) at n", o.defined ? String(o.value) : "⊥ (no answer)"],
          ["first row that answers", v.n >= 0 ? "k = " + o.need : "none"],
          ["small steps to a value", o.done ? String(o.steps) : "never (stopped at " + o.steps + ")"],
          ["deepest stack", o.done ? String(o.peak) : "unbounded"]];
      },
      note: "Computed in the browser by the part's own rules: fix f n → if n = 0 then 1 else n × f (n − 1), call by value, left to right. Evaluating fact n unrolls the recursion n + 1 times, and row k = n + 1 is the first that is defined at n. On negative inputs every row is ⊥ and the run is cut off after 48 steps.",
    });
  };

  // ---- Part 59: Cole and Vishkin's colouring of an oriented ring --------------------------------------------
  W.colevishkinring = function (el) {
    var PAL = [C.spot, C.idea, C.gain, C.implied, C.q, C.loss];
    var logStar = function (n) { var k = 0; while (n > 1) { n = Math.log(n) / Math.LN2; k++; } return k; };
    var distinct = function (a) { var seen = {}, d = 0; for (var i = 0; i < a.length; i++) if (!seen[a[i]]) { seen[a[i]] = 1; d++; } return d; };
    var colourOf = function (x) { return x < 6 ? PAL[x] : "hsl(" + ((x * 137.5) % 360).toFixed(0) + ",45%,52%)"; };
    var simulate = function (n, bits, anon, seed) {
      var r = QB.rng(seed * 7919 + n * 31 + bits), c = [], used = {}, v, x, i;
      for (v = 0; v < n; v++) {
        if (anon) { c.push(1); continue; }
        do { x = Math.floor(r() * Math.pow(2, bits)); } while (used[x]);
        used[x] = 1; c.push(x);
      }
      var hist = [c.slice()], bound = [Math.pow(2, bits)], b = bits, guard = 0;
      while (Math.max.apply(null, c) >= 6 && guard++ < 12) { // the bit-position step, every node at once
        var nxt = [];
        for (v = 0; v < n; v++) {
          var d = c[v] ^ c[(v + 1) % n];
          if (d === 0) { nxt.push(0); continue; } // identical neighbours: nothing to tell them apart
          i = 0; while (!((d >> i) & 1)) i++;
          nxt.push(2 * i + ((c[v] >> i) & 1));
        }
        c = nxt; hist.push(c.slice()); bound.push(2 * b); b = Math.ceil(Math.log(2 * b) / Math.LN2 - 1e-9);
      }
      var cv = hist.length - 1;
      for (var col = 5; col >= 3; col--) { // remove colours 5, 4 and 3: their nodes are never neighbours
        var out = c.slice();
        for (v = 0; v < n; v++) if (c[v] === col) {
          var p = out[(v + n - 1) % n], q = out[(v + 1) % n];
          out[v] = (p !== 0 && q !== 0) ? 0 : (p !== 1 && q !== 1) ? 1 : 2;
        }
        c = out; hist.push(c.slice()); bound.push(col);
      }
      return { hist: hist, bound: bound, cv: cv };
    };
    QB.widget(el, {
      title: "Three colours on a ring, in about log* n rounds",
      sub: "Each node knows its own identifier and its successor's. In a round it finds the lowest bit where the two differ, at position i, and takes the colour 2i plus its own bit there. Step through the rounds: identifiers of b bits shrink to about log b bits, then three clean-up rounds leave colours 0, 1 and 2. Then make every identifier equal: with nothing to tell neighbours apart, the ring cannot be coloured at all.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Nodes on the ring", min: 6, max: 40, step: 1, value: 24 },
        { k: "bits", label: "Bits in an identifier", min: 6, max: 20, step: 1, value: 20 },
        { k: "r", label: "Round shown", min: 0, max: 9, step: 1, value: 1 },
        { k: "anon", label: "Identifiers", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "all equal" : "distinct"; } },
      ],
      buttons: [{ label: "New identifiers", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var sim = simulate(v.n, v.bits, v.anon, s.seed), total = sim.hist.length - 1, r = Math.min(v.r, total), col = sim.hist[r], n = v.n, i;
        var good = 0; for (i = 0; i < n; i++) if (col[i] !== col[(i + 1) % n]) good++;
        var counts = sim.hist.map(distinct), rounds = sim.hist.map(function (_, k) { return k; });
        s.out = { r: r, total: total, used: counts[r], good: good, n: n, ls: logStar(n), cv: sim.cv, max: Math.max.apply(null, col) };
        var c = g.ctx, bx = g[0].box, cx = bx.x + bx.w / 2, cy = bx.y + 24 + (bx.h - 50) / 2, R = Math.min(bx.w, bx.h - 50) / 2 - 16;
        var rad = Math.max(4, Math.min(12, Math.PI * R / n * 0.72));
        label(c, "Round " + r + " of " + total + ": " + counts[r] + (counts[r] === 1 ? " colour" : " colours") + " in use", bx.x + 10, bx.y + 13, { bold: true, size: 12.5 });
        var pos = function (k) { var a = -Math.PI / 2 + 2 * Math.PI * k / n; return [cx + R * Math.cos(a), cy + R * Math.sin(a)]; };
        for (i = 0; i < n; i++) {
          var p = pos(i), q = pos((i + 1) % n), clash = col[i] === col[(i + 1) % n];
          c.strokeStyle = clash ? C.loss : "#3a475c"; c.lineWidth = clash ? 3 : 1.5;
          c.beginPath(); c.moveTo(p[0], p[1]); c.lineTo(q[0], q[1]); c.stroke();
        }
        for (i = 0; i < n; i++) {
          var o = pos(i);
          c.fillStyle = colourOf(col[i]); c.beginPath(); c.arc(o[0], o[1], rad, 0, 6.2832); c.fill();
          if (rad >= 8 && col[i] < 100) label(c, String(col[i]), o[0], o[1] + 0.5, { align: "center", size: 11, color: "#0e1117", bold: true });
        }
        label(c, s.out.max < 6 ? "colour = the number on the node" : "one hue per colour still in use", cx, cy - 8, { align: "center", color: C.muted, size: 11 });
        label(c, "red edge: neighbours agree", cx, cy + 8, { align: "center", color: C.muted, size: 11 });
        label(c, "the successor of a node is the next one clockwise", bx.x + 10, bx.y + bx.h - 12, { color: C.muted, size: 11 });
        var a = g[1].axes({ x: [0, Math.max(total, 4)], y: [1, Math.pow(2, v.bits) * 2], logy: true, title: "Colours in use after each round", xlabel: "round", nx: 6 });
        a.hline(3, { color: C.gain });
        a.line(rounds, sim.bound, { color: C.muted, dash: [5, 4], width: 1.4 });
        a.line(rounds, counts, { color: C.spot, width: 2 }).dots(rounds, counts, { color: C.spot, r: 3 });
        a.vline(r, { color: C.idea });
        a.legend([["colours in use", C.spot], ["the most the rule allows", C.muted], ["three", C.gain]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["rounds used", String(o.total)], ["log* n", String(o.ls)], ["colours at round " + o.r, String(o.used)],
          ["edges with two different colours", o.good + " of " + o.n]];
      },
      note: "Simulated identifiers, drawn at random without repeats. After a bit-position round b-bit colours are below 2b, so the dashed bound falls from 2^b to 2b, then to twice the bits of that, until colours are below 6; rounds 5, 4, 3 of the clean-up each remove one colour. Linial's theorem says no algorithm can beat about half of log* n rounds. With equal identifiers every node computes the same colour in every round.",
    });
  };

  // ---- Part 60: a matrix product crossing a systolic array ---------------------------------------------------
  W.systolicwave = function (el) {
    QB.widget(el, {
      title: "A matrix product as a diagonal wave",
      sub: "An N by N grid of multiply-add cells computes C = AB. Rows of A enter from the west and columns of B from the north, each lane one cycle behind the last, so A[i][k] and B[k][j] meet in cell (i, j) at cycle i + j + k. Step the cycle and watch the wave cross; then compare how much of the grid one product keeps busy with a long stream of rows through stationary weights.",
      panels: 2, height: 310,
      controls: [
        { k: "N", label: "Grid size N", min: 2, max: 16, step: 1, value: 4 },
        { k: "t", label: "Cycle", min: 0, max: 46, step: 1, value: 4 },
        { k: "m", label: "Rows streamed past stationary weights", min: 1, max: 32, step: 1, value: 16, fmt: function (x) { return "M = " + x + "N"; } },
      ],
      draw: function (g, v, s) {
        var N = v.N, T = 3 * N - 2, t = Math.min(v.t, T), c = g.ctx, bx = g[0].box, i, j, busy = 0, done = 0;
        var cell = Math.min((bx.w - 40) / N, (bx.h - 78) / N), x0 = bx.x + (bx.w - cell * N) / 2, y0 = bx.y + 48;
        for (i = 0; i < N; i++) for (j = 0; j < N; j++) {
          var k = t - i - j, state = k >= N ? 2 : k >= 0 ? 1 : 0;
          if (state === 1) busy++; if (state === 2) done++;
          c.fillStyle = state === 1 ? C.idea : state === 2 ? "rgba(74,222,128,0.30)" : "rgba(139,152,169,0.13)";
          c.fillRect(x0 + j * cell + 1, y0 + i * cell + 1, cell - 2, cell - 2);
          if (state === 1 && cell >= 17) label(c, String(k), x0 + (j + 0.5) * cell, y0 + (i + 0.5) * cell + 0.5, { align: "center", size: 11, color: "#0e1117", bold: true });
        }
        label(c, t < T ? "Cycle " + t + ": " + busy + " of " + N * N + " cells multiply and add" : "Finished: " + T + " cycles, " + N * N * N + " multiply-adds", bx.x + 10, bx.y + 13, { bold: true, size: 12.5 });
        label(c, "A enters from the west, B from the north", bx.x + 10, bx.y + 33, { color: C.muted, size: 11 });
        label(c, "gold: busy on term k   green: sum complete   grey: waiting", bx.x + 10, bx.y + bx.h - 12, { color: C.muted, size: 11 });
        var os = N / (3 * N - 2), M = v.m * N, ws = M / (M + 3 * N - 2);
        s.out = { T: T, t: t, busy: busy, cells: N * N, os: os, ws: ws, M: M };
        var ns = [], cu = [], cw = [];
        for (i = 2; i <= 64; i++) { ns.push(i); cu.push(i / (3 * i - 2)); cw.push(v.m * i / (v.m * i + 3 * i - 2)); }
        var a = g[1].axes({ x: [2, 64], y: [0, 1], title: "Share of cell-cycles doing work", xlabel: "grid size N", xticks: [2, 16, 32, 48, 64], yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.hline(1 / 3, { color: C.muted });
        a.line(ns, cw, { color: C.gain, width: 2 }).line(ns, cu, { color: C.spot, width: 2 });
        a.vline(N, { color: C.idea });
        a.dots([N], [os], { color: C.spot, r: 4.5 }).dots([N], [ws], { color: C.gain, r: 4.5 });
        a.text(64, 1 / 3, "one third", { align: "right", dx: -6, dy: -9, color: C.muted });
        a.legend([["a stream of M rows, weights stationary", C.gain], ["one product, outputs stationary", C.spot]], { pos: "br" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["cycles for one product, 3N − 2", String(o.T)], ["busy at cycle " + o.t, o.busy + " of " + o.cells],
          ["one product uses", QB.pct(o.os)], ["a stream of " + o.M + " rows uses", QB.pct(o.ws)]];
      },
      note: "Exact counts, no simulation: a cell is busy at cycle t when 0 ≤ t − i − j < N. One product keeps N/(3N − 2) of the cell-cycles busy, which falls to a third; a weight-stationary grid that loads its weights in N cycles and then streams M rows keeps M/(M + 3N − 2) busy, which rises to one as the stream grows.",
    });
  };

  // ---- Part 61: how far medians spread when nothing differs --------------------------------------------------
  W.noiseonlyspread = function (el) {
    var median = function (a) { var b = a.slice().sort(function (x, y) { return x - y; }), m = b.length >> 1; return b.length % 2 ? b[m] : 0.5 * (b[m - 1] + b[m]); };
    var experiment = function (K, r, sd, eff, rnd, keep) {
      var med = [], runs = [], i, j;
      for (i = 0; i < K; i++) {
        var row = [];
        for (j = 0; j < r; j++) row.push(Math.max(0.05, (1 + sd * rnd.normal()) * (i === K - 1 ? 1 + eff : 1)));
        med.push(median(row)); if (keep) runs.push(row);
      }
      var lo = Math.min.apply(null, med), hi = Math.max.apply(null, med);
      return { med: med, runs: runs, lo: lo, hi: hi, spread: (hi - lo) / lo };
    };
    QB.widget(el, {
      title: "Is the spread an effect, or only noise?",
      sub: "One program is timed under K settings, r runs each, and the medians are compared: the slowest setting against the fastest looks like a speedup. The right panel repeats the whole experiment with no difference between the settings at all. Raise the number of settings and the noise-only spread grows; then give the last setting a real effect and see how large it must be to leave the noise.",
      panels: 2, height: 300,
      controls: [
        { k: "K", label: "Settings compared", min: 2, max: 40, step: 1, value: 33 },
        { k: "r", label: "Runs per setting", min: 1, max: 25, step: 1, value: 5 },
        { k: "sd", label: "Run-to-run noise (sd)", min: 0.5, max: 8, step: 0.5, value: 4, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "eff", label: "Real slowdown of the last setting", min: 0, max: 15, step: 0.5, value: 0, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      buttons: [{ label: "New runs", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var K = v.K, r = v.r, sd = v.sd / 100, eff = v.eff / 100, i, j;
        var e = experiment(K, r, sd, eff, QB.rng(s.seed * 101 + 7), true);
        var sims = Math.max(80, Math.min(400, Math.floor(60000 / (K * r)))), rn = QB.rng(s.seed * 101 + 8), null_ = [], above = 0;
        for (i = 0; i < sims; i++) { var z = experiment(K, r, sd, 0, rn, false).spread; null_.push(z); if (z >= e.spread) above++; }
        s.out = { spread: e.spread, typical: median(null_), p: above / sims, sims: sims };
        var ylo = 1 - 3.6 * sd, yhi = (1 + eff) * (1 + 3.6 * sd), xs = [], ys = [], ks = [];
        for (i = 0; i < K; i++) { ks.push(i + 1); for (j = 0; j < r; j++) { xs.push(i + 1); ys.push(e.runs[i][j]); } }
        var a = g[0].axes({ x: [0, K + 1], y: [ylo, yhi], title: "One experiment: " + K + " settings, " + r + (r === 1 ? " run each" : " runs each"), xlabel: "setting", nx: 5, yfmt: function (y) { return y.toFixed(2); } });
        a.hline(e.lo, { color: C.muted }).hline(e.hi, { color: C.muted });
        a.dots(xs, ys, { color: C.spot, r: 1.8, alpha: 0.45 });
        a.dots(ks, e.med, { color: function (q) { return eff > 0 && q === K - 1 ? C.idea : C.spot; }, r: 4 });
        a.legend(eff > 0 ? [["median of a setting", C.spot], ["the setting that really is slower", C.idea], ["fastest and slowest median", C.muted]] : [["median of a setting", C.spot], ["fastest and slowest median", C.muted]], { pos: "tl" });
        var top = Math.max(Math.max.apply(null, null_), e.spread) * 1.08 + 1e-6, nb = 24, h = QB.hist(null_, 0, top, nb), mids = [], hmax = 1;
        for (i = 0; i < nb; i++) { mids.push((i + 0.5) * top / nb); hmax = Math.max(hmax, h[i]); }
        var b = g[1].axes({ x: [0, top], y: [0, hmax * 1.25], title: "No effect anywhere: " + sims + " experiments", xlabel: "spread of the medians, (slowest − fastest) / fastest", nx: 5, xfmt: function (x) { return (100 * x).toFixed(top < 0.05 ? 1 : 0) + "%"; } });
        b.bars(mids, h, top / nb, { color: C.cash, alpha: 0.75 });
        b.vline(e.spread, { color: C.idea, width: 2, dash: [] });
        b.text(e.spread, hmax * 1.25, "this experiment", { color: C.idea, dy: 12, dx: e.spread > top * 0.6 ? -6 : 6, align: e.spread > top * 0.6 ? "right" : "left", bg: true });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["spread seen", QB.pct(o.spread)], ["typical with noise alone", QB.pct(o.typical)],
          ["noise-only experiments at least as spread", QB.pct(o.p, 0)], ["verdict", o.p > 0.05 ? "within the noise" : "beyond the noise"]];
      },
      note: "Simulated data: each run takes 1 plus normal noise, in units of the true time, and only the last setting can differ. Grey bars: the spread of the medians in experiments where no setting differs. A spread that most noise-only experiments exceed shows that the medians moved, not that the settings moved them.",
    });
  };
})();
