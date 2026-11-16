// Interactives for Act XI, the graduate toolkit (Parts 44-50).  Each is an experiment the reader takes part in,
// built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  function gauss(rand) {
    var u = 1 - rand(), v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  function mulberry(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function corr(a, b) {
    var n = a.length, ma = 0, mb = 0, sab = 0, saa = 0, sbb = 0, i;
    for (i = 0; i < n; i++) { ma += a[i]; mb += b[i]; }
    ma /= n; mb /= n;
    for (i = 0; i < n; i++) { sab += (a[i] - ma) * (b[i] - mb); saa += (a[i] - ma) * (a[i] - ma); sbb += (b[i] - mb) * (b[i] - mb); }
    return sab / Math.sqrt(saa * sbb);
  }
  // upper tail of chi-square on 1 df
  function p1(x) {
    var z = Math.sqrt(Math.max(x, 0) / 2), t = 1 / (1 + 0.5 * z);
    var e = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
            t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
    return Math.min(1, e);
  }

  // ---- Part 44: draw the arrows; which diagrams can the data tell apart? ----
  W.diagrams = function (el) {
    var w = null;
    var N = 500;
    // the four ways to direct the edges X-M and M-Y
    var DIAG = [
      { name: "X → M → Y", a: [1, 1] },
      { name: "X ← M ← Y", a: [-1, -1] },
      { name: "X ← M → Y", a: [-1, 1] },
      { name: "X → M ← Y", a: [1, -1] },
    ];
    var TRUTHS = [0, 2, 3, 1, 3, 0];  // the hidden generating diagram in each of six rounds
    var S = { phase: "idle", k: -1, log: [], fit: null, data: null };

    function simulate(truth, seed) {
      var rand = mulberry(seed), X = [], M = [], Y = [], i, x, m, y;
      for (i = 0; i < N; i++) {
        if (truth === 0) { x = gauss(rand); m = 0.6 * x + 0.8 * gauss(rand); y = 0.6 * m + 0.8 * gauss(rand); }
        else if (truth === 1) { y = gauss(rand); m = 0.6 * y + 0.8 * gauss(rand); x = 0.6 * m + 0.8 * gauss(rand); }
        else if (truth === 2) { m = gauss(rand); x = 0.6 * m + 0.8 * gauss(rand); y = 0.6 * m + 0.8 * gauss(rand); }
        else { x = gauss(rand); y = gauss(rand); m = 0.5 * x + 0.5 * y + 0.7 * gauss(rand); }
        X.push(x); M.push(m); Y.push(y);
      }
      var rxm = corr(X, M), rmy = corr(M, Y), rxy = corr(X, Y);
      var part = (rxy - rxm * rmy) / Math.sqrt((1 - rxm * rxm) * (1 - rmy * rmy));
      var chain = -N * Math.log(1 - part * part), coll = -N * Math.log(1 - rxy * rxy);
      return { rxm: rxm, rmy: rmy, rxy: rxy, chi: [chain, chain, chain, coll] };
    }
    function next() {
      S.k++;
      if (S.k >= TRUTHS.length) { S.phase = "done"; task.clear(); }
      else { S.phase = "ask"; S.data = simulate(TRUTHS[S.k], 4400 + 97 * S.k + (w ? w.state.seed : 0)); }
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "4": 3 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side, how) {
        var choice = how === "tap" ? (side === 0 ? 0 : 3) : side;
        var d = S.data, best = Math.min.apply(null, d.chi), tied = [];
        for (var j = 0; j < 4; j++) if (d.chi[j] - best < 1e-9) tied.push(j);
        S.log.push({ k: S.k, choice: choice, truth: TRUTHS[S.k], tied: tied, fitsBest: tied.indexOf(choice) >= 0 });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 4200);
      },
    });
    function start() { task.clear(); S.k = -1; S.log = []; task.count = 0; next(); }

    function drawDiag(ctx, cx, cy, a, col, sc) {
      var xs = [cx - 70 * sc, cx, cx + 70 * sc], names = ["X", "M", "Y"], i;
      ctx.save();
      ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 2;
      for (i = 0; i < 2; i++) {
        var from = a[i] > 0 ? xs[i] : xs[i + 1], to = a[i] > 0 ? xs[i + 1] : xs[i], dir = to > from ? 1 : -1;
        var x0 = from + dir * 14 * sc, x1 = to - dir * 14 * sc;
        ctx.beginPath(); ctx.moveTo(x0, cy); ctx.lineTo(x1, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x1, cy); ctx.lineTo(x1 - dir * 8, cy - 5); ctx.lineTo(x1 - dir * 8, cy + 5);
        ctx.closePath(); ctx.fill();
      }
      ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.font = "600 " + Math.round(14 * sc) + "px system-ui, sans-serif";
      for (i = 0; i < 3; i++) {
        ctx.strokeRect(xs[i] - 12 * sc, cy - 12 * sc, 24 * sc, 24 * sc);
        ctx.fillText(names[i], xs[i], cy);
      }
      ctx.restore();
    }

    w = QB.widget(el, {
      title: "Draw the arrows",
      sub: "Each round, 500 people are simulated from a hidden diagram on X, M and Y. Look at the correlations and pick the diagram you think made them: press 1 to 4 (or tap left for the first, right for the last). Then see how well each diagram fits.",
      panels: 2, height: 380, weights: [1.4, 1],
      buttons: [
        { label: "Start", act: function () { start(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save(); ctx.textAlign = "center";
        if (S.phase === "ask" || S.phase === "shown") {
          var d = S.data, last = S.log[S.log.length - 1];
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Round " + (S.k + 1) + " of " + TRUTHS.length + ":  r(X,M) = " + d.rxm.toFixed(2) + "   r(M,Y) = " +
                       d.rmy.toFixed(2) + "   r(X,Y) = " + d.rxy.toFixed(2), b.cx, b.y + 26);
          var rowH = (b.h - 70) / 4;
          for (j = 0; j < 4; j++) {
            var y = b.y + 52 + rowH * (j + 0.5), col = C.ink;
            if (S.phase === "shown") col = d.chi[j] - Math.min.apply(null, d.chi) < 1e-9 ? "#5bd18b" : "#ef6f6c";
            ctx.fillStyle = C.muted; ctx.font = "600 14px system-ui, sans-serif"; ctx.textAlign = "left";
            ctx.fillText(String(j + 1), b.x + 22, y + 5);
            drawDiag(ctx, b.x + b.w * 0.36, y, DIAG[j].a, col, 1);
            ctx.textAlign = "left"; ctx.font = "12.5px system-ui, sans-serif";
            if (S.phase === "shown") {
              ctx.fillStyle = col;
              var p = p1(d.chi[j]);
              ctx.fillText("χ² = " + d.chi[j].toFixed(1) + " on 1 df, p " + (p < 0.001 ? "< 0.001" : "= " + p.toFixed(2)) +
                           (j === last.truth ? "   (the hidden diagram)" : "") + (j === last.choice ? "   your pick" : ""),
                           b.x + b.w * 0.6, y + 4);
            }
          }
          ctx.textAlign = "center";
        } else if (S.phase === "done") {
          T.message(ctx, b, "Six rounds.",
                    "The three diagrams without a collider always fit identically: the data cannot say which made them. Only a collider leaves a mark of its own, because it makes X and Y uncorrelated.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six rounds, each from a hidden diagram.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Each round: the hidden diagram, and how many fit best", c2.x + 10, c2.y + 18);
        var bh = (c2.h - 50) / TRUTHS.length;
        for (j = 0; j < S.log.length; j++) {
          var r = S.log[j], yy = c2.y + 34 + j * bh;
          cx.fillStyle = r.tied.length === 1 ? "#5bd18b" : "#f2c14e";
          cx.fillText((r.k + 1) + ".  " + DIAG[r.truth].name + "   " + (r.tied.length === 1 ? "only it fits best" :
                      r.tied.length + " diagrams tie"), c2.x + 14, yy + bh / 2);
        }
        cx.restore();
      },
      readout: function () {
        var only = S.log.filter(function (r) { return r.tied.length === 1; }).length;
        return [["rounds", String(task.count)], ["identified by the data", S.log.length ? only + " / " + S.log.length : "-"]];
      },
      note: "Nothing you answer is stored or sent. The data are simulated in your browser; the same reasoning holds for any sample size.",
    });
  };
  // ---- Part 45: an adaptive test on you.  Which is larger?  Each item is chosen where it tells the most. ----
  W.adaptive = function (el) {
    var w = null;
    var NODES = [], i;
    for (i = -40; i <= 40; i++) NODES.push(i / 10);
    var LEVELS = 9, A = 1.7, C0 = 0.5, N_ITEMS = 10;
    function bOf(level) { return -2.4 + 0.6 * (level - 1); }
    function pRight(th, b) { return C0 + (1 - C0) / (1 + Math.exp(-A * (th - b))); }
    function infoAt(th, b) {
      var P = pRight(th, b);
      return A * A * (P - C0) * (P - C0) * (1 - P) / ((1 - C0) * (1 - C0) * P);
    }
    function ri(rand, lo, hi) { return lo + Math.floor(rand() * (hi - lo + 1)); }
    // Two expressions for a level; returns {left, right, lv, rv}
    function makeItem(level, rand) {
      var a, b, c, d, L, R, lv, rv, tries = 0;
      do {
        tries++;
        if (level === 1) { a = ri(rand, 2, 9); b = ri(rand, 2, 9); c = a + b + (rand() < 0.5 ? -1 : 1) * ri(rand, 3, 5);
          L = a + " + " + b; R = String(c); lv = a + b; rv = c; }
        else if (level === 2) { a = ri(rand, 2, 9); b = ri(rand, 2, 9); c = ri(rand, 2, 9); d = a + b - c + (rand() < 0.5 ? -2 : 2);
          L = a + " + " + b; R = c + " + " + d; lv = a + b; rv = c + d; }
        else if (level === 3) { a = ri(rand, 12, 49); b = ri(rand, 12, 49); c = ri(rand, 12, 49); d = a + b - c + (rand() < 0.5 ? -3 : 3);
          L = a + " + " + b; R = c + " + " + d; lv = a + b; rv = c + d; }
        else if (level === 4) { a = ri(rand, 3, 9); b = ri(rand, 3, 9); c = a * b + (rand() < 0.5 ? -1 : 1) * ri(rand, 3, 6);
          L = a + " × " + b; R = String(c); lv = a * b; rv = c; }
        else if (level === 5) { a = ri(rand, 3, 9); b = ri(rand, 3, 9); c = ri(rand, 3, 9); d = Math.max(2, Math.round(a * b / c) + (rand() < 0.5 ? -1 : 1));
          L = a + " × " + b; R = c + " × " + d; lv = a * b; rv = c * d; }
        else if (level === 6) { a = ri(rand, 13, 39); b = ri(rand, 3, 9); c = Math.round(a * b * (1 + (rand() < 0.5 ? -1 : 1) * (0.03 + 0.04 * rand())));
          L = a + " × " + b; R = String(c); lv = a * b; rv = c; }
        else if (level === 7) { b = ri(rand, 3, 9); a = ri(rand, 1, b - 1); d = ri(rand, 3, 9); c = Math.max(1, Math.min(d - 1, Math.round(a / b * d) + (rand() < 0.5 ? 0 : 1)));
          L = a + "/" + b; R = c + "/" + d; lv = a / b; rv = c / d; }
        else if (level === 8) { a = ri(rand, 13, 29); b = ri(rand, 13, 29); c = a + ri(rand, 1, 3); d = b - ri(rand, 1, 3);
          L = a + " × " + b; R = c + " × " + d; lv = a * b; rv = c * d; }
        else { b = ri(rand, 7, 13); a = ri(rand, 2, b - 2); d = b + ri(rand, 1, 3); c = Math.round(a / b * d);
          L = a + "/" + b; R = c + "/" + d; lv = a / b; rv = c / d; }
      } while ((Math.abs(lv - rv) < 1e-9 || !isFinite(lv) || !isFinite(rv)) && tries < 50);
      if (Math.abs(lv - rv) < 1e-9) { R = String(Math.round(rv) + 1); rv = Math.round(rv) + 1; }
      return { left: L, right: R, lv: lv, rv: rv, level: level, b: bOf(level) };
    }
    var S = { phase: "idle", k: 0, log: [], item: null, post: null, est: 0, sd: 1, path: [], seed: 45 };
    function update() {
      var lp = NODES.map(function (t) { return -0.5 * t * t; }), j, m = 0, m2 = 0, z = 0, mx = -Infinity;
      S.log.forEach(function (r) {
        for (j = 0; j < NODES.length; j++) { var P = pRight(NODES[j], r.b); lp[j] += r.right ? Math.log(P) : Math.log(1 - P); }
      });
      for (j = 0; j < lp.length; j++) mx = Math.max(mx, lp[j]);
      for (j = 0; j < lp.length; j++) { var p = Math.exp(lp[j] - mx); z += p; m += p * NODES[j]; m2 += p * NODES[j] * NODES[j]; }
      S.est = m / z; S.sd = Math.sqrt(Math.max(m2 / z - (m / z) * (m / z), 0));
    }
    function choose(rand) {
      var best = 1, bi = -1, l;
      for (l = 1; l <= LEVELS; l++) { var v = infoAt(S.est, bOf(l)); if (v > bi) { bi = v; best = l; } }
      return makeItem(best, rand);
    }
    var rand = QB.rng ? QB.rng(45) : Math.random;
    function next() {
      if (S.k >= N_ITEMS) { S.phase = "done"; task.clear(); if (w) w.render(); return; }
      S.item = choose(rand); S.phase = "ask"; S.t0 = T.now();
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "f": 0, "j": 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var it = S.item, right = side === 0 ? it.lv > it.rv : it.rv > it.lv;
        S.log.push({ b: it.b, level: it.level, right: right });
        task.count++; S.k++;
        update();
        S.path.push([S.est, S.sd]);
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 700);
      },
    });
    function start(state) {
      task.clear(); S.k = 0; S.log = []; S.est = 0; S.sd = 1; S.path = [[0, 1]]; task.count = 0;
      rand = QB.rng ? QB.rng(45 + (state ? state.seed : 0)) : Math.random;
      next();
    }
    w = QB.widget(el, {
      title: "Which is larger?",
      sub: "Ten pairs. Press F if the left one is larger, J if the right one is (or tap the side). Each pair is chosen where your answers so far say it will tell the most.",
      panels: 2, height: 360, weights: [1.3, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; S.path = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if ((S.phase === "ask" || S.phase === "shown") && S.item) {
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Pair " + Math.min(S.k + (S.phase === "ask" ? 1 : 0), N_ITEMS) + " of " + N_ITEMS + "   (level " + S.item.level + " of 9)", b.cx, b.y + 24);
          ctx.fillStyle = C.ink; ctx.font = "600 26px system-ui, sans-serif";
          ctx.fillText(S.item.left, b.x + b.w * 0.27, b.cy);
          ctx.fillText(S.item.right, b.x + b.w * 0.73, b.cy);
          ctx.fillStyle = C.muted; ctx.font = "14px system-ui, sans-serif";
          ctx.fillText("or", b.cx, b.cy);
          if (S.phase === "shown") {
            var last = S.log[S.log.length - 1];
            ctx.fillStyle = last.right ? "#5bd18b" : "#ef6f6c"; ctx.font = "600 14px system-ui, sans-serif";
            ctx.fillText(last.right ? "right" : "not this time", b.cx, b.y + b.h - 34);
          } else {
            ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
            ctx.fillText("F: left    J: right", b.cx, b.y + b.h - 34);
          }
        } else if (S.phase === "done") {
          T.message(ctx, b, "Ten pairs.",
                    "The band narrowed as each answer was used, and harder pairs followed right answers. The difficulties here are set by design, not calibrated on people, so the position is not a measurement of you.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Ten pairs, chosen one at a time.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx, x0 = c2.x + 40, x1 = c2.x + c2.w - 14, y0 = c2.y + 30, y1 = c2.y + c2.h - 30;
        function X(k) { return x0 + (x1 - x0) * k / N_ITEMS; }
        function Y(t) { return y1 - (y1 - y0) * (t + 3) / 6; }
        cx.save(); cx.strokeStyle = C.muted; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(x0, y0); cx.lineTo(x0, y1); cx.lineTo(x1, y1); cx.stroke();
        cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif"; cx.textAlign = "left";
        cx.fillText("The estimate and its 95% band, pair by pair", c2.x + 10, c2.y + 16);
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.textAlign = "right";
        [-2, 0, 2].forEach(function (t) { cx.fillText(String(t), x0 - 6, Y(t) + 4); });
        for (j = 0; j < S.path.length; j++) {
          var e = S.path[j], lo = Math.max(-3, e[0] - 1.96 * e[1]), hi = Math.min(3, e[0] + 1.96 * e[1]);
          cx.strokeStyle = "rgba(179,157,219,0.6)"; cx.lineWidth = 5;
          cx.beginPath(); cx.moveTo(X(j), Y(lo)); cx.lineTo(X(j), Y(hi)); cx.stroke();
          cx.fillStyle = "#b39ddb"; cx.beginPath(); cx.arc(X(j), Y(e[0]), 3.5, 0, 2 * Math.PI); cx.fill();
        }
        for (j = 0; j < S.log.length; j++) {
          cx.fillStyle = S.log[j].right ? "#5bd18b" : "#ef6f6c";
          cx.fillRect(X(j + 1) - 3, Y(S.log[j].b) - 3, 6, 6);
        }
        cx.restore();
      },
      readout: function () {
        return [["pairs", String(task.count)], ["band width", S.path.length ? (2 * 1.96 * S.sd).toFixed(2) : "-"]];
      },
      note: "Nothing you answer is stored or sent. The squares mark each pair's difficulty (green right, red not); the scale is illustrative, so this is a demonstration of adaptive testing, not a score.",
    });
  };
  // ---- Part 46: your own scale from paired comparisons, fitted by Bradley-Terry. ----
  W.pairs = function (el) {
    var w = null;
    var ITEMS = ["apple", "banana", "cherry", "grape", "orange"];
    var PAIRS = [], i, j;
    for (i = 0; i < ITEMS.length; i++) for (j = i + 1; j < ITEMS.length; j++) PAIRS.push([i, j]);
    var S = { phase: "idle", k: -1, order: [], log: [], wins: null, v: null };
    function fit() {
      var n = ITEMS.length, W = [], N = [], v = [], a, b, it;
      for (a = 0; a < n; a++) { W.push([]); N.push([]); v.push(1); for (b = 0; b < n; b++) { W[a].push(0.5); N[a].push(a === b ? 0 : 1); } }
      // a half win each way keeps the fit finite (a weak prior)
      S.log.forEach(function (r) { W[r.win][r.lose] += 1; N[r.win][r.lose] += 1; N[r.lose][r.win] += 1; });
      for (it = 0; it < 300; it++) {
        var nv = [];
        for (a = 0; a < n; a++) {
          var wa = 0, den = 0;
          for (b = 0; b < n; b++) if (b !== a) { wa += W[a][b]; den += N[a][b] / (v[a] + v[b]); }
          nv.push(wa / den);
        }
        var g = Math.exp(nv.reduce(function (s, x) { return s + Math.log(x); }, 0) / n);
        v = nv.map(function (x) { return x / g; });
      }
      S.v = v;
    }
    function triads() {
      var n = ITEMS.length, beat = [], a, b, c, t = 0;
      for (a = 0; a < n; a++) { beat.push([]); for (b = 0; b < n; b++) beat[a].push(0); }
      S.log.forEach(function (r) { beat[r.win][r.lose] += 1; beat[r.lose][r.win] -= 1; });
      for (a = 0; a < n; a++) for (b = a + 1; b < n; b++) for (c = b + 1; c < n; c++) {
        var ab = beat[a][b], bc = beat[b][c], ca = beat[c][a];
        if ((ab > 0 && bc > 0 && ca > 0) || (ab < 0 && bc < 0 && ca < 0)) t++;
      }
      return t;
    }
    function next() {
      S.k++;
      if (S.k >= S.order.length) { S.phase = "done"; fit(); task.clear(); } else S.phase = "ask";
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "f": 0, "j": 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var p = S.order[S.k], left = p[0], right = p[1];
        S.log.push({ win: side === 0 ? left : right, lose: side === 0 ? right : left });
        task.count++;
        fit();
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 350);
      },
    });
    function start(state) {
      var rand = QB.rng(46 + (state ? state.seed : 0)), order = PAIRS.slice(), extra = [], k, t;
      for (k = order.length - 1; k > 0; k--) { var r = Math.floor(rand() * (k + 1)); t = order[k]; order[k] = order[r]; order[r] = t; }
      extra = [order[0], order[3]].map(function (p) { return [p[1], p[0]]; });  // two pairs again, sides swapped
      S.order = order.map(function (p) { return rand() < 0.5 ? p : [p[1], p[0]]; }).concat(extra);
      S.log = []; S.k = -1; S.v = null; task.count = 0; task.clear();
      next();
    }
    w = QB.widget(el, {
      title: "Which do you prefer?",
      sub: "Twelve pairs of fruit. Press F for the left one, J for the right (or tap a side). Every pair once, and two pairs again.",
      panels: 2, height: 340, weights: [1.2, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; S.v = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j2;
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "ask" || S.phase === "shown") {
          var p = S.order[Math.min(S.k, S.order.length - 1)];
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Pair " + (Math.min(S.k, S.order.length - 1) + 1) + " of " + S.order.length, b.cx, b.y + 24);
          ctx.fillStyle = C.ink; ctx.font = "600 26px system-ui, sans-serif";
          ctx.fillText(ITEMS[p[0]], b.x + b.w * 0.27, b.cy);
          ctx.fillText(ITEMS[p[1]], b.x + b.w * 0.73, b.cy);
          ctx.fillStyle = C.muted; ctx.font = "14px system-ui, sans-serif";
          ctx.fillText("or", b.cx, b.cy);
          ctx.fillText("F: left    J: right", b.cx, b.y + b.h - 30);
        } else if (S.phase === "done") {
          var t = triads();
          T.message(ctx, b, "Your scale is on the right.",
                    (t === 0 ? "No circular triads: your choices fit one line." : t + " circular triad" + (t > 1 ? "s" : "") + " (A over B, B over C, C over A): normal, and the reason Thurstone's method needs a model.") +
                    " The two repeated pairs show how stable a single choice is.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Twelve quick choices.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif"; cx.textAlign = "left";
        cx.fillText("Bradley-Terry scale (log strength), from your choices so far", c2.x + 10, c2.y + 18);
        if (S.v) {
          var logs = S.v.map(Math.log), lo = Math.min.apply(null, logs), hi = Math.max.apply(null, logs);
          if (hi - lo < 1e-6) { lo -= 1; hi += 1; }
          var x0 = c2.x + 30, x1 = c2.x + c2.w - 30, yl = c2.y + c2.h / 2;
          cx.strokeStyle = C.muted; cx.beginPath(); cx.moveTo(x0, yl); cx.lineTo(x1, yl); cx.stroke();
          for (j2 = 0; j2 < ITEMS.length; j2++) {
            var xx = x0 + (x1 - x0) * (logs[j2] - lo) / (hi - lo);
            cx.fillStyle = "#f2c14e"; cx.beginPath(); cx.arc(xx, yl, 5, 0, 2 * Math.PI); cx.fill();
            cx.fillStyle = C.ink; cx.font = "11px system-ui, sans-serif"; cx.textAlign = "center";
            cx.fillText(ITEMS[j2], xx, yl + (j2 % 2 ? 22 : -14));
          }
        }
        cx.restore();
      },
      readout: function () {
        return [["choices", String(task.count)], ["circular triads", S.log.length ? String(triads()) : "-"]];
      },
      note: "Nothing you choose is stored or sent. The scale has no zero and no unit: only the order and the gaps mean anything.",
    });
  };
  // ---- Part 47: one cloud, many people.  Guess the slope within one person before the colours show it. ----
  W.withinbetween = function (el) {
    var w = null;
    var ROUNDS = 6, COLS = ["#7ec8f5", "#f2c14e", "#5bd18b", "#ef6f6c", "#b39ddb", "#f29e4c", "#6f9bf2", "#e07bb5"];
    var S = { phase: "idle", k: -1, log: [], data: null };
    function makeCloud(rand) {
      var between = rand() < 0.5 ? -1 : 1, within = rand() < 0.5 ? -0.7 : 0.7, pts = [], p, t;
      if (rand() < 0.25) within = between * 0.7;  // sometimes they agree
      for (p = 0; p < 8; p++) {
        var mx = (rand() - 0.5) * 6, my = between * mx + (rand() - 0.5) * 0.6;
        for (t = 0; t < 10; t++) {
          var dx = (rand() - 0.5) * 2.4;
          pts.push({ p: p, x: mx + dx, y: my + within * dx + (rand() - 0.5) * 0.5 });
        }
      }
      return { pts: pts, between: between, within: within, focus: Math.floor(rand() * 8) };
    }
    var rand = QB.rng(47);
    function next() {
      S.k++;
      if (S.k >= ROUNDS) { S.phase = "done"; task.clear(); } else { S.phase = "ask"; S.data = makeCloud(rand); }
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "f": 0, "j": 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var guess = side === 0 ? -1 : 1, truth = S.data.within > 0 ? 1 : -1;
        S.log.push({ guess: guess, truth: truth, between: S.data.between });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 2400);
      },
    });
    w = QB.widget(el, {
      title: "Up or down, for one person?",
      sub: "Each cloud is eight people measured ten times. One person's points are ringed. When their x is higher than usual, is their y higher or lower? F: lower, J: higher (or tap left or right).",
      panels: 2, height: 340, weights: [1.3, 1],
      buttons: [
        { label: "Start", act: function (state) { rand = QB.rng(47 + state.seed); S.log = []; S.k = -1; task.count = 0; task.clear(); next(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "ask" || S.phase === "shown") {
          var x0 = b.x + 30, x1 = b.x + b.w - 30, y0 = b.y + 30, y1 = b.y + b.h - 40;
          var X = function (v) { return x0 + (x1 - x0) * (v + 5) / 10; }, Y = function (v) { return y1 - (y1 - y0) * (v + 6) / 12; };
          S.data.pts.forEach(function (q) {
            var col = S.phase === "shown" ? COLS[q.p] : "#9aa0a6";
            ctx.fillStyle = col; ctx.beginPath(); ctx.arc(X(q.x), Y(q.y), 3, 0, 2 * Math.PI); ctx.fill();
            if (q.p === S.data.focus) { ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(X(q.x), Y(q.y), 6, 0, 2 * Math.PI); ctx.stroke(); }
          });
          ctx.save(); ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Cloud " + (S.k + 1) + " of " + ROUNDS + (S.phase === "shown" ? ("   within: " + (S.data.within > 0 ? "up" : "down") + ", across people: " + (S.data.between > 0 ? "up" : "down")) : "   F: lower    J: higher"), b.cx, b.y + b.h - 16);
          ctx.restore();
        } else if (S.phase === "done") {
          var agree = S.log.filter(function (r) { return r.truth === r.between; }).length;
          T.message(ctx, b, "Six clouds.", "In " + (ROUNDS - agree) + " of them the slope within a person ran against the slope across people. The overall cloud cannot tell you which; only each person's own points can.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six clouds of people over time.");
        }
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your guess, within, and across people", c2.x + 10, c2.y + 18);
        S.log.forEach(function (r, i) {
          cx.fillStyle = r.guess === r.truth ? "#5bd18b" : "#ef6f6c";
          cx.fillText((i + 1) + ".  you: " + (r.guess > 0 ? "up" : "down") + "   within: " + (r.truth > 0 ? "up" : "down") + "   across: " + (r.between > 0 ? "up" : "down"), c2.x + 14, c2.y + 44 + i * 22);
        });
        cx.restore();
      },
      readout: function () { return [["clouds", String(task.count)]]; },
      note: "Nothing you answer is stored or sent. The clouds are generated in your browser.",
    });
  };
  // ---- Part 48: play a reversal bandit; the page fits a Q-learner to your choices and checks the fit. ----
  W.fitme = function (el) {
    var w = null;
    var N_TRIALS = 80, SWAP = 40, PG = 0.75, PB = 0.25;
    var AL = [], BE = [], i;
    for (i = 0; i < 25; i++) AL.push(0.02 + 0.98 * i / 24);
    for (i = 0; i < 25; i++) BE.push(0.5 + 14.5 * i / 24);
    function loglik(a, b, C, R) {
      var q0 = 0.5, q1 = 0.5, ll = 0, t, p1, d;
      for (t = 0; t < C.length; t++) {
        d = b * (q1 - q0);
        p1 = 1 / (1 + Math.exp(-d));
        p1 = Math.min(Math.max(p1, 1e-9), 1 - 1e-9);
        ll += C[t] === 1 ? Math.log(p1) : Math.log(1 - p1);
        if (C[t] === 1) q1 += a * (R[t] - q1); else q0 += a * (R[t] - q0);
      }
      return ll;
    }
    function fitGrid(C, R) {
      var best = -Infinity, bi = 0, bj = 0, L = [], ia, ib;
      for (ia = 0; ia < AL.length; ia++) {
        L.push([]);
        for (ib = 0; ib < BE.length; ib++) {
          var v = loglik(AL[ia], BE[ib], C, R);
          L[ia].push(v);
          if (v > best) { best = v; bi = ia; bj = ib; }
        }
      }
      return { L: L, a: AL[bi], b: BE[bj], ll: best };
    }
    function goodArm(t) { return t < SWAP ? 0 : 1; }
    function payoff(arm, t, rand) { return rand() < (arm === goodArm(t) ? PG : PB) ? 1 : 0; }
    function simulate(a, b, rand) {
      var q0 = 0.5, q1 = 0.5, C = [], R = [], t;
      for (t = 0; t < N_TRIALS; t++) {
        var p1 = 1 / (1 + Math.exp(-b * (q1 - q0))), c = rand() < p1 ? 1 : 0, r = payoff(c, t, rand);
        C.push(c); R.push(r);
        if (c === 1) q1 += a * (r - q1); else q0 += a * (r - q0);
      }
      return { C: C, R: R };
    }
    var S = { phase: "idle", t: 0, C: [], R: [], last: null, fit: null, rec: [], who: "", seed: 48 };
    var rand = mulberry(48);
    function finish() {
      S.phase = "done"; task.clear();
      S.fit = fitGrid(S.C, S.R);
      var r2 = mulberry(4800 + S.seed), k;
      S.rec = [];
      for (k = 0; k < 16; k++) {
        var sim = simulate(S.fit.a, S.fit.b, r2), f = fitGrid(sim.C, sim.R);
        S.rec.push([f.a, f.b]);
      }
      if (w) w.render();
    }
    function next() {
      if (S.t >= N_TRIALS) { finish(); return; }
      S.phase = "ask"; if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "f": 0, "j": 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var r = payoff(side, S.t, rand);
        S.C.push(side); S.R.push(r); S.last = { arm: side, r: r };
        S.t++; task.count++;
        S.phase = "shown"; if (w) w.render();
        task.later(next, 350);
      },
    });
    function start(state) {
      task.clear(); S.t = 0; S.C = []; S.R = []; S.fit = null; S.rec = []; S.who = "you"; task.count = 0;
      rand = mulberry(48 + (state ? state.seed : 0));
      next();
    }
    function demo(state) {
      task.clear(); S.who = "Psyche";
      rand = mulberry(480 + (state ? state.seed : 0));
      var sim = simulate(0.3, 5, rand);
      S.C = sim.C; S.R = sim.R; S.t = N_TRIALS; task.count = N_TRIALS;
      finish();
    }
    function spread(v) {
      var m = 0, s = 0; v.forEach(function (x) { m += x; }); m /= v.length;
      v.forEach(function (x) { s += (x - m) * (x - m); });
      return Math.sqrt(s / Math.max(v.length - 1, 1));
    }
    w = QB.widget(el, {
      title: "Two machines",
      sub: "Eighty choices. Press F for the left machine, J for the right (or tap a side). One pays more often than the other, and at some point they may change. Then the page fits a learning model to your choices.",
      panels: 2, height: 360, weights: [1.2, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Let Psyche play", act: function (state) { demo(state); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.C = []; S.R = []; S.fit = null; S.rec = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "ask" || S.phase === "shown") {
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Choice " + Math.min(S.t + (S.phase === "ask" ? 1 : 0), N_TRIALS) + " of " + N_TRIALS, b.cx, b.y + 24);
          [0, 1].forEach(function (arm) {
            var x = b.x + b.w * (arm === 0 ? 0.3 : 0.7), lit = S.phase === "shown" && S.last && S.last.arm === arm;
            ctx.fillStyle = lit ? (S.last.r ? "#5bd18b" : "#ef6f6c") : "rgba(127,127,127,0.25)";
            ctx.fillRect(x - 46, b.cy - 50, 92, 100);
            ctx.fillStyle = C.ink; ctx.font = "600 18px system-ui, sans-serif";
            ctx.fillText(arm === 0 ? "F" : "J", x, b.cy - 12);
            if (lit) { ctx.font = "600 14px system-ui, sans-serif"; ctx.fillText(S.last.r ? "paid" : "nothing", x, b.cy + 18); }
          });
          var won = 0; S.R.forEach(function (r) { won += r; });
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("paid so far: " + won, b.cx, b.y + b.h - 30);
        } else if (S.phase === "done" && S.fit) {
          var ra = spread(S.rec.map(function (x) { return x[0]; }));
          T.message(ctx, b, "Fitted: learning rate " + S.fit.a.toFixed(2) + ", inverse temperature " + S.fit.b.toFixed(1),
                    (S.who === "Psyche" ? "Psyche played with a planted learning rate of 0.3 and inverse temperature of 5. " : "") + "Sixteen simulated players with exactly these values, refitted, give learning rates spread by about " + ra.toFixed(2) + " (the dots). From eighty choices, a learning rate is a rough estimate, not a measurement of a trait.");
        } else {
          T.message(ctx, b, "On you", "Press Start to play, or let Psyche play to see a planted learner fitted.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx, x0 = c2.x + 40, x1 = c2.x + c2.w - 14, y0 = c2.y + 30, y1 = c2.y + c2.h - 34;
        function X(a) { return x0 + (x1 - x0) * (a - 0.02) / 0.98; }
        function Y(bb) { return y1 - (y1 - y0) * (bb - 0.5) / 14.5; }
        cx.save();
        cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif"; cx.textAlign = "left";
        cx.fillText("Log-likelihood of the choices; up: inverse temperature", c2.x + 10, c2.y + 16);
        if (S.fit) {
          var mx = S.fit.ll, cw = (x1 - x0) / AL.length + 1, ch = (y1 - y0) / BE.length + 1, ia, ib;
          for (ia = 0; ia < AL.length; ia++) for (ib = 0; ib < BE.length; ib++) {
            var drop = Math.min((mx - S.fit.L[ia][ib]) / 12, 1);
            cx.fillStyle = "rgba(179,157,219," + (0.9 * (1 - drop)).toFixed(3) + ")";
            cx.fillRect(X(AL[ia]) - cw / 2, Y(BE[ib]) - ch / 2, cw, ch);
          }
          S.rec.forEach(function (r) { cx.fillStyle = "#f2c14e"; cx.beginPath(); cx.arc(X(r[0]), Y(r[1]), 3, 0, 2 * Math.PI); cx.fill(); });
          cx.strokeStyle = "#ffffff"; cx.lineWidth = 2;
          cx.beginPath(); cx.arc(X(S.fit.a), Y(S.fit.b), 6, 0, 2 * Math.PI); cx.stroke();
        }
        cx.strokeStyle = C.muted; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(x0, y0); cx.lineTo(x0, y1); cx.lineTo(x1, y1); cx.stroke();
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.textAlign = "center";
        [0.25, 0.5, 0.75, 1].forEach(function (a) { cx.fillText(String(a), X(a), y1 + 13); });
        cx.fillText("learning rate", (x0 + x1) / 2, y1 + 26);
        cx.textAlign = "right";
        [1, 5, 10, 15].forEach(function (bb) { cx.fillText(String(bb), x0 - 6, Y(bb) + 4); });
        cx.restore();
      },
      readout: function () {
        return [["choices", String(task.count)], ["fit", S.fit ? "α " + S.fit.a.toFixed(2) + ", β " + S.fit.b.toFixed(1) : "-"]];
      },
      note: "Nothing you choose is stored or sent. The left machine pays 75% of the time and the right 25% for the first forty choices, then they swap. The fit is a grid search over the Q-learner of Part 17; the dots are refits of players simulated at your values, the recovery check of chapter four.",
    });
  };
  // ---- Part 49: choose a pipeline for Psyche's brain, predict, then see the map and how the other pipelines voted. ----
  W.pipelines = function (el) {
    var w = null, M = 32, NS = 16;
    var SM = [0, 2, 4], TH = ["p < 0.001 per voxel", "false discovery rate 5%", "Bonferroni 5%"];
    function blur(a, fw) {
      if (fw <= 0) return a.slice();
      var sg = fw / 2.355, r = Math.ceil(3 * sg), k = [], i, j, x, y, s = 0;
      for (i = -r; i <= r; i++) { k.push(Math.exp(-i * i / (2 * sg * sg))); s += k[k.length - 1]; }
      for (i = 0; i < k.length; i++) k[i] /= s;
      var tmp = new Float64Array(M * M), out = new Float64Array(M * M);
      for (y = 0; y < M; y++) for (x = 0; x < M; x++) {
        var v = 0; for (j = -r; j <= r; j++) { var xx = Math.min(M - 1, Math.max(0, x + j)); v += k[j + r] * a[y * M + xx]; }
        tmp[y * M + x] = v;
      }
      for (y = 0; y < M; y++) for (x = 0; x < M; x++) {
        var u = 0; for (j = -r; j <= r; j++) { var yy = Math.min(M - 1, Math.max(0, y + j)); u += k[j + r] * tmp[yy * M + x]; }
        out[y * M + x] = u;
      }
      return out;
    }
    function erfc(x) {
      var t = 1 / (1 + 0.5 * Math.abs(x));
      var r = t * Math.exp(-x * x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
              t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
      return x >= 0 ? r : 2 - r;
    }
    function pUpper(t, df) {  // one-sided p of a t statistic, via Fisher's normal approximation
      var z = t * (1 - 1 / (4 * df)) / Math.sqrt(1 + t * t / (2 * df));
      return 0.5 * erfc(z / Math.SQRT2);
    }
    var mask = new Uint8Array(M * M), regA = new Uint8Array(M * M), regB = new Uint8Array(M * M), x, y;
    for (y = 0; y < M; y++) for (x = 0; x < M; x++) {
      var cx = (x - 15.5) / (0.46 * M), cy = (y - 15.5) / (0.48 * M);
      mask[y * M + x] = cx * cx + cy * cy <= 1 ? 1 : 0;
      regA[y * M + x] = ((x - 10) * (x - 10) + (y - 12) * (y - 12) <= 9) ? 1 : 0;
      regB[y * M + x] = ((x - 21) * (x - 21) + (y - 19) * (y - 19) <= 9) ? 1 : 0;
    }
    var S = { seed: 49, data: null, results: null, guess: null, score: [0, 0] };
    function makeData(seed) {
      var rand = mulberry(seed), subj = [], motion = [], s, i;
      for (s = 0; s < NS; s++) {
        var dev = new Float64Array(M * M), err = new Float64Array(M * M);
        for (i = 0; i < M * M; i++) { dev[i] = gauss(rand); err[i] = gauss(rand); }
        dev = blur(dev, 6); err = blur(err, 2);
        var sd1 = 0, sd2 = 0; for (i = 0; i < M * M; i++) { sd1 += dev[i] * dev[i]; sd2 += err[i] * err[i]; }
        sd1 = Math.sqrt(sd1 / (M * M)); sd2 = Math.sqrt(sd2 / (M * M));
        var mo = rand() < 0.2 ? 0.6 + rand() * 0.6 : rand() * 0.15, sign = rand() < 0.5 ? -1 : 1, m = new Float64Array(M * M);
        for (y = 0; y < M; y++) for (x = 0; x < M; x++) {
          i = y * M + x;
          var rr = Math.sqrt(Math.pow((x - 15.5) / (0.46 * M), 2) + Math.pow((y - 15.5) / (0.48 * M), 2));
          var rim = Math.exp(-Math.pow((rr - 1) / 0.1, 2));
          m[i] = mask[i] ? (1.0 * regA[i] + 0.6 * regB[i] + 0.6 * dev[i] / sd1 + err[i] / sd2 + sign * 4 * mo * rim) : 0;
        }
        subj.push(m); motion.push(mo);
      }
      return { subj: subj, motion: motion };
    }
    function runPipe(sm, th, ex) {
      var keep = [], i, s, cut = S.data.motion.slice().sort(function (a, b) { return a - b; })[NS - 4];
      for (s = 0; s < NS; s++) if (!ex || S.data.motion[s] < cut) keep.push(blur(S.data.subj[s], SM[sm]));
      var n = keep.length, t = new Float64Array(M * M), ps = [];
      for (i = 0; i < M * M; i++) {
        if (!mask[i]) continue;
        var mu = 0, v = 0; for (s = 0; s < n; s++) mu += keep[s][i]; mu /= n;
        for (s = 0; s < n; s++) v += Math.pow(keep[s][i] - mu, 2); v /= (n - 1);
        t[i] = mu / Math.sqrt(v / n);
        ps.push([pUpper(t[i], n - 1), i]);
      }
      var on = new Uint8Array(M * M), m = ps.length;
      if (th === 0) ps.forEach(function (q) { if (q[0] < 0.001) on[q[1]] = 1; });
      else if (th === 2) ps.forEach(function (q) { if (q[0] < 0.05 / m) on[q[1]] = 1; });
      else {
        ps.sort(function (a, b) { return a[0] - b[0]; });
        var kmax = -1; for (i = 0; i < m; i++) if (ps[i][0] <= 0.05 * (i + 1) / m) kmax = i;
        for (i = 0; i <= kmax; i++) on[ps[i][1]] = 1;
      }
      var b = 0, a = 0, f = 0;
      for (i = 0; i < M * M; i++) if (on[i]) { if (regB[i]) b++; else if (regA[i]) a++; else f++; }
      return { t: t, on: on, B: b > 0, A: a > 0, falseVox: f };
    }
    function recompute() {
      S.data = makeData(S.seed); S.results = {};
      var sm, th, ex;
      for (sm = 0; sm < 3; sm++) for (th = 0; th < 3; th++) for (ex = 0; ex < 2; ex++)
        S.results[sm + "," + th + "," + ex] = runPipe(sm, th, ex);
    }
    recompute();
    function cur(v) { return S.results[v.sm + "," + v.th + "," + v.ex]; }
    function predict(yes, v) {
      S.guess = yes;
      var r = cur(v);
      S.score[1]++; if (r.B === yes) S.score[0]++;
    }
    var task = T.create(el, {
      keys: { "f": 0, "j": 1 },
      accepting: function () { return !!S.v; },
      respond: function (side) {
        if (S.guess === null) { predict(side === 0, S.v); task.count++; }
        else { S.seed++; S.guess = null; recompute(); }
        if (w) w.render();
      },
    });
    w = QB.widget(el, {
      title: "Choose a pipeline",
      sub: "Psyche's brain: 16 simulated people, a strong region on the left and a weaker one (outlined) on the right. Choose the smoothing, the threshold and whether to drop the four people who moved most, then predict: will the outlined region light up? Press F (it will light up) or J (it will stay dark), or tap the left or right half of the map; press again for a new brain.",
      panels: 2, height: 340, weights: [1, 1.15],
      controls: [
        { k: "sm", label: "Smoothing (voxels)", min: 0, max: 2, step: 1, value: 1, fmt: function (x) { return String(SM[x]); } },
        { k: "th", label: "Threshold", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return TH[x]; } },
        { k: "ex", label: "Drop the movers", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "yes" : "no"; } },
      ],
      onChange: function () { S.guess = null; },
      buttons: [
        { label: "New brain", act: function (state) { S.seed++; S.guess = null; recompute(); } },
        { label: "It will light up", act: function (state, v) { if (S.guess === null) { predict(true, v); task.count++; } } },
        { label: "It will stay dark", act: function (state, v) { if (S.guess === null) { predict(false, v); task.count++; } } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b0 = g[0].box, r = cur(v), i;
        S.v = v;
        task.box = { x: b0.x, y: b0.y, w: b0.w, h: b0.h, cx: b0.x + b0.w / 2, cy: b0.y + b0.h / 2 };
        var side = Math.min(b0.w - 20, b0.h - 40), cell = side / M, x0 = b0.x + (b0.w - side) / 2, y0 = b0.y + 26;
        ctx.save();
        ctx.fillStyle = C.ink; ctx.font = "600 12px system-ui, sans-serif"; ctx.textAlign = "left";
        ctx.fillText(S.guess === null ? "Predict first: the map appears after" : "The map from your pipeline", b0.x + 8, b0.y + 16);
        for (y = 0; y < M; y++) for (x = 0; x < M; x++) {
          i = y * M + x; if (!mask[i]) continue;
          var col = "#1b2029";
          if (S.guess !== null) {
            var tv = Math.max(0, Math.min(1, r.t[i] / 6));
            col = r.on[i] ? (regA[i] || regB[i] ? "#f2c14e" : "#ef6f6c") : "rgba(" + Math.round(40 + 120 * tv) + "," + Math.round(44 + 60 * tv) + "," + Math.round(56 + 20 * tv) + ",1)";
          }
          ctx.fillStyle = col; ctx.fillRect(x0 + x * cell, y0 + y * cell, cell + 0.5, cell + 0.5);
        }
        ctx.strokeStyle = "#7ec8f5"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x0 + 21.5 * cell, y0 + 19.5 * cell, 3.4 * cell, 0, 2 * Math.PI); ctx.stroke();
        if (S.guess !== null) {
          ctx.fillStyle = r.B === S.guess ? "#5bd18b" : "#ef6f6c"; ctx.font = "600 13px system-ui, sans-serif"; ctx.textAlign = "center";
          ctx.fillText((r.B ? "It lit up" : "It stayed dark") + (r.B === S.guess ? ": as you predicted" : ": not as you predicted"), b0.x + b0.w / 2, b0.y + b0.h - 6);
        }
        ctx.restore();
        var b1 = g[1].box, cx = g.ctx, yes = 0, k = 0;
        cx.save(); cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif"; cx.textAlign = "left";
        cx.fillText("All 18 pipelines on this brain: does the outlined region light up?", b1.x + 8, b1.y + 16);
        var cw = (b1.w - 140) / 6, ch = 30, gx = b1.x + 128, gy = b1.y + 46;
        cx.font = "11px system-ui, sans-serif"; cx.fillStyle = C.muted;
        ["0, keep", "0, drop", "2, keep", "2, drop", "4, keep", "4, drop"].forEach(function (s, j) { cx.textAlign = "center"; cx.fillText(s, gx + (j + 0.5) * cw, gy - 6); });
        for (var th = 0; th < 3; th++) {
          cx.textAlign = "right"; cx.fillStyle = C.muted; cx.fillText(TH[th].replace(" per voxel", ""), gx - 6, gy + th * (ch + 6) + ch / 2 + 4);
          for (var sm = 0; sm < 3; sm++) for (var ex = 0; ex < 2; ex++) {
            var rr = S.results[sm + "," + th + "," + ex], j2 = sm * 2 + ex;
            k++; if (rr.B) yes++;
            cx.fillStyle = S.guess === null ? "#2a303a" : (rr.B ? "#f2c14e" : "#3a3f48");
            cx.fillRect(gx + j2 * cw + 3, gy + th * (ch + 6), cw - 6, ch);
            if (sm === v.sm && th === v.th && ex === v.ex) { cx.strokeStyle = "#ffffff"; cx.lineWidth = 2; cx.strokeRect(gx + j2 * cw + 2, gy + th * (ch + 6) - 1, cw - 4, ch + 2); }
          }
        }
        cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "13px system-ui, sans-serif";
        cx.fillText(S.guess === null ? "Columns: smoothing, and whether the movers were dropped." : yes + " of " + k + " pipelines say it lights up. The planted effect is the same in all of them.", b1.x + 8, gy + 3 * (ch + 6) + 22);
        cx.restore();
      },
      readout: function () { return [["predictions right", S.score[0] + " of " + S.score[1]]]; },
      note: "Nothing you choose is stored or sent. The brain, its people and their head motion are simulated in your browser; red voxels are false positives, gold ones are in a planted region.",
    });
  };
})();
