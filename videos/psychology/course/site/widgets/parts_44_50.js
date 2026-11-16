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
})();
