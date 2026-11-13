// Interactives for the foundations and Act I: computation, proof, gates, arithmetic, memory, the computer (Parts 1-6).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // A custom-drawn panel: its title, and the rectangle left for the drawing.
  function panel(g, title, foot) {
    var c = g.ctx, b = g.box;
    c.save();
    c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
    c.fillText(title, b.x + 12, b.y + 8);
    if (foot) { c.fillStyle = C.muted; c.font = "11px system-ui, sans-serif"; c.textBaseline = "bottom"; c.fillText(foot, b.x + 12, b.y + b.h - 6); }
    c.restore();
    return { x: b.x + 12, y: b.y + 30, w: b.w - 24, h: b.h - 30 - (foot ? 26 : 10) };
  }
  function label(c, str, x, y, color, align, size) {
    c.save(); c.fillStyle = color || C.ink; c.font = (size || 11.5) + "px system-ui, sans-serif";
    c.textAlign = align || "left"; c.textBaseline = "middle"; c.fillText(str, x, y); c.restore();
  }

  // ---- Part 1: busy beavers on a tape ------------------------------------------------------------------------
  var CHAMP = { 2: "1RB1LB_1LA1RZ", 3: "1RB1RZ_1LB0RC_1LC1LA", 4: "1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 5: "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA" };
  var SN = { 2: "6", 3: "21", 4: "107", 5: "47,176,870" };
  function parseTM(table) { // per state: [write, move, next] on reading 0, then on reading 1; next -1 halts
    return table.split("_").map(function (p) {
      return [0, 1].map(function (s) { var a = p.substr(3 * s, 3); return [a.charAt(0) === "1" ? 1 : 0, a.charAt(1) === "R" ? 1 : -1, "ABCDE".indexOf(a.charAt(2))]; });
    });
  }
  function runTM(tm, ones, steps, each) { // from state A on the first of `ones` ones; each(t, tape, head, offset) per configuration
    var size = 2 * steps + ones + 5, off = steps + 2, tape = new Int8Array(size), i, head = off, st = 0, t = 0, count = ones;
    for (i = 0; i < ones; i++) tape[off + i] = 1;
    var lo = head, hi = head + Math.max(0, ones - 1);
    if (each) each(0, tape, head, off, count);
    while (t < steps && st >= 0) {
      var r = tm[st][tape[head]];
      count += r[0] - tape[head]; tape[head] = r[0]; head += r[1]; st = r[2]; t++;
      if (head < lo) lo = head; if (head > hi) hi = head;
      if (each) each(t, tape, head, off, count);
    }
    return { steps: t, halted: st < 0, lo: lo, hi: hi, ones: count };
  }
  W.beavertape = function (el) {
    QB.widget(el, {
      title: "A busy beaver's tape, step by step",
      sub: "Each row is the tape after one more step of the champion machine with the chosen number of states: blue cells hold a 1, gold is the head. Started on a blank tape it halts at exactly S(n) steps. Put a few ones on the tape first and watch the same table halt at another time, or not within the window at all.",
      panels: 2, height: 320,
      controls: [
        { k: "n", label: "States in the champion", min: 2, max: 5, step: 1, value: 4 },
        { k: "ones", label: "Ones on the starting tape", min: 0, max: 8, step: 1, value: 0 },
        { k: "steps", label: "Steps in the window", min: 10, max: 600, step: 10, value: 120 },
      ],
      draw: function (g, v, s) {
        var tm = parseTM(CHAMP[v.n]), first = runTM(tm, v.ones, v.steps, null);
        s.out = first; s.table = CHAMP[v.n];
        var c = g.ctx, r = panel(g[0], "Tape history (time runs down)", "blue: a 1   gold: the head   " + (first.halted ? "green line: halt" : ""));
        var lo = first.lo - 1, cols = first.hi - first.lo + 3, rows = v.steps + 1, cw = r.w / cols, rh = r.h / rows;
        var ts = [], os = [];
        c.fillStyle = C.bg; c.fillRect(r.x, r.y, r.w, r.h);
        runTM(tm, v.ones, v.steps, function (t, tape, head, off, count) {
          var y = r.y + t * rh, k, run = -1;
          c.fillStyle = C.spot;
          for (k = 0; k <= cols; k++) {
            var on = k < cols && tape[lo + k] === 1;
            if (on && run < 0) run = k;
            if (!on && run >= 0) { c.fillRect(r.x + run * cw, y, (k - run) * cw, Math.max(rh, 0.6)); run = -1; }
          }
          c.fillStyle = C.idea; c.fillRect(r.x + (head - lo) * cw, y, Math.max(cw, 1.5), Math.max(rh, 1));
          ts.push(t); os.push(count);
        });
        if (first.halted) { c.fillStyle = C.gain; c.fillRect(r.x, r.y + Math.min(r.h - 2, (first.steps + 1) * rh), r.w, 2); }
        c.strokeStyle = "#3a475c"; c.lineWidth = 1; c.strokeRect(r.x + 0.5, r.y + 0.5, r.w, r.h);
        var top = 2; for (var i = 0; i < os.length; i++) top = Math.max(top, os[i]);
        var a = g[1].axes({ x: [0, v.steps], y: [0, top + 1], title: "Ones on the tape", xlabel: "step" });
        a.line(ts, os, { color: C.spot });
        if (first.halted) { a.vline(first.steps, { color: C.gain }); a.text(first.steps, (top + 1) * 0.12, "halts", { color: C.gain, dx: first.steps > v.steps * 0.8 ? -6 : 6, align: first.steps > v.steps * 0.8 ? "right" : "left", bg: true }); }
      },
      readout: function (v, s) {
        return [["table", s.table], ["outcome", s.out.halted ? "halts at step " + s.out.steps : "still running at step " + s.out.steps],
          ["ones on the tape", String(s.out.ones)], ["S(" + v.n + ")", SN[v.n]]];
      },
      note: "The tables are the champions of Rado (2 states), Lin and Rado (3), Brady (4) and Marxen and Buntrock (5), in the standard text form: per state, what to write, where to move and which state to enter on reading 0 and on reading 1; Z halts. The 5-state champion needs 47,176,870 steps, so no window here shows it halting: 'still running' never tells you which kind of machine you have.",
    });
  };

  // ---- Part 2: the 15-puzzle's invariant -----------------------------------------------------------------------
  function permParity(board) { // 0 even, 1 odd; the blank (0) counts as tile 16
    var n = board.length, seen = new Array(n), cycles = 0, i, j;
    for (i = 0; i < n; i++) {
      if (seen[i]) continue;
      cycles++; j = i;
      while (!seen[j]) { seen[j] = true; j = (board[j] + n - 1) % n; }
    }
    return (n - cycles) % 2;
  }
  function blankDist(board) { var z = board.indexOf(0); return (3 - Math.floor(z / 4)) + (3 - z % 4); }
  var EO = ["even", "odd"];
  W.fifteenparity = function (el) {
    QB.widget(el, {
      title: "Fourteen, fifteen: an invariant no slide can change",
      sub: "Start from the solved 15-puzzle, lift out and exchange some pairs of tiles by hand (14 with 15, then 1 with 2, then 5 with 6), and slide at random. Every slide flips the swap parity and the parity of the blank's distance from home together, so their sum never moves. With one or three hand swaps the sum is odd and the solved board is out of reach; with two it is even again.",
      panels: 2, height: 310, weights: [0.8, 1.2],
      controls: [
        { k: "cheat", label: "Pairs exchanged by hand", min: 0, max: 3, step: 1, value: 1 },
        { k: "moves", label: "Slides made", min: 0, max: 120, step: 1, value: 30 },
      ],
      buttons: [{ label: "New walk", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 7), board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0], t, i, last = -1;
        var pairs = [[13, 14], [0, 1], [4, 5]];
        for (i = 0; i < v.cheat; i++) { t = board[pairs[i][0]]; board[pairs[i][0]] = board[pairs[i][1]]; board[pairs[i][1]] = t; }
        var par = [permParity(board)], dis = [blankDist(board)];
        for (i = 0; i < v.moves; i++) {
          var z = board.indexOf(0), row = Math.floor(z / 4), col = z % 4, opts = [];
          if (row > 0 && z - 4 !== last) opts.push(z - 4);
          if (row < 3 && z + 4 !== last) opts.push(z + 4);
          if (col > 0 && z - 1 !== last) opts.push(z - 1);
          if (col < 3 && z + 1 !== last) opts.push(z + 1);
          var to = opts[Math.min(opts.length - 1, Math.floor(r() * opts.length))];
          board[z] = board[to]; board[to] = 0; last = z;
          par.push(permParity(board)); dis.push(blankDist(board));
        }
        var inv = (par[v.moves] + dis[v.moves]) % 2;
        s.out = { par: par[v.moves], dis: dis[v.moves], inv: inv };
        var c = g.ctx, p = panel(g[0], "The board after " + v.moves + " slides", "blue: a tile away from its home square");
        var side = Math.min(p.w, p.h), cell = side / 4, x0 = p.x + (p.w - side) / 2, y0 = p.y + (p.h - side) / 2;
        for (i = 0; i < 16; i++) {
          var x = x0 + (i % 4) * cell, y = y0 + Math.floor(i / 4) * cell, tile = board[i];
          c.fillStyle = tile === 0 ? C.bg : (tile === i + 1 ? "#222b3a" : "#1d3a5f");
          c.fillRect(x + 2, y + 2, cell - 4, cell - 4);
          if (tile !== 0) {
            c.strokeStyle = tile === i + 1 ? "#3a475c" : C.spot; c.lineWidth = 1.2; c.strokeRect(x + 2.5, y + 2.5, cell - 5, cell - 5);
            label(c, String(tile), x + cell / 2, y + cell / 2 + 1, C.ink, "center", Math.max(12, Math.min(20, cell * 0.42)));
          }
        }
        var X = [], P = [], D = [], I = [];
        for (i = 0; i <= v.moves; i++) {
          X.push(i, i + 1); P.push(par[i], par[i]); D.push(2 + dis[i] % 2, 2 + dis[i] % 2); I.push(4 + (par[i] + dis[i]) % 2, 4 + (par[i] + dis[i]) % 2);
        }
        var a = g[1].axes({ x: [0, Math.max(10, v.moves + 1)], y: [-0.4, 5.9], yticks: [0, 1, 2, 3, 4, 5], yfmt: function (y) { return EO[y % 2]; }, title: "Three parities along the walk", xlabel: "slides" });
        a.line(X, P, { color: C.spot, width: 1.6 }).line(X, D, { color: C.idea, width: 1.6 }).line(X, I, { color: inv ? C.loss : C.gain, width: 2.4 });
        a.text(0, 1.45, "swap parity of the 16 squares", { color: C.spot, dx: 6, bg: true });
        a.text(0, 3.45, "blank's distance from home", { color: C.idea, dx: 6, bg: true });
        a.text(0, 5.45, "their sum: the invariant", { color: inv ? C.loss : C.gain, dx: 6, bg: true });
      },
      readout: function (v, s) {
        return [["swap parity", EO[s.out.par]], ["blank's distance from home", String(s.out.dis)], ["invariant", EO[s.out.inv]],
          ["solved board reachable", s.out.inv ? "no" : "yes"]];
      },
      note: "Simulated random slides (never undoing the last one). The swap parity is that of the permutation of all sixteen squares, the blank included. Johnson and Story (1879) proved both directions: a position can be solved exactly when the invariant is even.",
    });
  };

  // ---- Part 3: Shannon's counting argument -----------------------------------------------------------------------
  function circuitBits(n, s) { return s * Math.log(16 * (n + s) * (n + s)) / Math.LN2; } // log2 of (16 (n + s)^2)^s
  function gatesNeeded(n) { var f = Math.pow(2, n), s = 1; while (circuitBits(n, s) < f) s++; return s; }
  W.shannoncount = function (el) {
    QB.widget(el, {
      title: "Counting circuits against functions",
      sub: "There are 2^(2^n) functions of n inputs, and at most (16 (n + s)^2)^s circuits of s two-input gates: s choices of a gate kind and two wires. Both are drawn as numbers of bits. Slide the gate budget: until the blue curve reaches the gold line there are too few circuits to go round, so most functions have none.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Inputs n", min: 3, max: 16, step: 1, value: 8 },
        { k: "share", label: "Gate budget s, as a multiple of 2^n / n", min: 0.05, max: 2, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var n = v.n, F = Math.pow(2, n), need = gatesNeeded(n), budget = Math.max(1, Math.round(v.share * F / n));
        var bits = circuitBits(n, budget);
        s.out = { F: F, need: need, budget: budget, bits: bits };
        var smax = Math.max(need * 1.6, budget * 1.1, 4), xs = QB.linspace(0, smax, 120), ys = xs.map(function (x) { return circuitBits(n, x); });
        var a = g[0].axes({ x: [0, smax], y: [0, F * 1.7], title: "n = " + n + ": bits needed to name one", xlabel: "gates s", ny: 4 });
        a.area(xs, ys.map(function (y) { return Math.min(y, F); }), 0, { color: C.spot, alpha: 0.12 });
        a.line(xs, ys, { color: C.spot, width: 2 });
        a.hline(F, { color: C.idea, dash: [], width: 2 });
        a.vline(budget, { color: bits < F ? C.loss : C.gain, width: 1.6 });
        a.dots([need], [F], { color: C.ink, r: 4 });
        a.legend([["log2 of the number of functions: 2^n", C.idea], ["log2 of the number of circuits", C.spot], ["your budget", bits < F ? C.loss : C.gain]], { pos: "tl" });
        var ns = [], needs = [], ratio = [], lin = [];
        for (var k = 3; k <= 16; k++) { ns.push(k); needs.push(gatesNeeded(k)); ratio.push(Math.pow(2, k) / k); lin.push(4 * k); }
        var b = g[1].axes({ x: [3, 16], y: [1, 100000], logy: true, title: "Gates most functions need", xlabel: "inputs n" });
        b.line(ns, ratio, { color: C.idea, dash: [5, 4] }).line(ns, lin, { color: C.gain }).line(ns, needs, { color: C.spot, width: 2.2 });
        b.dots([n], [need], { color: C.ink, r: 4 });
        b.legend([["where the count first allows every function", C.spot], ["2^n / n", C.idea], ["4n: a circuit that grows like n", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out, short = o.F - o.bits;
        return [["functions", "2^" + o.F], ["circuits of " + o.budget + " gates", "at most 2^" + fmt(o.bits, 0)],
          ["functions with such a circuit", short > 0 ? "at most 1 in 2^" + fmt(short, 0) : "the count no longer forbids any"],
          ["gates most functions need", "more than " + (o.need - 1)], ["2^n / n", fmt(o.F / v.n, 0)]];
      },
      note: "The bound on circuits is the film's: each gate picks one of 16 two-input kinds and two of at most n + s wires. Counting proves that hard functions exist without naming one; Lupanov (1958) showed about 2^n / n gates always suffice, and the best lower bound proved for an explicit function is about 3.1 n.",
    });
  };

  // ---- Part 4: every value of a small floating-point format ------------------------------------------------------
  function num(v) { return String(+v.toPrecision(5)).replace("-", "−"); }
  function floatsOf(e, m) { // the non-negative finite values: [value, is subnormal], increasing
    var bias = Math.pow(2, e - 1) - 1, out = [], E, f, M = Math.pow(2, m);
    for (f = 0; f < M; f++) out.push([f / M * Math.pow(2, 1 - bias), true]);
    for (E = 1; E <= Math.pow(2, e) - 2; E++) for (f = 0; f < M; f++) out.push([(1 + f / M) * Math.pow(2, E - bias), false]);
    return out;
  }
  W.tinyfloat = function (el) {
    QB.widget(el, {
      title: "A small floating-point format, every value drawn",
      sub: "Each tick is one number the format can store (sign bit left out). The gap between neighbours doubles at every power of two, so the ruler is fine near zero and coarse far out. Move x and watch it snap to the nearest tick; add fraction bits to halve every gap, or exponent bits to stretch the range.",
      panels: 2, height: 300,
      controls: [
        { k: "m", label: "Fraction bits", min: 1, max: 5, step: 1, value: 2 },
        { k: "e", label: "Exponent bits", min: 2, max: 4, step: 1, value: 3 },
        { k: "t", label: "A real number x (position along the range)", min: 0, max: 1, step: 0.002, value: 0.62, fmt: function (x) { return x.toFixed(3); } },
      ],
      draw: function (g, v, s) {
        var fl = floatsOf(v.e, v.m), n = fl.length, top = fl[n - 1][0], x = v.t * v.t * top, i, k = 0;
        for (i = 0; i < n; i++) if (Math.abs(fl[i][0] - x) < Math.abs(fl[k][0] - x) || (Math.abs(fl[i][0] - x) === Math.abs(fl[k][0] - x) && i % 2 === 0)) k = i;
        var gap = k + 1 < n ? fl[k + 1][0] - fl[k][0] : fl[k][0] - fl[k - 1][0];
        s.out = { n: n, x: x, near: fl[k][0], gap: gap, top: top, sub: fl[k][1], tiny: fl[1][0] };
        var a = g[0].axes({ x: [0, top], y: [0, 1], noY: true, title: "The number line, 0 to " + num(top), xlabel: "value" });
        a.clip(function (c) {
          for (i = 0; i < n; i++) {
            c.strokeStyle = fl[i][1] ? C.q : C.spot; c.lineWidth = 1; c.beginPath();
            var px = Math.round(a.px(fl[i][0])) + 0.5; c.moveTo(px, a.py(0)); c.lineTo(px, a.py(fl[i][1] ? 0.3 : 0.42)); c.stroke();
          }
        });
        a.line([fl[k][0], fl[k][0]], [0, 0.62], { color: C.gain, width: 2.4 });
        a.line([x, x], [0, 0.74], { color: C.idea, width: 1.6, dash: [4, 3] });
        a.legend([["normal numbers", C.spot], ["subnormal numbers", C.q], ["x", C.idea], ["the float nearest x", C.gain]], { pos: "tr" });
        var xs = [], ys = [], lo = fl[1][0];
        for (i = 1; i < n - 1; i++) { xs.push(fl[i][0], fl[i + 1][0]); ys.push(fl[i + 1][0] - fl[i][0], fl[i + 1][0] - fl[i][0]); }
        var b = g[1].axes({ x: [lo, top], y: [lo / 2, Math.max(lo * 4, (top - fl[n - 2][0]) * 2)], logx: true, logy: true, title: "Gap to the next float (log scales)", xlabel: "value" });
        b.line(xs, ys, { color: C.spot, width: 2 });
        b.dots([Math.min(top, Math.max(lo, fl[k][0]))], [gap], { color: C.gain, r: 5 });
        b.legend([["gap between neighbours", C.spot], ["at the float nearest x", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["values stored", String(o.n)], ["x", num(o.x)], ["stored as", num(o.near) + (o.sub ? " (subnormal)" : "")],
          ["rounding error", num(Math.abs(o.x - o.near)) + (o.x > 0 ? " (" + QB.pct(Math.abs(o.x - o.near) / o.x, 1) + " of x)" : "")],
          ["gap here", num(o.gap)], ["machine epsilon", num(Math.pow(2, -v.m))], ["smallest positive", num(o.tiny)]];
      },
      note: "The layout is IEEE 754's with fewer bits: a biased exponent, a hidden leading 1 for normal numbers, an exponent field of zero for subnormals, and the top exponent reserved for infinity and NaN. Ties round to the even neighbour. binary32 has 8 exponent and 23 fraction bits; binary64 has 11 and 52.",
    });
  };

  // ---- Part 5: the latch as two wells and a saddle ---------------------------------------------------------------
  function tanh(x) { var e = Math.exp(-2 * Math.abs(x)), t = (1 - e) / (1 + e); return x < 0 ? -t : t; }
  W.latchsaddle = function (el) {
    QB.widget(el, {
      title: "A latch deciding: two wells and a saddle",
      sub: "Two inverters drive each other, and each voltage relaxes towards the inverter curve of the other. Start the pair nearly balanced and follow it: the common level dies out fast, then the imbalance grows exponentially until the latch falls into 0 or 1. Shrink the imbalance by powers of ten and the decision takes longer, without limit.",
      panels: 2, height: 320,
      controls: [
        { k: "ld", label: "Starting imbalance v1 − v2", min: -8, max: -0.5, step: 0.25, value: -3, fmt: function (x) { return "10^" + fmt(x, 2); } },
        { k: "c", label: "Starting common level", min: 0.1, max: 0.9, step: 0.02, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
        { k: "gain", label: "Inverter gain at its threshold", min: 2, max: 6, step: 0.25, value: 3, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var G = 2 * v.gain, f = function (x) { return 0.5 * (1 - tanh(G * (x - 0.5))); }, i;
        var lo = 0; for (i = 0; i < 200; i++) lo = f(f(lo));
        var hi = f(lo), sep = hi - lo, d = Math.pow(10, v.ld), lam = v.gain - 1;
        var v1 = Math.min(1, v.c + d / 2), v2 = Math.max(0, v.c - d / 2), dt = 0.02, T = 24, n = Math.round(T / dt);
        var ts = [0], a1 = [v1], a2 = [v2], tres = -1;
        for (i = 1; i <= n; i++) { // Runge-Kutta 4 on dv1/dt = f(v2) - v1, dv2/dt = f(v1) - v2 (time in units of RC)
          var k1a = f(v2) - v1, k1b = f(v1) - v2;
          var k2a = f(v2 + dt / 2 * k1b) - (v1 + dt / 2 * k1a), k2b = f(v1 + dt / 2 * k1a) - (v2 + dt / 2 * k1b);
          var k3a = f(v2 + dt / 2 * k2b) - (v1 + dt / 2 * k2a), k3b = f(v1 + dt / 2 * k2a) - (v2 + dt / 2 * k2b);
          var k4a = f(v2 + dt * k3b) - (v1 + dt * k3a), k4b = f(v1 + dt * k3a) - (v2 + dt * k3b);
          v1 += dt / 6 * (k1a + 2 * k2a + 2 * k3a + k4a); v2 += dt / 6 * (k1b + 2 * k2b + 2 * k3b + k4b);
          if (tres < 0 && Math.abs(v1 - v2) >= sep / 2) tres = i * dt;
          if (i % 5 === 0) { ts.push(i * dt); a1.push(v1); a2.push(v2); }
        }
        s.out = { tres: tres, est: Math.log(sep / d) / lam, lam: lam, sep: sep, d: d };
        var u = QB.linspace(0, 1, 80), fu = u.map(f);
        var a = g[0].axes({ x: [0, 1], y: [0, 1], title: "The state of the latch (v1 across, v2 up)", xlabel: "v1" });
        a.line([0, 1], [0, 1], { color: C.muted, dash: [4, 4], width: 1 });
        a.line(fu, u, { color: C.spot, width: 1.4 }).line(u, fu, { color: C.q, width: 1.4 });
        a.line(a1, a2, { color: C.idea, width: 2.4 });
        a.dots([lo, hi], [hi, lo], { color: C.gain, r: 5 }).dots([0.5], [0.5], { color: C.loss, r: 5 }).dots([a1[0]], [a2[0]], { color: C.idea, r: 4 });
        a.text(0.5, 0.5, "saddle", { color: C.loss, dx: 8, dy: -10, bg: true });
        a.text(lo, hi, "0", { color: C.gain, dx: 10, dy: 12 }).text(hi, lo, "1", { color: C.gain, dx: -14, dy: -12 });
        var b = g[1].axes({ x: [0, T], y: [0, 1], title: "The two voltages against time", xlabel: "time, in units of the gate's RC" });
        b.line(ts, a1, { color: C.idea, width: 2 }).line(ts, a2, { color: C.realized, width: 2 });
        if (tres >= 0) { b.vline(tres, { color: C.gain }); b.text(tres, 0.5, "decided", { color: C.gain, dx: tres > T * 0.75 ? -6 : 6, align: tres > T * 0.75 ? "right" : "left", bg: true }); }
        b.legend([["v1", C.idea], ["v2", C.realized]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["growth rate across the diagonal", "+" + fmt(o.lam, 2) + " per RC"], ["decay along it", "−" + fmt(o.lam + 2, 2) + " per RC"],
          ["decided after", o.tres >= 0 ? fmt(o.tres, 1) + " RC" : "not within 24 RC"], ["estimate (τ/λ) ln(Δ/δ)", fmt(o.est, 1) + " RC"]];
      },
      note: "The film's model: each inverter's curve is a tanh with the chosen slope at its threshold, and each wire is one RC. Left panel: the blue and purple curves are where one voltage stops changing; they cross at the two stable states (green) and the saddle (red). 'Decided' is when the voltages are half as far apart as they will end; the estimate ignores the time the common level takes to die out.",
    });
  };

  // ---- Part 6: Euclid on Pebble, one instruction at a time -------------------------------------------------------
  var EUCLID_LINE = [0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; // li assembles to two instructions
  var EUCLID_ADDR = ["00", "08", "10", "14", "18", "1c", "20", "24", "28", "2c", "30"];
  function euclidRun(a, b, limit, each) { // Pebble's registers a0, a1, t0 after each instruction
    var r = { a0: 0, a1: 0, t0: 0, pc: 0, n: 0, halted: false };
    while (!r.halted && r.n < limit) {
      switch (r.pc) {
        case 0: r.a0 = 0; r.pc = 1; break;
        case 1: r.a0 += a; r.pc = 2; break;
        case 2: r.a1 = 0; r.pc = 3; break;
        case 3: r.a1 += b; r.pc = 4; break;
        case 4: r.pc = r.a1 === 0 ? 12 : 5; break;
        case 5: r.pc = r.a0 < r.a1 ? 8 : 6; break;
        case 6: r.a0 -= r.a1; r.pc = 7; break;
        case 7: r.pc = 5; break;
        case 8: r.t0 = r.a0; r.pc = 9; break;
        case 9: r.a0 = r.a1; r.pc = 10; break;
        case 10: r.a1 = r.t0; r.pc = 11; break;
        case 11: r.pc = 4; break;
        default: r.halted = true;
      }
      r.n++;
      if (each) each(r);
    }
    return r;
  }
  function seconds(t) {
    if (t >= 3600) return fmt(t / 3600, 1) + " h";
    if (t >= 60) return fmt(t / 60, 1) + " min";
    if (t >= 1) return fmt(t, 1) + " s";
    if (t >= 1e-3) return fmt(t * 1e3, 1) + " ms";
    return fmt(t * 1e6, 2) + " µs";
  }
  W.pebblesteps = function (el) {
    QB.widget(el, {
      title: "Euclid on Pebble, one instruction at a time",
      sub: "The program is eleven lines of Pebble assembly, stored in memory as numbers. The gold line is the instruction the program counter points at; step forward and watch the registers a0 and a1 change. Change the two inputs: the listing stays the same, and only the number of instructions it takes changes.",
      panels: 2, height: 320, weights: [0.85, 1.15],
      controls: [
        { k: "a", label: "First number (in a0)", min: 1, max: 200, step: 1, value: 147 },
        { k: "b", label: "Second number (in a1)", min: 1, max: 200, step: 1, value: 63 },
        { k: "steps", label: "Instructions executed", min: 0, max: 620, step: 1, value: 12 },
      ],
      draw: function (g, v, s) {
        var xs = [0], y0 = [0], y1 = [0];
        var full = euclidRun(v.a, v.b, 100000, function (r) { xs.push(r.n); y0.push(r.a0); y1.push(r.a1); });
        var now = euclidRun(v.a, v.b, v.steps, null);
        s.out = { now: now, total: full.n, gcd: full.a0 };
        var lines = ["      li   a0, " + v.a, "      li   a1, " + v.b, "loop: beqz a1, done", "mod:  bltu a0, a1, swap", "      sub  a0, a0, a1",
          "      j    mod", "swap: mv   t0, a0", "      mv   a0, a1", "      mv   a1, t0", "      j    loop", "done: halt"];
        var c = g.ctx, p = panel(g[0], "The program in memory", "a0 = " + now.a0 + "   a1 = " + now.a1 + "   t0 = " + now.t0);
        var lh = Math.min(19, p.h / 11), cur = now.halted ? 10 : EUCLID_LINE[now.pc], i;
        c.save(); c.font = "12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"; c.textBaseline = "middle";
        for (i = 0; i < 11; i++) {
          var y = p.y + (i + 0.5) * lh;
          if (i === cur) { c.fillStyle = now.halted ? "rgba(74,222,128,0.22)" : "rgba(247,209,84,0.22)"; c.fillRect(p.x, y - lh / 2, Math.min(p.w, 300), lh); }
          c.fillStyle = C.muted; c.textAlign = "left"; c.fillText(EUCLID_ADDR[i], p.x + 6, y);
          c.fillStyle = i === cur ? (now.halted ? C.gain : C.idea) : C.ink; c.fillText(lines[i], p.x + 34, y);
        }
        c.restore();
        var top = Math.max(v.a, v.b) * 1.08;
        var a = g[1].axes({ x: [0, Math.max(full.n, 10)], y: [0, top], title: "The two registers, instruction by instruction", xlabel: "instructions executed" });
        var sx = [], s0 = [], s1 = [];
        for (i = 0; i < xs.length - 1; i++) { sx.push(xs[i], xs[i + 1]); s0.push(y0[i], y0[i]); s1.push(y1[i], y1[i]); }
        sx.push(full.n); s0.push(full.a0); s1.push(full.a1);
        a.line(sx, s0, { color: C.spot, width: 2 }).line(sx, s1, { color: C.idea, width: 2 });
        a.vline(now.n, { color: now.halted ? C.gain : C.ink, width: 1.4 });
        a.legend([["a0", C.spot], ["a1", C.idea], ["now", now.halted ? C.gain : C.ink]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["executed", o.now.n + " of " + o.total], ["state", o.now.halted ? "halted: a0 = gcd = " + o.gcd : "pc = 0x" + ((o.now.pc < 4 ? (o.now.pc >> 1) * 8 + (o.now.pc & 1) * 4 : 16 + (o.now.pc - 4) * 4)).toString(16)],
          ["whole run at 5.3 instructions a second", seconds(o.total / 5.3)], ["at one instruction per 380 MHz cycle", seconds(o.total / 380e6)]];
      },
      note: "The listing is the film's Euclid, by repeated subtraction; li assembles to two instructions, so the program occupies 13 words. Time is instructions × cycles per instruction × seconds per cycle, with one cycle per instruction on the single-cycle machine; 5.3 operations a second is the film's relay-machine rate and 380 MHz its assumed clock for Pebble, neither a measurement.",
    });
  };
})();
