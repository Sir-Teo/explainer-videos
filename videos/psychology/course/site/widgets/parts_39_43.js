// Interactives for Act X, When minds suffer, and the capstone (Parts 39-43).  Each is an experiment the reader takes
// part in, built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 39: what a positive screen means, case by case. ----
  W.screening = function (el) {
    var w = null;
    // six screening scenarios: prevalence, sensitivity, specificity
    var CASES = [
      { what: "A depression questionnaire in a general clinic", prev: 0.05, sens: 0.85, spec: 0.85 },
      { what: "The same questionnaire in a specialist mood clinic", prev: 0.40, sens: 0.85, spec: 0.85 },
      { what: "A rare condition, an excellent test", prev: 0.001, sens: 0.99, spec: 0.99 },
      { what: "A risk tool for a rare event", prev: 0.01, sens: 0.80, spec: 0.90 },
      { what: "A common condition, a mediocre test", prev: 0.25, sens: 0.70, spec: 0.80 },
      { what: "A screen used twice in a row, both positive", prev: 0.10, sens: 0.81, spec: 0.99 },
    ];
    var BINS = ["under 10%", "10 to 30%", "30 to 60%", "over 60%"];
    function ppv(c) { return c.prev * c.sens / (c.prev * c.sens + (1 - c.prev) * (1 - c.spec)); }
    function bin(p) { return p < 0.1 ? 0 : (p < 0.3 ? 1 : (p < 0.6 ? 2 : 3)); }
    var S = { phase: "idle", k: -1, log: [] };
    function next() {
      S.k++;
      if (S.k >= CASES.length) { S.phase = "done"; task.clear(); }
      else S.phase = "ask";
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "4": 3 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side, how) {
        var choice = how === "tap" ? (side === 0 ? 0 : 3) : side;
        S.log.push({ k: S.k, choice: choice, right: bin(ppv(CASES[S.k])) });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 1800);
      },
    });
    function start() { task.clear(); S.k = -1; S.log = []; task.count = 0; next(); }
    w = QB.widget(el, {
      title: "A positive screen",
      sub: "Each case is a screening test and a population. Someone screens positive: how likely is it that they have the condition? Press 1, 2, 3 or 4 for under 10%, 10 to 30%, 30 to 60% or over 60%.",
      panels: 2, height: 380, weights: [1.3, 1],
      buttons: [
        { label: "Start", act: function () { start(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save();
        if (S.phase === "ask" || S.phase === "shown") {
          var c = CASES[S.k], N = 10000, sick = N * c.prev, tp = sick * c.sens, fp = (N - sick) * (1 - c.spec);
          ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Case " + (S.k + 1) + " of " + CASES.length, b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "600 15px system-ui, sans-serif";
          T.wrap(ctx, c.what, b.cx, b.y + 48, b.w - 40, 19);
          ctx.font = "14px system-ui, sans-serif";
          ctx.fillText("prevalence " + (100 * c.prev).toFixed(c.prev < 0.01 ? 1 : 0) + "%,  sensitivity " + Math.round(100 * c.sens) + "%,  specificity " + Math.round(100 * c.spec) + "%", b.cx, b.y + 96);
          if (S.phase === "shown") {
            var p = ppv(c), last = S.log[S.log.length - 1];
            ctx.fillText("In 10,000 people: " + Math.round(sick) + " have it and " + Math.round(tp) + " of them test positive;", b.cx, b.cy + 10);
            ctx.fillText(Math.round(fp) + " of the " + Math.round(N - sick) + " without it test positive too.", b.cx, b.cy + 32);
            ctx.font = "600 15px system-ui, sans-serif";
            ctx.fillStyle = last.choice === last.right ? "#5bd18b" : "#ef6f6c";
            ctx.fillText("A positive means the condition " + Math.round(100 * p) + "% of the time (" + BINS[last.right] + ").", b.cx, b.cy + 62);
          } else {
            ctx.font = "600 14px system-ui, sans-serif";
            ctx.fillText("1: under 10%    2: 10 to 30%    3: 30 to 60%    4: over 60%", b.cx, b.y + b.h - 34);
          }
        } else if (S.phase === "done") {
          var right = S.log.filter(function (r) { return r.choice === r.right; }).length;
          T.message(ctx, b, "You placed " + right + " of " + CASES.length + " in the right range.",
                    "Most people overestimate when the condition is rare. Counting in natural frequencies (how many of 10,000 test positive, and how many of those have it) makes the base rate visible.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six screening cases.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your range against the true value, by case", c2.x + 10, c2.y + 18);
        var bh = (c2.h - 60) / CASES.length;
        for (j = 0; j < S.log.length; j++) {
          var r = S.log[j], y = c2.y + 36 + j * bh, wbin = (c2.w - 60) / 4;
          cx.fillStyle = "#3a3f48"; cx.fillRect(c2.x + 40, y, c2.w - 60, bh - 6);
          cx.fillStyle = "#7ec8f5"; cx.fillRect(c2.x + 40 + r.right * wbin, y, wbin - 2, bh - 6);
          cx.strokeStyle = r.choice === r.right ? "#5bd18b" : "#ef6f6c"; cx.lineWidth = 2;
          cx.strokeRect(c2.x + 40 + r.choice * wbin + 2, y + 2, wbin - 6, bh - 10);
          cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.fillText(String(r.k + 1), c2.x + 20, y + bh / 2);
        }
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif";
        cx.fillText("blue: the true range; outline: yours", c2.x + 10, c2.y + c2.h - 10);
        cx.restore();
      },
      readout: function () {
        var right = S.log.filter(function (r) { return r.choice === r.right; }).length;
        return [["answers", String(task.count)], ["in range", S.log.length ? right + " / " + S.log.length : "-"]];
      },
      note: "Nothing you answer is stored or sent. The cases are illustrations with round numbers, not the properties of any real test.",
    });
  };
  // ---- Part 40: the dot-probe, on you, and why twenty trials cannot measure a bias. ----
  W.dotprobe = function (el) {
    var w = null, DOT = "#7ec8f5", WORD = "#e8edf3";
    // mild words only: the task needs a contrast in valence, not distressing material
    var NEUTRAL = ["table", "carpet", "window", "garden", "pencil", "ladder", "kettle", "button"];
    var NEGATIVE = ["danger", "failure", "mistake", "alarm", "reject", "storm", "worry", "blame"];
    var run = T.timed(el, {
      keys: { f: 0, j: 1 },
      trials: function () { return w.v.n; },
      seed: function () { return w.state.seed; },
      stimulus: function (rand) {
        return { neg: rand() < 0.5 ? 0 : 1, dot: rand() < 0.5 ? 0 : 1, a: Math.floor(rand() * 8), b: Math.floor(rand() * 8) };
      },
      correct: function (stim, side) { return side === stim.dot; },
      render: function () { if (w) w.render(); },
      foreperiod: [500, 800], timeout: 2000, pause: { scored: 500, early: 900, timeout: 800 },
      words: { early: "Too early: wait for the dot.", timeout: "No answer in two seconds.",
        wrong: function () { return "Other side (not counted)."; } },
    });
    function stats() {
      var r = run.rts("probe"), m, sd = NaN;
      if (!r.length) return null;
      m = QB.mean(r);
      if (r.length > 2) {
        var ss = 0, i;
        for (i = 0; i < r.length; i++) ss += (r[i] - m) * (r[i] - m);
        sd = Math.sqrt(ss / (r.length - 1));
      }
      // trials of each kind needed to tell a 10 ms difference from noise (two-sided 5%, 80% power)
      var need = isFinite(sd) ? Math.ceil(2 * Math.pow(1.96 + 0.84, 2) * sd * sd / 100) : NaN;
      return { n: r.length, mean: m, sd: sd, need: need, rts: r };
    }
    w = QB.widget(el, {
      title: "The dot-probe, on you",
      sub: "Two words appear, one on the left and one on the right; then a dot replaces one of them. Press F (or tap left) if the dot is on the left, J (or tap right) if it is on the right, as fast as you can. Afterwards you see your times, and why a handful of trials cannot measure anything about one person.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [{ k: "n", label: "Trials", min: 12, max: 40, step: 4, value: 20, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [
        { label: "Start", act: function () { run.reset(); run.start("probe"); } },
        { label: "Clear", act: function () { run.reset(); } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, run.task), s = stats(), i;
        ctx.save(); ctx.textAlign = "center";
        if (run.phase === "wait" || run.phase === "go") {
          ctx.strokeStyle = C.muted; ctx.lineWidth = 2; ctx.beginPath();
          ctx.moveTo(b.cx - 8, b.cy); ctx.lineTo(b.cx + 8, b.cy); ctx.moveTo(b.cx, b.cy - 8); ctx.lineTo(b.cx, b.cy + 8);
          ctx.stroke();
          var xs = [b.x + b.w * 0.25, b.x + b.w * 0.75];
          if (run.phase === "wait") {
            ctx.fillStyle = WORD; ctx.font = "600 18px system-ui, sans-serif";
            for (i = 0; i < 2; i++) ctx.fillText(i === run.stim.neg ? NEGATIVE[run.stim.a] : NEUTRAL[run.stim.b], xs[i], b.cy + 6);
          } else {
            ctx.fillStyle = DOT; ctx.beginPath(); ctx.arc(xs[run.stim.dot], b.cy, 8, 0, 2 * Math.PI); ctx.fill();
          }
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("trial " + run.trial + " of " + v.n + "    left: F    right: J", b.cx, b.y + 22);
        } else if (run.phase === "feedback") {
          T.message(ctx, b, run.msg);
        } else if (run.phase === "done" && s) {
          T.message(ctx, b, "Your mean time: " + Math.round(s.mean) + " ms, spread " + (isFinite(s.sd) ? Math.round(s.sd) : "-") + " ms.",
                    "In groups, the threat bias is a difference of a few to a few tens of milliseconds. With your spread, telling a 10 ms difference from noise in one person would take about " + (isFinite(s.need) ? s.need.toLocaleString() : "-") + " trials of each kind. That is why the score is unreliable for individuals; no score is computed here.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Nothing you do is scored or kept.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your response times, trial by trial", c2.x + 10, c2.y + 18);
        if (s && s.n) {
          var lo = 150, hi = 1000, px = function (k) { return c2.x + 40 + (c2.w - 60) * k / Math.max(1, v.n - 1); };
          var py = function (t) { return c2.y + c2.h - 30 - (c2.h - 70) * (Math.min(hi, Math.max(lo, t)) - lo) / (hi - lo); };
          cx.fillStyle = "rgba(91,209,139,0.25)";
          cx.fillRect(c2.x + 40, py(s.mean + 10), c2.w - 60, Math.max(2, py(s.mean - 10) - py(s.mean + 10)));
          cx.fillStyle = DOT;
          for (i = 0; i < s.rts.length; i++) { cx.beginPath(); cx.arc(px(i), py(s.rts[i]), 4, 0, 2 * Math.PI); cx.fill(); }
          cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif";
          cx.fillText(hi + " ms", c2.x + 4, py(hi) + 4); cx.fillText(lo + " ms", c2.x + 4, py(lo) + 4);
          cx.fillText("green band: 20 ms, about the size of the group effect", c2.x + 10, c2.y + c2.h - 10);
        }
        cx.restore();
      },
      readout: function () {
        var s = stats();
        return [["answers", String(run.task.count)], ["mean time", s ? Math.round(s.mean) + " ms" : "-"]];
      },
      note: "Nothing you answer is stored or sent, and no bias score is computed: the point is the trial-to-trial spread. The words are mild on purpose.",
    });
  };

})();
