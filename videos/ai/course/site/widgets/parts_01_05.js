// Interactives for the foundations (Parts 1-5): codes, search, low rank, descent, decoding.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var log2 = function (x) { return Math.log(x) / Math.LN2; };
  var heading = function (c, text, x, y) { // a panel title for hand-drawn panels, in the style of Axes' titles
    c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top"; c.fillText(text, x, y);
  };

  // ---- Part 1: Huffman's code on single symbols and on blocks -------------------------------------------------
  W.huffmanblocks = function (el) {
    var names = ["Huffman", "Shannon (rounded up)"];
    var huffLen = function (p) { // codeword lengths of a Huffman code, by repeated merging (small alphabets)
      var n = p.length, nodes = [], depth = new Array(n).fill(0), i, j;
      for (i = 0; i < n; i++) nodes.push({ w: p[i], leaves: [i] });
      while (nodes.length > 1) {
        nodes.sort(function (a, b) { return a.w - b.w; });
        var a = nodes.shift(), b = nodes.shift(), m = { w: a.w + b.w, leaves: a.leaves.concat(b.leaves) };
        for (j = 0; j < m.leaves.length; j++) depth[m.leaves[j]]++;
        nodes.push(m);
      }
      return depth;
    };
    var huffMean = function (p) { // the expected length alone: the sum of the merged weights (two queues, sorted once)
      var a = Array.prototype.slice.call(p).sort(function (x, y) { return x - y; }), b = [], ia = 0, ib = 0, total = 0, k, t, pick;
      if (a.length < 2) return 1;
      for (k = 0; k < a.length - 1; k++) {
        t = 0;
        for (pick = 0; pick < 2; pick++) {
          if (ib >= b.length || (ia < a.length && a[ia] <= b[ib])) t += a[ia++]; else t += b[ib++];
        }
        b.push(t); total += t;
      }
      return total;
    };
    var shannonMean = function (p) { var s = 0; for (var i = 0; i < p.length; i++) s += p[i] * Math.ceil(log2(1 / p[i]) - 1e-9); return s; };
    QB.widget(el, {
      title: "Whole bits: a code against the entropy",
      sub: "A source of K symbols with probabilities proportional to 1/rank^s. Left: each symbol's surprise (blue) beside the length of its codeword (gold). Right: the code's bits per symbol when it is built for blocks of symbols. Raise the skew until one symbol is nearly certain: a codeword cannot be shorter than one bit, so single symbols waste almost a bit each, and blocks win it back.",
      panels: 2, height: 300,
      controls: [
        { k: "K", label: "Alphabet size K", min: 2, max: 12, step: 1, value: 3 },
        { k: "s", label: "Skew s", min: 0, max: 3, step: 0.05, value: 2.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "code", label: "Code", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return names[x]; } },
      ],
      draw: function (g, v, s) {
        var K = v.K, p = [], z = 0, i, j, n;
        for (i = 1; i <= K; i++) { p.push(Math.pow(i, -v.s)); z += p[i - 1]; }
        var H = 0, ideal = [];
        for (i = 0; i < K; i++) { p[i] /= z; ideal.push(log2(1 / p[i])); H += p[i] * ideal[i]; }
        var len = v.code === 0 ? huffLen(p) : ideal.map(function (x) { return Math.ceil(x - 1e-9); });
        var L1 = 0, kraft = 0;
        for (i = 0; i < K; i++) { L1 += p[i] * len[i]; kraft += Math.pow(2, -len[i]); }
        var ns = [], per = [], bound = [], block = p.slice(), size = K;
        for (n = 1; size <= 2048 && n <= 11; n++) {
          ns.push(n); per.push((v.code === 0 ? huffMean(block) : shannonMean(block)) / n); bound.push(H + 1 / n);
          size *= K;
          if (size <= 2048) { var nb = []; for (i = 0; i < block.length; i++) for (j = 0; j < K; j++) nb.push(block[i] * p[j]); block = nb; }
        }
        s.out = [H, L1, kraft, per[per.length - 1], ns.length];
        var idx = [], top = 1;
        for (i = 0; i < K; i++) { idx.push(i + 1); top = Math.max(top, ideal[i], len[i]); }
        var a = g[0].axes({ x: [0.3, K + 0.7], y: [0, Math.ceil(top * 1.25)], title: "Single symbols: surprise and codeword length", xlabel: "symbol, by rank", xticks: idx, ny: 4 });
        a.bars(idx.map(function (x) { return x - 0.2; }), ideal, 0.36, { color: C.spot, gap: 0 });
        a.bars(idx.map(function (x) { return x + 0.2; }), len, 0.36, { color: C.idea, gap: 0 });
        a.legend([["surprise, log2(1/p)", C.spot], ["codeword length", C.idea]], { pos: "tl" });
        var ymax = Math.max(H + 1.15, per[0] + 0.15), ymin = Math.max(0, H - 0.25), nmax = Math.max(2, ns.length);
        var b = g[1].axes({ x: [0.5, nmax + 0.5], y: [ymin, ymax], title: "Blocks of n symbols: bits per symbol", xlabel: "block length n", xticks: QB.linspace(1, nmax, nmax) });
        var fine = QB.linspace(1, nmax, 60);
        b.line(fine, fine.map(function (x) { return H + 1 / x; }), { color: C.muted, dash: [4, 4], width: 1.2 });
        b.hline(H, { color: C.gain, dash: [], width: 1.5 });
        b.line(ns, per, { color: C.idea, width: 1.6 }).dots(ns, per, { color: C.idea, r: 3.5 });
        b.legend([[names[v.code] + " code", C.idea], ["entropy H", C.gain], ["H + 1/n", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["entropy H", fmt(s.out[0], 3) + " bits"], ["code, single symbols", fmt(s.out[1], 3)], ["wasted per symbol", fmt(s.out[1] - s.out[0], 3)],
          ["blocks of " + s.out[4], fmt(s.out[3], 3)], ["Kraft sum", fmt(s.out[2], 3)]];
      },
      note: "Exact, no simulation: symbols are independent, and blocks are coded up to 2,048 block symbols. Every code shown obeys H ≤ L/n < H + 1/n; Huffman's is the shortest symbol code, and its Kraft sum is exactly 1.",
    });
  };

  // ---- Part 2: best-first search on a grid, from Dijkstra through A* to greedy --------------------------------
  W.astarweight = function (el) {
    var NC = 36, NR = 22, N = NC * NR, START = 11 * NC + 4, GOAL = 11 * NC + 31;
    var DR = [1, -1, 0, 0, 1, 1, -1, -1], DC = [0, 0, 1, -1, 1, -1, 1, -1];
    var makeMap = function (seed, density) {
      var r = QB.rng(seed * 7 + 3), wall = new Array(N).fill(false), k, i, j;
      var blocks = Math.round(density * N / 5);
      for (k = 0; k < blocks; k++) { // short walls, horizontal or vertical
        var r0 = Math.floor(r() * NR), c0 = Math.floor(r() * NC), horiz = r() < 0.5, len = 3 + Math.floor(r() * 5);
        for (i = 0; i < len; i++) { var rr = r0 + (horiz ? 0 : i), cc = c0 + (horiz ? i : 0); if (rr < NR && cc < NC) wall[rr * NC + cc] = true; }
      }
      for (i = -1; i <= 1; i++) for (j = -1; j <= 1; j++) { wall[START + i * NC + j] = false; wall[GOAL + i * NC + j] = false; }
      return wall;
    };
    var search = function (wall, w) { // f = g + w h, h the straight-line distance; ties go to the deeper node
      var g = new Array(N).fill(Infinity), parent = new Array(N).fill(-1), closed = new Array(N).fill(false), order = new Array(N).fill(-1);
      var heap = [], step = 0, gr = Math.floor(GOAL / NC), gc = GOAL % NC, k;
      var less = function (a, b) { return a[0] < b[0] - 1e-12 || (Math.abs(a[0] - b[0]) <= 1e-12 && a[1] > b[1]); };
      var push = function (e) { var i = heap.length; heap.push(e); while (i > 0) { var q = (i - 1) >> 1; if (!less(heap[i], heap[q])) break; var t = heap[i]; heap[i] = heap[q]; heap[q] = t; i = q; } };
      var pop = function () {
        var top = heap[0], last = heap.pop(), i = 0;
        if (heap.length) { heap[0] = last; for (;;) { var l = 2 * i + 1, r = l + 1, m = i; if (l < heap.length && less(heap[l], heap[m])) m = l; if (r < heap.length && less(heap[r], heap[m])) m = r; if (m === i) break; var t = heap[i]; heap[i] = heap[m]; heap[m] = t; i = m; } }
        return top;
      };
      g[START] = 0; push([0, 0, START]);
      while (heap.length) {
        var u = pop()[2];
        if (closed[u]) continue;
        closed[u] = true; order[u] = step++;
        if (u === GOAL) break;
        var ur = Math.floor(u / NC), uc = u % NC;
        for (k = 0; k < 8; k++) {
          var vr = ur + DR[k], vc = uc + DC[k];
          if (vr < 0 || vr >= NR || vc < 0 || vc >= NC) continue;
          var x = vr * NC + vc;
          if (wall[x] || closed[x]) continue;
          if (k >= 4 && (wall[ur * NC + vc] || wall[vr * NC + uc])) continue; // a diagonal step may not cut a corner
          var ng = g[u] + (k >= 4 ? Math.SQRT2 : 1);
          if (ng < g[x] - 1e-12) { g[x] = ng; parent[x] = u; push([ng + w * Math.sqrt((vr - gr) * (vr - gr) + (vc - gc) * (vc - gc)), ng, x]); }
        }
      }
      var found = closed[GOAL], path = [];
      if (found) for (var q = GOAL; q !== -1; q = parent[q]) path.push(q);
      return { found: found, cost: found ? g[GOAL] : 0, expanded: step, order: order, path: path };
    };
    var WS = QB.linspace(0, 5, 21);
    QB.widget(el, {
      title: "From Dijkstra to A* to greedy: one dial",
      sub: "Best-first search from the green cell to the red one, always expanding the cell with the smallest f = g + w·h, where g is the cost so far and h the straight-line distance to the goal. At w = 0 this is Dijkstra's algorithm, at w = 1 it is A*. Push w past 1: the search expands fewer cells (blue), but the heuristic now overestimates and the path (gold) can stop being the shortest.",
      panels: 2, height: 310, weights: [1.25, 1],
      controls: [
        { k: "w", label: "Heuristic weight w", min: 0, max: 5, step: 0.25, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "dens", label: "Walls", min: 0, max: 0.4, step: 0.02, value: 0.2, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      buttons: [{ label: "New map", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var key = s.seed + ":" + v.dens, i;
        if (s.key !== key) { // the map and the sweep over w change only with the map
          s.key = key; s.wall = makeMap(s.seed, v.dens); s.sweep = WS.map(function (w) { return search(s.wall, w); });
        }
        var cur = s.sweep[Math.round(v.w / 0.25)], opt = s.sweep[0];
        s.out = [cur.found, cur.expanded, opt.expanded, cur.cost, opt.cost];
        var c = g.ctx, bx = g[0].box, cell = Math.max(4, Math.min((bx.w - 24) / NC, (bx.h - 62) / NR)), x0 = bx.x + (bx.w - cell * NC) / 2, y0 = bx.y + 30;
        c.save();
        heading(c, "The map: cells expanded at w = " + v.w.toFixed(2), x0, bx.y + 8);
        for (i = 0; i < N; i++) {
          var px = x0 + (i % NC) * cell, py = y0 + Math.floor(i / NC) * cell;
          if (s.wall[i]) c.fillStyle = "#56627a";
          else if (cur.order[i] >= 0) { var t = cur.order[i] / Math.max(1, cur.expanded - 1); c.fillStyle = "rgb(" + Math.round(40 + 48 * t) + "," + Math.round(86 + 80 * t) + "," + Math.round(150 + 105 * t) + ")"; }
          else c.fillStyle = "#1b2330";
          c.fillRect(px + 0.5, py + 0.5, cell - 1, cell - 1);
        }
        if (cur.found) {
          c.strokeStyle = C.idea; c.lineWidth = Math.max(2, cell * 0.3); c.lineJoin = "round"; c.beginPath();
          for (i = 0; i < cur.path.length; i++) { var qx = x0 + (cur.path[i] % NC + 0.5) * cell, qy = y0 + (Math.floor(cur.path[i] / NC) + 0.5) * cell; if (i) c.lineTo(qx, qy); else c.moveTo(qx, qy); }
          c.stroke();
        }
        var dot = function (cellIndex, color) { c.fillStyle = color; c.beginPath(); c.arc(x0 + (cellIndex % NC + 0.5) * cell, y0 + (Math.floor(cellIndex / NC) + 0.5) * cell, Math.max(3.5, cell * 0.45), 0, 6.2832); c.fill(); };
        dot(START, C.gain); dot(GOAL, C.loss);
        c.fillStyle = C.muted; c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "top"; c.textAlign = "center";
        c.fillText(cur.found ? "blue: expanded (lighter = later); gold: the path found" : "the walls leave no path on this map", x0 + cell * NC / 2, y0 + cell * NR + 7);
        c.restore();
        var ex = s.sweep.map(function (r) { return r.expanded; }), top = Math.max(10, Math.max.apply(null, ex) * 1.15);
        var a = g[1].axes({ x: [-0.2, 5.2], y: [0, top], title: "Cells expanded against w", xlabel: "heuristic weight w", xticks: [0, 1, 2, 3, 4, 5] });
        a.line(WS, ex, { color: C.muted, width: 1.2 });
        a.dots(WS, ex, { r: 4, color: function (k) { return !s.sweep[k].found ? C.muted : s.sweep[k].cost <= opt.cost + 1e-9 ? C.gain : C.loss; } });
        a.vline(v.w, { color: C.idea });
        a.legend([["shortest path found", C.gain], ["a longer path", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        if (!o[0]) return [["path", "none on this map"], ["cells expanded", String(o[1])]];
        return [["cells expanded", String(o[1])], ["Dijkstra expands", String(o[2])], ["path cost", fmt(o[3], 2)], ["shortest", fmt(o[4], 2)],
          ["excess", QB.pct(o[4] > 0 ? o[3] / o[4] - 1 : 0)]];
      },
      note: "Simulated maps. Moves go to the eight neighbours, at cost 1 or √2, so the straight-line distance never overestimates and A* (w ≤ 1) is optimal. For w > 1 the path found costs at most w times the shortest.",
    });
  };

  // ---- Part 3: the best rank-k copy of a picture ---------------------------------------------------------------
  W.lowrankcopy = function (el) {
    var M = 32, pics = ["landscape", "plaid", "diagonal stripes"];
    var picture = function (kind, noise, seed) {
      var r = QB.rng(seed * 11 + 5), A = [], i, j, x;
      for (i = 0; i < M; i++) {
        A.push(new Array(M));
        for (j = 0; j < M; j++) {
          if (kind === 0) { // sky, a sun, two ridges and a lake, drawn by formula
            var ridge1 = 17 + 5 * Math.sin(j / 5.2) + 2 * Math.sin(j / 1.9), ridge2 = 22 + 3 * Math.sin(j / 3.1 + 2);
            x = 0.85 - 0.35 * i / M;
            if ((i - 7) * (i - 7) + (j - 23) * (j - 23) < 14) x = 1;
            if (i > ridge1) x = 0.45;
            if (i > ridge2) x = 0.25;
            if (i > 27) x = 0.6 + 0.08 * Math.sin(j / 2.5);
          } else if (kind === 1) x = 0.5 + 0.25 * Math.sin(i / 2.4) + 0.25 * Math.cos(j / 3.3);
          else x = ((i + j) % 8) < 4 ? 0.85 : 0.2;
          A[i][j] = x + noise * 0.5 * r.normal();
        }
      }
      return A;
    };
    var eigen = function (A) { // eigenvalues and eigenvectors of A^T A by cyclic Jacobi rotations: the squared singular values and V
      var G = [], V = [], i, j, k, p, q, sweep;
      for (i = 0; i < M; i++) { G.push(new Array(M).fill(0)); V.push(new Array(M).fill(0)); V[i][i] = 1; }
      for (i = 0; i < M; i++) for (j = i; j < M; j++) { var d = 0; for (k = 0; k < M; k++) d += A[k][i] * A[k][j]; G[i][j] = d; G[j][i] = d; }
      for (sweep = 0; sweep < 12; sweep++) {
        var off = 0;
        for (p = 0; p < M - 1; p++) for (q = p + 1; q < M; q++) {
          var gpq = G[p][q]; off += gpq * gpq;
          if (Math.abs(gpq) < 1e-14) continue;
          var theta = (G[q][q] - G[p][p]) / (2 * gpq), t = (theta >= 0 ? 1 : -1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
          var cs = 1 / Math.sqrt(t * t + 1), sn = t * cs;
          for (k = 0; k < M; k++) { var a = G[k][p], b = G[k][q]; G[k][p] = cs * a - sn * b; G[k][q] = sn * a + cs * b; }
          for (k = 0; k < M; k++) { a = G[p][k]; b = G[q][k]; G[p][k] = cs * a - sn * b; G[q][k] = sn * a + cs * b; }
          for (k = 0; k < M; k++) { a = V[k][p]; b = V[k][q]; V[k][p] = cs * a - sn * b; V[k][q] = sn * a + cs * b; }
        }
        if (off < 1e-18) break;
      }
      var ord = [];
      for (i = 0; i < M; i++) ord.push(i);
      ord.sort(function (x, y) { return G[y][y] - G[x][x]; });
      return { sig: ord.map(function (o) { return Math.sqrt(Math.max(0, G[o][o])); }), V: V, ord: ord };
    };
    QB.widget(el, {
      title: "The best rank-k copy",
      sub: "A 32 × 32 picture is a matrix; keeping its top k singular values gives the closest matrix of rank k (Eckart-Young). Slide k: the landscape is recognisable after a handful of pieces, the plaid is exact at rank 2, and the diagonal stripes resist. Add noise and watch a flat floor of singular values appear that no small rank can capture.",
      panels: 2, height: 300, weights: [1.25, 1],
      controls: [
        { k: "k", label: "Rank kept k", min: 0, max: 32, step: 1, value: 4 },
        { k: "pic", label: "Picture", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return pics[x]; } },
        { k: "noise", label: "Noise added", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New noise", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var key = v.pic + ":" + v.noise + ":" + s.seed, i, j, m;
        if (s.key !== key) { s.key = key; s.A = picture(v.pic, v.noise, s.seed); s.E = eigen(s.A); }
        var A = s.A, E = s.E, k = v.k, B = [], Ak = [];
        for (i = 0; i < M; i++) { // A_k = A V_k V_k^T
          B.push(new Array(k)); Ak.push(new Array(M).fill(0));
          for (m = 0; m < k; m++) { var d = 0, col = E.ord[m]; for (j = 0; j < M; j++) d += A[i][j] * E.V[j][col]; B[i][m] = d; }
          for (m = 0; m < k; m++) { var cl = E.ord[m]; for (j = 0; j < M; j++) Ak[i][j] += B[i][m] * E.V[j][cl]; }
        }
        var total = 0, tail = 0;
        for (i = 0; i < M; i++) { total += E.sig[i] * E.sig[i]; if (i >= k) tail += E.sig[i] * E.sig[i]; }
        s.out = [total > 0 ? Math.sqrt(tail / total) : 0, k < M ? E.sig[k] : 0, E.sig[0], k * (2 * M + 1)];
        var c = g.ctx, bx = g[0].box, cell = Math.max(2, Math.min((bx.w - 36) / (2 * M), (bx.h - 64) / M)), side = cell * M, gap = 12;
        var x0 = bx.x + (bx.w - 2 * side - gap) / 2, y0 = bx.y + 30;
        var show = function (X, xl, name) {
          for (var a = 0; a < M; a++) for (var b = 0; b < M; b++) {
            var u = Math.round(255 * Math.max(0, Math.min(1, X[a][b])));
            c.fillStyle = "rgb(" + u + "," + u + "," + u + ")"; c.fillRect(xl + b * cell, y0 + a * cell, cell + 0.5, cell + 0.5);
          }
          c.fillStyle = C.muted; c.font = "11.5px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "top"; c.fillText(name, xl + side / 2, y0 + side + 7);
        };
        c.save();
        heading(c, "The picture and its rank-" + k + " copy", x0, bx.y + 8);
        show(A, x0, "original, 1,024 numbers"); show(Ak, x0 + side + gap, "rank " + k + ": " + s.out[3] + " numbers");
        c.restore();
        var idx = [], floor = 0.01, top = Math.max(1, E.sig[0]) * 1.6;
        for (i = 1; i <= M; i++) idx.push(i);
        var a2 = g[1].axes({ x: [0, M + 1], y: [floor, top], logy: true, title: "Singular values (log scale)", xlabel: "index i", xticks: [1, 8, 16, 24, 32] });
        a2.bars(idx, E.sig.map(function (x) { return Math.max(floor, x); }), 0.8, { color: function (q) { return q < k ? C.idea : C.cash; }, gap: 0.5 });
        a2.legend([["kept", C.idea], ["dropped: the error", C.cash]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["relative error ‖A − A_k‖/‖A‖", QB.pct(s.out[0])], ["next singular value", fmt(s.out[1], 2)], ["largest", fmt(s.out[2], 2)],
          ["numbers stored", s.out[3] + " of 1024"]];
      },
      note: "The pictures are drawn by formula; the noise is simulated. The relative error is exactly the square root of the dropped singular values' share of the sum of squares, in the Frobenius norm. A rank-k copy stores k columns, k rows and k singular values.",
    });
  };

  // ---- Part 4: gradient descent on a quadratic valley ----------------------------------------------------------
  W.quadraticdescent = function (el) {
    QB.widget(el, {
      title: "Descent in a valley: the step size and the condition number",
      sub: "Gradient descent on f(x, y) = ½(x² + κy²), a valley κ times more sharply curved across than along. Each step multiplies the across coordinate by 1 − ηκ and the along coordinate by 1 − η. Raise the step: past 1/κ the path zigzags, at 2κ/(κ + 1) it is as fast as it can be, and past 2/κ it diverges. Then raise κ and watch the best possible rate slow down.",
      panels: 2, height: 300,
      controls: [
        { k: "kappa", label: "Condition number κ", min: 1, max: 50, step: 1, value: 25 },
        { k: "u", label: "Step size η, in units of 1/κ", min: 0.05, max: 2.2, step: 0.05, value: 1.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "steps", label: "Steps shown", min: 5, max: 100, step: 5, value: 40 },
      ],
      draw: function (g, v, s) {
        var kap = v.kappa, eta = v.u / kap, fy = 1 - v.u, fx = 1 - eta, x = 1, y = 0.55, xs = [x], ys = [y], n0 = Math.sqrt(x * x + y * y), ts = [0], err = [0], i;
        for (i = 1; i <= v.steps; i++) {
          x *= fx; y *= fy;
          xs.push(Math.max(-50, Math.min(50, x))); ys.push(Math.max(-50, Math.min(50, y)));
          ts.push(i); err.push(Math.max(-14, Math.log(Math.max(1e-300, Math.sqrt(x * x + y * y) / n0)) / Math.LN10));
        }
        var q = Math.max(Math.abs(fx), Math.abs(fy)), best = (kap - 1) / (kap + 1);
        s.out = [Math.abs(fy), Math.abs(fx), q, best, q >= 1 ? -1 : q <= 0 ? 1 : Math.ceil(Math.log(0.01) / Math.log(q))];
        var a = g[0].axes({ x: [-1.25, 1.25], y: [-0.8, 0.8], title: "The path over the contours of f", xlabel: "x, along the valley" });
        var th = QB.linspace(0, 2 * Math.PI, 90), levels = [0.02, 0.08, 0.2, 0.4, 0.7, 1.1, 1.7, 2.6, 4, 6.5, 11];
        levels.forEach(function (lv) {
          a.line(th.map(function (t) { return Math.sqrt(2 * lv) * Math.cos(t); }), th.map(function (t) { return Math.sqrt(2 * lv / kap) * Math.sin(t); }), { color: C.spot, width: 1, alpha: 0.45 });
        });
        a.line(xs, ys, { color: C.idea, width: 1.6 }).dots(xs, ys, { color: C.idea, r: 2.4 });
        a.dots([1], [0.55], { color: C.gain, r: 5 }).dots([0], [0], { color: C.ink, r: 3.5 });
        a.text(1, 0.55, "start", { color: C.gain, dx: -8, dy: -12, align: "right", bg: true });
        var top = Math.max(1, Math.ceil(Math.max.apply(null, err))), lo = Math.min(-2, Math.max(-14, Math.floor(Math.min.apply(null, err))));
        var b = g[1].axes({ x: [0, v.steps], y: [lo, top], title: "Distance to the minimum, log10 of |x_t|/|x_0|", xlabel: "step t", ny: 5 });
        b.hline(0, { color: C.muted });
        b.line(ts, ts.map(function (t) { return best > 0 ? Math.max(-14, t * Math.log(best) / Math.LN10) : (t ? -14 : 0); }), { color: C.gain, width: 1.3, dash: [5, 4] });
        b.line(ts, err, { color: q >= 1 ? C.loss : C.idea, width: 2 });
        b.legend([["this step size", q >= 1 ? C.loss : C.idea], ["best fixed step", C.gain]], { pos: q >= 1 ? "tl" : "bl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["factor across, |1 − ηκ|", fmt(o[0], 3)], ["factor along, |1 − η|", fmt(o[1], 3)], ["rate per step", fmt(o[2], 3)],
          ["best possible, (κ − 1)/(κ + 1)", fmt(o[3], 3)], ["steps to 1%", o[4] < 0 ? "never" : String(o[4])]];
      },
      note: "Exact iteration, no noise; the start is the green dot. The rate is the larger of the two factors: the path converges exactly when 0 < η < 2/κ, the largest curvature being κ. The dashed line is the best fixed step, η = 2/(1 + κ).",
    });
  };

  // ---- Part 5: temperature, top-p and min-p on a next-token distribution ---------------------------------------
  W.nucleuscut = function (el) {
    var V = 200, SHOW = 40;
    var temper = function (z, T) { // softmax(z / T), sorted from likeliest to least likely (z is sorted)
      var p = [], sum = 0, i;
      for (i = 0; i < V; i++) { p.push(Math.exp((z[i] - z[0]) / T)); sum += p[i]; }
      for (i = 0; i < V; i++) p[i] /= sum;
      return p;
    };
    var kept = function (p, topp, minp) { // [tokens kept by top-p, tokens kept by min-p]
      var cum = 0, np = V, nm = 0, i;
      for (i = 0; i < V; i++) { cum += p[i]; if (cum >= topp - 1e-12) { np = i + 1; break; } }
      for (i = 0; i < V; i++) if (p[i] >= minp * p[0]) nm++;
      return [np, Math.max(1, nm)];
    };
    QB.widget(el, {
      title: "How a language model chooses: temperature, top-p, min-p",
      sub: "Simulated scores for 200 candidate next tokens, sorted from likeliest. Temperature reshapes the distribution; top-p then keeps the smallest set of tokens whose probabilities add up to p (blue bars), and min-p keeps every token at least a fraction of the likeliest one (above the orange line). Make the context open (low sharpness) and then nearly certain: the same top-p keeps dozens of tokens in one case and one in the other.",
      panels: 2, height: 300,
      controls: [
        { k: "sharp", label: "Sharpness of the scores", min: 0.5, max: 4, step: 0.1, value: 1.2, fmt: function (x) { return x.toFixed(1); } },
        { k: "T", label: "Temperature T", min: 0.3, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "topp", label: "Top-p", min: 0.5, max: 1, step: 0.01, value: 0.9, fmt: function (x) { return x.toFixed(2); } },
        { k: "minp", label: "Min-p", min: 0, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New scores", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 500), z = [], i;
        for (i = 0; i < V; i++) z.push(-v.sharp * Math.log(i + 1) + 0.35 * r.normal());
        z.sort(function (a, b) { return b - a; });
        var p = temper(z, v.T), H = 0, mass = 0, kp = kept(p, v.topp, v.minp);
        for (i = 0; i < V; i++) { if (p[i] > 0) H -= p[i] * log2(p[i]); if (i < kp[0]) mass += p[i]; }
        s.out = [H, kp[0], kp[1], mass, p[0]];
        var idx = [];
        for (i = 1; i <= SHOW; i++) idx.push(i);
        var a = g[0].axes({ x: [0, SHOW + 1], y: [0, Math.max(0.02, p[0] * 1.2)], title: "The " + SHOW + " likeliest tokens at T = " + v.T.toFixed(2), xlabel: "token, by rank", xticks: [1, 10, 20, 30, 40] });
        a.bars(idx, p.slice(0, SHOW), 0.8, { color: function (k) { return k < kp[0] ? C.spot : C.cash; }, gap: 0.5 });
        a.hline(v.minp * p[0], { color: C.implied, dash: [], width: 1.4 });
        a.legend([["kept by top-p", C.spot], ["cut by top-p", C.cash], ["min-p threshold", C.implied]], { pos: "tr" });
        var Ts = QB.linspace(0.3, 2, 35), nP = [], nM = [];
        Ts.forEach(function (T) { var k = kept(temper(z, T), v.topp, v.minp); nP.push(k[0]); nM.push(k[1]); });
        var b = g[1].axes({ x: [0.3, 2], y: [1, V], logy: true, title: "Tokens kept against temperature", xlabel: "temperature T", yticks: [1, 2, 5, 10, 20, 50, 100, 200], xticks: [0.5, 1, 1.5, 2] });
        b.line(Ts, nP, { color: C.spot, width: 2 }).line(Ts, nM, { color: C.implied, width: 2 });
        b.vline(v.T, { color: C.idea });
        b.legend([["top-p " + v.topp.toFixed(2), C.spot], ["min-p " + v.minp.toFixed(2), C.implied]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["entropy", fmt(o[0], 2) + " bits"], ["likeliest token", QB.pct(o[4])], ["top-p keeps", o[1] + " tokens (" + QB.pct(o[3]) + ")"], ["min-p keeps", o[2] + " tokens"]];
      },
      note: "Simulated data: the scores fall off as a power of the rank, with noise. Temperature is applied first, then one truncation rule; the kept tokens are renormalized before sampling. A real model's distribution has tens of thousands of tokens.",
    });
  };
})();
