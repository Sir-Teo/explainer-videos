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
})();
