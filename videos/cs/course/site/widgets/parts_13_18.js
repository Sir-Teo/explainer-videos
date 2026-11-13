// Interactives for Computer Science, Built, Parts 13-18: the compiler, lambda and types, runtimes, counting steps,
// data structures, graphs.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 13: register allocation as colouring, in SSA and after the copies come back ---------------------
  W.ssacoloring = function (el) {
    var T = 48, PAIRS = 6;
    var build = function (v, seed) { // the live ranges of one loop body: each value is a list of [from, to) pieces
      var r = QB.rng(seed + 130), vals = [], i, d, len, tops = [], bots = [];
      for (i = 0; i < 30; i++) {
        d = Math.floor(r() * (T - 3)); len = 2 + Math.floor(-Math.log(1 - 0.999 * r()) * 5);
        if (i < v.n) vals.push({ p: [[d, Math.min(T, d + len)]], kind: 0 });
      }
      for (i = 0; i < PAIRS; i++) { tops.push([0, 3 + Math.floor(r() * 10)]); bots.push([T - 3 - Math.floor(r() * 10), T]); }
      for (i = 0; i < PAIRS; i++) {
        if (i < v.c) vals.unshift({ p: [tops[i], bots[i]], kind: 1 }); // one value around the back edge
        else { vals.push({ p: [tops[i]], kind: 0 }); vals.push({ p: [bots[i]], kind: 0 }); } // a phi splits it
      }
      return vals;
    };
    var meets = function (a, b) {
      for (var i = 0; i < a.p.length; i++) for (var j = 0; j < b.p.length; j++) if (a.p[i][0] < b.p[j][1] && b.p[j][0] < a.p[i][1]) return true;
      return false;
    };
    var solve = function (vals) {
      var n = vals.length, i, j, k, adj = [], order = [];
      for (i = 0; i < n; i++) { adj.push([]); for (j = 0; j < n; j++) adj[i].push(i !== j && meets(vals[i], vals[j])); }
      for (i = 0; i < n; i++) order.push(i);
      order.sort(function (a, b) { return (vals[b].kind - vals[a].kind) || (vals[a].p[0][0] - vals[b].p[0][0]) || (a - b); });
      var col = new Array(n).fill(-1), used = 0;
      for (k = 0; k < n; k++) { // greedy: the lowest register no overlapping value holds
        i = order[k]; var taken = {};
        for (j = 0; j < n; j++) if (adj[i][j] && col[j] >= 0) taken[col[j]] = 1;
        var c = 0; while (taken[c]) c++;
        col[i] = c; used = Math.max(used, c + 1);
      }
      var live = new Array(T).fill(0), most = 0;
      for (i = 0; i < n; i++) for (j = 0; j < vals[i].p.length; j++) for (k = vals[i].p[j][0]; k < vals[i].p[j][1]; k++) live[k]++;
      for (k = 0; k < T; k++) most = Math.max(most, live[k]);
      // chordal? maximum cardinality search, then every vertex's earlier neighbours must be a clique through its latest one
      var w = new Array(n).fill(0), pos = new Array(n).fill(-1), seq = [], chordal = true, best, u, a;
      for (k = 0; k < n; k++) {
        best = -1; for (i = 0; i < n; i++) if (pos[i] < 0 && (best < 0 || w[i] > w[best])) best = i;
        pos[best] = k; seq.push(best);
        for (j = 0; j < n; j++) if (adj[best][j] && pos[j] < 0) w[j]++;
      }
      for (k = 0; k < n && chordal; k++) {
        i = seq[k]; u = -1;
        for (j = 0; j < n; j++) if (adj[i][j] && pos[j] < k && (u < 0 || pos[j] > pos[u])) u = j;
        if (u < 0) continue;
        for (a = 0; a < n; a++) if (adj[i][a] && pos[a] < k && a !== u && !adj[u][a]) { chordal = false; break; }
      }
      return { col: col, used: used, live: live, most: most, chordal: chordal };
    };
    QB.widget(el, {
      title: "Registers as colours: one loop body, in SSA and after its phi-functions become copies",
      sub: "Each bar is a value, drawn from its definition to its last use and placed in the row of the register a greedy colouring gives it. In SSA (no copies) the rows used equal the most values live at once. Turn phi-functions into copies around the back edge and the same code can need an extra row; lower the register count and the rows that no longer exist are spilled.",
      panels: 2, height: 320, weights: [1.35, 1],
      controls: [
        { k: "n", label: "Values in the loop body", min: 6, max: 30, step: 1, value: 18 },
        { k: "c", label: "Phi-functions replaced by copies", min: 0, max: PAIRS, step: 1, value: 0 },
        { k: "k", label: "Registers", min: 2, max: 13, step: 1, value: 8 },
      ],
      buttons: [{ label: "New program", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var vals = build(v, s.seed), r = solve(vals), rows = Math.max(r.used, v.k), i, j, spilled = 0;
        for (i = 0; i < vals.length; i++) if (r.col[i] >= v.k) spilled++;
        s.out = [r.most, r.used, spilled, r.chordal, vals.length];
        var yt = []; for (i = 0; i < rows; i++) yt.push(i + 0.5);
        var a = g[0].axes({ x: [0, T], y: [rows, 0], yticks: yt, yfmt: function (y) { return "r" + Math.floor(y); }, title: "Which value holds which register", xlabel: "program point in the loop body", xticks: [0, 12, 24, 36, 48] });
        a.clip(function (c) {
          if (rows > v.k) { c.fillStyle = "rgba(248,113,113,0.13)"; c.fillRect(a.x0, a.py(v.k), a.w, a.py(rows) - a.py(v.k)); }
          var hgt = Math.max(3, Math.abs(a.py(1) - a.py(0)) - 4);
          for (i = 0; i < vals.length; i++) for (j = 0; j < vals[i].p.length; j++) {
            c.fillStyle = r.col[i] >= v.k ? C.loss : vals[i].kind ? C.idea : C.spot;
            c.globalAlpha = 0.9;
            c.fillRect(a.px(vals[i].p[j][0]) + 1, a.py(r.col[i]) + 2, Math.max(2, a.px(vals[i].p[j][1]) - a.px(vals[i].p[j][0]) - 2), hgt);
          }
        });
        a.legend([["in a register", C.spot], ["carried around the back edge", C.idea], ["spilled", C.loss]], { pos: "br" });
        var xs = [], ys = [];
        for (i = 0; i < T; i++) { xs.push(i, i + 1); ys.push(r.live[i], r.live[i]); }
        var top = Math.max(r.used, v.k, r.most) + 2;
        var b = g[1].axes({ x: [0, T], y: [0, top], title: "Values live at each point", xlabel: "program point", xticks: [0, 12, 24, 36, 48] });
        b.area(xs, ys, 0, { color: C.spot, alpha: 0.3 }).line(xs, ys, { color: C.spot, width: 1.5 });
        b.hline(v.k, { color: C.loss, dash: [5, 4], width: 1.4 }).hline(r.used, { color: C.idea, dash: [2, 3], width: 1.6 });
        b.legend([["live values", C.spot], ["rows the colouring uses", C.idea], ["registers", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["most values live at once", String(s.out[0])], ["registers the colouring uses", String(s.out[1])], ["interference graph chordal", s.out[3] ? "yes" : "no"], ["values spilled", s.out[2] + " of " + s.out[4]]];
      },
      note: "Simulated live ranges, not a compiled program. With no copies the interference graph is an interval graph, which is chordal, and greedy colouring in order of definition is optimal. A value carried around the back edge must keep one register at both ends of the loop; the greedy colouring is then a heuristic, as in production allocators.",
    });
  };

  // ---- Part 14: Church arithmetic, reduced in the browser under two strategies --------------------------------
  W.churchbeta = function (el) {
    var LIMIT = 1200, fresh = 0, memo = {};
    var V = function (x) { return ["v", x]; }, Lm = function (x, b) { return ["l", x, b]; }, Ap = function (f, a) { return ["a", f, a]; };
    var size = function (t) { return t[0] === "v" ? 1 : t[0] === "l" ? 1 + size(t[2]) : 1 + size(t[1]) + size(t[2]); };
    var free = function (t, bound, out) {
      if (t[0] === "v") { if (!bound[t[1]]) out[t[1]] = 1; } else if (t[0] === "a") { free(t[1], bound, out); free(t[2], bound, out); }
      else { var had = bound[t[1]]; bound[t[1]] = 1; free(t[2], bound, out); if (!had) delete bound[t[1]]; }
      return out;
    };
    var subst = function (t, x, s, fv) { // t[x := s], renaming a bound variable that would capture a free one of s
      if (t[0] === "v") return t[1] === x ? s : t;
      if (t[0] === "a") return Ap(subst(t[1], x, s, fv), subst(t[2], x, s, fv));
      if (t[1] === x) return t;
      if (fv[t[1]]) { var y = "_" + (fresh++); return Lm(y, subst(subst(t[2], t[1], V(y), {}), x, s, fv)); }
      return Lm(t[1], subst(t[2], x, s, fv));
    };
    var contract = function (t) { return subst(t[1][2], t[1][1], t[2], free(t[2], {}, {})); };
    var step = function (t, inner) { // one beta-step: leftmost-outermost (normal order) or leftmost-innermost (applicative)
      var r;
      if (t[0] === "v") return null;
      if (t[0] === "l") { r = step(t[2], inner); return r ? Lm(t[1], r) : null; }
      if (!inner && t[1][0] === "l") return contract(t);
      r = step(t[1], inner); if (r) return Ap(r, t[2]);
      r = step(t[2], inner); if (r) return Ap(t[1], r);
      return inner && t[1][0] === "l" ? contract(t) : null;
    };
    var church = function (n) { var b = V("x"), i; for (i = 0; i < n; i++) b = Ap(V("f"), b); return Lm("f", Lm("x", b)); };
    var number = function (t) { // the n of a Church numeral, or -1
      if (t[0] !== "l" || t[2][0] !== "l") return -1;
      var f = t[1], x = t[2][1], b = t[2][2], n = 0;
      while (b[0] === "a" && b[1][0] === "v" && b[1][1] === f) { b = b[2]; n++; }
      return b[0] === "v" && b[1] === x && f !== x ? n : -1;
    };
    var OMEGA = Ap(Lm("x", Ap(V("x"), V("x"))), Lm("x", Ap(V("x"), V("x"))));
    var OPS = [
      ["plus", Lm("m", Lm("n", Lm("f", Lm("x", Ap(Ap(V("m"), V("f")), Ap(Ap(V("n"), V("f")), V("x")))))))],
      ["times", Lm("m", Lm("n", Lm("f", Ap(V("m"), Ap(V("n"), V("f"))))))],
      ["pow", Lm("m", Lm("n", Ap(V("n"), V("m"))))],
      ["second Ω", Lm("a", Lm("b", V("b")))],
    ];
    var run = function (op, m, n, inner) {
      var key = [op, m, n, inner ? 1 : 0].join(","), t, k, sizes, big = 0, nx;
      if (memo[key]) return memo[key];
      t = op === 3 ? Ap(Ap(OPS[3][1], OMEGA), church(n)) : Ap(Ap(OPS[op][1], church(m)), church(n));
      sizes = [size(t)];
      for (k = 0; k < LIMIT; k++) { nx = step(t, inner); if (!nx) break; t = nx; sizes.push(size(t)); }
      for (nx = 0; nx < sizes.length; nx++) big = Math.max(big, sizes[nx]);
      return (memo[key] = { steps: k, done: k < LIMIT, sizes: sizes, big: big, value: k < LIMIT ? number(t) : -1 });
    };
    QB.widget(el, {
      title: "Arithmetic with functions alone, counted in beta-steps",
      sub: "The term is reduced here, one beta-step at a time, by normal order (leftmost-outermost, thin blue) and by applicative order (innermost first, thick gold); where the two agree the blue line runs inside the gold one. Change the numerals and the operation and watch the step counts; then choose 'second Ω', a function that ignores its first argument, applied to a term with no normal form.",
      panels: 2, height: 300,
      controls: [
        { k: "op", label: "Operation", min: 0, max: 3, step: 1, value: 2, fmt: function (x) { return OPS[x][0]; } },
        { k: "m", label: "m", min: 1, max: 4, step: 1, value: 2 },
        { k: "n", label: "n", min: 1, max: 4, step: 1, value: 3 },
      ],
      draw: function (g, v, s) {
        var a = run(v.op, v.m, v.n, false), b = run(v.op, v.m, v.n, true), i, xs, cut = Math.max(a.steps, b.done ? b.steps : Math.min(b.steps, Math.max(40, 3 * a.steps)));
        s.out = [a, b];
        var top = 0, ya = a.sizes.slice(0, cut + 1), yb = b.sizes.slice(0, cut + 1);
        for (i = 0; i < ya.length; i++) top = Math.max(top, ya[i]);
        for (i = 0; i < yb.length; i++) top = Math.max(top, yb[i]);
        var p = g[0].axes({ x: [0, Math.max(cut, 4)], y: [0, 1.15 * top + 1], title: "Size of the term after each step", xlabel: "beta-steps" });
        xs = QB.linspace(0, yb.length - 1, Math.max(yb.length, 2));
        p.line(xs.slice(0, yb.length), yb, { color: C.idea, width: 4.5, alpha: 0.75 });
        xs = QB.linspace(0, ya.length - 1, Math.max(ya.length, 2));
        p.line(xs.slice(0, ya.length), ya, { color: C.spot, width: 1.8 });
        if (b.done) p.dots([b.steps], [b.sizes[b.steps]], { color: C.idea, r: 6 });
        else p.text(cut, yb[yb.length - 1], "still running", { color: C.idea, align: "right", dx: -6, dy: -12, bg: true });
        p.dots([a.steps], [a.sizes[a.steps]], { color: C.spot, r: 3.5 });
        p.legend([["normal order", C.spot], ["applicative order", C.idea]], { pos: "tl" });
        var ns = [1, 2, 3, 4], sa = [], sb = [];
        for (i = 0; i < 4; i++) { sa.push(Math.max(1, run(v.op, v.m, ns[i], false).steps)); sb.push(Math.max(1, run(v.op, v.m, ns[i], true).steps)); }
        var q = g[1].axes({ x: [0.5, 4.5], y: [1, 2000], logy: true, xticks: ns, title: "Beta-steps against n" + (v.op === 3 ? "" : ", at m = " + v.m), xlabel: "n" });
        q.hline(LIMIT, { color: C.loss });
        q.text(0.5, LIMIT, "cut off: " + LIMIT + " steps", { color: C.loss, dx: 6, dy: 10 });
        q.line(ns, sb, { color: C.idea, width: 4.5, alpha: 0.75 }).dots(ns, sb, { color: C.idea, r: 5 });
        q.line(ns, sa, { color: C.spot, width: 1.8 }).dots(ns, sa, { color: C.spot, r: 3 });
        q.vline(v.n, { color: C.muted });
      },
      readout: function (v, s) {
        var a = s.out[0], b = s.out[1], name = v.op === 3 ? "(λa b. b) Ω " + v.n : OPS[v.op][0] + " " + v.m + " " + v.n;
        var show = function (r) { return r.done ? r.steps + " steps" : "no normal form in " + LIMIT + " steps"; };
        return [["term", name], ["result", a.done ? (a.value >= 0 ? "the numeral " + a.value : "not a numeral") : "none"], ["normal order", show(a)], ["applicative order", show(b)], ["largest term", Math.max(a.big, b.big) + " nodes"]];
      },
      note: "Computed in your browser by a small reducer with capture-avoiding substitution; numerals are λf. λx. f (f ... x). Step counts belong to these encodings and these two strategies. Ω = (λx. x x)(λx. x x) reduces to itself, so a strategy that evaluates arguments first never returns; normal order finds a normal form whenever one exists.",
    });
  };

  // ---- Part 15: a semispace collector's sawtooth, and its cost L / (S - L) ----------------------------------
  W.cheneycost = function (el) {
    var A = 10000;
    var world = function (L, seed) { // lifetimes, in words allocated: four in five objects die young, the rest carry the live data
      var r = QB.rng(seed + 150), tau = Math.max(20, 5 * (L - 12)), start = [], death = [], i;
      var expo = function (mean) { return -mean * Math.log(1 - 0.999999 * r()); };
      for (i = 0; i < Math.round(0.2 * tau); i++) start.push(expo(tau)); // the long-lived objects already there
      for (i = 0; i < A; i++) death.push(i + (r() < 0.8 ? expo(15) : expo(tau)));
      return { start: start, death: death };
    };
    var collect = function (S, w, trace) { // allocate A one-word objects in a semispace of S words
      var old = w.start.slice(), young = [], used = old.length, copied = 0, n = 0, t, i, keep, oom = used >= S;
      if (trace) { trace.x.push(0); trace.y.push(used); }
      for (t = 0; t < A && !oom; t++) {
        if (used >= S) { // full: copy what is still reachable into the other half
          keep = [];
          for (i = 0; i < old.length; i++) if (old[i] > t) keep.push(old[i]);
          for (i = 0; i < young.length; i++) if (young[i] > t) keep.push(young[i]);
          if (trace) { trace.x.push(t, t); trace.y.push(used, keep.length); trace.cx.push(t); trace.cy.push(keep.length); }
          old = keep; young = []; used = keep.length; copied += used; n++;
          if (used >= S) { oom = true; break; }
        }
        young.push(w.death[t]); used++;
      }
      if (trace) { trace.x.push(t); trace.y.push(used); }
      return { copied: copied, n: n, oom: oom, done: t, live: n ? copied / n : w.start.length };
    };
    QB.widget(el, {
      title: "Cheney's collector: memory against copying",
      sub: "A simulated program allocates ten thousand one-word objects; most die young and the rest hold the live data. When the semispace is full the collector copies what is still reachable (green) into the other half. Shrink the semispace towards the live data and watch the collections crowd together and the cost per allocated word climb the gold curve, until the program no longer fits.",
      panels: 2, height: 300,
      controls: [
        { k: "S", label: "Semispace S (words)", min: 200, max: 2000, step: 20, value: 700 },
        { k: "L", label: "Live data L (words)", min: 50, max: 800, step: 10, value: 300 },
      ],
      buttons: [{ label: "New run", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var w = world(v.L, s.seed), tr = { x: [], y: [], cx: [], cy: [] }, r = collect(v.S, w, tr), i, S, q;
        s.out = r;
        var a = g[0].axes({ x: [0, A], y: [0, Math.max(v.S, r.live) * 1.18], title: "Words in use as the program allocates", xlabel: "words allocated so far" });
        a.hline(v.S, { color: C.loss, dash: [5, 4], width: 1.4 });
        a.line(tr.x, tr.y, { color: C.spot, width: 1.3 });
        a.dots(tr.cx, tr.cy, { color: C.gain, r: 2.6 });
        a.legend([["in use", C.spot], ["live after a collection", C.gain], ["semispace", C.loss]], { pos: "br" });
        if (r.oom) a.text(A / 2, Math.max(v.S, r.live) * 0.5, "out of memory: the live data does not fit", { color: C.loss, align: "center", bg: true });
        var xs = [], ys = [], mx = [], my = [];
        for (S = 200; S <= 2000; S += 150) { q = collect(S, w, null); if (!q.oom) { xs.push(S); ys.push(q.copied / A); } }
        for (S = 200; S <= 2000; S += 10) if (S > r.live * 1.02) { mx.push(S); my.push(r.live / (S - r.live)); }
        var b = g[1].axes({ x: [200, 2000], y: [0, 3], title: "Words copied per word allocated", xlabel: "semispace S (words)", xticks: [200, 500, 1000, 1500, 2000] });
        if (r.live > 200) b.area([200, Math.min(2000, r.live)], [3, 3], 0, { color: C.loss, alpha: 0.13 });
        if (mx.length > 1) b.line(mx, my, { color: C.idea, width: 1.8 });
        b.dots(xs, ys, { color: C.spot, r: 3.2 });
        b.vline(v.S, { color: C.muted });
        b.legend([["simulated", C.spot], ["L / (S − L)", C.idea], ["S below L: no room", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var r = s.out, room = v.S - r.live;
        return [["collections", r.oom ? r.n + ", then out of memory" : String(r.n)], ["live at a collection, mean", fmt(r.live, 0) + " words"],
          ["copied per word allocated", r.oom ? "does not finish" : fmt(r.copied / A, 2)], ["L / (S − L)", room > 1 ? fmt(r.live / room, 2) : "no room"], ["memory reserved", 2 * v.S + " words"]];
      },
      note: "Simulated data: object lifetimes are random, objects are one word, and roots, scanning and bookkeeping cost nothing. The gold curve uses the mean live size measured at this run's collections. A copying collector reserves two semispaces and never touches garbage, so its work is the live data, once per collection.",
    });
  };

  // ---- Part 16: quicksort's comparisons, by pivot rule and by how sorted the input already is ----------------
  W.pivotluck = function (el) {
    var RULES = ["first element", "median of three", "random"];
    var lgfact = function (n) { var s = 0, i; for (i = 2; i <= n; i++) s += Math.log(i); return s / Math.LN2; };
    var expected = function (n) { var h = 0, i; for (i = 1; i <= n; i++) h += 1 / i; return 2 * (n + 1) * h - 4 * n; };
    var input = function (n, d, r) { // sorted, then each position swapped with an earlier one with probability d
      var a = [], i, j, t;
      for (i = 0; i < n; i++) a.push(i);
      for (i = n - 1; i > 0; i--) if (r() < d) { j = Math.floor(r() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    };
    var count = function (a, rule, r) { // key comparisons of quicksort on distinct keys
      var n = a.length, p, c = n - 1, lo = [], hi = [], i, x, y, z;
      if (n <= 1) return 0;
      if (rule === 0) p = a[0];
      else if (rule === 2) p = a[Math.floor(r() * n)];
      else { x = a[0]; y = a[n >> 1]; z = a[n - 1]; p = Math.max(Math.min(x, y), Math.min(Math.max(x, y), z)); c += n > 2 ? 3 : 1; }
      for (i = 0; i < n; i++) { if (a[i] < p) lo.push(a[i]); else if (a[i] > p) hi.push(a[i]); }
      return c + count(lo, rule, r) + count(hi, rule, r);
    };
    QB.widget(el, {
      title: "How lucky does quicksort need to be?",
      sub: "Each dot is one run of quicksort, placed at the number of key comparisons it made, between the lower bound lg n! (red) and the worst case n(n − 1)/2 (grey). With random pivots the runs sit near 2(n + 1)Hₙ − 4n (gold) whatever the input. Switch to the first element as pivot and slide the disorder to zero: on sorted input every run pays the worst case.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Keys n", min: 20, max: 400, step: 10, value: 200 },
        { k: "rule", label: "Pivot rule", min: 0, max: 2, step: 1, value: 2, fmt: function (x) { return RULES[x]; } },
        { k: "d", label: "Disorder of the input", min: 0, max: 100, step: 5, value: 100, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New inputs", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 160), n = v.n, d = v.d / 100, runs = [], ys = [], i, m, sum;
        for (i = 0; i < 50; i++) { runs.push(count(input(n, d, r), v.rule, r)); ys.push(0.06 + 0.6 * r()); }
        var lo = lgfact(n), ex = expected(n), hi = n * (n - 1) / 2, mean = QB.mean(runs);
        s.out = [mean, ex, lo, hi];
        var a = g[0].axes({ x: [0.8 * lo, 1.25 * hi], y: [0, 1], logx: true, noY: true, title: "50 runs at n = " + n + ", " + RULES[v.rule] + " as pivot", xlabel: "key comparisons (log scale)" });
        a.vline(lo, { color: C.loss, dash: [], width: 1.6 }).vline(ex, { color: C.idea, dash: [], width: 1.6 }).vline(hi, { color: C.cash, dash: [], width: 1.6 });
        a.dots(runs, ys, { color: C.spot, r: 3, alpha: 0.8 });
        a.legend([["one run", C.spot], ["lg n!", C.loss], ["2(n + 1)Hₙ − 4n", C.idea], ["n(n − 1)/2", C.cash]], { pos: "tr" });
        var ns = [20, 40, 80, 160, 280, 400], ms = [], l = [], e = [], w = [], gx = [];
        for (i = 0; i < ns.length; i++) { sum = 0; for (m = 0; m < 8; m++) sum += count(input(ns[i], d, r), v.rule, r); ms.push(sum / 8); }
        for (m = 20; m <= 400; m += 10) { gx.push(m); l.push(lgfact(m)); e.push(expected(m)); w.push(m * (m - 1) / 2); }
        var b = g[1].axes({ x: [20, 400], y: [40, 100000], logx: true, logy: true, xticks: [20, 50, 100, 200, 400], title: "Mean comparisons against n", xlabel: "n" });
        b.line(gx, w, { color: C.cash, width: 1.4 }).line(gx, e, { color: C.idea, width: 1.6 }).line(gx, l, { color: C.loss, width: 1.4 });
        b.line(ns, ms, { color: C.spot, width: 1.2 }).dots(ns, ms, { color: C.spot, r: 3.5 });
        b.vline(n, { color: C.muted });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["mean comparisons", fmt(o[0], 0)], ["2(n + 1)Hₙ − 4n", fmt(o[1], 0)], ["mean / expected", fmt(o[0] / o[1], 2)], ["lg n!", fmt(o[2], 0)], ["n(n − 1)/2", fmt(o[3], 0)]];
      },
      note: "Simulated inputs: n distinct keys, sorted, then each position swapped with a random earlier one with the probability set by the disorder slider (100% is a uniform shuffle). One comparison is counted per key per partition, plus three to find a median of three. Deterministic rules vary only with the input; the random rule varies with its own coin flips.",
    });
  };

  // ---- Part 17: an open-addressing table filling up, and the probes a miss costs -----------------------------
  W.probeclusters = function (el) {
    var M = 512, COLS = 32, NAMES = ["linear probing", "double hashing"];
    var fill = function (v, seed) {
      var r = QB.rng(seed + 170), t = new Array(M).fill(0), q = v.bad / 100, target = Math.round(v.load / 100 * M), n, s, d, marks = [], costs = [];
      var home = function () { return r() < q ? Math.floor(r() * M / 8) : Math.floor(r() * M); };
      var miss = function () { // mean probes of an unsuccessful search in the table as it stands
        var i, k, sum = 0, w, tot = 0, dist = new Array(M).fill(0), rr = QB.rng(seed + 171), p;
        if (v.scheme === 0) { // exact: from every home, the distance to the next empty slot
          k = 0; for (i = 2 * M - 1; i >= 0; i--) { k = t[i % M] ? k + 1 : 0; if (i < M) dist[i] = Math.min(k, M) + 1; }
          for (i = 0; i < M; i++) { w = (1 - q) + (i < M / 8 ? 8 * q : 0); sum += w * dist[i]; tot += w; }
          return sum / tot;
        }
        for (k = 0; k < 400; k++) { // sampled: a fresh key's own probe sequence
          s = rr() < q ? Math.floor(rr() * M / 8) : Math.floor(rr() * M); d = 1 + 2 * Math.floor(rr() * M / 2); p = 1;
          while (t[s] && p < M) { s = (s + d) % M; p++; }
          sum += p;
        }
        return sum / 400;
      };
      for (n = 0; n < target; n++) {
        if (n % 26 === 0 && n > 0) { marks.push(n / M); costs.push(miss()); }
        s = home(); d = v.scheme === 0 ? 1 : 1 + 2 * Math.floor(r() * M / 2);
        while (t[s]) s = (s + d) % M;
        t[s] = 1;
      }
      var best = 0, at = 0, run = 0, i;
      for (i = 0; i < 2 * M; i++) { if (t[i % M]) { run++; if (run > best && run <= M) { best = run; at = i; } } else run = 0; }
      return { t: t, n: target, marks: marks, costs: costs, now: miss(), best: best, at: at };
    };
    QB.widget(el, {
      title: "A hash table filling up: clusters, and what a miss costs",
      sub: "Keys are inserted one by one into 512 slots, drawn row by row. Raise the load and watch runs of occupied slots merge under linear probing while the cost of an unsuccessful search leaves the uniform-probing curve for Knuth's. Then give some keys a poor hash that sends them to the first eighth of the table: the constant-time promise fails at a load that looked safe.",
      panels: 2, height: 310,
      controls: [
        { k: "load", label: "Load (keys / slots)", min: 5, max: 95, step: 1, value: 60, fmt: function (x) { return x + "%"; } },
        { k: "scheme", label: "Collision rule", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return NAMES[x]; } },
        { k: "bad", label: "Keys with a poor hash", min: 0, max: 100, step: 5, value: 0, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New keys", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = fill(v, s.seed), a = v.load / 100, c = g.ctx, bx = g[0].box, i;
        s.out = [r.n, r.now, 0.5 * (1 + 1 / ((1 - a) * (1 - a))), 1 / (1 - a), r.best];
        var rows = M / COLS, cell = Math.min((bx.w - 28) / COLS, (bx.h - 78) / rows), x0 = bx.x + (bx.w - cell * COLS) / 2, y0 = bx.y + 30;
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The table: " + r.n + " of " + M + " slots occupied", x0, bx.y + 6);
        for (i = 0; i < M; i++) {
          var inBest = r.best > 1 && ((r.at - i + 2 * M) % M) < r.best;
          c.fillStyle = r.t[i] ? (inBest ? C.idea : C.spot) : "#1d2533";
          c.fillRect(x0 + (i % COLS) * cell + 0.5, y0 + Math.floor(i / COLS) * cell + 0.5, cell - 1, cell - 1);
        }
        c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "top";
        var ly = y0 + rows * cell + 8, lx = x0;
        [["occupied", C.spot], ["the longest run", C.idea], ["empty", "#2a3446"]].forEach(function (it) {
          c.fillStyle = it[1]; c.fillRect(lx, ly + 1, 10, 10); c.fillStyle = C.muted; c.fillText(it[0], lx + 14, ly); lx += 22 + c.measureText(it[0]).width + 10;
        });
        c.fillStyle = C.muted; c.fillText("slots read left to right, row after row", x0, ly + 17);
        c.restore();
        var xs = QB.linspace(0.02, 0.95, 94), k = [], u = [];
        for (i = 0; i < xs.length; i++) { k.push(0.5 * (1 + 1 / ((1 - xs[i]) * (1 - xs[i])))); u.push(1 / (1 - xs[i])); }
        var b = g[1].axes({ x: [0, 1], y: [1, 300], logy: true, title: "Probes for an unsuccessful search", xlabel: "load", xticks: [0, 0.25, 0.5, 0.75, 1] });
        b.line(xs, u, { color: C.cash, width: 1.4, dash: [5, 4] }).line(xs, k, { color: C.idea, width: 1.8 });
        b.dots(r.marks, r.costs, { color: C.spot, r: 2.6 }).dots([a], [r.now], { color: C.spot, r: 5 });
        b.vline(a, { color: C.muted });
        b.legend([["this table, as it filled", C.spot], ["linear probing (Knuth)", C.idea], ["uniform probing: 1/(1 − α)", C.cash]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["keys", String(o[0])], ["probes for a miss, this table", fmt(o[1], 2)], ["Knuth, linear probing", fmt(o[2], 2)], ["uniform probing", fmt(o[3], 2)], ["longest run", o[4] + " slots"]];
      },
      note: "Simulated keys with random homes; a key with a poor hash has its home in the first 64 slots. For linear probing the miss cost is exact for the table shown (averaged over the homes a new key would get); for double hashing it is sampled over 400 new keys. Knuth's formula ½(1 + 1/(1 − α)²) assumes random homes and a large table.",
    });
  };

  // ---- Part 18: Dijkstra, A* and an estimate that overshoots, on a grid of streets --------------------------
  W.astarweight = function (el) {
    var COLS = 36, ROWS = 22, N = COLS * ROWS, SRC = 11 * COLS + 2;
    var city = function (v, seed) { // blocked cells; the source and the target stay open
      var r = QB.rng(seed + 180), wall = new Array(N), i;
      for (i = 0; i < N; i++) wall[i] = r() < v.walls / 100;
      wall[SRC] = false; wall[11 * COLS + v.tx] = false;
      return wall;
    };
    var search = function (wall, tgt, w) { // best-first on g + w * (Manhattan distance to the target), on a binary heap
      var g = new Array(N).fill(-1), par = new Array(N).fill(-1), closed = new Array(N).fill(false), heap = [], order = [], tx = tgt % COLS, ty = Math.floor(tgt / COLS);
      var h = function (c) { return Math.abs(c % COLS - tx) + Math.abs(Math.floor(c / COLS) - ty); };
      var less = function (a, b) { return a[0] < b[0] - 1e-9 || (Math.abs(a[0] - b[0]) <= 1e-9 && a[1] < b[1]); };
      var push = function (e) { var i = heap.length, p; heap.push(e); while (i > 0) { p = (i - 1) >> 1; if (!less(heap[i], heap[p])) break; e = heap[i]; heap[i] = heap[p]; heap[p] = e; i = p; } };
      var pop = function () {
        var top = heap[0], last = heap.pop(), i = 0, l, m, t;
        if (heap.length) { heap[0] = last; for (;;) { l = 2 * i + 1; m = i; if (l < heap.length && less(heap[l], heap[m])) m = l; if (l + 1 < heap.length && less(heap[l + 1], heap[m])) m = l + 1; if (m === i) break; t = heap[i]; heap[i] = heap[m]; heap[m] = t; i = m; } }
        return top;
      };
      g[SRC] = 0; push([w * h(SRC), h(SRC), SRC, 0]);
      var e, c, k, nb, x, y, found = false;
      while (heap.length) {
        e = pop(); c = e[2];
        if (closed[c] || e[3] !== g[c]) continue;
        closed[c] = true; order.push(c);
        if (c === tgt) { found = true; break; }
        x = c % COLS; y = Math.floor(c / COLS);
        nb = [x > 0 ? c - 1 : -1, x < COLS - 1 ? c + 1 : -1, y > 0 ? c - COLS : -1, y < ROWS - 1 ? c + COLS : -1];
        for (k = 0; k < 4; k++) if (nb[k] >= 0 && !wall[nb[k]] && !closed[nb[k]] && (g[nb[k]] < 0 || g[c] + 1 < g[nb[k]])) { g[nb[k]] = g[c] + 1; par[nb[k]] = c; push([g[nb[k]] + w * h(nb[k]), h(nb[k]), nb[k], g[nb[k]]]); }
      }
      var path = [];
      if (found) for (c = tgt; c >= 0; c = par[c]) path.push(c);
      return { order: order, path: path, len: found ? g[tgt] : -1 };
    };
    QB.widget(el, {
      title: "Exact routes with less search, until the estimate overshoots",
      sub: "A route is sought from the white cell to the red one; every step costs 1. The search expands the cell with the least (steps so far) + weight × (straight-line steps still to go). Weight 0 is Dijkstra, weight 1 is A*: both return a shortest route, and A* expands fewer cells. Push the weight above 1 and the search gets faster still, but the route it returns can be longer than the shortest.",
      panels: 2, height: 320, weights: [1.5, 1],
      controls: [
        { k: "w", label: "Weight on the estimate", min: 0, max: 3, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
        { k: "walls", label: "Blocked cells", min: 0, max: 35, step: 1, value: 22, fmt: function (x) { return x + "%"; } },
        { k: "tx", label: "Target column", min: 12, max: 34, step: 1, value: 32 },
      ],
      buttons: [{ label: "New city", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var wall = city(v, s.seed), tgt = 11 * COLS + v.tx, r = search(wall, tgt, v.w), best = search(wall, tgt, 0).len, c = g.ctx, bx = g[0].box, i;
        s.out = [r.order.length, r.len, best];
        var cell = Math.min((bx.w - 24) / COLS, (bx.h - 74) / ROWS), x0 = bx.x + (bx.w - cell * COLS) / 2, y0 = bx.y + 28;
        var put = function (k, col, inset) { c.fillStyle = col; c.fillRect(x0 + (k % COLS) * cell + inset, y0 + Math.floor(k / COLS) * cell + inset, cell - 2 * inset, cell - 2 * inset); };
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Cells expanded: " + r.order.length + (r.len < 0 ? ", no route" : ", route of " + r.len + " steps"), x0, bx.y + 6);
        for (i = 0; i < N; i++) put(i, wall[i] ? "#3a475c" : "#1a2130", 0.5);
        for (i = 0; i < r.order.length; i++) put(r.order[i], C.spot, 0.5);
        for (i = 0; i < r.path.length; i++) put(r.path[i], C.idea, 0.5);
        put(SRC, "#ffffff", 0.5); put(tgt, C.loss, 0.5);
        c.font = "11.5px system-ui, sans-serif";
        var ly = y0 + ROWS * cell + 8, lx = x0;
        [["expanded", C.spot], ["route", C.idea], ["blocked", "#3a475c"], ["source", "#ffffff"], ["target", C.loss]].forEach(function (it, j) {
          if (j === 3 && bx.w < 420) { lx = x0; ly += 16; }
          c.fillStyle = it[1]; c.fillRect(lx, ly + 1, 10, 10); c.fillStyle = C.muted; c.fillText(it[0], lx + 14, ly); lx += 24 + c.measureText(it[0]).width;
        });
        c.restore();
        var ws = [], ex = [], okx = [], oky = [], badx = [], bady = [], q, top = 1;
        for (i = 0; i <= 12; i++) {
          q = search(wall, tgt, i * 0.25); ws.push(i * 0.25); ex.push(q.order.length); top = Math.max(top, q.order.length);
          if (q.len === best) { okx.push(i * 0.25); oky.push(q.order.length); } else { badx.push(i * 0.25); bady.push(q.order.length); }
        }
        var b = g[1].axes({ x: [0, 3], y: [0, top * 1.25], title: "Cells expanded against the weight", xlabel: "weight on the estimate", xticks: [0, 1, 2, 3] });
        b.area([1, 3], [top * 1.25, top * 1.25], 0, { color: C.loss, alpha: 0.08 });
        b.line(ws, ex, { color: C.muted, width: 1.2 });
        b.dots(okx, oky, { color: C.gain, r: 3.6 }).dots(badx, bady, { color: C.loss, r: 3.6 });
        b.vline(v.w, { color: C.idea, dash: [], width: 1.4 });
        b.legend([["shortest route found", C.gain], ["a longer route", C.loss], ["current weight", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out, none = o[2] < 0;
        return [["cells expanded", String(o[0])], ["route found", o[1] < 0 ? "none" : o[1] + " steps"], ["shortest route", none ? "none: the target is walled off" : o[2] + " steps"], ["extra steps", none || o[1] < 0 ? "0" : String(o[1] - o[2])]];
      },
      note: "Simulated grid; moves go up, down, left and right. With weight at most 1 the estimate never exceeds the true remaining distance, which is the condition for an exact answer; beyond 1 (the shaded region) that guarantee is gone, though the route found is at most the weight times the shortest. Ties are broken towards the target.",
    });
  };
})();
