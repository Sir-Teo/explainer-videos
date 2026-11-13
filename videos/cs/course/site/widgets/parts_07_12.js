// Interactives for Act II, Making It Fast, and the start of Act III (Parts 7-12).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 7: how deep should a pipeline be? ---------------------------------------------------------------
  W.pipedepth = function (el) {
    var T = 2560; // ps of logic in one instruction, as in the part's depth model
    QB.widget(el, {
      title: "How deep should a pipeline be?",
      sub: "One instruction's 2,560 ps of logic is cut into k equal stages, each followed by a register that costs o. A fraction b of instructions is a mispredicted branch and loses k − 1 cycles. Start with b = 0 and deepen: the speedup climbs towards 1 + t/o, never k. Then raise b and watch a best depth appear and move left.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Stages k", min: 1, max: 80, step: 1, value: 5 },
        { k: "o", label: "Register overhead o", min: 10, max: 300, step: 5, value: 70, fmt: function (x) { return x + " ps"; } },
        { k: "b", label: "Instructions that pay a flush, b", min: 0, max: 0.2, step: 0.0005, value: 0.0265, fmt: function (x) { return (100 * x).toFixed(2) + "%"; } },
      ],
      draw: function (g, v, s) {
        var ks = [], cyc = [], tim = [], spI = [], spH = [], k, clock, t1 = T + v.o;
        for (k = 1; k <= 80; k++) {
          clock = T / k + v.o;
          ks.push(k); cyc.push(clock); tim.push(clock * (1 + v.b * (k - 1)));
          spI.push(t1 / clock); spH.push(t1 / tim[k - 1]);
        }
        var best = 1; for (k = 2; k <= 80; k++) if (tim[k - 1] < tim[best - 1]) best = k;
        var kstar = v.b > 0 ? Math.sqrt(T * (1 - v.b) / (v.b * v.o)) : 0;
        s.out = { clock: cyc[v.k - 1], cpi: 1 + v.b * (v.k - 1), time: tim[v.k - 1], sp: spH[v.k - 1], best: best, kstar: kstar, lim: 1 + T / v.o };
        var ytop = Math.ceil(Math.max(T + v.o, tim[79]) / 1000) * 1000;
        var a = g[0].axes({ x: [1, 80], y: [0, ytop], title: "Time per instruction (ps)", xlabel: "stages k", xticks: [1, 20, 40, 60, 80] });
        a.line(ks, cyc, { color: C.spot, width: 1.5 }).line(ks, tim, { color: C.idea, width: 2.2 });
        a.hline(v.o, { color: C.muted });
        a.vline(best, { color: C.gain });
        a.dots([v.k], [tim[v.k - 1]], { color: C.idea, r: 5 });
        a.legend([["cycle time t/k + o", C.spot], ["with flushes: × (1 + b(k − 1))", C.idea]], { pos: "tr" });
        var top = Math.max(10, Math.ceil(Math.min(80, s.out.lim) / 10) * 10);
        var bx = g[1].axes({ x: [1, 80], y: [0, top], title: "Speedup over one stage", xlabel: "stages k", xticks: [1, 20, 40, 60, 80] });
        bx.line([1, 80], [1, 80], { color: C.muted, dash: [4, 4], width: 1 });
        bx.text(0.55 * top, 0.55 * top, "ideal: k", { color: C.muted, dx: 8, bg: true });
        if (s.out.lim <= top) { bx.hline(s.out.lim, { color: C.loss }); bx.text(80, s.out.lim, "limit 1 + t/o", { color: C.loss, align: "right", dx: -6, dy: 12, bg: true }); }
        bx.line(ks, spI, { color: C.spot, width: 1.5 }).line(ks, spH, { color: C.idea, width: 2.2 });
        bx.vline(best, { color: C.gain });
        bx.dots([v.k], [spH[v.k - 1]], { color: C.idea, r: 5 });
        bx.legend([["no flushes", C.spot], ["with flushes", C.idea], ["fastest depth", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["cycle", fmt(o.clock, 0) + " ps"], ["CPI", fmt(o.cpi, 3)], ["time per instruction", fmt(o.time, 0) + " ps"],
          ["speedup", fmt(o.sp, 2) + "×"], ["limit 1 + t/o", fmt(o.lim, 1) + "×"],
          ["best depth", o.kstar > 0 ? (o.kstar > 80 ? "beyond 80" : String(o.best) + " (k* = " + fmt(o.kstar, 1) + ")") : "none: deeper is faster"]];
      },
      note: "The part's teaching model, not a hardware design: equally splittable logic, a fixed register overhead, a fixed fraction b that loses k − 1 cycles. The continuous optimum is k* = √(t(1 − b)/(b·o)); the default b = 2.65% is the Job's measured value and gives about 37. Real predictors and stage balances change with depth.",
    });
  };

  // ---- Part 8: the scan loop on an oracle scheduler ---------------------------------------------------------
  W.dataflowlimit = function (el) {
    // one fast-path trip of the Job's scan: [kind, source registers, destination register]; 0 t0, 1 a2, 2 t1, 3 s1, 4 a1
    var TRIP = [["branch", [1, 3], -1], ["load", [0], 2], ["branch", [2, 4], -1], ["alu", [0], 0], ["alu", [1], 1], ["jump", [], -1]];
    var NAMES = ["beq a2, s1", "lw t1, 4(t0)", "bne t1, a1", "addi t0", "addi a2", "j scan"];
    var COL = { load: C.spot, branch: C.loss, alu: C.gain, jump: C.cash };
    var schedule = function (trips, width, loadLat, rename, inOrder) { // explainer/cs/pebble/limits.py, in miniature
      var ready = [0, 0, 0, 0, 0], lastRead = [0, 0, 0, 0, 0], written = [0, 0, 0, 0, 0], used = {}, start = [], lat = [], end = 0, prev = -1, i, j, k;
      for (i = 0; i < trips * 6; i++) {
        var ins = TRIP[i % 6], l = ins[0] === "load" ? loadLat : 1, t = inOrder ? prev + 1 : 0, d = ins[2];
        for (j = 0; j < ins[1].length; j++) t = Math.max(t, ready[ins[1][j]]);
        if (!rename && d >= 0) t = Math.max(t, lastRead[d], written[d] - l + 1);
        if (width > 0) { while ((used[t] || 0) >= width) t++; used[t] = (used[t] || 0) + 1; }
        start.push(t); lat.push(l); prev = t; end = Math.max(end, t + l);
        for (j = 0; j < ins[1].length; j++) { k = ins[1][j]; lastRead[k] = Math.max(lastRead[k], t); }
        if (d >= 0) { ready[d] = t + l; written[d] = t + l; }
      }
      return { start: start, lat: lat, cycles: end };
    };
    QB.widget(el, {
      title: "The dataflow limit: one scan loop, more and more start slots",
      sub: "Each bar is an instruction of the Job's scan loop (the fast path, six instructions a trip), placed as early as its inputs allow with W starts a cycle. Widen the machine: the schedule shrinks until it hits the longest dependency chain and then stops. Turn renaming off and the reuse of t1, t0 and a2 holds the trips apart.",
      panels: 2, height: 320,
      controls: [
        { k: "w", label: "Starts per cycle W", min: 1, max: 8, step: 1, value: 2 },
        { k: "trips", label: "Trips round the loop", min: 1, max: 6, step: 1, value: 4 },
        { k: "lat", label: "Load latency", min: 1, max: 6, step: 1, value: 2, fmt: function (x) { return x + (x === 1 ? " cycle" : " cycles"); } },
        { k: "ren", label: "Register renaming", min: 0, max: 1, step: 1, value: 1, fmt: function (x) { return x ? "on" : "off"; } },
      ],
      draw: function (g, v, s) {
        var n = v.trips * 6, sc = schedule(v.trips, v.w, v.lat, v.ren, false), span = schedule(v.trips, 0, v.lat, 1, false).cycles;
        var ino = schedule(v.trips, 0, v.lat, 1, true).cycles, ws = [], cyc = [], bnd = [], w, i;
        for (w = 1; w <= 8; w++) { ws.push(w); cyc.push(schedule(v.trips, w, v.lat, v.ren, false).cycles); bnd.push(Math.max(Math.ceil(n / w), span)); }
        s.out = { n: n, span: span, cycles: sc.cycles, bound: bnd[v.w - 1], ino: ino };
        var xmax = Math.max(12, sc.cycles);
        var a = g[0].axes({ x: [0, xmax], y: [0, n], title: n + " instructions in " + sc.cycles + " cycles", xlabel: "cycle", noY: true });
        var c = g.ctx, rowH = a.h / n;
        c.save();
        for (i = 0; i < n; i++) {
          var x1 = a.px(sc.start[i]), x2 = a.px(sc.start[i] + sc.lat[i]), y = a.y0 + i * rowH;
          if (i % 12 < 6) { c.fillStyle = "rgba(255,255,255,0.035)"; c.fillRect(a.x0, y, a.w, rowH); }
          c.fillStyle = COL[TRIP[i % 6][0]]; c.fillRect(x1 + 1, y + 1, Math.max(2, x2 - x1 - 2), Math.max(2, rowH - 2));
        }
        if (rowH >= 13) { // room to name the instructions
          c.font = "11px ui-monospace, monospace"; c.textBaseline = "middle"; c.textAlign = "left"; c.fillStyle = C.ink;
          for (i = 0; i < n; i++) if (a.px(sc.start[i] + sc.lat[i]) + 6 + c.measureText(NAMES[i % 6]).width < a.x0 + a.w) c.fillText(NAMES[i % 6], a.px(sc.start[i] + sc.lat[i]) + 5, a.y0 + (i + 0.5) * rowH);
        }
        c.restore();
        a.legend([["load", COL.load], ["branch", COL.branch], ["add", COL.alu], ["jump", COL.jump]], { pos: "tr" });
        var top = Math.max(12, Math.ceil(Math.max(cyc[0], ino) / 6) * 6 + 6);
        var b = g[1].axes({ x: [0.4, 8.6], y: [0, top], title: "Cycles against width", xlabel: "starts per cycle W", xticks: ws });
        b.bars(ws, cyc, 0.7, { color: function (k) { return k === v.w - 1 ? C.idea : "#5b6b82"; } });
        b.line(ws, bnd, { color: C.spot, width: 2 });
        b.dots(ws, bnd, { color: C.spot, r: 3 });
        b.hline(span, { color: C.loss });
        b.hline(ino, { color: C.muted });
        b.legend([["scheduled", C.idea], ["bound max(⌈N/W⌉, L)", C.spot], ["span L", C.loss], ["in order", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["instructions N", String(o.n)], ["span L", String(o.span)], ["cycles at W = " + v.w, String(o.cycles)], ["lower bound", String(o.bound)],
          ["instructions per cycle", fmt(o.n / Math.max(1, o.cycles), 2)], ["one at a time, in order", String(o.ino) + " cycles"]];
      },
      note: "The part's oracle scheduler in miniature: a known path, loads of the chosen latency and one cycle for everything else, unlimited units, W starts a cycle. With renaming off, a write waits for earlier reads and writes of the same register name. The span L is computed with renaming on. A real core adds a front end, finite queues and in-order retirement.",
    });
  };

  // ---- Part 9: a scan a little longer than the cache --------------------------------------------------------
  W.scanthrash = function (el) {
    var PASSES = 8, POL = ["LRU", "random", "MIN (offline)"];
    var replay = function (K, cap, policy, rand, marks) { // misses of PASSES cyclic scans over K lines, fully associative
      var cache = [], misses = 0, t, i, x, pos, victim, far, d;
      for (t = 0; t < PASSES * K; t++) {
        x = t % K; pos = cache.indexOf(x);
        if (pos >= 0) { if (policy === 0) { cache.splice(pos, 1); cache.push(x); } if (marks) marks.push(0); continue; }
        misses++; if (marks) marks.push(1);
        if (cache.length >= cap) {
          victim = 0; // LRU: the front of the list
          if (policy === 1) victim = Math.floor(rand() * cache.length);
          if (policy === 2) { far = -1; for (i = 0; i < cache.length; i++) { d = (cache[i] - x + K) % K; if (d > far) { far = d; victim = i; } } }
          cache.splice(victim, 1);
        }
        cache.push(x);
      }
      return misses / (PASSES * K);
    };
    QB.widget(el, {
      title: "A scan one line longer than the cache",
      sub: "A program reads K cache lines in order, eight times over, through a fully associative cache of C lines. While K is at most C only the first pass misses. Make the scan one line longer than the cache: LRU has always just evicted the line it needs and misses every time, while Belady's MIN, which sees the future, misses once in C.",
      panels: 2, height: 300,
      controls: [
        { k: "K", label: "Lines in the scan K", min: 2, max: 48, step: 1, value: 17 },
        { k: "cap", label: "Cache capacity C (lines)", min: 2, max: 32, step: 1, value: 16 },
        { k: "pol", label: "Policy drawn on the left", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return POL[x]; } },
      ],
      buttons: [{ label: "New random evictions", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var marks = [], ks = [], m = [[], [], []], K, p, i;
        for (K = 2; K <= 48; K++) { ks.push(K); for (p = 0; p < 3; p++) m[p].push(replay(K, v.cap, p, QB.rng(s.seed * 97 + K), null)); }
        replay(v.K, v.cap, v.pol, QB.rng(s.seed * 97 + v.K), marks);
        s.out = [m[0][v.K - 2], m[1][v.K - 2], m[2][v.K - 2]];
        var a = g[0].axes({ x: [0, PASSES * v.K], y: [-1, v.K], title: POL[v.pol] + ": green hit, red miss", xlabel: "reference (eight passes)", noY: true, xticks: [0, 2 * v.K, 4 * v.K, 6 * v.K, 8 * v.K] });
        var xs = [], ys = [];
        for (i = 0; i < marks.length; i++) { xs.push(i + 0.5); ys.push(v.K - 1 - (i % v.K)); }
        a.dots(xs, ys, { color: function (j) { return marks[j] ? C.loss : C.gain; }, r: v.K > 24 ? 1.8 : 2.6 });
        var b = g[1].axes({ x: [2, 48], y: [0, 1.05], title: "Miss fraction against scan length", xlabel: "lines in the scan K", xticks: [2, 12, 24, 36, 48], yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.vline(v.cap, { color: C.muted });
        b.text(v.cap, 0.72, "K = C", { color: C.muted, dx: -6, align: "right", bg: true });
        b.line(ks, m[2], { color: C.gain, width: 2 }).line(ks, m[1], { color: C.idea, width: 1.6 }).line(ks, m[0], { color: C.loss, width: 2 });
        b.dots([v.K], [s.out[v.pol]], { color: C.ink, r: 4.5 });
        b.legend([["LRU", C.loss], ["random", C.idea], ["MIN", C.gain]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["LRU misses", QB.pct(s.out[0])], ["random misses", QB.pct(s.out[1])], ["MIN misses", QB.pct(s.out[2])],
          ["scan / cache", v.K + " / " + v.cap + " lines"]];
      },
      note: "A simulated reference stream from an empty cache, first pass included, with a forced insertion on every miss. Random replacement uses a seeded generator: one seed is one draw, not a guarantee. MIN needs the future, so it is a yardstick, not a design. Real caches add sets, prefetching and other traffic.",
    });
  };

  // ---- Part 10: a greedy schedule between its two bounds ----------------------------------------------------
  W.greedybrent = function (el) {
    var N = 96, PMAX = 16;
    var dag = function (reach, seed) { // nodes in order, each using up to two of the `reach` nodes before it
      var r = QB.rng(seed), preds = [], v, k, lo, a, b;
      for (v = 0; v < N; v++) {
        lo = Math.max(0, v - reach); k = Math.min(2, v - lo); preds.push([]);
        if (k > 0 && r() < 0.9) { a = lo + Math.floor(r() * (v - lo)); preds[v].push(a); if (k > 1 && r() < 0.5) { b = lo + Math.floor(r() * (v - lo)); if (b !== a) preds[v].push(b); } }
      }
      return preds;
    };
    var span = function (preds) { var fin = [], best = 0, v, j, m; for (v = 0; v < N; v++) { m = 0; for (j = 0; j < preds[v].length; j++) m = Math.max(m, fin[preds[v][j]]); fin.push(m + 1); best = Math.max(best, m + 1); } return best; };
    var greedy = function (preds, p) { // never leave a processor idle while a node is ready
      var left = [], done = [], steps = [], count = 0, v, j, run;
      for (v = 0; v < N; v++) { left.push(preds[v].length); done.push(false); }
      while (count < N) {
        run = [];
        for (v = 0; v < N && run.length < p; v++) if (!done[v] && left[v] === 0) run.push(v);
        for (j = 0; j < run.length; j++) done[run[j]] = true;
        for (v = 0; v < N; v++) if (!done[v]) { left[v] = 0; for (j = 0; j < preds[v].length; j++) if (!done[preds[v][j]]) left[v]++; }
        steps.push(run); count += run.length;
      }
      return steps;
    };
    QB.widget(el, {
      title: "Greedy scheduling and Brent's bound",
      sub: "A computation of 96 unit tasks, each waiting for up to two earlier ones, is run by p processors that never idle while a task is ready. Gold steps keep every processor busy; blue steps do not, and each of those shortens the longest remaining chain. Add processors until the schedule stops shrinking: it has reached the span.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Processors p", min: 1, max: PMAX, step: 1, value: 7 },
        { k: "reach", label: "How far back a task may depend", min: 1, max: 40, step: 1, value: 12, fmt: function (x) { return x + (x === 1 ? " task" : " tasks"); } },
      ],
      buttons: [{ label: "New computation", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var preds = dag(v.reach, s.seed + 500), tinf = span(preds), ps = [], tp = [], lo = [], hi = [], p, i, j;
        for (p = 1; p <= PMAX; p++) { ps.push(p); tp.push(greedy(preds, p).length); lo.push(Math.max(Math.ceil(N / p), tinf)); hi.push(N / p + tinf); }
        var steps = greedy(preds, v.p), full = 0;
        for (i = 0; i < steps.length; i++) if (steps[i].length === v.p) full++;
        s.out = { tinf: tinf, steps: steps.length, full: full, lo: lo[v.p - 1], hi: hi[v.p - 1] };
        var a = g[0].axes({ x: [0, steps.length], y: [0, v.p], title: "The schedule: " + steps.length + " steps on " + v.p + (v.p === 1 ? " processor" : " processors"), xlabel: "step", noY: true });
        var c = g.ctx, cw = a.w / steps.length, ch = a.h / v.p;
        c.save();
        for (i = 0; i < steps.length; i++) {
          c.fillStyle = steps[i].length === v.p ? C.idea : C.spot;
          for (j = 0; j < steps[i].length; j++) c.fillRect(a.x0 + i * cw + 0.5, a.y0 + j * ch + 0.5, Math.max(1, cw - 1), Math.max(1, ch - 1));
        }
        c.restore();
        var top = Math.ceil((N + tinf) / 20) * 20;
        var b = g[1].axes({ x: [0.5, PMAX + 0.5], y: [0, top], title: "Steps against processors", xlabel: "processors p", xticks: [1, 4, 8, 12, 16] });
        b.area(ps, hi, lo, { color: C.spot, alpha: 0.13 });
        b.line(ps, hi, { color: C.implied, width: 1.6 }).line(ps, lo, { color: C.cash, width: 1.6 });
        b.hline(tinf, { color: C.loss });
        b.dots(ps, tp, { color: function (k) { return k === v.p - 1 ? C.ink : C.gain; }, r: 3.5 });
        b.legend([["Brent: T₁/p + T∞", C.implied], ["greedy schedule", C.gain], ["max(T₁/p, T∞)", C.cash], ["span T∞", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["work T₁", String(N)], ["span T∞", String(o.tinf)], ["parallelism", fmt(N / o.tinf, 1)], ["greedy steps", String(o.steps)],
          ["bounds", o.lo + " to " + fmt(o.hi, 1)], ["complete / incomplete", o.full + " / " + (o.steps - o.full)], ["speedup", fmt(N / o.steps, 2) + "×"]];
      },
      note: "A simulated computation of unit-cost tasks; the scheduler takes ready tasks in order. Brent's theorem: at most T₁/p complete steps and at most T∞ incomplete ones, so the white dot always lies in the shaded band. Real schedulers pay for stealing, caches and communication, which this count leaves out.",
    });
  };

  // ---- Part 11: one unchecked copy into an 80-byte frame ----------------------------------------------------
  W.framesmash = function (el) {
    var CODE = 72, RA = 76, FRAME = 80, CELLS = 96; // greet's frame on Pebble: 64-byte buffer, saved return address at 76(sp)
    var KIND = ["plain letters", "the attack"];
    var region = function (off, canary) { return off < 64 ? "buf" : off < 72 ? "gap" : off < 76 ? (canary ? "canary" : "gap") : off < 80 ? "ra" : "above"; };
    var BASE = { buf: C.spot, gap: C.cash, canary: C.gain, ra: C.loss, above: "#3a475c" };
    var inputColor = function (off, kind) { return kind === 0 ? C.house : off < CODE ? C.q : off < RA ? C.house : off < FRAME ? C.implied : C.house; };
    var outcome = function (v) {
      var L = v.len, o = { canary: "none", ret: "", run: "", console: "", verdict: "" };
      if (v.canary) o.canary = L >= 72 ? "changed" : "intact";
      if (o.canary === "changed") { o.console = "*** stack smashing detected ***"; o.verdict = "stopped by the canary"; return o; }
      if (L < RA) { o.ret = "caller"; o.console = L === 0 ? "hello,   bye" : "hello, <the name>   bye"; o.verdict = "returns normally"; return o; }
      if (v.kind === 1 && L >= FRAME) {
        o.ret = "buffer";
        if (v.nx) { o.run = "fault"; o.console = "fault: execute from the stack"; o.verdict = "stopped by the no-execute stack"; }
        else { o.run = "runs"; o.console = "pwned"; o.verdict = "runs the attacker's code"; }
        return o;
      }
      o.ret = "wild"; o.console = "(crash: a jump to a wrong address)"; o.verdict = "crashes"; return o;
    };
    var flow = function (c, items, x, y, maxw) { // a legend that wraps: [[label, color], ...]
      var cx = x, cy = y, i, w;
      c.font = "11px system-ui, sans-serif"; c.textBaseline = "middle"; c.textAlign = "left";
      for (i = 0; i < items.length; i++) {
        w = 16 + c.measureText(items[i][0]).width + 12;
        if (cx + w > x + maxw && cx > x) { cx = x; cy += 16; }
        c.fillStyle = items[i][1]; c.fillRect(cx, cy - 5, 10, 10);
        c.fillStyle = C.ink; c.fillText(items[i][0], cx + 15, cy); cx += w;
      }
    };
    QB.widget(el, {
      title: "One unchecked copy into an 80-byte frame",
      sub: "greet keeps a 64-byte buffer at the bottom of its frame and the address it will return to at byte 76. gets copies the input upward with no bound, then writes a zero byte. Lengthen the input until it reaches the return address, switch from plain letters to the attack (code, padding, then the buffer's own address), and turn on each defence to see which step it stops.",
      panels: 2, height: 310, weights: [1.15, 1],
      controls: [
        { k: "len", label: "Bytes of input", min: 0, max: 95, step: 1, value: 3 },
        { k: "kind", label: "The input is", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return KIND[x]; } },
        { k: "canary", label: "Stack canary", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "on" : "off"; } },
        { k: "nx", label: "No-execute stack", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "on" : "off"; } },
      ],
      draw: function (g, v, s) {
        var c = g.ctx, b = g[0].box, o = outcome(v), i, r, k;
        s.out = o;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The stack, low addresses at the bottom", b.x + 12, b.y + 8);
        var x0 = b.x + 40, y0 = b.y + 32, gw = b.w - 52, gh = b.h - 32 - 62, cw = gw / 16, ch = gh / 6;
        c.font = "11px system-ui, sans-serif"; c.textBaseline = "middle";
        for (r = 0; r < 6; r++) {
          var y = y0 + (5 - r) * ch;
          c.fillStyle = C.muted; c.textAlign = "right"; c.fillText("+" + 16 * r, x0 - 6, y + ch / 2);
          for (k = 0; k < 16; k++) {
            i = 16 * r + k;
            var reg = region(i, v.canary), x = x0 + k * cw;
            c.globalAlpha = i < v.len ? 1 : 0.28; c.fillStyle = i < v.len ? inputColor(i, v.kind) : BASE[reg];
            c.fillRect(x + 1, y + 1, cw - 2, ch - 2);
            c.globalAlpha = 1;
            if (i === v.len) { c.fillStyle = C.ink; c.fillRect(x + 1, y + 1, cw - 2, ch - 2); if (cw > 11) { c.fillStyle = C.bg; c.textAlign = "center"; c.fillText("0", x + cw / 2, y + ch / 2); } }
            if (reg !== "buf" && reg !== "above" && i >= v.len) { c.strokeStyle = BASE[reg]; c.lineWidth = 1; c.strokeRect(x + 1.5, y + 1.5, cw - 3, ch - 3); }
          }
        }
        var items = [["buffer", BASE.buf], ["gap", BASE.gap]];
        if (v.canary) items.push(["canary", BASE.canary]);
        items.push(["return address", BASE.ra], ["caller's stack", BASE.above], ["input", C.house]);
        if (v.kind) { items[items.length - 1] = ["input: code", C.q]; items.push(["padding", C.house], ["address", C.implied]); }
        flow(c, items, b.x + 12, y0 + gh + 14, b.w - 24);
        // what happens, step by step
        var d = g[1].box, lx = d.x + 14, ly = d.y + 8, line = function (color, text) {
          c.fillStyle = color; c.beginPath(); c.arc(lx + 4, ly + 9, 4, 0, 6.2832); c.fill();
          c.fillStyle = C.ink; c.font = "12px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top"; c.fillText(text, lx + 16, ly + 2); ly += 25;
        };
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("What the processor does", lx, ly); ly += 28;
        line(C.spot, "gets copies " + v.len + (v.len === 1 ? " byte" : " bytes") + " and a zero byte");
        line(v.len <= 63 ? C.gain : C.idea, v.len <= 63 ? "the copy stays inside the buffer" : "the copy runs " + (v.len - 63) + " past the buffer");
        if (o.canary !== "none") line(o.canary === "intact" ? C.gain : C.loss, o.canary === "intact" ? "canary intact: greet may return" : "canary changed: the program stops");
        if (o.ret) line(o.ret === "caller" ? C.gain : C.loss, o.ret === "caller" ? "ret goes back to the caller" : o.ret === "buffer" ? "ret jumps into the buffer" : "ret jumps to a wrong address");
        if (o.run) line(o.run === "runs" ? C.loss : C.gain, o.run === "runs" ? "the input's bytes run as code" : "the stack may not be executed");
        ly += 8;
        c.fillStyle = C.muted; c.font = "11px system-ui, sans-serif"; c.fillText("the console shows", lx, ly); ly += 18;
        c.fillStyle = "#0b0e14"; c.fillRect(lx, ly, d.w - 28, 30);
        c.fillStyle = o.console === "pwned" ? C.loss : C.ink; c.font = "12px ui-monospace, monospace"; c.textBaseline = "middle"; c.fillText(o.console, lx + 8, ly + 15);
        c.restore();
      },
      readout: function (v, s) {
        var reach = v.len < 64 ? "in the buffer" : v.len < 72 ? "in the gap" : v.len < 76 ? (v.canary ? "in the canary" : "in the gap") : v.len < 80 ? "in the return address" : "past the frame";
        return [["bytes copied", String(v.len) + " + 1"], ["the zero byte lands", reach], ["result", s.out.verdict]];
      },
      note: "A model of the part's Pebble program, not a real exploit: the film's attack is 72 bytes of code, 4 of padding and the buffer's 4-byte address, then a newline. The canary is assumed unknown to the attacker. Randomizing the stack's address and checking the buffer's bounds are the part's other two defences; neither is drawn here.",
    });
  };

  // ---- Part 12: (a+)+b against a row of a's -----------------------------------------------------------------
  W.regexblowup = function (el) {
    var NMAX = 30, SHOWN = 14;
    // step counts of the part's two matchers on this pattern (explainer/cs/lang/regex.py; Lab 12 asserts them)
    var back = function (n, hasB) { return hasB ? 2 * n + 10 : 7 * Math.pow(2, n) - 2; };
    var sets = function (n, hasB) { return n === 1 ? (hasB ? 12 : 10) : 13 * n - (hasB ? 2 : 4); };
    var group = function (x) { return String(Math.round(x)).replace(/\B(?=(\d{3})+(?!\d))/g, ","); };
    QB.widget(el, {
      title: "(a+)+b against a row of a's",
      sub: "The pattern says: one or more a's, one or more times, then b. On aaa…ab a backtracking matcher succeeds on its first try. Take the b away and it must try every way of cutting the a's into groups before it can say no, and each extra a doubles the work. A matcher that follows all the automaton's states at once never backs up.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Number of a's, n", min: 1, max: NMAX, step: 1, value: 6 },
        { k: "b", label: "The text ends in", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "b (a match)" : "a (no match)"; } },
      ],
      draw: function (g, v, s) {
        var ns = [], yb = [], ys = [], n, i, k, c = g.ctx;
        for (n = 1; n <= NMAX; n++) { ns.push(n); yb.push(back(n, v.b)); ys.push(sets(n, v.b)); }
        s.out = [back(v.n, v.b), sets(v.n, v.b), Math.pow(2, v.n - 1)];
        // the ways to cut n a's into groups, as the backtracker tries them: longest first group first
        var d = g[0].box, x0 = d.x + 14, y0 = d.y + 34, total = s.out[2], rows = Math.min(total, SHOWN), rh = Math.min(16, (d.h - 34 - 30) / SHOWN);
        var cw = Math.min(18, (d.w - 28 - 70) / v.n), gap = Math.min(5, cw * 0.45);
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText(v.b ? "The first try matches" : "Every way to cut " + v.n + (v.n === 1 ? " a" : " a's") + " into groups fails", x0, d.y + 8);
        for (i = 0; i < rows; i++) {
          // row i: bit k of i set means a cut after position n - 1 - k (so row 0 is one group of all the a's)
          var x = x0, live = v.b ? i === 0 : true, colors = [C.spot, C.q], gi = 0;
          for (k = 0; k < v.n; k++) {
            c.globalAlpha = live ? 1 : 0.22; c.fillStyle = colors[gi % 2];
            c.fillRect(x, y0 + i * rh + 1, cw - 1, rh - 3);
            x += cw;
            if (k < v.n - 1 && ((i >> (v.n - 2 - k)) & 1)) { x += gap; gi++; }
          }
          c.globalAlpha = live ? 1 : 0.22; c.fillStyle = v.b && i === 0 ? C.gain : C.loss; c.font = "11px ui-monospace, monospace"; c.textBaseline = "middle";
          c.fillText(v.b ? (i === 0 ? "b ✓" : "") : "b ✗", Math.min(x + 6, d.x + d.w - 40), y0 + i * rh + rh / 2 - 1);
        }
        c.globalAlpha = 1; c.fillStyle = C.muted; c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "top";
        c.fillText(v.b ? "the other " + group(total - 1) + " cuts are never tried" : total > rows ? "… and " + group(total - rows) + " more: 2^(n−1) = " + group(total) + " in all" : group(total) + (total === 1 ? " way" : " ways") + " in all: 2^(n−1)", x0, y0 + SHOWN * rh + 8);
        c.restore();
        var a = g[1].axes({ x: [1, NMAX], y: [1, 1e10], logy: true, title: "Steps against the number of a's", xlabel: "number of a's, n", xticks: [1, 5, 10, 15, 20, 25, 30], yticks: [1, 100, 1e4, 1e6, 1e8, 1e10],
          yfmt: function (y) { return y >= 1e4 ? "10^" + Math.round(Math.log(y) / Math.LN10) : group(y); } });
        a.line(ns, ys, { color: C.gain, width: 2 }).line(ns, yb, { color: C.loss, width: 2 });
        a.vline(v.n, { color: C.idea });
        a.dots([v.n, v.n], [s.out[0], s.out[1]], { color: function (j) { return j ? C.gain : C.loss; }, r: 4.5 });
        a.legend([["backtracking", C.loss], ["all states at once", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["backtracking steps", group(s.out[0])], ["state-set work", group(s.out[1])], ["ways to cut the a's", group(s.out[2])],
          ["backtracking / state sets", (s.out[0] / s.out[1] >= 100 ? group(s.out[0] / s.out[1]) : fmt(s.out[0] / s.out[1], 1)) + "×"]];
      },
      note: "Step counts of the part's own naive backtracker (7·2ⁿ − 2 on a failure, 2n + 10 on a match) and of its Thompson simulation (about 13n): work counters, not seconds, on a logarithmic axis. Production backtracking engines prune some of these searches; the film's Python timings still grow about fourfold for every two added a's.",
    });
  };
})();
