// Interactives for Act III, Sensing (Parts 11-15).  Each is an experiment the reader takes part in, built on the
// task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 11: which patch is brighter?  A 2-down 1-up staircase, then your psychometric function, fitted -----
  W.threshold = function (el) {
    var w = null, BASE = 110, N = 50, OK = "#5bd18b", BAD = "#ef6f6c", YOU = "#f2c14e";
    var S = { phase: "idle", trial: 0, seed: 0, level: 24, run: 0, dir: 0, side: 0, log: [], reversals: [], last: null };
    function z(p) { // inverse of the standard normal cdf (Acklam's rational approximation)
      var a = [-39.6968302866538, 220.946098424521, -275.928510446969, 138.357751867269, -30.6647980661472, 2.50662827745924],
          b = [-54.4760987982241, 161.585836858041, -155.698979859887, 66.8013118877197, -13.2806815528857],
          c = [-0.00778489400243029, -0.322396458041136, -2.40075827716184, -2.54973253934373, 4.37466414146497, 2.93816398269878],
          d = [0.00778469570904146, 0.32246712907004, 2.445134137143, 3.75440866190742], q, r;
      if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    }
    function phi(x) { // the standard normal cdf
      var t = 1 / (1 + 0.2316419 * Math.abs(x)), y = 0.3989423 * Math.exp(-x * x / 2) * t *
        (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
      return x > 0 ? 1 - y : y;
    }
    function psi(x, a, b) { return 0.5 + 0.48 * phi((Math.log(x) - a) / b); } // 2AFC, a 2% lapse, in log increment
    function fit() { // maximum likelihood on a grid over the log threshold and spread
      if (S.log.length < 10) return null;
      var best = null, i, j, k;
      for (i = 0; i <= 60; i++) for (j = 0; j <= 30; j++) {
        var a = Math.log(0.5) + i * (Math.log(40) - Math.log(0.5)) / 60, b = 0.08 + j * 0.04, ll = 0;
        for (k = 0; k < S.log.length; k++) { var p = psi(S.log[k].x, a, b); ll += S.log[k].ok ? Math.log(p) : Math.log(1 - p); }
        if (!best || ll > best.ll) best = { a: a, b: b, ll: ll };
      }
      best.th = Math.exp(best.a + best.b * z((0.75 - 0.5) / 0.48));
      return best;
    }
    function next() {
      S.trial++;
      var u = QB.rng(5101 * S.seed + 31 * S.trial + 3);
      S.side = u() < 0.5 ? 0 : 1;
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      var ok = side === S.side;
      S.log.push({ x: S.level, ok: ok }); task.count++;
      S.last = ok;
      if (ok) { S.run++; if (S.run === 2) { S.run = 0; if (S.dir === 1) S.reversals.push(S.level); S.dir = -1; S.level = Math.max(0.3, S.level / 1.25); } }
      else { S.run = 0; if (S.dir === -1) S.reversals.push(S.level); S.dir = 1; S.level = Math.min(40, S.level * 1.25); }
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= N) { S.phase = "done"; w.render(); } else next(); }, 450);
    }
    function staircaseEstimate() {
      var r = S.reversals.slice(-6), s = 0, i;
      if (!r.length) return NaN;
      for (i = 0; i < r.length; i++) s += Math.log(r[i]);
      return Math.exp(s / r.length);
    }

    w = QB.widget(el, {
      title: "Which patch is brighter? Your own threshold",
      sub: "Two grey patches; one is brighter by the percentage shown in the plot. F, or tap the left half: left is brighter. J, or tap the right half: right is brighter. Guess when you are not sure: that is the rule of a forced choice. Two right in a row makes the next trial harder, one wrong makes it easier. After fifty trials the page fits your psychometric function.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function () { task.clear(); S.seed++; S.trial = 0; S.level = 24; S.run = 0; S.dir = 0; S.log = []; S.reversals = []; next(); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.log = []; S.reversals = []; S.last = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Fifty trials, about two minutes. Sit back from the screen and keep the room lighting steady.");
        } else if (S.phase === "done") {
          var f = fit(), se = staircaseEstimate();
          T.message(ctx, b, "Finished.", "Your 75% threshold, fitted: " + (f ? f.th.toFixed(1) + "%" : "–") + ". The staircase's own estimate (aimed at 70.7%): " +
            (isNaN(se) ? "–" : se.toFixed(1) + "%") + ". Screens differ, so compare your own runs, not other people's.");
        } else {
          var side = Math.max(40, Math.min(b.h - 90, (b.w - 80) / 2)), gap = Math.max(16, b.w - 2 * side - 40);
          var x0 = b.x + (b.w - 2 * side - gap) / 2, y0 = b.y + (b.h - side) / 2 - 6, hi = Math.round(BASE * (1 + S.level / 100));
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("trial " + S.trial + " of " + N, b.cx, b.y + 18);
          var lo = "rgb(" + BASE + "," + BASE + "," + BASE + ")", up = "rgb(" + hi + "," + hi + "," + hi + ")";
          ctx.fillStyle = S.side === 0 ? up : lo; ctx.fillRect(x0, y0, side, side);
          ctx.fillStyle = S.side === 1 ? up : lo; ctx.fillRect(x0 + side + gap, y0, side, side);
          if (S.phase === "feedback") {
            ctx.fillStyle = S.last ? OK : BAD; ctx.font = "600 13px system-ui, sans-serif";
            ctx.fillText(S.last ? "Right" : "Wrong", b.cx, b.y + b.h - 18);
          } else {
            ctx.fillStyle = C.muted; ctx.font = "12.5px system-ui, sans-serif";
            ctx.fillText(b.w < 420 ? "F / left        J / right" : "F, or tap the left half: left        J, or tap the right half: right", b.cx, b.y + b.h - 18);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [0, Math.max(N, S.log.length)], y: [0, 40], title: "Your staircase, and the threshold fitted to all your answers", xlabel: "trial; the difference in percent, upward" });
        if (S.log.length) {
          var xs = [], ys = [], i;
          for (i = 0; i < S.log.length; i++) { xs.push(i + 1); ys.push(S.log[i].x); }
          a.line(xs, ys, { color: C.muted, width: 1 });
          for (i = 0; i < S.log.length; i++) a.dots([i + 1], [S.log[i].x], { color: S.log[i].ok ? OK : BAD, r: 3 });
        }
        if (S.phase === "done") {
          var ff = fit();
          if (ff) {
            a.line([0, N], [ff.th, ff.th], { color: YOU, width: 2, dash: [5, 4] });
            a.text(1, ff.th + 1.6, "fitted 75% threshold " + ff.th.toFixed(1) + "%", { color: YOU, size: 11 });
          }
        }
      },
      readout: function () {
        var se = staircaseEstimate(), ff = S.phase === "done" ? fit() : null, k = 0, i;
        for (i = 0; i < S.log.length; i++) if (S.log[i].ok) k++;
        return [["trials", String(S.log.length)], ["right", S.log.length ? Math.round(100 * k / S.log.length) + "%" : "–"],
          ["current difference", S.phase === "idle" ? "–" : S.level.toFixed(1) + "%"],
          ["staircase estimate", isNaN(se) ? "–" : se.toFixed(1) + "%"], ["fitted 75% threshold", ff ? ff.th.toFixed(1) + "%" : "–"]];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The patches differ in the grey level your screen is asked to show, not in measured light, and screens, brightness settings and room light all change the result: compare your own runs, not other people's. The fit is maximum likelihood on a grid, a cumulative Gaussian in the logarithm of the difference with a guess rate of 50% and a lapse rate fixed at 2%, as in the film's chapter 6. The staircase is two-down one-up, so its turning points gather near the 70.7% point (chapter 7).",
    });
  };

  // ---- Part 12: old or new?  A recognition test with confidence, and your own ROC -------------------------------
  W.oldnew = function (el) {
    var w = null, NS = 16, OK = "#5bd18b", FA = "#f28fb8", YOU = "#f2c14e", ROC = "#7ec8f5";
    var POOL = ["candle", "harbour", "violin", "pepper", "ladder", "comet", "garden", "button", "tunnel", "feather",
      "anchor", "orange", "mirror", "basket", "thunder", "pillow", "rocket", "saddle", "island", "kettle", "marble",
      "lantern", "cactus", "wallet", "helmet", "meadow", "trumpet", "blanket", "glacier", "pencil", "dolphin", "carpet"];
    var NAMES = ["sure new", "probably new", "maybe new", "maybe old", "probably old", "sure old"];
    var S = { phase: "idle", seed: 0, study: [], test: [], i: 0, ratings: [] };
    function z(p) { // inverse normal cdf (Acklam)
      var a = [-39.6968302866538, 220.946098424521, -275.928510446969, 138.357751867269, -30.6647980661472, 2.50662827745924],
          b = [-54.4760987982241, 161.585836858041, -155.698979859887, 66.8013118877197, -13.2806815528857],
          c = [-0.00778489400243029, -0.322396458041136, -2.40075827716184, -2.54973253934373, 4.37466414146497, 2.93816398269878],
          d = [0.00778469570904146, 0.32246712907004, 2.445134137143, 3.75440866190742], q, r;
      if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    }
    function phi(x) {
      var t = 1 / (1 + 0.2316419 * Math.abs(x)), y = 0.3989423 * Math.exp(-x * x / 2) * t *
        (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
      return x > 0 ? 1 - y : y;
    }
    function shuffle(arr, u) { var a = arr.slice(), i, j, t; for (i = a.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function start() {
      var u = QB.rng(7919 * (++S.seed) + 17), words = shuffle(POOL, u), old = words.slice(0, NS), fresh = words.slice(NS, 2 * NS), test = [], i;
      for (i = 0; i < NS; i++) { test.push({ word: old[i], old: true }); test.push({ word: fresh[i], old: false }); }
      S.study = old; S.test = shuffle(test, u); S.i = 0; S.ratings = []; S.phase = "study"; w.render();
    }
    function summary() { // counts per rating, cumulative points, d' and c at the old/new boundary
      var n = S.ratings.length, so = [0, 0, 0, 0, 0, 0], sn = [0, 0, 0, 0, 0, 0], i, no = 0, nn = 0;
      for (i = 0; i < n; i++) { if (S.test[i].old) { so[S.ratings[i]]++; no++; } else { sn[S.ratings[i]]++; nn++; } }
      if (!no || !nn) return null;
      var pts = [], h = 0, f = 0, k;
      for (k = 5; k >= 1; k--) { h += so[k]; f += sn[k]; pts.push([f / nn, h / no]); }
      var hits = so[3] + so[4] + so[5], fas = sn[3] + sn[4] + sn[5];
      var H = (hits + 0.5) / (no + 1), F = (fas + 0.5) / (nn + 1);
      var area = 0, px = 0, py = 0;
      for (k = 0; k < pts.length; k++) { area += (pts[k][0] - px) * (pts[k][1] + py) / 2; px = pts[k][0]; py = pts[k][1]; }
      area += (1 - px) * (1 + py) / 2;
      return { pts: pts, hits: hits, fas: fas, no: no, nn: nn, d: z(H) - z(F), c: -0.5 * (z(H) + z(F)), area: area };
    }
    var task = T.create(el, { keys: { "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, f: 1, j: 4 },
      accepting: function () { return S.phase === "study" || S.phase === "test"; }, respond: answer });
    function answer(v, how) {
      if (!w) return;
      if (how === "tap") v = v === 0 ? 1 : 4;
      if (S.phase === "study") {
        task.count++; S.i++;
        if (S.i >= S.study.length) { S.i = 0; S.phase = "test"; }
        w.render(); return;
      }
      if (S.phase !== "test") return;
      S.ratings.push(v); task.count++; S.i++;
      if (S.i >= S.test.length) S.phase = "done";
      w.render();
    }

    w = QB.widget(el, {
      title: "Old or new? Your recognition ROC",
      sub: "First, sixteen words: read each and press any key, or tap, for the next. Then thirty-two words, half of them old. Rate each: 1 sure new, 2 probably new, 3 maybe new, 4 maybe old, 5 probably old, 6 sure old. F and J (or tapping the left or right half) give 2 and 5. The page turns your ratings into hits, false alarms, d', c and your own ROC.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function () { task.clear(); start(); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.ratings = []; S.i = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Sixteen words to read at your own pace, then thirty-two to rate. About three minutes.");
        } else if (S.phase === "study") {
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("study: word " + (S.i + 1) + " of " + S.study.length + ". Remember it, then press a key or tap", b.cx, b.y + 18);
          ctx.fillStyle = C.ink; ctx.font = "600 30px system-ui, sans-serif";
          ctx.fillText(S.study[S.i], b.cx, b.cy);
        } else if (S.phase === "test") {
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("test: word " + (S.i + 1) + " of " + S.test.length, b.cx, b.y + 18);
          ctx.fillStyle = C.ink; ctx.font = "600 30px system-ui, sans-serif";
          ctx.fillText(S.test[S.i].word, b.cx, b.cy - 6);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText(b.w < 420 ? "1 ... 6, or tap left (new) / right (old)" : "1 sure new  2  3  4  5  6 sure old;  F = probably new,  J = probably old", b.cx, b.y + b.h - 18);
        } else {
          var s = summary();
          T.message(ctx, b, "Finished.", s ? ("Hits " + s.hits + " of " + s.no + ", false alarms " + s.fas + " of " + s.nn + ": d' = " + s.d.toFixed(2) + ", c = " + s.c.toFixed(2) + ". The area under your ROC is " + s.area.toFixed(2) + ".") : "");
        }
        ctx.restore();

        var a = g[1].axes({ x: [0, 1], y: [0, 1], title: "Your ROC from your confidence ratings", xlabel: "false-alarm rate; hit rate upward" });
        a.line([0, 1], [0, 1], { color: C.muted, width: 1, dash: [4, 4] });
        var xs = [], ys = [], k, x;
        for (k = 0; k <= 60; k++) { x = k / 60; xs.push(x); ys.push(1 - phi(z(Math.min(0.9999, Math.max(0.0001, 1 - x))) - 1.2)); }
        a.line(xs, ys, { color: ROC, width: 1.5 });
        a.text(0.42, 0.18, "Psyche, d' = 1.2", { color: ROC, size: 11 });
        var s2 = S.ratings.length ? summary() : null;
        if (s2) {
          var px = [0], py = [0];
          for (k = 0; k < s2.pts.length; k++) { px.push(s2.pts[k][0]); py.push(s2.pts[k][1]); }
          px.push(1); py.push(1);
          a.line(px, py, { color: YOU, width: 2 });
          for (k = 0; k < s2.pts.length; k++) a.dots([s2.pts[k][0]], [s2.pts[k][1]], { color: k === 2 ? OK : YOU, r: 4 });
        }
      },
      readout: function () {
        var s = S.ratings.length ? summary() : null;
        return [["phase", S.phase], ["rated", String(S.ratings.length) + " of " + (S.test.length || 2 * NS)],
          ["hit rate", s ? Math.round(100 * s.hits / s.no) + "%" : "–"], ["false-alarm rate", s ? Math.round(100 * s.fas / s.nn) + "%" : "–"],
          ["d'", s ? s.d.toFixed(2) : "–"], ["c", s ? s.c.toFixed(2) : "–"], ["area under ROC", s ? s.area.toFixed(2) : "–"]];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. Each boundary between ratings is a criterion: count only 'sure old' as old and you get the strictest point, then 'sure or probably old', and so on (chapter 3). The green point is the old/new boundary, where d' and c are computed with the log-linear correction (k + 0.5)/(n + 1) (chapter 4). The area is the trapezoid under your points. Sixteen words of each kind make a small test: one standard error of d' is about 0.5. The blue curve is an equal-variance observer with d' = 1.2 for comparison; real recognition curves are usually lopsided, with a zROC slope near 0.8 (chapter 6).",
    });
  };
  // ---- Part 13: which patch has stripes?  Four staircases, one per bar width, and your own CSF -------------------
  W.contrast = function (el) {
    var w = null, NPER = 16, OK = "#5bd18b", BAD = "#ef6f6c", YOU = "#f2c14e";
    var CYC = [1.5, 4, 10, 24];  // cycles across a patch
    var S = { phase: "idle", trial: 0, seed: 0, order: [], k: 0, side: 0, last: null, st: [] };
    function fresh() {
      S.st = CYC.map(function () { return { c: 0.3, run: 0, dir: 0, rev: [], n: 0 }; });
    }
    fresh();
    function estimate(st) { // the geometric mean of the last reversals, or the current level
      var r = st.rev.slice(-4), s = 0, i;
      if (!r.length) return st.n ? st.c : NaN;
      for (i = 0; i < r.length; i++) s += Math.log(r[i]);
      return Math.exp(s / r.length);
    }
    function next() {
      var u = QB.rng(7919 * S.seed + 41 * S.trial + 5);
      S.k = S.order[S.trial]; S.side = u() < 0.5 ? 0 : 1; S.trial++;
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      var st = S.st[S.k], ok = side === S.side;
      st.n++; task.count++; S.last = ok;
      if (ok) { st.run++; if (st.run === 2) { st.run = 0; if (st.dir === 1) st.rev.push(st.c); st.dir = -1; st.c = Math.max(0.004, st.c / 1.4); } }
      else { st.run = 0; if (st.dir === -1) st.rev.push(st.c); st.dir = 1; st.c = Math.min(1, st.c * 1.4); }
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= S.order.length) { S.phase = "done"; w.render(); } else next(); }, 420);
    }
    function start() {
      task.clear(); S.seed++; S.trial = 0; fresh();
      var u = QB.rng(104729 * S.seed + 17), order = [], i, j, t;
      for (i = 0; i < NPER; i++) for (j = 0; j < CYC.length; j++) order.push(j);
      for (i = order.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      S.order = order; next();
    }
    function patch(ctx, x, y, size, cycles, contrast, striped) {
      // drawn at the screen's own pixel density on a canvas of its own, then placed (the page canvas is scaled)
      var dpr = Math.min(window.devicePixelRatio || 1, 2), n = Math.round(size * dpr);
      var off = document.createElement("canvas"); off.width = n; off.height = n;
      var oc = off.getContext("2d"), img = oc.createImageData(n, n), d = img.data, i, j, v;
      for (j = 0; j < n; j++) for (i = 0; i < n; i++) {
        var r = Math.sqrt(Math.pow(i - n / 2, 2) + Math.pow(j - n / 2, 2)) / (n / 2);
        var win = r < 0.7 ? 1 : (r < 1 ? 0.5 * (1 + Math.cos(Math.PI * (r - 0.7) / 0.3)) : 0);
        var s = striped ? contrast * win * Math.sin(2 * Math.PI * cycles * i / n) : 0;
        v = Math.round(128 * (1 + s) + (Math.random() - 0.5)); // a little dither below one grey level
        var k = 4 * (j * n + i); d[k] = d[k + 1] = d[k + 2] = Math.max(0, Math.min(255, v)); d[k + 3] = 255;
      }
      oc.putImageData(img, 0, 0);
      ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(off, x, y, size, size); ctx.restore();
    }

    w = QB.widget(el, {
      title: "Which patch has stripes? Your contrast sensitivity",
      sub: "Two grey patches; one holds faint vertical stripes. F, or tap the left half: the left one has stripes. J, or tap the right half: the right one. Guess when you are not sure. Four widths of stripe are mixed at random, each with its own staircase: two right in a row makes its stripes fainter, one wrong makes them stronger. After 64 trials the page draws your contrast sensitivity at the four widths.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; fresh(); S.last = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Sixty-four trials, about three minutes. Sit at arm's length and keep your screen's brightness and the room lighting steady.");
        } else if (S.phase === "done") {
          var best = 0, bi = 0, i;
          for (i = 0; i < CYC.length; i++) { var e = estimate(S.st[i]); if (1 / e > best) { best = 1 / e; bi = i; } }
          T.message(ctx, b, "Finished.", "You were most sensitive to the " + ["widest", "wide", "narrow", "narrowest"][bi] + " stripes, seen at about " + (100 / best).toFixed(1) + "% contrast. Screens differ: compare your own runs, and try again from twice as far away.");
        } else {
          var size = Math.floor(Math.max(60, Math.min(b.h - 80, (b.w - 70) / 2, 180))), gap = Math.max(16, Math.min(60, b.w - 2 * size - 30));
          var x0 = Math.round(b.x + (b.w - 2 * size - gap) / 2), y0 = Math.round(b.y + (b.h - size) / 2 - 6), st = S.st[S.k];
          ctx.fillStyle = "rgb(128,128,128)"; ctx.fillRect(x0 - 8, y0 - 8, 2 * size + gap + 16, size + 16);
          patch(ctx, x0, y0, size, CYC[S.k], st.c, S.side === 0);
          patch(ctx, x0 + size + gap, y0, size, CYC[S.k], st.c, S.side === 1);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("trial " + S.trial + " of " + S.order.length, b.cx, b.y + 16);
          if (S.phase === "feedback") {
            ctx.fillStyle = S.last ? OK : BAD; ctx.font = "600 13px system-ui, sans-serif";
            ctx.fillText(S.last ? "Right" : "Wrong", b.cx, b.y + b.h - 16);
          } else {
            ctx.fillStyle = C.muted; ctx.font = "12.5px system-ui, sans-serif";
            ctx.fillText(b.w < 420 ? "F / left        J / right" : "F, or tap the left half: left        J, or tap the right half: right", b.cx, b.y + b.h - 16);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [1, 32], y: [1, 300], logx: true, logy: true, xticks: CYC, xfmt: function (v) { return String(v); },
          title: "Your sensitivity, 1 / threshold", xlabel: "cycles across a patch" });
        var xs = [], ys = [], i;
        for (i = 0; i < CYC.length; i++) { var e2 = estimate(S.st[i]); if (!isNaN(e2)) { xs.push(CYC[i]); ys.push(Math.min(300, 1 / e2)); } }
        if (xs.length) {
          if (xs.length > 1) a.line(xs, ys, { color: S.phase === "done" ? YOU : C.muted, width: 2 });
          a.dots(xs, ys, { color: YOU, r: 4 });
        }
      },
      readout: function () {
        var out = [["trials", String(S.trial)]], i;
        for (i = 0; i < CYC.length; i++) {
          var e = estimate(S.st[i] || { rev: [], n: 0 });
          out.push([CYC[i] + " cycles", isNaN(e) ? "–" : (100 * e).toFixed(1) + "%"]);
        }
        return out;
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The stripes are sine gratings in a soft round window, drawn in the grey levels your screen is asked to show, with a little random dither so contrasts below one grey level (about 0.8%) are not simply lost. Cycles across a patch become cycles per degree only once you fix the patch's size on your screen and your distance: at arm's length a 4 cm patch spans about 4 degrees, so the four widths are roughly 0.4, 1, 2.5 and 6 cycles per degree. Each width has its own two-down one-up staircase (chapter 7 of Part 11), and the threshold is the geometric mean of its last four turning points. Most people are most sensitive to the middle widths and need much more contrast for the finest: the band-pass shape of chapter 6.",
    });
  };
  // ---- Part 14: which shaft is longer?  Two staircases find your own Müller-Lyer illusion --------------------------
  W.illusion = function (el) {
    var w = null, NPER = 20, YOU = "#f2c14e", UPC = "#7ec8f5", DNC = "#b39ddb";
    var S = { phase: "idle", trial: 0, seed: 0, order: [], k: 0, jit: [0, 0], last: null, st: [] };
    function fresh() {  // comparison length as a ratio of the standard: one staircase starts long, one short
      S.st = [{ r: 1.45, dir: 0, rev: [], hist: [] }, { r: 0.85, dir: 0, rev: [], hist: [] }];
    }
    fresh();
    function pse(st) {
      var r = st.rev.slice(-4), s = 0, i;
      if (!r.length) return st.hist.length ? st.r : NaN;
      for (i = 0; i < r.length; i++) s += Math.log(r[i]);
      return Math.exp(s / r.length);
    }
    function both() {
      var a = pse(S.st[0]), b = pse(S.st[1]);
      if (isNaN(a)) return b; if (isNaN(b)) return a;
      return Math.sqrt(a * b);
    }
    function next() {
      var u = QB.rng(7919 * S.seed + 41 * S.trial + 3);
      S.k = S.order[S.trial]; S.jit = [u() - 0.5, u() - 0.5]; S.trial++;
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(which) {  // 0: the left shaft (fins out) looks longer; 1: the right one (fins in)
      if (S.phase !== "show" || !w) return;
      var st = S.st[S.k], d = which === 1 ? -1 : 1;  // right looked longer: shorten it
      st.hist.push(st.r); task.count++; S.last = which;
      if (st.dir !== 0 && d !== st.dir) st.rev.push(st.r);
      st.dir = d;
      var step = st.rev.length >= 2 ? 1.025 : 1.07;
      st.r = Math.max(0.6, Math.min(1.7, d > 0 ? st.r * step : st.r / step));
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= S.order.length) { S.phase = "done"; w.render(); } else next(); }, 300);
    }
    function start() {
      task.clear(); S.seed++; S.trial = 0; fresh();
      var u = QB.rng(104729 * S.seed + 29), order = [], i, j, t;
      for (i = 0; i < NPER; i++) { order.push(0); order.push(1); }
      for (i = order.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      S.order = order; next();
    }
    function shaft(ctx, cx, y, len, out, fin) {
      var a = 35 * Math.PI / 180, x0 = cx - len / 2, x1 = cx + len / 2, s = out ? 1 : -1;
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y);
      ctx.moveTo(x0, y); ctx.lineTo(x0 - s * fin * Math.cos(a), y - fin * Math.sin(a));
      ctx.moveTo(x0, y); ctx.lineTo(x0 - s * fin * Math.cos(a), y + fin * Math.sin(a));
      ctx.moveTo(x1, y); ctx.lineTo(x1 + s * fin * Math.cos(a), y - fin * Math.sin(a));
      ctx.moveTo(x1, y); ctx.lineTo(x1 + s * fin * Math.cos(a), y + fin * Math.sin(a));
      ctx.stroke();
    }

    w = QB.widget(el, {
      title: "Which shaft is longer? Your own Müller-Lyer illusion",
      sub: "Two shafts: the left one has its fins turned out, the right one has them turned in. Judge only the shafts, end to end. F, or tap the left half: the left shaft is longer. J, or tap the right half: the right one is longer. There is no right answer to learn. Two staircases, mixed at random, change the right shaft's length after every answer, one starting long and one short; both settle where the two look equal. After 40 trials the page reports your illusion.",
      panels: 2, height: 340, weights: [1.15, 1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; fresh(); S.last = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Forty judgments, about two minutes. Answer quickly, by how the shafts look.");
        } else if (S.phase === "done") {
          var p = both();
          T.message(ctx, b, "Finished.", "The two shafts looked equal when the fins-in shaft was " + (100 * (p - 1)).toFixed(0) + "% longer than the fins-out one. That is the size of your illusion here; in the laboratory it is often 10 to 30%, and it depends on the fins' angle and length.");
        } else {
          var L = Math.max(50, Math.min(b.w * 0.22, 150)), fin = Math.max(10, L * 0.2), st = S.st[S.k];
          ctx.strokeStyle = YOU; ctx.lineWidth = 3; ctx.lineCap = "round";
          var sh = Math.min(30, b.h * 0.15), yc = b.y + b.h / 2;
          shaft(ctx, b.x + b.w * 0.27, yc + S.jit[0] * sh, L, true, fin);
          shaft(ctx, b.x + b.w * 0.73, yc + S.jit[1] * sh, L * st.r, false, fin);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("trial " + S.trial + " of " + S.order.length, b.cx, b.y + 16);
          ctx.font = "12.5px system-ui, sans-serif";
          ctx.fillText(S.phase === "feedback" ? "Noted" : (b.w < 420 ? "F / left        J / right" : "F, or tap the left half: left        J, or tap the right half: right"), b.cx, b.y + b.h - 16);
        }
        ctx.restore();

        var a = g[1].axes({ x: [0, NPER + 1], y: [0.6, 1.8], title: "The right shaft's length, as a share of the left",
          xlabel: "trial in each staircase" });
        [0, 1].forEach(function (k) {
          var h = S.st[k].hist, xs = [], i;
          for (i = 0; i < h.length; i++) xs.push(i + 1);
          if (h.length > 1) a.line(xs, h, { color: k ? DNC : UPC, width: 2 });
          if (h.length) a.dots(xs, h, { color: k ? DNC : UPC, r: 3 });
        });
        a.line([0, NPER + 1], [1, 1], { color: C.muted, width: 1 });
        var q = both();
        if (S.phase === "done" && !isNaN(q)) a.line([0, NPER + 1], [q, q], { color: YOU, width: 2 });
      },
      readout: function () {
        var a = pse(S.st[0]), b2 = pse(S.st[1]), q = both();
        var f = function (v) { return isNaN(v) ? "–" : (100 * v).toFixed(0) + "%"; };
        return [["trials", String(S.trial)], ["staircase from long", f(a)], ["staircase from short", f(b2)],
          ["point of equality", f(q)], ["illusion", isNaN(q) ? "–" : (100 * (q - 1)).toFixed(0) + "%"]];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. Each staircase lengthens the right shaft after you call the left one longer and shortens it after you call the right one longer, by 7% at first and 2.5% after its second turning point, so it hovers where you answer each way half the time: the point of subjective equality (Part 11, chapter 7). Each staircase's estimate is the geometric mean of its last four turning points, and the two are averaged; starting one long and one short guards against a bias toward the first answer. The shafts are shifted up and down at random so that their ends are not compared along one line. Chapter 4 gives Gregory's account of the illusion, and why its link to rectangular buildings is now contested.",
    });
  };
  // ---- Part 15: up or down?  Do you hear the fundamental, or the spectrum? ----------------------------------------
  W.pitchdir = function (el) {
    var w = null, NCON = 24, NAGREE = 8, YOU = "#f2c14e", F0C = "#5bd18b", SPC = "#7ec8f5";
    var S = { phase: "idle", trial: 0, seed: 0, order: [], cur: null, last: null, res: [] };
    var ctx = null;
    function audio() {
      if (!ctx) {
        var A = window.AudioContext || window.webkitAudioContext;
        if (!A) return null;
        try { ctx = new A(); } catch (e) { return null; }
      }
      if (ctx.state === "suspended" && ctx.resume) ctx.resume();
      return ctx;
    }
    function complexTone(ac, t0, f0, harmonics, dur) {
      var g = ac.createGain();
      g.gain.setValueAtTime(0, t0);
      g.gain.linearRampToValueAtTime(0.18 / harmonics.length, t0 + 0.02);
      g.gain.setValueAtTime(0.18 / harmonics.length, t0 + dur - 0.03);
      g.gain.linearRampToValueAtTime(0, t0 + dur);
      g.connect(ac.destination);
      harmonics.forEach(function (h) {
        var o = ac.createOscillator();
        o.type = "sine"; o.frequency.value = f0 * h;
        o.connect(g); o.start(t0); o.stop(t0 + dur + 0.02);
      });
    }
    // a trial: two tones; conflict trials move the fundamental one way and the harmonics' spectrum the other
    function makeTrial(u, conflict) {
      var f1 = 180 + 60 * u(), up = u() < 0.5, ratio = 1.26;  // about four semitones
      var f2 = up ? f1 * ratio : f1 / ratio;
      var lowH = [2, 3, 4], highH = [5, 6, 7];
      var h1, h2;
      if (conflict) { h1 = up ? highH : lowH; h2 = up ? lowH : highH; }  // f0 up, components down (or the reverse)
      else { h1 = [1, 2, 3, 4]; h2 = [1, 2, 3, 4]; }
      return { f1: f1, f2: f2, h1: h1, h2: h2, up: up, conflict: conflict };
    }
    function play(tr) {
      var ac = audio();
      if (!ac) return 0;
      var t0 = ac.currentTime + 0.05;
      complexTone(ac, t0, tr.f1, tr.h1, 0.45);
      complexTone(ac, t0 + 0.7, tr.f2, tr.h2, 0.45);
      return 1250;
    }
    function next() {
      var u = QB.rng(7919 * S.seed + 41 * S.trial + 7);
      S.cur = makeTrial(u, S.order[S.trial]); S.trial++;
      S.phase = "listen"; w.render();
      var wait = play(S.cur);
      task.later(function () { S.phase = "show"; w.render(); }, wait || 300);
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {  // 0: down (lower), 1: up (higher)
      if (S.phase !== "show" || !w) return;
      var saidUp = side === 1, tr = S.cur;
      task.count++;
      S.res.push({ conflict: tr.conflict, f0: saidUp === tr.up });
      S.last = saidUp;
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= S.order.length) { S.phase = "done"; w.render(); } else next(); }, 450);
    }
    function start() {
      task.clear(); S.seed++; S.trial = 0; S.res = []; audio();
      var u = QB.rng(104729 * S.seed + 31), order = [], i, j, t;
      for (i = 0; i < NCON; i++) order.push(true);
      for (i = 0; i < NAGREE; i++) order.push(false);
      for (i = order.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      S.order = order; next();
    }
    function share(conflict) {
      var n = 0, k = 0;
      S.res.forEach(function (r) { if (r.conflict === conflict) { n++; if (r.f0) k++; } });
      return n ? k / n : NaN;
    }

    w = QB.widget(el, {
      title: "Up or down? The pitch that is not in the sound",
      sub: "Each trial plays two short tones. Did the pitch go up or down? F, or tap the left half: down. J, or tap the right half: up. Use headphones or good speakers at a comfortable level. In most trials the two tones disagree: the fundamental, which neither tone contains, moves one way, and the harmonics you actually hear move the other. There is no right answer to learn; the page counts which one you follow.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Play again", act: function () { if (S.cur && (S.phase === "show" || S.phase === "listen")) play(S.cur); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.res = []; S.cur = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Thirty-two pairs of tones, about two minutes, with sound on. Turn the volume down before you begin, then up to comfortable.");
        } else if (S.phase === "done") {
          var p = share(true), q = share(false);
          T.message(c, b, "Finished.", "On the disagreeing pairs you followed the missing fundamental " + Math.round(100 * p) + "% of the time, and the harmonics " + Math.round(100 * (1 - p)) + "%. On the agreeing pairs you were right " + Math.round(100 * q) + "% of the time. People differ widely on this test, and many sit near one end.");
        } else {
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("pair " + S.trial + " of " + S.order.length, b.cx, b.y + 16);
          c.font = "600 22px system-ui, sans-serif"; c.fillStyle = S.phase === "listen" ? YOU : C.ink;
          c.fillText(S.phase === "listen" ? "Listen" : (S.phase === "feedback" ? "Noted" : "Up or down?"), b.cx, b.cy);
          c.font = "12.5px system-ui, sans-serif"; c.fillStyle = C.muted;
          c.fillText(b.w < 420 ? "F / down        J / up" : "F, or tap the left half: down        J, or tap the right half: up", b.cx, b.y + b.h - 16);
        }
        c.restore();

        var a = g[1].axes({ x: [0, 3], y: [0, 1], xticks: [1, 2], xfmt: function (v) { return v === 1 ? "disagreeing" : "agreeing"; },
          title: "Answers that followed the fundamental", xlabel: "pairs" });
        a.line([0, 3], [0.5, 0.5], { color: C.muted, width: 1 });
        var p1 = share(true), p2 = share(false);
        if (!isNaN(p1)) { a.line([1, 1], [0, p1], { color: F0C, width: 16 }); }
        if (!isNaN(p2)) { a.line([2, 2], [0, p2], { color: SPC, width: 16 }); }
      },
      readout: function () {
        var p = share(true), q = share(false), f = function (v) { return isNaN(v) ? "–" : Math.round(100 * v) + "%"; };
        return [["pairs", String(S.trial)], ["disagreeing: followed the fundamental", f(p)], ["agreeing: right", f(q)]];
      },
      note: "Nothing you answer is stored or sent, and no sound is recorded: the tones are made in your browser. Each tone is a few harmonics of a fundamental between about 180 and 300 Hz, and the fundamental itself is never played in the disagreeing pairs. In those pairs the fundamental moves by about four semitones while the harmonics jump the other way (from the 2nd to 4th harmonics to the 5th to 7th, or back), so a listener who hears the missing fundamental (chapter 4's autocorrelation) and a listener who hears the spectrum's edge answer oppositely. The agreeing pairs include the fundamental and check that you can hear the direction at all. Cheap speakers that cannot play low notes do not matter here: the fundamental is missing on purpose.",
    });
  };
})();
