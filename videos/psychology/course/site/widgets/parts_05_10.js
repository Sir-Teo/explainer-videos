// Interactives for Act II, The Wet Machine (Parts 5-10).  As in Act I, each is an experiment the reader takes part
// in, built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 5: you are the cell downstream; which of two spike trains came from the stronger stimulus? ---------
  W.spiketrain = function (el) {
    var w = null, audio = null;
    var LO = 20, HI = 30, BLOCK = 12, YOU = "#f2c14e", IDEAL = "#9fd8f0";
    var S = { phase: "idle", trial: 0, win: 200, left: [], right: [], strong: 0, msg: "", ok: false, log: [], seed: 0 };

    // A Poisson train: waiting times between signals are exponential.  Times in ms, up to `ms`.
    function train(u, rate, ms) {
      var t = 0, out = [];
      for (;;) { t += -Math.log(1 - u()) / rate * 1000; if (t >= ms) break; out.push(t); }
      return out;
    }
    function pmf(k, lam) { var lp = -lam + k * Math.log(lam), i; for (i = 2; i <= k; i++) lp -= Math.log(i); return Math.exp(lp); }
    // How often a reader who simply counts is right: P(more in the stronger train) + half of P(a tie).
    function ideal(ms) {
      var a = LO * ms / 1000, b = HI * ms / 1000, n = Math.ceil(b + 10 * Math.sqrt(b) + 12), win = 0, tie = 0, below = 0, j;
      for (j = 0; j <= n; j++) { var pa = pmf(j, a), pb = pmf(j, b); win += pb * below; tie += pb * pa; below += pa; }
      return win + 0.5 * tie;
    }
    var GRID = [], CURVE = [], q;
    for (q = 50; q <= 1000; q += 25) { GRID.push(q); CURVE.push(ideal(q)); }

    function next() {
      S.trial++;
      var u = QB.rng(7001 * S.seed + 131 * S.trial + Math.round(S.win));
      S.strong = u() < 0.5 ? 0 : 1;
      var weak = train(u, LO, S.win), strong = train(u, HI, S.win);
      S.left = S.strong === 0 ? strong : weak; S.right = S.strong === 0 ? weak : strong;
      S.phase = "show"; S.msg = "";
      w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      S.ok = side === S.strong;
      S.log.push({ win: S.win, correct: S.ok }); task.count++;
      var ns = S.strong ? S.right.length : S.left.length, nw = S.strong ? S.left.length : S.right.length;
      S.msg = (S.ok ? "Right. " : "No. ") + "The " + (S.strong ? "right" : "left") + " one: " + ns + " signals against " + nw + ".";
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= BLOCK) { S.phase = "done"; w.render(); } else next(); }, 1000);
    }
    function click(when) {
      var o = audio.createOscillator(), g = audio.createGain();
      o.frequency.value = 900;
      g.gain.setValueAtTime(0.22, when); g.gain.exponentialRampToValueAtTime(0.001, when + 0.004);
      o.connect(g); g.connect(audio.destination); o.start(when); o.stop(when + 0.006);
    }
    // Adrian listened to his fibres through a loudspeaker: each signal a click.  Left recording first, then right.
    function hear() {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC || (S.phase !== "show" && S.phase !== "feedback")) return;
      try {
        audio = audio || new AC();
        var t0 = audio.currentTime + 0.05, gap = S.win / 1000 + 0.4;
        [S.left, S.right].forEach(function (tr, k) { tr.forEach(function (ms) { click(t0 + k * gap + ms / 1000); }); });
      } catch (err) { audio = null; }
    }
    function score(win) {
      var n = 0, k = 0, i;
      for (i = 0; i < S.log.length; i++) if (win === undefined || S.log[i].win === win) { n++; if (S.log[i].correct) k++; }
      return { n: n, k: k };
    }

    w = QB.widget(el, {
      title: "Reading a spike train",
      sub: "You are the cell downstream. Two recordings appear, made from one model sensory cell under two stimuli; one stimulus was stronger, and the cell answered it with 30 signals a second instead of 20. Every signal is the same size. Say which recording came from the stronger stimulus: F for the left, J for the right, or tap a side. Then change the length of the recordings and try again.",
      panels: 2, height: 340, weights: [1.35, 1],
      controls: [
        { k: "win", label: "Length of each recording", min: 50, max: 1000, step: 50, value: 200, fmt: function (x) { return x.toFixed(0) + " ms"; } },
      ],
      buttons: [
        { label: "Start", act: function (state, v) { task.clear(); S.win = v.win; S.seed++; S.trial = 0; next(); } },
        { label: "Hear this pair", act: function () { hear(); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.log = []; S.msg = ""; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, k;
        ctx.save();
        ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Twelve pairs of recordings; for each, say which came from the stronger stimulus.");
        } else if (S.phase === "done") {
          var all = score(S.win);
          T.message(ctx, b, "Block finished: " + all.k + " of " + all.n + " right at " + S.win + " ms.",
            "Move the slider to a shorter or a longer recording and press Start again. Your dots collect on the other panel, beside the curve for a reader who simply counts.");
        } else {
          ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText(b.w < 420 ? "pair " + S.trial + " of " + BLOCK + ": which was the stronger stimulus?"
            : "pair " + S.trial + " of " + BLOCK + ", " + S.win + " ms each: which came from the stronger stimulus?", b.cx, b.y + 26);
          ctx.strokeStyle = "#1b2230"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(b.cx, b.y + 48); ctx.lineTo(b.cx, b.y + b.h - 62); ctx.stroke();
          var halves = [S.left, S.right];
          for (k = 0; k < 2; k++) {
            var x0 = (k ? b.cx + 14 : b.x + 22), x1 = (k ? b.x + b.w - 22 : b.cx - 14), y = b.cy - 6, tr = halves[k];
            ctx.strokeStyle = "#2a3242"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x0, y + 26); ctx.lineTo(x1, y + 26); ctx.stroke();
            ctx.strokeStyle = S.phase === "feedback" && k === S.strong ? YOU : C.ink; ctx.lineWidth = 2; ctx.beginPath();
            for (i = 0; i < tr.length; i++) { var x = x0 + (x1 - x0) * tr[i] / S.win; ctx.moveTo(x, y - 26); ctx.lineTo(x, y + 26); }
            ctx.stroke();
            ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
            ctx.fillText(k ? "J, or tap here" : "F, or tap here", (x0 + x1) / 2, b.y + b.h - 46);
          }
          if (S.phase === "feedback") {
            ctx.fillStyle = S.ok ? YOU : C.loss; ctx.font = "600 13px system-ui, sans-serif";
            ctx.fillText(S.msg, b.cx, b.y + b.h - 22);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [40, 1200], y: [0.4, 1.03], logx: true, title: "How often right, by length of recording", xlabel: "length of each recording (ms)" });
        a.hline(0.5, { color: C.muted });
        a.text(45, 0.53, "guessing", { color: C.muted, dx: 4, size: 11 });
        a.line(GRID, CURVE, { color: IDEAL });
        a.text(1000, 0.72, "a reader who counts", { color: IDEAL, align: "right", dx: -4, size: 11 });
        var seen = {}, xs = [], ys = [];
        for (i = 0; i < S.log.length; i++) seen[S.log[i].win] = true;
        for (k in seen) { var sc = score(Number(k)); xs.push(Number(k)); ys.push(sc.k / sc.n); }
        if (xs.length) {
          a.dots(xs, ys, { color: YOU, r: 6, alpha: 0.95 });
          a.text(45, 0.97, "you", { color: YOU, dx: 4, size: 11.5, bold: true });
        } else {
          a.text(45, 0.97, "Your answers appear here as dots.", { color: C.muted, dx: 4, size: 11.5 });
        }
        a.vline(v.win, { color: "#2a3242" });
      },
      readout: function (v) {
        var all = score(), here = score(S.win);
        return [
          ["pairs answered", String(all.n)],
          ["right so far", all.n ? QB.pct(all.k / all.n, 0) : "–"],
          ["at " + S.win + " ms", here.n ? here.k + " of " + here.n : "–"],
          ["a reader who counts, at the slider's length", QB.pct(ideal(v ? v.win : S.win), 0)],
        ];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The recordings are simulated: a model cell that fires at random moments, 20 times a second under the weaker stimulus and 30 under the stronger. With a long recording the difference is plain. With a short one it often is not, and nobody could do better: the curve is the best that any reader can manage by counting, about 62% for 50 ms and 92% for a second. A brain has to act within a fraction of a second, so it cannot count one cell for long. It reads many cells at once instead, which is one reason it has so many. Press Hear this pair to listen as Adrian did in 1926, with each signal a click (left recording first).",
    });
  };
})();
