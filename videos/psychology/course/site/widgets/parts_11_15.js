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
})();
