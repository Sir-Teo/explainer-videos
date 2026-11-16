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

  // ---- Part 41: shading on you.  Bumps or dents, and the prior that light comes from above. ----
  W.shading = function (el) {
    var w = null, BUMP = "#5bd18b", DENT = "#ef6f6c";
    // the direction the light seems to come from, in degrees clockwise from straight up
    var ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];
    var S = { phase: "idle", k: -1, order: [], log: [] };
    function shuffle(seed) {
      var r = QB.rng(seed), a = [], i, j, t;
      for (i = 0; i < 2; i++) for (j = 0; j < ANGLES.length; j++) a.push(ANGLES[j]);
      for (i = a.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function next() {
      S.k++;
      if (S.k >= S.order.length) { S.phase = "done"; task.clear(); } else S.phase = "ask";
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        S.log.push({ angle: S.order[S.k], bump: side === 0 });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 400);
      },
    });
    function start(seed) { task.clear(); S.order = shuffle(seed); S.k = -1; S.log = []; task.count = 0; next(); }
    function disc(ctx, x, y, r, angle) {
      var a = (angle - 90) * Math.PI / 180, dx = Math.cos(a) * r, dy = Math.sin(a) * r;
      var g = ctx.createLinearGradient(x + dx, y + dy, x - dx, y - dy);
      g.addColorStop(0, "#f2f2f2"); g.addColorStop(1, "#202020");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI); ctx.fill();
    }
    function shareBump(angle) {
      var n = 0, b = 0, i;
      for (i = 0; i < S.log.length; i++) if (S.log[i].angle === angle) { n++; if (S.log[i].bump) b++; }
      return n ? b / n : NaN;
    }
    w = QB.widget(el, {
      title: "Bumps or dents, on you",
      sub: "Each disc is shaded light to dark. Does it bulge toward you, or is it a dent? Press F (or tap left) for a bump, J (or tap right) for a dent. Sixteen discs; then see how your answers follow the direction of the light.",
      panels: 2, height: 340, weights: [1, 1.1],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i;
        ctx.save(); ctx.textAlign = "center";
        if (S.phase === "ask" || S.phase === "shown") {
          disc(ctx, b.cx, b.cy, Math.min(b.w, b.h) * 0.22, S.order[S.k]);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("disc " + (S.k + 1) + " of " + S.order.length + "    bump: F    dent: J", b.cx, b.y + 22);
        } else if (S.phase === "done") {
          T.message(ctx, b, "Finished.", "On the right: how often you saw a bump, by where the light side was. A prior that light comes from above predicts bumps when the light side is up and dents when it is down, with doubt when it is to the side.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Nothing you answer is scored or kept.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "center"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Share you saw as bumps, by direction of the light side", c2.x + c2.w / 2, c2.y + 18);
        var bw = (c2.w - 40) / ANGLES.length, base = c2.y + c2.h - 50, top = c2.y + 40;
        for (i = 0; i < ANGLES.length; i++) {
          var x = c2.x + 20 + i * bw, pr = (Math.cos(ANGLES[i] * Math.PI / 180) + 1) / 2, sh = shareBump(ANGLES[i]);
          cx.strokeStyle = "#9aa4b2"; cx.setLineDash([3, 3]);
          cx.strokeRect(x + 4, base - (base - top) * pr, bw - 8, (base - top) * pr);
          cx.setLineDash([]);
          if (isFinite(sh)) { cx.fillStyle = sh >= 0.5 ? BUMP : DENT; cx.fillRect(x + 8, base - (base - top) * sh, bw - 16, (base - top) * sh); }
          disc(cx, x + bw / 2, base + 20, Math.min(12, bw / 3), ANGLES[i]);
        }
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif";
        cx.fillText("dashed: what a light-from-above prior predicts", c2.x + c2.w / 2, c2.y + c2.h - 6);
        cx.restore();
      },
      readout: function () {
        return [["answers", String(task.count)], ["bumps", String(S.log.filter(function (r) { return r.bump; }).length)]];
      },
      note: "Nothing you answer is stored or sent. The prediction is a cosine of the light's direction, a simple stand-in for the prior; people differ, and the bias toward light from slightly left of above is well known.",
    });
  };

  // ---- Part 42: the two-graphs problem, case by case.  Can this design show that therapy worked? ----
  W.twographs = function (el) {
    var w = null;
    var CASES = [
      { what: "Clients' symptom scores at the first and last session of therapy: they fell by a third.", right: 1,
        why: "No control: people come at their worst and improve anyway (regression to the mean, natural recovery)." },
      { what: "People randomized to therapy or a waiting list; the therapy group improved more.", right: 0,
        why: "Randomization makes the groups comparable, so therapy did more than waiting, though waiting may itself do a little harm." },
      { what: "People who chose therapy against people who were offered it and declined; the first group improved more.", right: 1,
        why: "Self-selection: those who choose therapy may differ in motivation, support or severity." },
      { what: "People randomized to therapy or to a credible placebo therapy with the same time and warmth; therapy did better.", right: 0,
        why: "The strongest design here: it shows something beyond the common factors." },
      { what: "A randomized trial analysed only the people who finished; 40% dropped out of therapy and 10% of the control arm.", right: 2,
        why: "Uneven dropout breaks the randomization; analyse everyone randomized (intention to treat)." },
      { what: "A meta-analysis of the published trials finds a large effect.", right: 2,
        why: "It shows an effect, but published trials overstate its size when unpublished ones are missing." },
    ];
    var NAMES = ["yes", "no", "only partly"];
    var S = { phase: "idle", k: -1, log: [] };
    function next() {
      S.k++;
      if (S.k >= CASES.length) { S.phase = "done"; task.clear(); } else S.phase = "ask";
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side, how) {
        var choice = how === "tap" ? (side === 0 ? 0 : 1) : side;
        S.log.push({ k: S.k, choice: choice, right: CASES[S.k].right });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 2600);
      },
    });
    function start() { task.clear(); S.k = -1; S.log = []; task.count = 0; next(); }
    w = QB.widget(el, {
      title: "Did the therapy work?",
      sub: "Each case is a study. Can it show that the therapy caused the improvement? Press 1 for yes, 2 for no, 3 for only partly (or tap left for yes, right for no).",
      panels: 2, height: 360, weights: [1.4, 1],
      buttons: [
        { label: "Start", act: function () { start(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save(); ctx.textAlign = "center";
        if (S.phase === "ask" || S.phase === "shown") {
          var c = CASES[S.k];
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Study " + (S.k + 1) + " of " + CASES.length, b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "600 15px system-ui, sans-serif";
          T.wrap(ctx, c.what, b.cx, b.y + 52, b.w - 40, 20);
          if (S.phase === "shown") {
            var last = S.log[S.log.length - 1];
            ctx.font = "600 14px system-ui, sans-serif";
            ctx.fillStyle = last.choice === last.right ? "#5bd18b" : "#ef6f6c";
            ctx.fillText("The answer: " + NAMES[c.right] + ".", b.cx, b.cy + 30);
            ctx.fillStyle = C.ink; ctx.font = "13px system-ui, sans-serif";
            T.wrap(ctx, c.why, b.cx, b.cy + 54, b.w - 40, 18);
          } else {
            ctx.font = "600 14px system-ui, sans-serif"; ctx.fillStyle = C.ink;
            ctx.fillText("1: yes    2: no    3: only partly", b.cx, b.y + b.h - 30);
          }
        } else if (S.phase === "done") {
          var right = S.log.filter(function (r) { return r.choice === r.right; }).length;
          T.message(ctx, b, "You matched " + right + " of " + CASES.length + ".",
                    "Only a comparison with a randomized control can show what therapy added; the kind of control decides what it shows.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six studies.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your answer and the answer, by study", c2.x + 10, c2.y + 18);
        var bh = (c2.h - 50) / CASES.length;
        for (j = 0; j < S.log.length; j++) {
          var r = S.log[j], y = c2.y + 34 + j * bh;
          cx.fillStyle = r.choice === r.right ? "#5bd18b" : "#ef6f6c";
          cx.fillText((r.k + 1) + ".  you: " + NAMES[r.choice] + "   answer: " + NAMES[r.right], c2.x + 14, y + bh / 2);
        }
        cx.restore();
      },
      readout: function () {
        var right = S.log.filter(function (r) { return r.choice === r.right; }).length;
        return [["answers", String(task.count)], ["matched", S.log.length ? right + " / " + S.log.length : "-"]];
      },
      note: "Nothing you answer is stored or sent. The studies are illustrations, not descriptions of particular trials.",
    });
  };

  // ---- Part 43: the Stroop task, run as a replication on you. ----
  W.stroop = function (el) {
    var w = null;
    var INKS = [["RED", "#ef6f6c"], ["GREEN", "#5bd18b"], ["BLUE", "#7ec8f5"], ["YELLOW", "#f2c14e"]];
    var KEYS = { d: 0, f: 1, j: 2, k: 3 };
    var run = T.timed(el, {
      keys: KEYS,
      trials: function () { return w.v.n; },
      seed: function () { return w.state.seed; },
      stimulus: function (rand) {
        var ink = Math.floor(rand() * 4), congruent = rand() < 0.5;
        var word = congruent ? ink : (ink + 1 + Math.floor(rand() * 3)) % 4;
        return { ink: ink, word: word, congruent: congruent };
      },
      correct: function (stim, side) { return side === stim.ink; },
      render: function () {
        var L = run ? run.log : [];
        if (L.length && L[L.length - 1].stim === undefined) L[L.length - 1].stim = run.stim;
        if (w) w.render();
      },
      foreperiod: [700, 1200], timeout: 2500, pause: { scored: 300, early: 800, timeout: 800 },
      words: { early: "Too early: wait for the word.", timeout: "No answer in time.",
        wrong: function () { return "Wrong ink (not counted)."; } },
    });
    function split() {
      var c = [], i = [], k, r;
      for (k = 0; k < run.log.length; k++) {
        r = run.log[k];
        if (!r.correct || !r.stim || r.rt < 200 || r.rt > 2000) continue;
        (r.stim.congruent ? c : i).push(r.rt);
      }
      return { c: c, i: i };
    }
    function mean(a) { return a.length ? QB.mean(a) : NaN; }
    w = QB.widget(el, {
      title: "The Stroop task, on you",
      sub: "Name the ink colour, not the word: D for red, F for green, J for blue, K for yellow. Answer as fast as you can while staying right. Then see your own Stroop effect against the plan's smallest effect of interest, 20 ms.",
      panels: 2, height: 330, weights: [1.1, 1],
      controls: [{ k: "n", label: "Trials", min: 24, max: 96, step: 8, value: 48, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [
        { label: "Start", act: function () { run.reset(); run.start("stroop"); } },
        { label: "Clear", act: function () { run.reset(); } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, run.task);
        ctx.save(); ctx.textAlign = "center";
        if (run.phase === "go") {
          ctx.fillStyle = INKS[run.stim.ink][1]; ctx.font = "700 40px system-ui, sans-serif";
          ctx.fillText(INKS[run.stim.word][0], b.cx, b.cy + 14);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("trial " + run.trial + " of " + v.n + "    D red   F green   J blue   K yellow", b.cx, b.y + 22);
        } else if (run.phase === "wait") {
          ctx.strokeStyle = C.muted; ctx.lineWidth = 2; ctx.beginPath();
          ctx.moveTo(b.cx - 10, b.cy); ctx.lineTo(b.cx + 10, b.cy); ctx.moveTo(b.cx, b.cy - 10); ctx.lineTo(b.cx, b.cy + 10);
          ctx.stroke();
        } else if (run.phase === "feedback") {
          T.message(ctx, b, run.msg);
        } else if (run.phase === "done") {
          var s = split(), d = mean(s.i) - mean(s.c);
          T.message(ctx, b, isFinite(d) ? "Your Stroop effect: " + Math.round(d) + " ms." : "Finished.",
                    "Incongruent minus congruent, correct trials between 200 and 2,000 ms, the exclusions fixed in advance. Nearly everyone is slower on incongruent trials; the plan's smallest effect of interest is 20 ms.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Nothing you do is kept or sent.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx, sp = split(), mc = mean(sp.c), mi = mean(sp.i);
        cx.save(); cx.textAlign = "center"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your mean time, by condition", c2.x + c2.w / 2, c2.y + 18);
        var base = c2.y + c2.h - 40, top = c2.y + 40, hi = 1200, bw = c2.w / 5;
        [[mc, "congruent", "#5bd18b", 1.5], [mi, "incongruent", "#ef6f6c", 3.5]].forEach(function (q) {
          var x = c2.x + q[3] * bw - bw / 2;
          if (isFinite(q[0])) {
            var h = (base - top) * Math.min(q[0], hi) / hi;
            cx.fillStyle = q[2]; cx.fillRect(x, base - h, bw, h);
            cx.fillStyle = C.ink; cx.font = "12px system-ui, sans-serif"; cx.fillText(Math.round(q[0]) + " ms", x + bw / 2, base - h - 6);
          }
          cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.fillText(q[1], x + bw / 2, base + 16);
        });
        cx.restore();
      },
      readout: function () {
        var s = split(), d = mean(s.i) - mean(s.c);
        return [["answers", String(run.task.count)], ["Stroop effect", isFinite(d) ? Math.round(d) + " ms" : "-"]];
      },
      note: "Nothing you answer is stored or sent. A single person's effect is noisy; the Stroop effect is large enough that most people see it in 48 trials.",
    });
  };
})();
