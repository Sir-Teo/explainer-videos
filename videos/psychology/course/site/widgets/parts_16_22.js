// Interactives for Act IV, Learning and Memory (Parts 16-22).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 16: the gardener's game.  Predict each plant; your predictions reveal the contingency you learned ------
  W.contingency = function (el) {
    var w = null, PER = 20, LATE = 10, YOU = "#f2c14e", OK = "#5bd18b", CS = "#7ec8f5", BAD = "#ef6f6c", US = "#f2a65a";
    // four blocks: P(bloom | fertilizer), P(bloom | none)
    var BLOCKS = [[0.75, 0.75], [0.75, 0.25], [0.25, 0.25], [0.25, 0.75]];
    var S = { phase: "idle", seed: 0, block: 0, trial: 0, order: [], plan: [], cur: null, said: null, res: [] };
    function deck(u, p1, p0) {
      // exactly PER trials: half fertilized; within each half the share that bloom is fixed, so each block's
      // contingency is exact; the order is shuffled
      var half = PER / 2, out = [], i, j, t, k1 = Math.round(p1 * half), k0 = Math.round(p0 * half);
      for (i = 0; i < half; i++) out.push({ f: true, bloom: i < k1 });
      for (i = 0; i < half; i++) out.push({ f: false, bloom: i < k0 });
      for (i = out.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = out[i]; out[i] = out[j]; out[j] = t; }
      return out;
    }
    function start() {
      task.clear(); S.seed++; S.block = 0; S.res = []; S.said = null;
      var u = QB.rng(104729 * S.seed + 17), order = [0, 1, 2, 3], i, j, t;
      for (i = 3; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      S.order = order; begin();
    }
    function begin() {
      var b = BLOCKS[S.order[S.block]], u = QB.rng(7919 * S.seed + 131 * S.block + 3);
      S.plan = deck(u, b[0], b[1]); S.trial = 0; S.res.push([]);
      S.phase = "intro"; w.render();
      task.later(next, 1600);
    }
    function next() {
      S.cur = S.plan[S.trial]; S.trial++; S.said = null;
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {  // 0: will not bloom, 1: will bloom
      if (S.phase !== "show" || !w) return;
      task.count++;
      S.said = side === 1;
      S.res[S.block].push({ f: S.cur.f, bloom: S.cur.bloom, said: S.said });
      S.phase = "feedback"; w.render();
      task.later(function () {
        if (S.trial < PER) { next(); return; }
        S.block++;
        if (S.block >= BLOCKS.length) { S.phase = "done"; w.render(); } else begin();
      }, 700);
    }
    // your contingency in a block: P(you predict bloom | fertilizer) - P(you predict bloom | none), late trials only
    function yours(k) {
      var r = S.res[k];
      if (!r || r.length < PER) return NaN;
      var late = r.slice(PER - LATE), a = 0, na = 0, b = 0, nb = 0;
      late.forEach(function (x) { if (x.f) { na++; if (x.said) a++; } else { nb++; if (x.said) b++; } });
      if (!na || !nb) return NaN;
      return a / na - b / nb;
    }
    function bloomRate(k) {
      var r = S.res[k]; if (!r || r.length < PER) return NaN;
      var late = r.slice(PER - LATE), n = 0;
      late.forEach(function (x) { if (x.said) n++; });
      return n / late.length;
    }
    function plant(c, x, y, s, fert, bloom, show) {
      c.save();
      c.fillStyle = "#3a2a20"; c.strokeStyle = "#9aa3ad"; c.lineWidth = 1.5;
      c.beginPath(); c.moveTo(x - 0.3 * s, y + 0.5 * s); c.lineTo(x + 0.3 * s, y + 0.5 * s);
      c.lineTo(x + 0.38 * s, y + 0.1 * s); c.lineTo(x - 0.38 * s, y + 0.1 * s); c.closePath(); c.fill(); c.stroke();
      c.strokeStyle = OK; c.lineWidth = 4;
      c.beginPath(); c.moveTo(x, y + 0.1 * s); c.lineTo(x, y - 0.45 * s); c.stroke();
      if (show) {
        if (bloom) {
          c.fillStyle = US;
          for (var i = 0; i < 5; i++) {
            var a = i * 2 * Math.PI / 5;
            c.beginPath(); c.arc(x + 0.16 * s * Math.cos(a), y - 0.55 * s + 0.16 * s * Math.sin(a), 0.13 * s, 0, 2 * Math.PI); c.fill();
          }
          c.fillStyle = YOU; c.beginPath(); c.arc(x, y - 0.55 * s, 0.08 * s, 0, 2 * Math.PI); c.fill();
        } else {
          c.strokeStyle = "#7c858f"; c.lineWidth = 4;
          c.beginPath(); c.moveTo(x, y - 0.45 * s); c.lineTo(x + 0.18 * s, y - 0.35 * s); c.stroke();
        }
      }
      if (fert) {
        c.fillStyle = CS; c.fillRect(x - 0.72 * s, y - 0.05 * s, 0.32 * s, 0.4 * s);
        c.fillStyle = "#05070b"; c.font = "600 " + Math.round(0.2 * s) + "px system-ui, sans-serif";
        c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("F", x - 0.56 * s, y + 0.15 * s);
      }
      c.restore();
    }

    w = QB.widget(el, {
      title: "The gardener's game: does the fertilizer work?",
      sub: "Four batches of twenty plants. Some get fertilizer (a blue F bag), some do not. Before each plant is revealed, predict whether it will bloom: F, or tap the left half, for no; J, or tap the right half, for yes. In some batches the fertilizer helps, in some it harms, and in some it does nothing while most plants bloom anyway. Your predictions in the last ten plants of each batch show the contingency you learned.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.block = 0; S.trial = 0; S.res = []; S.cur = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Eighty plants in four batches, about three minutes. Predict each one, then see it.");
        } else if (S.phase === "intro") {
          T.message(c, b, "Batch " + (S.block + 1) + " of 4", "A new fertilizer, a new set of plants.");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "On the right: your learned contingency in each batch (late predictions) against the true one. The two batches where the fertilizer did nothing differ only in how often plants bloomed. If your point for the blooming batch sits above zero, you showed the outcome-density effect of chapter four.");
        } else {
          var s = Math.min(b.h * 0.42, 90);
          plant(c, b.cx, b.cy + 0.05 * s, s, S.cur.f, S.cur.bloom, S.phase === "feedback");
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("batch " + (S.block + 1) + " of 4, plant " + S.trial + " of " + PER, b.cx, b.y + 16);
          c.font = "600 18px system-ui, sans-serif";
          if (S.phase === "feedback") {
            var right = S.said === S.cur.bloom;
            c.fillStyle = S.cur.bloom ? US : C.muted;
            c.fillText(S.cur.bloom ? "Bloomed" : "Did not bloom", b.cx, b.y + 40);
            c.font = "12.5px system-ui, sans-serif"; c.fillStyle = right ? OK : BAD;
            c.fillText(right ? "as you predicted" : "not as you predicted", b.cx, b.y + b.h - 16);
          } else {
            c.fillStyle = C.ink; c.fillText("Will it bloom?", b.cx, b.y + 40);
            c.font = "12.5px system-ui, sans-serif"; c.fillStyle = C.muted;
            c.fillText(b.w < 420 ? "F / no        J / yes" : "F, or tap the left half: no        J, or tap the right half: yes", b.cx, b.y + b.h - 16);
          }
        }
        c.restore();

        var a = g[1].axes({ x: [-0.75, 0.75], y: [-1, 1], xticks: [-0.5, 0, 0.5], yticks: [-1, -0.5, 0, 0.5, 1],
          title: "Your contingency against the true one", xlabel: "true ΔP", ylabel: "yours" });
        a.line([-0.75, 0.75], [-0.75, 0.75], { color: C.muted, width: 1 });
        a.line([-0.75, 0.75], [0, 0], { color: C.muted, width: 0.5 });
        for (var k = 0; k < S.res.length; k++) {
          var v = yours(k), blk = BLOCKS[S.order[k]];
          if (isNaN(v)) continue;
          var dp = (Math.round(blk[0] * PER / 2) - Math.round(blk[1] * PER / 2)) / (PER / 2), col = dp !== 0 ? OK : (blk[0] > 0.5 ? US : CS);
          var x = dp + (dp === 0 ? (blk[0] > 0.5 ? 0.06 : -0.06) : 0);
          a.dots([x], [v], { color: col, r: 6 });
        }
      },
      readout: function () {
        var f = function (v) { return isNaN(v) ? "–" : (v >= 0 ? "+" : "") + v.toFixed(2); }, rows = [["plants", String(S.res.reduce(function (n, r) { return n + r.length; }, 0))]];
        for (var k = 0; k < S.res.length; k++) {
          var blk = BLOCKS[S.order[k]];
          if (S.res[k].length < PER) { rows.push(["batch " + (k + 1), "in progress"]); continue; }
          rows.push(["batch " + (k + 1) + " (true ΔP " + (blk[0] >= blk[1] ? "+" : "") + ((Math.round(blk[0] * PER / 2) - Math.round(blk[1] * PER / 2)) / (PER / 2)).toFixed(2) + ", bloom " + Math.round(100 * (Math.round(blk[0] * PER / 2) + Math.round(blk[1] * PER / 2)) / PER) + "%)", f(yours(k))]);
        }
        return rows;
      },
      note: "Nothing you answer is stored or sent. Each batch has exactly ten fertilized and ten unfertilized plants, and the number of each that bloom is fixed (eight of ten, or three of ten), so the true contingency ΔP = P(bloom | fertilizer) − P(bloom | none) is exact; only the order is random. Your learned contingency is the same difference computed from your predictions in the last ten plants of the batch, after you have had time to learn. Rescorla and Wagner's rule, with the garden as a cue present on every trial, predicts that this difference settles at the true ΔP, and that early on, when blooms are common, it runs high: the outcome-density effect.",
    });
  };
  // ---- Part 17: two slot machines.  Play eighty pulls; your learning rate and inverse temperature are fitted --------
  W.bandit = function (el) {
    var w = null, N = 80, SWAP = 40, A = "#7ec8f5", B = "#f2a65a", OK = "#5bd18b", BAD = "#ef6f6c", YOU = "#f2c14e";
    var S = { phase: "idle", seed: 0, t: 0, ch: [], rw: [], plan: [], last: null, fit: null };
    // each machine's payouts are dealt from a fixed deck: in each block of ten pulls of the good machine, eight pay
    function deal(u) {
      var out = [], k, i, j, tmp, blk;
      for (k = 0; k < N; k += 10) {
        blk = [];
        for (i = 0; i < 10; i++) blk.push(i < 8);
        for (i = 9; i > 0; i--) { j = Math.floor(u() * (i + 1)); tmp = blk[i]; blk[i] = blk[j]; blk[j] = tmp; }
        out = out.concat(blk);
      }
      return out;
    }
    function start() {
      task.clear(); S.seed++; S.t = 0; S.ch = []; S.rw = []; S.last = null; S.fit = null;
      var u = QB.rng(6151 * S.seed + 29);
      S.good = deal(u); S.bad = deal(u).map(function (x) { return !x; });  // the poor machine pays 20%
      S.first = u() < 0.5 ? 0 : 1;  // which machine starts good
      S.phase = "play"; w.render();
    }
    function better(t) { return t < SWAP ? S.first : 1 - S.first; }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "play"; }, respond: pull });
    function pull(k) {
      if (S.phase !== "play" || !w) return;
      task.count++;
      var r = k === better(S.t) ? S.good[S.t] : S.bad[S.t];
      S.ch.push(k); S.rw.push(r ? 1 : 0); S.last = { k: k, r: r }; S.t++;
      S.phase = "shown"; w.render();
      task.later(function () {
        if (S.t >= N) { S.fit = fit(); S.phase = "done"; } else S.phase = "play";
        w.render();
      }, 450);
    }
    function loglik(al, be) {
      var q = [0.5, 0.5], ll = 0, t, d, p;
      for (t = 0; t < S.ch.length; t++) {
        d = be * (q[1] - q[0]);
        p = 1 / (1 + Math.exp(-d));
        ll += Math.log(Math.max(1e-12, S.ch[t] === 1 ? p : 1 - p));
        q[S.ch[t]] += al * (S.rw[t] - q[S.ch[t]]);
      }
      return ll;
    }
    function fit() {  // maximum likelihood on a grid, alpha 0.02 ... 1, beta 0.25 ... 20
      var best = { ll: -Infinity }, i, j, al, be, ll;
      for (i = 1; i <= 50; i++) for (j = 1; j <= 80; j++) {
        al = i / 50; be = j / 4; ll = loglik(al, be);
        if (ll > best.ll) best = { ll: ll, a: al, b: be };
      }
      var q = [0.5, 0.5], Q = [[], []];
      for (var t = 0; t < S.ch.length; t++) { Q[0].push(q[0]); Q[1].push(q[1]); q[S.ch[t]] += best.a * (S.rw[t] - q[S.ch[t]]); }
      best.Q = Q;
      return best;
    }
    function wsls() {
      var ws = 0, nw = 0, ls = 0, nl = 0, t;
      for (t = 1; t < S.ch.length; t++) {
        if (S.rw[t - 1]) { nw++; if (S.ch[t] === S.ch[t - 1]) ws++; } else { nl++; if (S.ch[t] !== S.ch[t - 1]) ls++; }
      }
      return [nw ? ws / nw : NaN, nl ? ls / nl : NaN];
    }
    function machine(c, x, y, s, col, name, lit, paid) {
      c.save();
      c.fillStyle = "#11161d"; c.strokeStyle = col; c.lineWidth = lit ? 4 : 2;
      c.beginPath(); c.rect(x - 0.42 * s, y - 0.6 * s, 0.84 * s, 1.1 * s); c.fill(); c.stroke();
      c.fillStyle = col; c.font = "600 " + Math.round(0.2 * s) + "px system-ui, sans-serif";
      c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(name, x, y - 0.4 * s);
      c.fillStyle = "#05070b"; c.fillRect(x - 0.3 * s, y - 0.22 * s, 0.6 * s, 0.38 * s);
      if (lit) {
        c.fillStyle = paid ? YOU : C.muted; c.font = "600 " + Math.round(0.17 * s) + "px system-ui, sans-serif";
        c.fillText(paid ? "+1" : "0", x, y - 0.03 * s);
      }
      c.restore();
    }

    w = QB.widget(el, {
      title: "Two slot machines: what is your learning rate?",
      sub: "Eighty pulls. One machine pays out more often than the other; which one may change, without warning. Pull the left machine with F (or tap the left half) and the right one with J (or the right half). At the end, a Q-learner is fitted to your choices by maximum likelihood, as in chapter five: your learning rate α and your inverse temperature β.",
      panels: 2, height: 320, weights: [1, 1.1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.t = 0; S.ch = []; S.rw = []; S.fit = null; S.last = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Eighty pulls, about two minutes. Win as much as you can.");
        } else if (S.phase === "done") {
          var tot = S.rw.reduce(function (n, x) { return n + x; }, 0);
          T.message(c, b, "Finished: " + tot + " of 80.", "On the right: your choices, what paid, and the two values of the Q-learner fitted to you. The machines swapped after pull 40. A high α means you followed the latest outcomes; a low β means your choices were noisy, or that you explored.");
        } else {
          var s = Math.min(b.h * 0.5, 110), lit = S.phase === "shown" && S.last;
          machine(c, b.cx - 0.6 * s, b.cy + 0.08 * s, s, A, "left", lit && S.last.k === 0, lit && S.last.r);
          machine(c, b.cx + 0.6 * s, b.cy + 0.08 * s, s, B, "right", lit && S.last.k === 1, lit && S.last.r);
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("pull " + Math.min(S.t + (S.phase === "play" ? 1 : 0), N) + " of " + N + ",  won so far " +
            S.rw.reduce(function (n, x) { return n + x; }, 0), b.cx, b.y + 16);
          c.font = "12.5px system-ui, sans-serif";
          c.fillText(b.w < 420 ? "F / left        J / right" : "F, or tap the left half: left        J, or tap the right half: right", b.cx, b.y + b.h - 16);
        }
        c.restore();

        var a = g[1].axes({ x: [0, N], y: [-0.15, 1.15], xticks: [0, 20, 40, 60, 80], yticks: [0, 0.5, 1],
          title: S.fit ? "Your choices and your fitted values" : "Your choices (values when you finish)", xlabel: "pull", ylabel: "value" });
        a.line([SWAP, SWAP], [-0.15, 1.15], { color: C.muted, width: 1, dash: [4, 4] });
        if (S.fit) {
          var xs = []; for (var t = 0; t < S.ch.length; t++) xs.push(t + 1);
          a.line(xs, S.fit.Q[0], { color: A, width: 2.5 });
          a.line(xs, S.fit.Q[1], { color: B, width: 2.5 });
        }
        if (S.phase === "done") {
          var x0 = [], y0 = [], x1 = [], y1 = [];
          for (var k = 0; k < S.ch.length; k++) {
            if (S.rw[k]) { x1.push(k + 1); y1.push(S.ch[k] === 0 ? 1.08 : -0.08); } else { x0.push(k + 1); y0.push(S.ch[k] === 0 ? 1.08 : -0.08); }
          }
          a.dots(x0, y0, { color: C.muted, r: 2.2 });
          a.dots(x1, y1, { color: YOU, r: 3.2 });
          a.text(1, 1.08, "left", { color: A, dx: -2, dy: -10, size: 11 });
          a.text(1, -0.08, "right", { color: B, dx: -2, dy: 14, size: 11 });
        }
      },
      readout: function () {
        var rows = [["pulls", String(S.ch.length)], ["won", String(S.rw.reduce(function (n, x) { return n + x; }, 0))]];
        if (S.phase !== "done") { rows.push(["your α and β", S.ch.length ? "when you finish" : "–"]); return rows; }
        var v = wsls();
        rows.push(["win-stay", isNaN(v[0]) ? "–" : Math.round(100 * v[0]) + "%"]);
        rows.push(["lose-shift", isNaN(v[1]) ? "–" : Math.round(100 * v[1]) + "%"]);
        rows.push(["fitted learning rate α", S.fit.a.toFixed(2) + (S.fit.a <= 0.02 || S.fit.a >= 1 ? " (at the grid's edge)" : "")]);
        rows.push(["fitted inverse temperature β", S.fit.b.toFixed(2) + (S.fit.b >= 20 || S.fit.b <= 0.25 ? " (at the grid's edge)" : "")]);
        return rows;
      },
      note: "Nothing you do is stored or sent. The good machine pays on eight of every ten pulls and the poor one on two, dealt from fixed decks so the rates are exact; they swap after pull 40. The fit is the one in the film: a Q-learner starting both values at 0.5, moving the chosen one by α times the prediction error, and choosing by a softmax with β, with α and β searched on a grid for the largest log-likelihood of your eighty choices. Eighty choices pin α only loosely, and α and β trade off: chapter five's parameter recovery is the check to run before reading much into one person's numbers.",
    });
  };
  // ---- Part 18: visual search.  Find the red bar, or the red vertical bar; your set-size functions and slopes ----
  W.search = function (el) {
    var w = null, SIZES = [4, 8, 16, 32], REPS = 4, RED = "#ef6f6c", GREEN = "#5bd18b", OK = "#5bd18b", BAD = "#ef6f6c";
    var FEAT = "#f2c14e", CONJ = "#7ec8f5";
    var S = { phase: "idle", seed: 0, k: 0, plan: [], cur: null, t0: 0, res: [], last: null };
    function shuffle(u, a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(u() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function display(u, kind, n, present) {
      // items: {x, y (0..1), red, vertical}; positions on a jittered grid
      var side = Math.ceil(Math.sqrt(n * 2)), cells = [], items = [], i;
      for (i = 0; i < side * side; i++) cells.push(i);
      shuffle(u, cells);
      for (i = 0; i < n; i++) {
        var c = cells[i], red, vert;
        if (kind === "feature") { red = false; vert = true; } else { red = i % 2 === 0; vert = !red; }
        items.push({ x: (c % side + 0.5 + (u() - 0.5) * 0.3) / side, y: (Math.floor(c / side) + 0.5 + (u() - 0.5) * 0.3) / side,
                     red: red, vert: vert });
      }
      if (present) { var t = Math.floor(u() * n); items[t].red = true; items[t].vert = true; }
      return items;
    }
    function start() {
      task.clear(); S.seed++; S.k = 0; S.res = []; S.last = null;
      var u = QB.rng(48611 * S.seed + 7), plan = [];
      ["feature", "conjunction"].forEach(function (kind) {
        SIZES.forEach(function (n) { for (var r = 0; r < REPS; r++) { plan.push([kind, n, true]); plan.push([kind, n, false]); } });
      });
      S.plan = shuffle(u, plan); S.u = u;
      S.phase = "ready"; w.render();
      task.later(next, 900);
    }
    function next() {
      if (S.k >= S.plan.length) { S.phase = "done"; w.render(); return; }
      var p = S.plan[S.k];
      S.cur = { kind: p[0], n: p[1], present: p[2], items: display(S.u, p[0], p[1], p[2]) };
      S.phase = "fix"; w.render();
      task.later(function () { S.phase = "show"; w.render(); S.t0 = performance.now(); }, 500);
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {  // 0: absent, 1: present
      if (S.phase !== "show" || !w) return;
      task.count++;
      var rt = performance.now() - S.t0, said = side === 1;
      S.res.push({ kind: S.cur.kind, n: S.cur.n, present: S.cur.present, rt: rt, ok: said === S.cur.present });
      S.last = S.res[S.res.length - 1]; S.k++;
      S.phase = "feedback"; w.render();
      task.later(next, 450);
    }
    function means(kind, present) {
      return SIZES.map(function (n) {
        var r = S.res.filter(function (x) { return x.kind === kind && x.present === present && x.n === n && x.ok; });
        if (!r.length) return NaN;
        var v = r.map(function (x) { return x.rt; }).sort(function (a, b) { return a - b; });
        return v[Math.floor((v.length - 1) / 2)];  // the median, robust to a slow trial
      });
    }
    function slope(ys) {
      var xs = [], yy = [];
      SIZES.forEach(function (n, i) { if (!isNaN(ys[i])) { xs.push(n); yy.push(ys[i]); } });
      if (xs.length < 2) return NaN;
      var mx = xs.reduce(function (a, b) { return a + b; }, 0) / xs.length, my = yy.reduce(function (a, b) { return a + b; }, 0) / yy.length;
      var num = 0, den = 0;
      for (var i = 0; i < xs.length; i++) { num += (xs[i] - mx) * (yy[i] - my); den += (xs[i] - mx) * (xs[i] - mx); }
      return num / den;
    }

    w = QB.widget(el, {
      title: "Visual search: find the target",
      sub: "Sixty-four displays. In some the target is a red bar among green bars; in others it is a red vertical bar among red horizontals and green verticals. Press J (or tap the right half) if the target is there, F (or the left half) if it is not, as fast as you can without mistakes. Your set-size functions appear as you go.",
      panels: 2, height: 330, weights: [1, 1.1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.k = 0; S.res = []; S.cur = null; S.last = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. About three minutes. J: the target is there; F: it is not.");
        } else if (S.phase === "ready") {
          T.message(c, b, "Get ready", "Red bar, or red vertical bar: the kind changes from display to display.");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "On the right: your median correct RT against the number of items. Feature search should be nearly flat; conjunction search should climb, faster when the target is absent.");
        } else {
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("display " + (S.k + (S.phase === "feedback" ? 0 : 1)) + " of " + S.plan.length + ":  find the " +
            (S.cur.kind === "feature" ? "red bar" : "red vertical bar"), b.cx, b.y + 16);
          if (S.phase === "fix") {
            c.strokeStyle = C.ink; c.lineWidth = 2;
            c.beginPath(); c.moveTo(b.cx - 8, b.cy); c.lineTo(b.cx + 8, b.cy); c.moveTo(b.cx, b.cy - 8); c.lineTo(b.cx, b.cy + 8); c.stroke();
          } else if (S.phase === "show") {
            var side = Math.min(b.w, b.h) - 60, x0 = b.cx - side / 2, y0 = b.cy - side / 2 + 6, L = Math.max(10, side / 18);
            S.cur.items.forEach(function (it) {
              c.fillStyle = it.red ? RED : GREEN;
              var px = x0 + it.x * side, py = y0 + it.y * side;
              if (it.vert) c.fillRect(px - L * 0.15, py - L / 2, L * 0.3, L); else c.fillRect(px - L / 2, py - L * 0.15, L, L * 0.3);
            });
            c.fillStyle = C.muted; c.font = "12.5px system-ui, sans-serif";
            c.fillText(b.w < 420 ? "F / absent        J / present" : "F, or tap the left half: absent        J, or tap the right half: present", b.cx, b.y + b.h - 14);
          } else if (S.phase === "feedback" && S.last) {
            c.font = "600 18px system-ui, sans-serif"; c.fillStyle = S.last.ok ? OK : BAD;
            c.fillText(S.last.ok ? Math.round(S.last.rt) + " ms" : "not right: the target was " + (S.last.present ? "there" : "not there"), b.cx, b.cy);
          }
        }
        c.restore();

        var top = 1500;
        S.res.forEach(function (x) { if (x.ok) top = Math.max(top, Math.min(x.rt, 4000)); });
        top = Math.ceil(top / 500) * 500;
        var yt = []; for (var q = 500; q <= top; q += (top > 2500 ? 1000 : 500)) yt.push(q);
        var a = g[1].axes({ x: [0, 34], y: [0, top], xticks: [4, 8, 16, 32], yticks: yt,
          title: "Your set-size functions (dashed: target absent)", xlabel: "items in the display", ylabel: "median RT, ms" });
        [["feature", FEAT], ["conjunction", CONJ]].forEach(function (kc) {
          [true, false].forEach(function (pr) {
            var ys = means(kc[0], pr), xs = [], yy = [];
            SIZES.forEach(function (n, i) { if (!isNaN(ys[i])) { xs.push(n); yy.push(Math.min(ys[i], top)); } });
            if (xs.length > 1) a.line(xs, yy, { color: kc[1], width: pr ? 2.5 : 1.5, dash: pr ? null : [5, 4] });
            if (xs.length) a.dots(xs, yy, { color: kc[1], r: pr ? 4 : 3 });
          });
        });
        a.text(5, top * 0.95, "feature", { color: FEAT, size: 11.5, bold: true });
        a.text(5, top * 0.87, "conjunction", { color: CONJ, size: 11.5, bold: true });
      },
      readout: function () {
        var f = function (v) { return isNaN(v) ? "–" : v.toFixed(0) + " ms an item"; };
        var rows = [["displays", String(S.res.length)],
                    ["errors", S.res.length ? Math.round(100 * S.res.filter(function (x) { return !x.ok; }).length / S.res.length) + "%" : "–"]];
        if (S.phase !== "done") { rows.push(["your slopes", S.res.length ? "when you finish" : "–"]); return rows; }
        rows.push(["feature, present", f(slope(means("feature", true)))]);
        rows.push(["feature, absent", f(slope(means("feature", false)))]);
        rows.push(["conjunction, present", f(slope(means("conjunction", true)))]);
        rows.push(["conjunction, absent", f(slope(means("conjunction", false)))]);
        return rows;
      },
      note: "Nothing you do is stored or sent. Each kind of search has four target-present and four target-absent displays at each of four set sizes, shuffled. Each point is the median of your correct responses, which a single slow trial cannot drag up. In the film, Psyche's guided search gives slopes near 0 for feature search and about 12 (present) and 35 (absent) ms an item for conjunctions; Treisman and Gelade's observers in 1980 were slower, about 29 and 67. Four trials a point is few, so expect noisy lines: the shape matters more than the numbers.",
    });
  };

  W.change = function (el) {
    var w = null, SIZES = [2, 4, 6, 8], REPS = 6, OK = "#5bd18b", BAD = "#ef6f6c", MEM = "#f2c14e", PSY = "#5bd18b";
    var HUES = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#42d4f4", "#f032e6", "#ffffff"];
    var S = { phase: "idle", seed: 0, k: 0, plan: [], cur: null, res: [], last: null };
    function shuffle(u, a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(u() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function display(u, n, change) {
      // n squares at distinct cells of a jittered 4 x 3 grid, distinct colours; one is probed
      var cells = [], i;
      for (i = 0; i < 12; i++) cells.push(i);
      shuffle(u, cells);
      var cols = shuffle(u, HUES.slice()), items = [];
      for (i = 0; i < n; i++) {
        var c = cells[i];
        items.push({ x: (c % 4 + 0.5 + (u() - 0.5) * 0.35) / 4, y: (Math.floor(c / 4) + 0.5 + (u() - 0.5) * 0.35) / 3,
                     col: cols[i] });
      }
      var probe = Math.floor(u() * n), test = items[probe].col;
      if (change) test = cols[n + Math.floor(u() * (cols.length - n))];  // a colour not in the display
      return { items: items, probe: probe, test: test };
    }
    function start() {
      task.clear(); S.seed++; S.k = 0; S.res = []; S.last = null;
      var u = QB.rng(70919 * S.seed + 3), plan = [];
      SIZES.forEach(function (n) { for (var r = 0; r < REPS; r++) { plan.push([n, true]); plan.push([n, false]); } });
      S.plan = shuffle(u, plan); S.u = u;
      S.phase = "ready"; w.render();
      task.later(next, 900);
    }
    function next() {
      if (S.k >= S.plan.length) { S.phase = "done"; w.render(); return; }
      var p = S.plan[S.k];
      S.cur = { n: p[0], change: p[1], d: display(S.u, p[0], p[1]) };
      S.phase = "fix"; w.render();
      task.later(function () {
        S.phase = "sample"; w.render();
        task.later(function () {
          S.phase = "blank"; w.render();
          task.later(function () { S.phase = "test"; w.render(); }, 900);
        }, 150);
      }, 500);
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "test"; }, respond: answer });
    function answer(side) {  // 0: same, 1: different
      if (S.phase !== "test" || !w) return;
      task.count++;
      var said = side === 1;
      S.res.push({ n: S.cur.n, change: S.cur.change, said: said, ok: said === S.cur.change });
      S.last = S.res[S.res.length - 1]; S.k++;
      S.phase = "feedback"; w.render();
      task.later(next, 500);
    }
    function rates(n) {
      var ch = S.res.filter(function (x) { return x.n === n && x.change; }),
          sa = S.res.filter(function (x) { return x.n === n && !x.change; });
      if (!ch.length || !sa.length) return null;
      var H = ch.filter(function (x) { return x.said; }).length / ch.length,
          F = sa.filter(function (x) { return x.said; }).length / sa.length;
      return { H: H, F: F, K: n * (H - F), acc: (ch.filter(function (x) { return x.ok; }).length + sa.filter(function (x) { return x.ok; }).length) / (ch.length + sa.length) };
    }
    function capacity() {
      var ks = [];
      [4, 6, 8].forEach(function (n) { var r = rates(n); if (r) ks.push(r.K); });
      if (!ks.length) return NaN;
      return ks.reduce(function (a, b) { return a + b; }, 0) / ks.length;
    }

    w = QB.widget(el, {
      title: "Change detection: how many can you hold?",
      sub: "Forty-eight trials. Coloured squares flash for 150 ms; after a blank of 0.9 s one square comes back, outlined. Press J (or tap the right half) if its colour changed, F (or the left half) if it is the same. Don't name the colours: just look. Your K appears as you go.",
      panels: 2, height: 330, weights: [1, 1.1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.k = 0; S.res = []; S.cur = null; S.last = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. About three minutes. J: the colour changed; F: it is the same.");
        } else if (S.phase === "ready") {
          T.message(c, b, "Get ready", "Two, four, six or eight squares, mixed. Keep your eyes on the centre.");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "On the right: your K at each set size, from your hits and false alarms. It should rise, then level off near your capacity.");
        } else {
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("trial " + (S.k + (S.phase === "feedback" ? 0 : 1)) + " of " + S.plan.length, b.cx, b.y + 16);
          var W_ = Math.min(b.w - 40, (b.h - 70) * 4 / 3), H_ = W_ * 3 / 4, x0 = b.cx - W_ / 2, y0 = b.cy - H_ / 2 + 4,
              side = Math.max(14, W_ / 11);
          if (S.phase === "fix" || S.phase === "blank" || S.phase === "sample" || S.phase === "test") {
            c.strokeStyle = C.ink; c.lineWidth = 2;
            c.beginPath(); c.moveTo(b.cx - 6, b.cy); c.lineTo(b.cx + 6, b.cy); c.moveTo(b.cx, b.cy - 6); c.lineTo(b.cx, b.cy + 6); c.stroke();
          }
          if (S.phase === "sample") {
            S.cur.d.items.forEach(function (it) {
              c.fillStyle = it.col; c.fillRect(x0 + it.x * W_ - side / 2, y0 + it.y * H_ - side / 2, side, side);
            });
          } else if (S.phase === "test") {
            var it = S.cur.d.items[S.cur.d.probe], px = x0 + it.x * W_, py = y0 + it.y * H_;
            c.fillStyle = S.cur.d.test; c.fillRect(px - side / 2, py - side / 2, side, side);
            c.strokeStyle = C.ink; c.lineWidth = 2; c.strokeRect(px - side / 2 - 5, py - side / 2 - 5, side + 10, side + 10);
            c.fillStyle = C.muted; c.font = "12.5px system-ui, sans-serif";
            c.fillText(b.w < 420 ? "F / same        J / changed" : "F, or tap the left half: same        J, or tap the right half: changed", b.cx, b.y + b.h - 14);
          } else if (S.phase === "feedback" && S.last) {
            c.font = "600 18px system-ui, sans-serif"; c.fillStyle = S.last.ok ? OK : BAD;
            c.fillText(S.last.ok ? "right" : "not right: it " + (S.last.change ? "changed" : "was the same"), b.cx, b.cy);
          }
        }
        c.restore();

        var a = g[1].axes({ x: [0, 9], y: [-1, 8], xticks: SIZES, yticks: [0, 2, 4, 6, 8],
          title: "Your capacity: K = N (hits − false alarms)", xlabel: "squares in the display", ylabel: "K" });
        a.line([0, 8.5], [0, 8.5], { color: C.muted, width: 1, dash: [3, 4] });
        a.text(6.6, 7.6, "K = N", { color: C.muted, size: 11 });
        a.line([2, 3.5, 8], [2, 3.5, 3.5], { color: PSY, width: 1.5, dash: [5, 4] });
        a.text(5.6, 3.05, "Psyche: 3.5 slots", { color: PSY, size: 11 });
        var xs = [], ys = [];
        SIZES.forEach(function (n) { var r = rates(n); if (r) { xs.push(n); ys.push(Math.max(-1, r.K)); } });
        if (xs.length > 1) a.line(xs, ys, { color: MEM, width: 2.5 });
        if (xs.length) a.dots(xs, ys, { color: MEM, r: 4 });
      },
      readout: function () {
        var rows = [["trials", String(S.res.length)],
                    ["correct", S.res.length ? Math.round(100 * S.res.filter(function (x) { return x.ok; }).length / S.res.length) + "%" : "–"]];
        SIZES.forEach(function (n) {
          var r = rates(n);
          rows.push([n + " squares: hits, false alarms", r ? Math.round(100 * r.H) + "%, " + Math.round(100 * r.F) + "%" : "–"]);
        });
        var k = capacity();
        rows.push(["your K (mean over 4, 6, 8)", S.phase === "done" && !isNaN(k) ? k.toFixed(1) : (S.res.length ? "when you finish" : "–")]);
        return rows;
      },
      note: "Nothing you do is stored or sent. Six change and six no-change trials at each of four set sizes, shuffled. K comes from the slot model derived in the film: if K of the N squares are stored and the rest guessed, hits minus false alarms is K/N. Luck and Vogel's observers, and Cowan's review, put K at about three to four. Twelve trials a set size is few, so your K is a rough estimate, good to about one item; the next chapter of the film explains why K may not count slots at all.",
    });
  };
  W.recall = function (el) {
    var w = null, LISTS = 3, LEN = 10, GOLD = "#f2c14e", BLUE = "#7ec8f5", RED = "#ef6f6c", GREEN = "#5bd18b";
    var POOLS = [
      ["APPLE", "BRIDGE", "CAMEL", "DRUM", "FEATHER", "GLOVE", "HAMMER", "ISLAND", "KETTLE", "LEMON",
       "ANCHOR", "BELL", "CLOUD", "DESK", "ENGINE", "FORK", "GRAPE", "HELMET", "IGLOO", "JUG"],
      ["MAGNET", "NEEDLE", "ORANGE", "PARROT", "QUILT", "ROCKET", "SADDLE", "TOWEL", "VIOLIN", "WAGON",
       "MIRROR", "NAPKIN", "OWL", "PIANO", "RABBIT", "SHOVEL", "TRAIN", "UMBRELLA", "VASE", "WHEEL"],
      ["BANANA", "CANOE", "DONKEY", "ENVELOPE", "FLUTE", "GIRAFFE", "HARBOR", "JELLY", "KITE", "LANTERN",
       "BUTTON", "CARPET", "DOLPHIN", "EAGLE", "FENCE", "GUITAR", "HONEY", "JEWEL", "KNIFE", "LIZARD"],
    ];
    var LETTERS = "abcdefghijklmnopqrst", KEYS = {}, i;
    for (i = 0; i < 20; i++) KEYS[LETTERS[i]] = i;
    var S = { phase: "idle", seed: 0, list: 0, k: 0, study: [], grid: [], said: [], lists: [], xy: null, msg: "" };
    function shuffle(u, a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(u() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function begin() {
      var u = QB.rng(48611 * S.seed + 97 * S.list + 5), pool = shuffle(u, POOLS[S.list].slice());
      S.study = pool.slice(0, LEN); S.grid = shuffle(u, pool.slice()); S.said = []; S.k = 0;
      S.phase = "ready"; w.render();
      task.later(show, 400);
    }
    function show() {
      if (S.k >= LEN) { S.phase = "recall"; w.render(); return; }
      S.phase = "word"; w.render();
      task.later(function () { S.phase = "gap"; w.render(); task.later(function () { S.k++; show(); }, 50); },
                 Math.round(1000 * S.secs) - 50);
    }
    function start() {
      task.clear(); S.seed++; S.list = 0; S.lists = []; S.msg = ""; S.secs = S.speed || 0.7;
      begin();
    }
    function done() {
      if (S.phase !== "recall") return;
      S.lists.push({ study: S.study.slice(), said: S.said.slice() });
      S.list++;
      if (S.list >= LISTS) { S.phase = "done"; w.render(); return; }
      S.phase = "between"; w.render();
      task.later(begin, 1200);
    }
    // where the pointer went down, for the kit's tap (which only says left or right half)
    el.addEventListener("pointerdown", function (e) {
      if (!e.target || e.target.tagName !== "CANVAS") return;
      var r = e.target.getBoundingClientRect();
      S.xy = [e.clientX - r.left, e.clientY - r.top];
    });
    var task = T.create(el, { keys: KEYS, accepting: function () { return S.phase === "recall"; }, respond: pick });
    function cellAt(x, y) {
      var g = S.geo;
      if (!g || x < g.x0 || x > g.x0 + 5 * g.cw || y < g.y0 || y > g.y0 + 4 * g.ch) return -1;
      return Math.min(3, Math.floor((y - g.y0) / g.ch)) * 5 + Math.min(4, Math.floor((x - g.x0) / g.cw));
    }
    function pick(side, how) {
      if (S.phase !== "recall") return;
      var idx = how === "key" ? side : (S.xy ? cellAt(S.xy[0], S.xy[1]) : -1);
      if (idx < 0) return;
      task.count++;
      S.said.push(S.grid[idx]);  // a repeat is kept as a response, and left out of the curves
      w.render();
    }
    function positions(L) {  // serial positions (1..LEN) of a list's recalls, 0 for a word not studied
      return L.said.map(function (wd) { return L.study.indexOf(wd) + 1; });
    }
    function curves() {
      var spc = [], n = S.lists.length, crpA = {}, crpP = {}, intr = 0, reps = 0, firsts = [];
      for (i = 0; i < LEN; i++) spc.push(0);
      for (var l = -3; l <= 3; l++) { crpA[l] = 0; crpP[l] = 0; }
      S.lists.forEach(function (L) {
        var seen = {}, prev = 0;
        positions(L).forEach(function (p) {
          if (p === 0) { intr++; prev = 0; return; }
          if (seen[p]) { reps++; return; }
          if (!Object.keys(seen).length) firsts.push(p);
          if (prev) {
            for (var q = 1; q <= LEN; q++) if (!seen[q] && Math.abs(q - prev) <= 3) crpP[q - prev]++;
            if (Math.abs(p - prev) <= 3) crpA[p - prev]++;
          }
          seen[p] = true; spc[p - 1] += 1; prev = p;
        });
      });
      return { n: n, spc: spc.map(function (x) { return n ? x / n : 0; }), intr: intr, reps: reps, firsts: firsts,
               crp: [-3, -2, -1, 1, 2, 3].map(function (l) { return crpP[l] ? crpA[l] / crpP[l] : NaN; }) };
    }

    w = QB.widget(el, {
      title: "Free recall: your serial-position and lag-CRP curves",
      sub: "Three lists of ten words, one word at a time. Then twenty words appear, the ten you saw and ten you did not. Click (or type the letter of) each word you remember, in the order the words come back to you, before you read the rest; then press Done. Try to recall first and look second.",
      panels: 3, height: 340, weights: [1.35, 1, 1],
      controls: [{ k: "secs", label: "Seconds per word", min: 0.7, max: 2, step: 0.1, value: 0.7,
                   fmt: function (x) { return x.toFixed(1) + " s"; } }],
      onChange: function (v) { S.speed = v.secs; },
      buttons: [
        { label: "Start", act: start },
        { label: "Done", act: done },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.lists = []; S.said = []; S.list = 0; } },
      ],
      draw: function (g, v) {
        if (v && v.secs) S.speed = v.secs;
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Watch ten words; then click the ones you remember, in the order they come to you, and press Done. Three lists, about three minutes.");
        } else if (S.phase === "ready") {
          T.message(c, b, "List " + (S.list + 1) + " of " + LISTS, "Just watch the words.");
        } else if (S.phase === "word") {
          c.fillStyle = C.ink; c.font = "600 30px system-ui, sans-serif";
          c.fillText(S.study[S.k], b.cx, b.cy);
        } else if (S.phase === "between") {
          T.message(c, b, "Next list", "Words recalled: " + S.lists[S.lists.length - 1].said.length + ".");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "On the right: how often you recalled each position, and where your next recall went after each one. Most people's curves rise at the end, and peak at +1.");
        } else if (S.phase === "recall") {
          var x0 = b.x + 16, y0 = b.y + 34, cw = (b.w - 32) / 5, ch = (b.h - 74) / 4;
          S.geo = { x0: x0, y0: y0, cw: cw, ch: ch };
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("click each word as it comes back, then Done (recalled so far: " + S.said.length + ")", b.cx, b.y + 18);
          S.grid.forEach(function (wd, j) {
            var cx = x0 + (j % 5 + 0.5) * cw, cy = y0 + (Math.floor(j / 5) + 0.5) * ch, n = S.said.indexOf(wd);
            c.fillStyle = n >= 0 ? "#2a3445" : "#101722"; c.fillRect(cx - cw / 2 + 3, cy - ch / 2 + 3, cw - 6, ch - 6);
            c.fillStyle = n >= 0 ? GOLD : C.ink; c.font = (cw < 70 ? "10.5px" : "12.5px") + " system-ui, sans-serif";
            c.fillText(wd, cx, cy - 4);
            c.fillStyle = C.muted; c.font = "10px system-ui, sans-serif";
            c.fillText(n >= 0 ? String(n + 1) : LETTERS[j], cx, cy + 11);
          });
        }
        c.restore();

        var r = curves(), xs = [], k;
        for (k = 1; k <= LEN; k++) xs.push(k);
        var a = g[1].axes({ x: [0.5, LEN + 0.5], y: [0, 1], xticks: [1, 4, 7, 10], yticks: [0, 0.5, 1],
          title: "Recalled, by position", xlabel: "position in the list", ylabel: "share of lists" });
        if (r.n) { a.line(xs, r.spc, { color: GOLD, width: 2.5 }); a.dots(xs, r.spc, { color: GOLD, r: 3.5 }); }
        var bb = g[2].axes({ x: [-3.5, 3.5], y: [0, 1], xticks: [-3, -2, -1, 1, 2, 3], yticks: [0, 0.5, 1],
          title: "Where the next recall went", xlabel: "lag", ylabel: "CRP" });
        var neg = [[-3, r.crp[0]], [-2, r.crp[1]], [-1, r.crp[2]]].filter(function (p) { return !isNaN(p[1]); }),
            pos = [[1, r.crp[3]], [2, r.crp[4]], [3, r.crp[5]]].filter(function (p) { return !isNaN(p[1]); });
        [[neg, BLUE], [pos, GOLD]].forEach(function (q) {
          if (q[0].length > 1) bb.line(q[0].map(function (p) { return p[0]; }), q[0].map(function (p) { return p[1]; }), { color: q[1], width: 2.5 });
          if (q[0].length) bb.dots(q[0].map(function (p) { return p[0]; }), q[0].map(function (p) { return p[1]; }), { color: q[1], r: 3.5 });
        });
        bb.text(-3.3, 0.93, "open data, 16-word lists: +1 0.45, -1 0.26", { color: C.muted, size: 10.5 });
      },
      readout: function () {
        var r = curves(), mean = function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; };
        return [["lists", r.n + " of " + LISTS],
                ["words recalled per list", r.n ? (r.spc.reduce(function (x, y) { return x + y; }, 0)).toFixed(1) : "–"],
                ["position of your first recall", r.firsts.length ? mean(r.firsts).toFixed(1) + " (10 = last)" : "–"],
                ["CRP at +1 and -1", isNaN(r.crp[3]) || isNaN(r.crp[2]) ? "–" : r.crp[3].toFixed(2) + ", " + r.crp[2].toFixed(2)],
                ["words chosen that were not shown", String(r.intr)],
                ["repeats", String(r.reps)]];
      },
      note: "Nothing you do is stored or sent. The curves are computed as in the film: the share of lists in which each position was recalled, and the lag-conditional response probability, which divides the transitions you made at each lag by the transitions that were possible (to a word you had not yet recalled). Choosing from a grid makes this partly a recognition test, so your order is the order you found the words; recall first, then look. Three short lists give noisy curves: the open data behind the film's average 3,528 lists.",
    });
  };

  W.drm = function (el) {
    var w = null, GOLD = "#f2c14e", PINK = "#f28fb8", GREY = "#9aa4b2", PURPLE = "#b39ddb";
    // four lists of associates built around a word they leave out (after Roediger and McDermott's lists)
    var LISTS = [
      { lure: "CHAIR", words: ["TABLE", "SIT", "LEGS", "SEAT", "COUCH", "DESK", "RECLINER", "SOFA", "WOOD", "CUSHION"] },
      { lure: "MOUNTAIN", words: ["HILL", "VALLEY", "CLIMB", "SUMMIT", "TOP", "MOLEHILL", "PEAK", "PLAIN", "GLACIER", "GOAT"] },
      { lure: "NEEDLE", words: ["THREAD", "PIN", "EYE", "SEWING", "SHARP", "POINT", "PRICK", "THIMBLE", "HAYSTACK", "THORN"] },
      { lure: "SWEET", words: ["SOUR", "CANDY", "SUGAR", "BITTER", "GOOD", "TASTE", "TOOTH", "NICE", "HONEY", "SODA"] },
    ];
    var UNRELATED = ["LADDER", "PENCIL", "RIVER", "JACKET", "ONION", "TRUMPET", "BOTTLE", "CASTLE"];
    var KEYS = { r: 0, k: 1, n: 2 }, NAMES = ["remember", "know", "new"];
    var S = { phase: "idle", seed: 0, list: 0, k: 0, study: [], test: [], t: 0, answers: [], xy: null };
    function shuffle(u, a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(u() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function begin() {
      var u = QB.rng(7919 * S.seed + 31 * S.list + 3), L = LISTS[S.list];
      S.study = L.words.slice(); S.k = 0;
      // the test: two studied words (one early, one late), the missing word, and an unrelated word
      S.test = shuffle(u, [{ w: L.words[1], kind: "studied" }, { w: L.words[7], kind: "studied" },
                           { w: L.lure, kind: "lure" }, { w: UNRELATED[(2 * S.list + S.seed) % UNRELATED.length], kind: "unrelated" }]);
      S.t = 0; S.phase = "ready"; w.render();
      task.later(show, 400);
    }
    function show() {
      if (S.k >= S.study.length) { S.phase = "test"; w.render(); return; }
      S.phase = "word"; w.render();
      task.later(function () { S.phase = "gap"; w.render(); task.later(function () { S.k++; show(); }, 60); },
                 Math.round(1000 * S.secs) - 60);
    }
    function start() {
      task.clear(); S.seed++; S.list = 0; S.answers = []; S.secs = S.speed || 0.6;
      begin();
    }
    el.addEventListener("pointerdown", function (e) {
      if (!e.target || e.target.tagName !== "CANVAS") return;
      var r = e.target.getBoundingClientRect();
      S.xy = [e.clientX - r.left, e.clientY - r.top];
    });
    var task = T.create(el, { keys: KEYS, accepting: function () { return S.phase === "test"; }, respond: answer });
    function answer(side, how) {
      if (S.phase !== "test") return;
      var choice = side;
      if (how === "tap") {
        var b = S.box;
        if (!b || !S.xy) return;
        choice = Math.max(0, Math.min(2, Math.floor(3 * (S.xy[0] - b.x) / b.w)));
      }
      task.count++;
      var item = S.test[S.t];
      S.answers.push({ kind: item.kind, choice: choice });
      S.t++;
      if (S.t >= S.test.length) {
        S.list++;
        if (S.list >= LISTS.length) { S.phase = "done"; w.render(); return; }
        S.phase = "between"; w.render();
        task.later(begin, 900);
        return;
      }
      w.render();
    }
    function rates() {
      var out = {};
      ["studied", "lure", "unrelated"].forEach(function (k) {
        var a = S.answers.filter(function (x) { return x.kind === k; });
        out[k] = { n: a.length,
                   old: a.length ? a.filter(function (x) { return x.choice < 2; }).length / a.length : NaN,
                   rem: a.length ? a.filter(function (x) { return x.choice === 0; }).length / a.length : NaN };
      });
      return out;
    }

    w = QB.widget(el, {
      title: "Words that were never there: a DRM experiment",
      sub: "Four short lists, one word at a time. After each list, four words: for each, say whether you remember it being shown (R), just know it was there (K), or it is new (N). Press the key, or tap the left, middle or right of the box.",
      panels: 2, height: 330, weights: [1.4, 1],
      controls: [{ k: "secs", label: "Seconds per word", min: 0.6, max: 1.5, step: 0.1, value: 0.6,
                   fmt: function (x) { return x.toFixed(1) + " s"; } }],
      onChange: function (v) { S.speed = v.secs; },
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.answers = []; S.list = 0; } },
      ],
      draw: function (g, v) {
        if (v && v.secs) S.speed = v.secs;
        var c = g.ctx, b = T.stage(g, 0, task);
        S.box = b;
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Watch ten words; then judge four words: R if you remember seeing it, K if you just know it was there, N if it is new. Four lists, about two minutes.");
        } else if (S.phase === "ready") {
          T.message(c, b, "List " + (S.list + 1) + " of " + LISTS.length, "Just watch the words, and try to remember them.");
        } else if (S.phase === "word") {
          c.fillStyle = C.ink; c.font = "600 30px system-ui, sans-serif";
          c.fillText(S.study[S.k], b.cx, b.cy);
        } else if (S.phase === "between") {
          T.message(c, b, "Next list", "");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "Each list was built around a word that was not shown: CHAIR, MOUNTAIN, NEEDLE, SWEET. On the right: how often you called each kind of word old, and how often you said you remembered it.");
        } else if (S.phase === "test") {
          var item = S.test[S.t];
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("word " + (S.t + 1) + " of " + S.test.length + ": was it in the list you just saw?", b.cx, b.y + 18);
          c.fillStyle = C.ink; c.font = "600 30px system-ui, sans-serif";
          c.fillText(item.w, b.cx, b.cy - 18);
          [["R: remember", GOLD], ["K: know", PURPLE], ["N: new", GREY]].forEach(function (q, j) {
            var x = b.x + (j + 0.5) * b.w / 3, y = b.y + b.h - 34;
            c.strokeStyle = q[1]; c.lineWidth = 1.5; c.strokeRect(x - b.w / 7, y - 15, 2 * b.w / 7, 30);
            c.fillStyle = q[1]; c.font = "13px system-ui, sans-serif"; c.fillText(q[0], x, y);
          });
        }
        c.restore();

        var r = rates(), kinds = ["studied", "lure", "unrelated"], cols = [GOLD, PINK, GREY];
        var a = g[1].axes({ x: [0, 3], y: [0, 1], xticks: [], yticks: [0, 0.5, 1],
          title: "Called old (dark: remembered)", xlabel: "studied     the missing word     unrelated", ylabel: "share" });
        kinds.forEach(function (k, j) {
          if (!r[k].n) return;
          a.bars([j + 0.5], [r[k].old], 0.55, { color: cols[j], alpha: 0.4 });
          a.bars([j + 0.5], [r[k].rem], 0.55, { color: cols[j], alpha: 1 });
        });
        a.text(0.1, 0.95, "1995: studied 86%, missing word 84%", { color: C.muted, size: 10.5 });
      },
      readout: function () {
        var r = rates(), f = function (x) { return isNaN(x) ? "–" : Math.round(100 * x) + "%"; };
        return [["lists", Math.min(S.list, LISTS.length) + " of " + LISTS.length],
                ["studied words called old", f(r.studied.old)],
                ["missing words called old", f(r.lure.old)],
                ["unrelated words called old", f(r.unrelated.old)],
                ["missing words you said you remembered", f(r.lure.rem)]];
      },
      note: "Nothing you do is stored or sent. Each list holds associates of one word that is never shown, after the lists of Deese (1959) and Roediger and McDermott (1995). In their first experiment students called the missing word old 84% of the time, against 86% for words they had studied. Four lists give you only four missing words, so your own rate is a rough one; but most people call at least one of them old, and many say they remember it.",
    });
  };
})();
