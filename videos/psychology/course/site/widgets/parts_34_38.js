// Interactives for Act IX, Other people (Parts 34-38).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 34: Asch's lines, alone and after five recorded answers.  The five answers are scripted. ----
  W.lines = function (el) {
    var w = null, N = 12, CRIT = [2, 3, 5, 6, 8, 9, 11, 12], NAMES = ["A", "B", "C"];
    var S = { phase: "idle", block: "", k: 0, trial: null, shown: 0, msg: "", seed: 1,
              log: { alone: [], group: [] } };
    var lastX = 0.5;
    // read where a tap landed (thirds of the stage: A, B, C); registered before the task kit's own listener
    el.addEventListener("pointerdown", function (e) {
      var b = task && task.box, c = e.target;
      if (!b || !c || c.tagName !== "CANVAS") return;
      var r = c.getBoundingClientRect();
      lastX = (e.clientX - r.left - b.x) / b.w;
    });
    function makeTrial(k) {
      var rand = QB.rng(S.seed * 7919 + k * 104729 + (S.block === "group" ? 31 : 0));
      var std = 70 + Math.round(70 * rand()), right = Math.floor(3 * rand()), lens = [], i;
      var d1 = 0.22 + 0.2 * rand(), d2 = 0.22 + 0.2 * rand();
      var others = [std * (1 - d1), std * (1 + d2)];
      if (rand() < 0.5) others.reverse();
      for (i = 0; i < 3; i++) lens.push(i === right ? std : others.shift());
      var crit = S.block === "group" && CRIT.indexOf(k) >= 0, wrong = right;
      if (crit) { wrong = (right + 1 + Math.floor(2 * rand())) % 3; }
      return { std: std, lens: lens, right: right, crit: crit, said: wrong };
    }
    function next() {
      if (S.k >= N) { S.phase = "done"; task.clear(); if (w) w.render(); return; }
      S.k++; S.trial = makeTrial(S.k); S.shown = 0; S.msg = "";
      if (S.block === "group") {
        S.phase = "reveal";
        (function step() {
          S.shown++; if (w) w.render();
          if (S.shown < 5) task.later(step, 450); else task.later(function () { S.phase = "go"; if (w) w.render(); }, 450);
        })();
      } else { S.phase = "go"; if (w) w.render(); }
    }
    function answer(i) {
      var t = S.trial;
      S.log[S.block].push({ trial: S.k, crit: t.crit, right: i === t.right, withGroup: t.crit && i === t.said });
      task.count++;
      S.phase = "feedback"; S.msg = "You said " + NAMES[i] + ".";
      if (w) w.render();
      task.later(next, 650);
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "a": 0, "b": 1, "c": 2 },
      accepting: function () { return S.phase === "go"; },
      respond: function (side, how) { answer(how === "tap" ? Math.max(0, Math.min(2, Math.floor(lastX * 3))) : side); },
    });
    function start(block) { task.clear(); S.block = block; S.log[block] = []; S.k = 0; S.seed++; next(); }
    function tally(block) {
      var L = S.log[block], crit = 0, conf = 0, err = 0, errNon = 0, i;
      for (i = 0; i < L.length; i++) {
        if (!L[i].right) { err++; if (!L[i].crit) errNon++; }
        if (L[i].crit) { crit++; if (L[i].withGroup) conf++; }
      }
      return { n: L.length, err: err, crit: crit, conf: conf, errNon: errNon };
    }
    w = QB.widget(el, {
      title: "Which line matches?",
      sub: "A standard line on the left, three comparison lines on the right. Say which matches it: press 1, 2 or 3 (or A, B, C), or tap the third of the stage under your answer. Run it alone first, then with five earlier answers shown before yours.",
      panels: 2, height: 380, weights: [1.35, 1],
      buttons: [
        { label: "Alone", act: function () { start("alone"); } },
        { label: "With five others", act: function () { start("group"); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = { alone: [], group: [] }; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, t = S.trial;
        if ((S.phase === "go" || S.phase === "reveal" || S.phase === "feedback") && t) {
          var sc = Math.min(1, (b.h - 150) / 160), base = b.y + b.h - 70;
          ctx.save(); ctx.textAlign = "center"; ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted;
          ctx.fillText((S.block === "group" ? "With five others" : "Alone") + ": trial " + S.k + " of " + N, b.cx, b.y + 26);
          ctx.lineWidth = 6; ctx.lineCap = "butt"; ctx.strokeStyle = C.ink;
          var xs = b.x + b.w * 0.16;
          ctx.beginPath(); ctx.moveTo(xs, base); ctx.lineTo(xs, base - t.std * sc); ctx.stroke();
          ctx.fillStyle = C.muted; ctx.fillText("standard", xs, base + 18);
          for (i = 0; i < 3; i++) {
            var x = b.x + b.w * (0.44 + 0.2 * i);
            ctx.strokeStyle = "#cfd6de";
            ctx.beginPath(); ctx.moveTo(x, base); ctx.lineTo(x, base - t.lens[i] * sc); ctx.stroke();
            ctx.fillStyle = C.ink; ctx.font = "600 14px system-ui, sans-serif"; ctx.fillText(NAMES[i] + "  (" + (i + 1) + ")", x, base + 20);
          }
          if (S.block === "group") {
            ctx.font = "12px system-ui, sans-serif";
            for (i = 0; i < 5; i++) {
              var px = b.x + 40 + i * 52, py = b.y + 54;
              ctx.fillStyle = "#2a3039"; ctx.beginPath(); ctx.arc(px, py, 15, 0, 2 * Math.PI); ctx.fill();
              if (i < S.shown) { ctx.fillStyle = C.ink; ctx.font = "600 14px system-ui, sans-serif"; ctx.fillText(NAMES[t.said], px, py + 5); }
            }
            ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted; ctx.textAlign = "left";
            ctx.fillText(S.shown < 5 ? "earlier answers..." : "your turn", b.x + 40 + 5 * 52 - 18, b.y + 58);
          }
          if (S.phase === "feedback") { ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.fillText(S.msg, b.cx, b.y + b.h - 24); }
          ctx.restore();
        } else if (S.phase === "done") {
          var r = tally(S.block);
          T.message(ctx, b, S.block === "group" ? "Done: " + r.conf + " of " + r.crit + " answers went with a wrong majority." : "Done: " + r.err + " errors in " + r.n + " trials.",
                    S.block === "group" ? "On " + r.crit + " of the twelve trials the five recorded answers were unanimous and wrong. The film shows what Asch's participants did with real people in the room." : "Now run it with five others. The lines are just as easy.");
        } else {
          T.message(ctx, b, "On you", "Press Alone for twelve trials with no one else, then With five others. Answer what you see.");
        }
        // the record
        var c2 = g[1].box, cx = g.ctx, a = tally("alone"), gr = tally("group"), y0 = c2.y + c2.h - 40, hmax = c2.h - 110;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your errors, alone and with the group", c2.x + 10, c2.y + 18);
        var bars = [["alone", a.n ? a.err / a.n : NaN, "#7ec8f5"], ["with five, wrong majority", gr.crit ? gr.conf / gr.crit : NaN, "#f2c14e"],
                    ["with five, right majority", gr.n - gr.crit > 0 ? gr.errNon / (gr.n - gr.crit) : NaN, "#9aa3ad"]];
        cx.font = "11px system-ui, sans-serif";
        bars.forEach(function (bb, j) {
          var bx = c2.x + 30 + j * (c2.w - 50) / 3, bw = (c2.w - 50) / 3 - 18;
          cx.strokeStyle = "#2a3039"; cx.strokeRect(bx, y0 - hmax, bw, hmax);
          if (!isNaN(bb[1])) {
            cx.fillStyle = bb[2]; cx.fillRect(bx, y0 - hmax * bb[1], bw, hmax * bb[1]);
            cx.fillStyle = C.ink; cx.textAlign = "center"; cx.fillText(Math.round(100 * bb[1]) + "%", bx + bw / 2, y0 - hmax * bb[1] - 6);
          }
          cx.fillStyle = C.muted; cx.textAlign = "center"; T.wrap(cx, bb[0], bx + bw / 2, y0 + 14, bw + 10, 13);
        });
        cx.restore();
      },
      readout: function () {
        var a = tally("alone"), gr = tally("group");
        return [["answers", String(task.count)], ["alone, errors", a.n ? a.err + " / " + a.n : "-"],
                ["with a wrong majority", gr.crit ? gr.conf + " / " + gr.crit : "-"]];
      },
      note: "Nothing you answer is stored or sent. The five earlier answers are scripted: there is no one else, and you know it, which is the main difference from Asch's room, where the others were present, spoke aloud and were in on it. Eight of the twelve trials are critical: the majority is unanimous and chooses a line that is clearly wrong.",
    });
  };

  // ---- Part 35: goal inference.  Watch an agent walk; say where it is going; compare with inverse planning. ----
  W.goals = function (el) {
    var w = null, H = 7, WD = 9, BETA = 0.7;
    var WALL = {}, i;
    for (i = 1; i <= 5; i++) WALL[i + "," + 4] = 1;
    var GOALS = [[0, 8], [6, 8], [3, 0]], GNAME = ["A", "B", "C"], GCOL = ["#f2c14e", "#5bd18b", "#7ec8f5"];
    // each path is a list of [row, col]; the reader is asked at the steps in ASK
    var PATHS = [
      [[3, 3], [2, 3], [1, 3], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8]],
      [[3, 3], [4, 3], [5, 3], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8]],
      [[3, 6], [2, 6], [1, 6], [0, 6], [0, 5], [0, 4], [0, 3], [1, 3], [2, 3], [3, 3], [3, 2], [3, 1], [3, 0]],
      [[3, 5], [4, 5], [5, 5], [6, 5], [6, 6], [6, 7], [6, 8]],
      [[3, 2], [2, 2], [1, 2], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8]],
      [[0, 6], [0, 5], [0, 4], [0, 3], [1, 3], [2, 3], [3, 3], [3, 2], [3, 1], [3, 0]],
    ];
    var ASK = [1, 3, 5];
    var S = { phase: "idle", trial: -1, step: 0, asked: {}, log: [], order: [] };
    function dist(goal) {
      var D = [], r, c, q = [goal], k;
      for (r = 0; r < H; r++) { D.push([]); for (c = 0; c < WD; c++) D[r].push(Infinity); }
      D[goal[0]][goal[1]] = 0;
      while (q.length) {
        var cur = q.shift();
        [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(function (m) {
          var rr = cur[0] + m[0], cc = cur[1] + m[1];
          if (rr < 0 || rr >= H || cc < 0 || cc >= WD || WALL[rr + "," + cc] || D[rr][cc] < Infinity) return;
          D[rr][cc] = D[cur[0]][cur[1]] + 1; q.push([rr, cc]);
        });
      }
      return D;
    }
    var DS = GOALS.map(dist);
    function moveProb(D, a, b) {
      var opts = [[1, 0], [-1, 0], [0, 1], [0, -1]], z = 0, pb = 0;
      opts.forEach(function (m) {
        var rr = a[0] + m[0], cc = a[1] + m[1];
        if (rr < 0 || rr >= H || cc < 0 || cc >= WD || !isFinite(D[rr][cc])) return;
        var v = Math.exp(-BETA * (1 + D[rr][cc]));
        z += v; if (rr === b[0] && cc === b[1]) pb = v;
      });
      return z > 0 ? pb / z : 0;
    }
    function posterior(path, upto) {
      var p = [1 / 3, 1 / 3, 1 / 3], k, g;
      for (k = 0; k < upto; k++) {
        var s = 0;
        for (g = 0; g < 3; g++) { p[g] *= moveProb(DS[g], path[k], path[k + 1]); s += p[g]; }
        for (g = 0; g < 3; g++) p[g] = s > 0 ? p[g] / s : 1 / 3;
      }
      return p;
    }
    function nextTrial() {
      S.trial++;
      if (S.trial >= S.order.length) { S.phase = "done"; task.clear(); if (w) w.render(); return; }
      S.step = 0; S.asked = {}; S.phase = "walk"; walk();
    }
    function walk() {
      var path = PATHS[S.order[S.trial]];
      if (w) w.render();
      if (ASK.indexOf(S.step) >= 0 && S.step < path.length - 1) { S.phase = "ask"; if (w) w.render(); return; }
      if (S.step >= path.length - 1) { task.later(nextTrial, 900); return; }
      task.later(function () { S.step++; walk(); }, 420);
    }
    function answer(g) {
      var path = PATHS[S.order[S.trial]], p = posterior(path, S.step), best = p.indexOf(Math.max.apply(null, p));
      S.log.push({ trial: S.trial, step: S.step, you: g, model: best, p: p[g] });
      S.asked[S.step] = g; task.count++;
      S.phase = "walk"; S.step++;
      task.later(walk, 250);
    }
    var lastX = 0.5;
    el.addEventListener("pointerdown", function (e) {
      var b = task && task.box, c = e.target;
      if (!b || !c || c.tagName !== "CANVAS") return;
      var r = c.getBoundingClientRect();
      lastX = (e.clientX - r.left - b.x) / b.w;
    });
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "a": 0, "b": 1, "c": 2 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side, how) { answer(how === "tap" ? Math.max(0, Math.min(2, Math.floor(lastX * 3))) : side); },
    });
    function start() {
      task.clear(); S.log = []; S.trial = -1;
      S.order = PATHS.map(function (_, k) { return k; });
      nextTrial();
    }
    function agree() {
      var n = S.log.length, a = 0, k;
      for (k = 0; k < n; k++) if (S.log[k].you === S.log[k].model) a++;
      return { n: n, a: a };
    }
    w = QB.widget(el, {
      title: "Where is it going?",
      sub: "An agent walks toward one of three goals, A, B or C, around a wall. It stops three times on each walk: say where you think it is heading, with 1, 2 or 3 (or A, B, C), or tap the third of the board. The right panel compares your answers with a Bayesian observer that assumes the agent takes short paths, Part 35's inverse planner.",
      panels: 2, height: 380, weights: [1.25, 1],
      buttons: [
        { label: "Start", act: function () { start(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), r, c, k;
        var cell = Math.min((b.w - 40) / WD, (b.h - 70) / H), x0 = b.cx - cell * WD / 2, y0 = b.y + 44;
        ctx.save();
        for (r = 0; r < H; r++) for (c = 0; c < WD; c++) {
          ctx.fillStyle = WALL[r + "," + c] ? "#3a3f48" : "#11161d";
          ctx.fillRect(x0 + c * cell + 1, y0 + r * cell + 1, cell - 2, cell - 2);
        }
        GOALS.forEach(function (gl, k2) {
          ctx.fillStyle = GCOL[k2]; ctx.globalAlpha = 0.85;
          ctx.fillRect(x0 + gl[1] * cell + 3, y0 + gl[0] * cell + 3, cell - 6, cell - 6);
          ctx.globalAlpha = 1; ctx.fillStyle = "#05070b"; ctx.textAlign = "center"; ctx.font = "600 14px system-ui, sans-serif";
          ctx.fillText(GNAME[k2], x0 + (gl[1] + 0.5) * cell, y0 + (gl[0] + 0.5) * cell + 5);
        });
        if ((S.phase === "walk" || S.phase === "ask") && S.trial >= 0) {
          var path = PATHS[S.order[S.trial]];
          ctx.strokeStyle = "#cfd6de"; ctx.lineWidth = 3; ctx.beginPath();
          for (k = 0; k <= S.step && k < path.length; k++) {
            var px = x0 + (path[k][1] + 0.5) * cell, py = y0 + (path[k][0] + 0.5) * cell;
            if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
          }
          ctx.stroke();
          var cur = path[Math.min(S.step, path.length - 1)];
          ctx.fillStyle = "#ef6f6c"; ctx.beginPath();
          ctx.arc(x0 + (cur[1] + 0.5) * cell, y0 + (cur[0] + 0.5) * cell, cell * 0.3, 0, 2 * Math.PI); ctx.fill();
          ctx.fillStyle = C.muted; ctx.textAlign = "center"; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("Walk " + (S.trial + 1) + " of " + S.order.length + (S.phase === "ask" ? ": where is it going? 1, 2 or 3" : ""), b.cx, b.y + 28);
        } else if (S.phase === "done") {
          var ag = agree();
          T.message(ctx, b, "Done: you agreed with the model on " + ag.a + " of " + ag.n + " guesses.", "People and the inverse planner usually agree, because both assume the agent takes efficient routes to what it wants. Where you differ, look at the steps: the model changes its mind only as fast as the path allows.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six short walks; three guesses on each.");
        }
        ctx.restore();
        // the comparison
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("The model's belief at each of your guesses", c2.x + 10, c2.y + 18);
        var rows = S.log.slice(-9), rh = Math.min(30, (c2.h - 60) / 9);
        rows.forEach(function (row, j) {
          var path = PATHS[S.order[row.trial]], p = posterior(path, row.step), y = c2.y + 40 + j * rh, x = c2.x + 70, wbar = c2.w - 90;
          cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif";
          cx.fillText("walk " + (row.trial + 1) + ", step " + row.step, c2.x + 6, y + rh * 0.55);
          var acc = 0;
          for (var gg = 0; gg < 3; gg++) {
            cx.fillStyle = GCOL[gg]; cx.globalAlpha = gg === row.you ? 1 : 0.45;
            cx.fillRect(x + acc * wbar, y + 4, p[gg] * wbar, rh - 8); acc += p[gg];
          }
          cx.globalAlpha = 1;
        });
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif";
        cx.fillText("bright: your answer; width: the model's probability", c2.x + 10, c2.y + c2.h - 10);
        cx.restore();
      },
      readout: function () {
        var ag = agree();
        return [["answers", String(task.count)], ["agreed with the model", ag.n ? ag.a + " / " + ag.n : "-"]];
      },
      note: "Nothing you answer is stored or sent. The model is the one in explainer/psychology/psyche/social.py: an agent picks each move with probability proportional to exp(-0.7 (1 + distance left)), and Bayes' rule turns the path into beliefs about the goal, as in Baker, Saxe and Tenenbaum's inverse planning (2009).",
    });
  };
})();
